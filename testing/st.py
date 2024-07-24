import streamlit as st
import socket
import time
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

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

# Function to get data from the Raspberry Pi Pico W
def get_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 400))
        s.sendall(b'REQUEST_DATA')
        data = s.recv(1024).decode('utf-8')
    return float(data)  # Convert received data to float

# Initialize a list to store temperature data
temperature_data = []

# Create a DataFrame for temperature data
df = pd.DataFrame(columns=["Time", "Temperature"])

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    with st.expander("People Counter", expanded=True):
        frame_placeholder = st.container(height=425, border=True)
            
with col2:
    with st.expander("Linimasa Temperatur", expanded=True):
        line_chart_placeholder = st.empty()
    with st.expander("Temperatur Real Time", expanded=True):
        gauge_placeholder = st.empty()

with col3:
    with st.expander("History", expanded=True):
        history_placeholder = st.container(height=305, border=True)
        
    info_placeholder = st.container(height=100, border=True)

last_temp = 0
last_time_update = 0

while True:
    current_time = time.time()
    local_time = datetime.fromtimestamp(current_time)
    formatted_time = local_time.strftime("%H:%M:%S")
    
    temp = get_data()
    
    temperature_data.append((formatted_time, temp))
    
    if len(temperature_data) > 10:
        temperature_data = temperature_data[-10:]
    
    df = pd.DataFrame(temperature_data, columns=["Time", "Temperature"])
    df.set_index("Time", inplace=True)
    
    # Update the line chart
    with line_chart_placeholder.container():
        st.line_chart(df, height=200)

    # Update the gauge chart
    with gauge_placeholder.container():
        delta_temp = temp - last_temp
        
        # if delta_temp == 0:
            
        if temp > last_temp:
            st.metric(label="Laboratorium", value=str(temp) + " °C", delta=f"{delta_temp} pada {formatted_time[:5]}", delta_color="inverse")
            last_temp = temp
        elif temp < last_temp:
            st.metric(label="Laboratorium", value=str(temp) + " °C", delta=f"{delta_temp} pada {formatted_time[:5]}", delta_color="inverse")
            last_temp = temp
    
    time.sleep(1)
