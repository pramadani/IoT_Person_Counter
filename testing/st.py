import streamlit as st
import socket
import time
import plotly.graph_objects as go

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
        s.connect(('127.0.0.1', 400))
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
    xaxis=dict(
        range=[0, 10],  # Adjust as needed
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

# Create a two-column layout
col1, col2 = st.columns([10, 3])  # Adjust the second value to take the remaining space

# Create placeholders for the charts in the two columns
with col1:
    st.title("Real-Time Temperature Data")
with col2:
    line_chart_placeholder = st.empty()
    gauge_placeholder = st.empty()

start_time = time.time()

while True:
    temp = get_data()
    
    temperature_data.append(temp)
    
    current_time = time.time() - start_time
    fig_line.data[0].x = list(range(len(temperature_data)))
    fig_line.data[0].y = temperature_data

    # Update gauge chart value
    fig_gauge.data[0].value = temp
    
    # Update the line chart and gauge chart
    with line_chart_placeholder.container():
        st.plotly_chart(fig_line, use_container_width=True)

    with gauge_placeholder.container():
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    time.sleep(1)
