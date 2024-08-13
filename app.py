from multiprocessing import Manager  # type: ignore
import streamlit as st
import time
from temperature import start_temperature_process
from sound import start_sound_process
from person_count import start_camera_thread
from data import update_temp_df, update_count_df
from style import add_css
import gc

chart_delay = 60
sound_delay = 60

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Room Occupancy App", 
    page_icon="📷"
)
add_css(st, "style.css")
st.markdown("<script>window.onload = () => setInterval(() => location.reload(), 100000)</script>", unsafe_allow_html=True)

@st.cache_resource
def init():
    manager = Manager()
    ns = manager.Namespace()
    
    ns.temperature = None
    ns.person_count = None
    ns.frame = None
    ns.toggle_sound = True

    start_temperature_process(ns)
    start_sound_process(sound_delay, ns)
    start_camera_thread(ns)
    
    return ns

with st.sidebar:
    with st.container(border=True):
        st.image('./resources/logo_crop.png')
    with st.container(border=True):
        sound_container = st.empty()
        with sound_container:
            st.metric(label="Sound", value="🔊 On")
        button = st.button('Toggle Sound')

last_count = None
last_temp = None

col1, col2 = st.columns([1,1])

with col1:       
    with st.container(border=True):
        st.text("IoT Room Occupancy App 💻")

    with st.container(border=True):
        st.subheader("📷 Realtime Camera")
        frame_container = st.empty()
        with frame_container:
            st.write("Waiting for Camera")
        
with col2:
    with st.container(border=True):
        st.subheader("🕑 Realtime Occupancy")
        col2_1, col2_2 = st.columns([1,1])
        with col2_1:
            person_count_container = st.empty()
            with person_count_container:
                st.write("Waiting for AI Model")
        with col2_2:
            temperature_container = st.empty()
            with temperature_container:
                st.write("Waiting for Sensor")
                
    col2_3, col2_4 = st.columns([1,1])
    with col2_3:
        with st.container(border=True):
            person_df_container = st.empty()
            with person_df_container:
                st.write("Waiting for AI Model")
    with col2_4:
        with st.container(border=True):
            temperature_df_container = st.empty()
            with temperature_df_container:
                st.write("Waiting for Sensor")
                    
if __name__ == "__main__":   
    ns = init()

    with sound_container:
        if button:
            ns.toggle_sound = not ns.toggle_sound
        if ns.toggle_sound is True:
            st.metric(label="Sound", value="🔊 On")
        elif ns.toggle_sound is False:
            st.metric(label="Sound", value="🔊 Off")

    while True:
        with temperature_container:
            if ns.temperature is not None and ns.temperature != last_temp:
                last_temp = ns.temperature
                st.metric(label="Temperature", value=f"🌡️ {str(ns.temperature)}")
            
        with person_count_container:
            if ns.person_count is not None and ns.person_count != last_count:
                last_count = ns.person_count
                st.metric(label="Person Counter", value=f"👦🏻 {str(ns.person_count)}")
                
        with frame_container:
            if ns.frame:
                st.image(ns.frame, use_column_width=True)
                
        with temperature_df_container:
            if ns.temperature is not None:
                fig_temp = update_temp_df(chart_delay, ns.temperature)
                st.plotly_chart(fig_temp, use_container_width=True)
                
        with person_df_container:
            if ns.person_count is not None:
                fig_person = update_count_df(chart_delay, ns.person_count)
                st.plotly_chart(fig_person, use_container_width=True)
        
        time.sleep(0.02)