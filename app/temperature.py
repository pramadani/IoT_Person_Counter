import socket
from multiprocessing import Process # type: ignore

def receive_data(IP, PORT, temperature):
    addr = (IP, PORT)
    s = socket.socket()
    s.connect(addr)
    s.send(b'streamlit')

    while True:
        data = s.recv(1024)
        if data:
            temperature.value = data.decode('utf-8')

def start_temperature_process(IP, PORT, temperature):
    process = Process(target=receive_data, args=(IP, PORT, temperature))
    process.daemon = True
    process.start()