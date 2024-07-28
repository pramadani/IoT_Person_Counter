
import socket
import threading

temperature = "0"

def receive_data(IP, PORT):
    global temperature
    addr = (IP, PORT)
    s = socket.socket()
    s.connect(addr)
    s.send(b'streamlit')

    while True:
        data = s.recv(1024)
        if data:
            temperature = data.decode('utf-8')

def start_temperature_thread(IP, PORT):
    threading.Thread(target=receive_data, args=(IP, PORT), daemon=True).start()