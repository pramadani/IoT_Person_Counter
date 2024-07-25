import streamlit as st
import socket
import time
import pandas as pd
import plotly.graph_objects as go
import cv2
from datetime import datetime
from ultralytics import YOLO
from playsound import playsound

# Set the default page configuration to wide mode
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

logo_url = './resource/logo_crop.png'
st.sidebar.image(logo_url)

with st.sidebar:
    st.text("Menu")

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
    [data-testid="stMetric"] {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
    }
    [data-testid="stSidebar"] {
        width: 200px !important;
    }
    [data-testid="stSidebarHeader"] {
        padding: 0px !important;
    }
    [data-testid="stAppViewBlockContainer"] {
        height: 100vh;
        overflow: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

model = YOLO("yolov8n.pt")  # load an official model

# Start video capture
cap = cv2.VideoCapture(0)

width = 640
height = 360
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

frame_skip = 1
frame_count = 0

# Function to get data from the Raspberry Pi Pico W
def get_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 400))
        s.sendall(b'REQUEST_DATA')
        data = s.recv(1024).decode('utf-8')
    return float(data)  # Convert received data to float

# Initialize a list to store temperature data
if 'temperature_data' not in st.session_state:
    st.session_state.temperature_data = []

# Initialize a list to store people counter data
if 'people_counter_data' not in st.session_state:
    st.session_state.people_counter_data = []

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    with st.expander("Camera", expanded=True):
        frame_placeholder = st.empty()
    with st.expander("People Counter", expanded=True):
        col4, col5 = st.columns([1,3])
        with col4 :
            people_counter_placeholder = st.empty() 
        with col5 :
            counter_line_chart_placeholder = st.empty()
            
with col2:
    with st.expander("Linimasa Temperatur", expanded=True):
        line_chart_placeholder = st.empty()
    with st.expander("Temperatur Real Time", expanded=True):
        gauge_placeholder = st.empty()

with col3:
    with st.expander("History", expanded=True):
        history_placeholder = st.container()
        
    info_placeholder = st.container()

# Initialize timing variables
start_time = time.time()
last_temp_update = 0
last_gauge_update = 0
line_chart_update_interval = 5  # seconds
gauge_update_interval = 1  # seconds
last_temp = None
last_play_time = 0

while True:
    current_time = time.time()

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

    if people_counter > 1 and current_time - last_play_time > 20:  # Check if 20 seconds have passed
        playsound("resource/10_person.mp3")
        last_play_time = current_time  # Update the last play time

    (text_width, text_height), baseline = cv2.getTextSize(people_counter_text, cv2.FONT_HERSHEY_SIMPLEX, 2, 1)
    top_left_corner = (20, 70 - text_height - baseline - 5)
    bottom_right_corner = (330, 70)
    
    # Convert the image to RGB for displaying in Streamlit
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with frame_placeholder.container():
        frame_placeholder.image(img_rgb, channels="RGB")
        
    with people_counter_placeholder.container():  # Update the people counter display
        st.metric(label="People Counter", value=people_counter)

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
    
        # Append people counter data to session state
        st.session_state.people_counter_data.append((current_time_str, people_counter))
        
        # Convert to DataFrame
        df_counter = pd.DataFrame(st.session_state.people_counter_data, columns=["Time", "PeopleCounter"])
        df_counter.set_index("Time", inplace=True)
        
        # Slice the DataFrame to keep only the last 10 records
        df_counter_last_10 = df_counter.tail(10)
        
        # Calculate min and max for y-axis
        min_counter = df_counter_last_10["PeopleCounter"].min()
        max_counter = df_counter_last_10["PeopleCounter"].max()
        y_min_counter = min_counter - 1  # Adding margin
        y_max_counter = max_counter + 1  # Adding margin
        
        # Update the line chart for people counter using Plotly
        fig_counter = go.Figure()
        fig_counter.add_trace(go.Scatter(x=df_counter_last_10.index, y=df_counter_last_10["PeopleCounter"], mode='lines+markers', name='People Counter'))
        fig_counter.update_layout(
            title='Linimasa People Counter',
            xaxis_title='Time',
            yaxis_title='People Count',
            yaxis=dict(range=[y_min_counter, y_max_counter]),  # Set the y-axis range
            height=300
        )
        
        with counter_line_chart_placeholder.container():
            st.plotly_chart(fig_counter, use_container_width=True)
    
    # Sleep for a short duration to prevent high CPU usage
    time.sleep(0.1)
