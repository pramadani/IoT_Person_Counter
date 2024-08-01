import multiprocessing
import time

def capture_and_draw_frame(namespace):
    import cv2
    from PIL import Image
    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        if not ret:
            break
        
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        namespace.capture = Image.fromarray(img_rgb)

        if hasattr(namespace, 'result'):
            results = namespace.result
            for result in results:
                for box in result.boxes:
                    if box.cls[0] == 0 and box.conf[0] > 0.3:  # Assuming class 0 is 'person' and checking confidence
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        confidence = box.conf[0]
                        cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(img_rgb, f"confidence: {confidence:.2f}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
        
        namespace.frame = Image.fromarray(img_rgb)

    cap.release()

def predict(namespace):
    from ultralytics import YOLO
    
    model = YOLO('yolov8n.pt')

    while True:
        if hasattr(namespace, 'capture'):
            img = namespace.capture
            results = model(img)
            namespace.result = results
            person_count = 0
            for result in results:
                for box in result.boxes:
                    if box.cls[0] == 0 and box.conf[0] > 0.3:  # Assuming class 0 is 'person' and checking confidence
                        person_count += 1
            
            namespace.person_count = person_count
            
def start_camera_thread(namespace):
    capture_process = multiprocessing.Process(target=capture_and_draw_frame, args=(namespace,)) # type: ignore
    predict_process = multiprocessing.Process(target=predict, args=(namespace,)) # type: ignore
    capture_process.start()
    predict_process.start()
