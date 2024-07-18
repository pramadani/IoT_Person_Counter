import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO
from playsound import playsound
import time

people_counter = ''
last_play_time = 0  # Initialize the last play time to zero

st.set_page_config(layout="wide", page_title="People Counter", page_icon="👥")

# Add custom CSS to hide the Streamlit menu and toolbar
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stToolbar"] {display: none;}
            button[title^=Exit]+div [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
                }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def People_Count():
    global people_counter, last_play_time
    # Load the YOLO model
    model = YOLO("yolov8n.pt")  # load an official model
    
    # Start video capture
    cap = cv2.VideoCapture(4)
    
    # Reduce frame size for faster processing
    width = 1280
    height = 720
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    frame_skip = 1
    frame_count = 0
    
    stframe = st.empty()

    while True:
        ret, img = cap.read()
        if not ret:
            break
        
        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        # Get image dimensions
        height, width, _ = img.shape
        
        # Run YOLO model
        results = model(img)
        
        # Initialize person count
        p = 0
        
        for result in results:
            boxes = result.boxes.data.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2, confidence, class_id = box
                label = model.names[int(class_id)]
                if label == 'person' and confidence > 0.3:
                    p += 1
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    color = (0, 0, 0)
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    text = f"{label}:{confidence:.2f}"
                    
                    # Get the text size and draw the filled rectangle with padding
                    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                    cv2.rectangle(img, (x1, y1 - text_height - baseline - 5), (x1 + text_width, y1), color, thickness=-1)
                    
                    # Put the text on top of the filled rectangle
                    cv2.putText(img, text, (x1, y1 - baseline - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

        # Get the text size for "People Counter" and draw the filled rectangle
        people_counter_text = "People Counter: " + str(p)
        people_counter = p

        current_time = time.time()  # Get the current time
        if people_counter > 1 and current_time - last_play_time > 20:  # Check if 60 seconds have passed
            playsound("resource/10_person.mp3")
            last_play_time = current_time  # Update the last play time

        (text_width, text_height), baseline = cv2.getTextSize(people_counter_text, cv2.FONT_HERSHEY_SIMPLEX, 2, 1)
        top_left_corner = (20, 70 - text_height - baseline - 5)
        bottom_right_corner = (330, 70)
        
        cv2.rectangle(img, top_left_corner, bottom_right_corner, (0, 0, 255), thickness=-1)
        
        # Put the "People Counter" text on top of the filled rectangle
        cv2.putText(img, people_counter_text, (25, 70 - baseline - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        # Convert the image to RGB for displaying in Streamlit
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        stframe.image(img_rgb, channels="RGB")

    cap.release()

if __name__ == "__main__":
    People_Count()
