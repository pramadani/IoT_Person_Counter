import cv2
import numpy as np
from multiprocessing import Process, Manager # type: ignore
import time
from ultralytics import YOLO

def predict_objects(capture, namespace, person_count):
    model = YOLO('yolov8n.pt')
    
    results = model(capture)
    
    predictions = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy.tolist()
            conf = box.conf
            cls = box.cls
            predictions.append([x1, y1, x2, y2, conf, cls])

    namespace.predict_result = predictions
    person_count.value = len(predictions)

def detect_objects(namespace, person_count):
    while True:
        if namespace.capture is not None:
            predict_process = Process(target=predict_objects, args=(namespace.capture, namespace, person_count))
            predict_process.start()
            # predict_process.join()

        time.sleep(0.1)

def capture_and_process(namespace):
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, capture = cap.read()
        if not ret:
            break

        namespace.capture = capture.copy()

        for detection in namespace.predict_result:
            x1, y1, x2, y2, conf, cls = detection
            cv2.rectangle(capture, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        namespace.frame = capture.copy()

        cv2.imshow('Detected Objects', capture)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    manager = Manager()
    namespace = manager.Namespace()
    
    namespace.capture = None
    namespace.predict_result = []
    namespace.frame = None
    person_count = manager.Value('i', 0)

    detection_process = Process(target=detect_objects, args=(namespace,person_count))
    detection_process.start()

    capture_process = Process(target=capture_and_process, args=(namespace,))
    capture_process.start()

if __name__ == "__main__":
    main()
