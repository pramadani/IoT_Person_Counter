from multiprocessing import Manager  # type: ignore
import streamlit as st
import time
from port import IP, PORT
from temperature import start_temperature_process
from sound import start_sound_process
from person_count import start_camera_thread
from data import update_temp_df, update_count_df

if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.image('logo_crop.png')
    
    with st.sidebar:
        st.text("Menu")

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
    
    manager = Manager()
    ns = manager.Namespace()
    
    ns.temperature = 0.0
    ns.person_count = 0
    ns.frame = None
    
    start_temperature_process(IP, PORT, ns)
    start_sound_process(5, ns)
    start_camera_thread(ns)
    
    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        with st.expander("Camera", expanded=True):
            frame_container = st.empty()
            with frame_container:
                st.write("Waiting for Camera")
            
    with col2:
        with st.expander("Person Count", expanded=True):
            person_count_container = st.empty()
            with person_count_container:
                st.write("Waiting for AI Model")
                    
        with st.container(border=True):
            person_df_container = st.empty()
            with person_df_container:
                st.write("Waiting for AI Model")
                        
    with col3:
        with st.expander("Temperature", expanded=True):
            temperature_container = st.empty()
            with temperature_container:
                st.write("Waiting for Sensor")
    
        with st.container(border=True):
            temperature_df_container = st.empty()
            with temperature_df_container:
                st.write("Waiting for Sensor")

    last_count = 0
    last_temp = 0
    
    while True:
        with temperature_container:
            if ns.temperature and ns.temperature != last_temp:
                last_temp = ns.temperature
                st.metric(label="Realtime Temperature", value=str(ns.temperature))
            
        with person_count_container:
            if ns.person_count and ns.person_count != last_count:
                last_count = ns.person_count
                st.metric(label="Realtime Counter", value=str(ns.person_count))
                
        with frame_container:
            if ns.frame:
                st.image(ns.frame, caption='Live Kamera', use_column_width=True)
                
        with temperature_df_container:
            if ns.temperature:
                fig_temp = update_temp_df(10, ns.temperature)
                st.plotly_chart(fig_temp, use_container_width=True)
                
        with person_df_container:
            if ns.person_count:
                fig_person = update_count_df(10, ns.person_count)
                st.plotly_chart(fig_person, use_container_width=True)
        
        time.sleep(0.02)
