from multiprocessing import Manager # type: ignore
import streamlit as st
import time
from port import IP, PORT
from temperature import start_temperature_process
from sound import start_sound_process

if __name__ == "__main__":
    manager = Manager()
    
    temperature = manager.Value('s', "0")
    person_count = manager.Value('i', 0)
    
    start_temperature_process(IP, PORT, temperature)
    start_sound_process(5, person_count)

    conn_container = st.empty()
    while True:
        with conn_container:
            st.write(f"Current Temperature: {temperature.value}")
            time.sleep(1)