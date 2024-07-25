import socket
import threading

latest_data = ""

def handle_pico_connection(conn, addr):
    global latest_data
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            latest_data = data.decode('utf-8')
            print(f"Received data: {latest_data}")

def handle_streamlit_connection(conn, addr):
    global latest_data
    with conn:
        print(f"Streamlit connected by {addr}")
        while True:
            if latest_data:
                conn.sendall(latest_data.encode('utf-8'))
                latest_data = ""

def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 65432))
    server_socket.listen()

    print("Socket server listening on port 65432")

    while True:
        conn, addr = server_socket.accept()
        client_type = conn.recv(1024).decode('utf-8')
        if client_type == 'pico':
            threading.Thread(target=handle_pico_connection, args=(conn, addr)).start()
        elif client_type == 'streamlit':
            threading.Thread(target=handle_streamlit_connection, args=(conn, addr)).start()

if __name__ == "__main__":
    start_socket_server()
