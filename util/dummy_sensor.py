import socket
import time
import random

def conn_init(IP, PORT):
    addr = (IP, PORT)
    client_socket = socket.socket()
    client_socket.connect(addr)
    print("Connection to server established.")
    return client_socket

def send_to_server(client_socket, data):
    client_socket.send(data.encode('utf-8'))
    print(f"Sent temperature: {data}")

def get_temperature():
    temperature = random.randint(16, 30)
    return str(temperature)

if __name__ == "__main__":  
    client_socket = conn_init("127.0.0.1", 65432)

    while True:
        temperature = get_temperature()
        send_to_server(client_socket, temperature)
        time.sleep(1)