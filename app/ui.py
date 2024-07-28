
import streamlit as st
import time
from port import IP, PORT
from temperature import temperature, start_temperature_thread

start_temperature_thread(IP, PORT)

conn_container = st.empty()

while True:
    with conn_container:
        st.write(f"Current Temperature: {temperature}")
        time.sleep(1)