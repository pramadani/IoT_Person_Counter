import streamlit as st
import socket
import time
import pandas as pd
from datetime import datetime
import threading
from style import style
import cv2
from ultralytics import YOLO

cam_index = 0

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

def configure_style():
    st.markdown(style, unsafe_allow_html=True)

    
    logo_url = './resource/logo_crop.png'
    st.sidebar.image(logo_url)

    with st.sidebar:
        st.text("Menu")

def thread_socket():
    def receive_data():
        global latest_temp
        addr = ('192.168.58.17', 65432)
        s = socket.socket()
        s.connect(addr)
        s.send(b'streamlit')
        while True:
            data = s.recv(1024)
            if data:
                latest_temp = float(data.decode('utf-8'))
    
    threading.Thread(target=receive_data, daemon=True).start()

def configure_layout():
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        with st.expander("People Counter", expanded=True):
            frame_ = st.container(height=425, border=True)
                
    with col2:
        with st.expander("Linimasa Temperatur", expanded=True):
            temp_ = st.empty()
        with st.expander("Temperatur Real Time", expanded=True):
            gauge_ = st.empty()

    with col3:
        with st.expander("History", expanded=True):
            history_ = st.container(height=305, border=True)
            
        info_ = st.container(height=100, border=True)
        
    return col1, col2, col3, frame_, temp_, gauge_, history_, info_

def get_time():
    current_time = time.time()
    local_time = datetime.fromtimestamp(current_time)
    formatted_time = local_time.strftime("%H:%M:%S")
    return current_time, formatted_time

def update_temperature(temperature_data, last_temp, last_gauge_update):
    current_time, formatted_time = get_time()
    
    # temp = latest_temp
    
    # temperature_data.append((formatted_time, temp))
    # if len(temperature_data) > 10:
    #     temperature_data = temperature_data[-10:]
    
    # df = pd.DataFrame(temperature_data, columns=["Time", "Temperature"])
    # df["Temperature"] = df["Temperature"].apply(lambda x: f"{x} C")
    # df.set_index("Time", inplace=True)
    
    # with temp_.container():
    #     st.line_chart(df, height=200)

    # with gauge_.container():
    #     delta_temp = temp - last_temp
    
    #     st.metric(label="Laboratorium", value=str(temp) + " °C", delta=delta_temp, delta_color="off")
    #     last_temp = temp
        # Update gauge chart every second
    if current_time - last_gauge_update >= gauge_update_interval:
        temp = get_data()
        temp = float(temp)
        
        # Update the gauge chart
        with gauge_placeholder.container():
            if last_temp is not None:
                delta_temp = temp - last_temp
                st.metric(label="Laboratorium", value=f"{temp} °C", delta=f"{delta_temp:.2f} °C")
            else:
                st.metric(label="Laboratorium", value=f"{temp} °C")
            last_temp = temp
        
        last_gauge_update = current_time

    # Update line chart every 5 seconds
    if current_time - last_temp_update >= line_chart_update_interval:
        # Get data
        current_time_str = datetime.now().strftime("%H:%M:%S")
        temp = get_data()
        temp = float(temp)
        
        # Append data to session state
        st.session_state.temperature_data.append((current_time_str, temp))
        
        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.temperature_data, columns=["Time", "Temperature"])
        df.set_index("Time", inplace=True)
        
        # Slice the DataFrame to keep only the last 10 records
        df_last_10 = df.tail(10)
        
        # Calculate min and max for y-axis
        min_temp = df_last_10["Temperature"].min()
        max_temp = df_last_10["Temperature"].max()
        y_min = min_temp - 4  # Adding margin
        y_max = max_temp + 4  # Adding margin
        
        # Update the line chart using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_last_10.index, y=df_last_10["Temperature"], mode='lines+markers', name='Temperature'))
        fig.update_layout(
            title='Linimasa Temperatur',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            yaxis=dict(range=[y_min, y_max])  # Set the y-axis range
        )
        
        with line_chart_placeholder.container():
            st.plotly_chart(fig, use_container_width=True)
        
        # Update the last update time
        last_temp_update = current_time

def configure_person_count(cam_index):
    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(cam_index)

    width = 640
    height = 360
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    return cap, model

# def update_person(frame_count):
#     ret, img = cap.read()
#     if not ret:
#         break
    
#     frame_count += 1
#     if frame_count % frame_skip != 0:
#         continue

#     # Get image dimensions
#     height, width, _ = img.shape
    
#     # Run YOLO model
#     results = model(img)
    
#     # Initialize person count
#     p = 0
    
#     for result in results:
#         boxes = result.boxes.data.cpu().numpy()
#         for box in boxes:
#             x1, y1, x2, y2, confidence, class_id = box
#             label = model.names[int(class_id)]
#             if label == 'person' and confidence > 0.3:
#                 p += 1
#                 x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#                 color = (0, 0, 0)
#                 cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
#                 text = f"{label}:{confidence:.2f}"
                
#                 # Get the text size and draw the filled rectangle with padding
#                 (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
#                 cv2.rectangle(img, (x1, y1 - text_height - baseline - 5), (x1 + text_width, y1), color, thickness=-1)
                
#                 # Put the text on top of the filled rectangle
#                 cv2.putText(img, text, (x1, y1 - baseline - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

#     # Get the text size for "People Counter" and draw the filled rectangle
#     people_counter_text = "People Counter: " + str(p)
#     people_counter = p

#     (text_width, text_height), baseline = cv2.getTextSize(people_counter_text, cv2.FONT_HERSHEY_SIMPLEX, 2, 1)
#     top_left_corner = (20, 70 - text_height - baseline - 5)
#     bottom_right_corner = (330, 70)
    
#     cv2.rectangle(img, top_left_corner, bottom_right_corner, (0, 0, 255), thickness=-1)
    
#     cv2.putText(img, people_counter_text, (25, 70 - baseline - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     with frame_placeholder.container():
#         frame_placeholder.image(img_rgb, channels="RGB")


configure_style()
thread_socket()

col1, col2, col3, frame_, temp_, gauge_, history_, info_ = configure_layout()
cap, model = configure_person_count(cam_index)
latest_temp = 0
temperature_data = []
df = pd.DataFrame(columns=["Time", "Temperature"])
last_temp = 0
last_time_update = 0
frame_skip = 1
frame_count = 0

while True:
    update_temperature(temperature_data, last_temp)
    
    time.sleep(1)
