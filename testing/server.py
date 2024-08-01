import socket
import threading
from port import PORT

temperature_data = ""

def handle_pico_connection(conn, addr):
    global temperature_data
    with conn:
        print(f"Connected by Pico at {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            temperature_data = data.decode('utf-8')
            print(f"Received data: {temperature_data}")

def handle_streamlit_connection(conn, addr):
    global temperature_data
    with conn:
        print(f"Streamlit connected by {addr}")
        while True:
            if temperature_data:
                conn.sendall(temperature_data.encode('utf-8'))
                temperature_data = ""

def start_socket_server(IP='0.0.0.0', PORT=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f"Socket server listening on port {PORT}")

    while True:
        conn, addr = server_socket.accept()
        client_type = conn.recv(1024).decode('utf-8')
        if client_type == 'pico':
            threading.Thread(target=handle_pico_connection, args=(conn, addr)).start()
        elif client_type == 'streamlit':
            threading.Thread(target=handle_streamlit_connection, args=(conn, addr)).start()

if __name__ == "__main__":    
    start_socket_server(PORT=PORT)
