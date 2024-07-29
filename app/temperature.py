import socket
from multiprocessing import Process, Manager  # type: ignore

def receive_data(IP, PORT, namespace):
    addr = (IP, PORT)
    s = socket.socket()
    s.connect(addr)
    s.send(b'streamlit')

    while True:
        data = s.recv(1024)
        if data:
            namespace.temperature = float(data.decode('utf-8'))

def start_temperature_process(IP, PORT, namespace):
    process = Process(target=receive_data, args=(IP, PORT, namespace))
    process.daemon = True
    process.start()