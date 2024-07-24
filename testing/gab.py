import streamlit as st
import socket
import time
import plotly.graph_objects as go
import cv2
import numpy as np
from ultralytics import YOLO
from playsound import playsound

# Set the default page configuration to wide mode
st.set_page_config(
    layout="wide"  # Set layout to wide
)

# Add custom CSS to hide specific elements and adjust padding
st.markdown(
    """
    <style>
    .st-emotion-cache-12fmjuu, .ezrtsby2 {
        display: none !important;
    }
    
    .block-container.st-emotion-cache-1jicfl2.ea3mdgi5 {
        padding: 0.5rem 2.5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to get data from the Raspberry Pi Pico W
def get_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.58.17', 400))
        s.sendall(b'REQUEST_DATA')
        data = s.recv(1024).decode('utf-8')
    return float(data)  # Convert received data to float

# Initialize a list to store temperature data
temperature_data = []

# Create a Plotly figure for the line chart
fig_line = go.Figure()

# Add a line plot to the figure
fig_line.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', name='Temperature'))

# Set figure layout for line chart
fig_line.update_layout(
    yaxis_title="Temperature (°C)",
    xaxis=dict( # Adjust as needed
        showticklabels=False,  # Hide x-axis tick labels
        showline=False,       # Hide x-axis line
        showgrid=False        # Hide x-axis grid lines
    ),
    yaxis=dict(range=[16, 30]),  # Adjust as needed
    height=300  # Resize the height of the line chart
)

# Create a Plotly figure for the gauge
fig_gauge = go.Figure()

# Add a gauge to the figure
fig_gauge.add_trace(go.Indicator(
    mode="gauge+number",
    value=0,
    gauge=dict(
        axis=dict(range=[16, 30]),
        bar=dict(color="royalblue"),
        steps=[dict(range=[16, 22], color="lightgray"), dict(range=[22, 30], color="lightcyan")]
    )
))

# Set figure layout for gauge
fig_gauge.update_layout(height=280)  # Resize the height of the gauge

    # Load the YOLO model
model = YOLO("yolov8n.pt")  # load an official model

# Start video capture
cap = cv2.VideoCapture(4)

# Reduce frame size for faster processing
# width = 1280
# height = 720
width = 640
height = 360
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

frame_skip = 1
frame_count = 0

# Create a two-column layout
# col = st.columns((4.5, 1.5), gap='medium') # Adjust the second value to take the remaining space
col1, col2 = st.columns([1, 1]) 

# Create placeholders for the charts in the two columns
with col1:
    stframe = st.empty()
with col2:
    line_chart_placeholder = st.empty()
    gauge_placeholder = st.empty()
    


start_time = time.time()
last_play_time = 0
temp_update_time = -2

while True:
    current_time = time.time() - start_time

    if current_time - temp_update_time > 1:
        temp = get_data()
    
        temperature_data.append(temp)

        if len(temperature_data) > 10:
            temperature_data = temperature_data[-10:]

        fig_line.data[0].x = list(range(len(temperature_data)))
        fig_line.data[0].y = temperature_data

        # Update gauge chart value
        fig_gauge.data[0].value = temp

        with line_chart_placeholder.container(): 
            st.plotly_chart(fig_line, use_container_width=True)
        with gauge_placeholder.container():
            st.plotly_chart(fig_gauge, use_container_width=True)
        temp_update_time = current_time

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

    with stframe.container():
        # People_Count()
        stframe.image(img_rgb, channels="RGB")

    # if current_time - temp_update_time > 1:  # Check if 60 seconds have passed
    #     with line_chart_placeholder.container(): 
    #         st.plotly_chart(fig_line, use_container_width=True)
    #     with gauge_placeholder.container():
    #         st.plotly_chart(fig_gauge, use_container_width=True)
    #     temp_update_time = current_time
    
    
