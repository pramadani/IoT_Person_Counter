import socket
from multiprocessing import Process # type: ignore

IP = "0.0.0.0"
PORT = 65432

def receive_data(namespace):
    global IP
    global PORT
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f"Socket server listening on port {PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by Pico at {addr}")
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    try:
                        temperature_now = float(data.decode('utf-8'))
                    except:
                        continue
                    namespace.temperature = temperature_now
                    print(f"Received data: {namespace.temperature}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()

def start_temperature_process(namespace):
    process = Process(target=receive_data, args=(namespace,))
    process.daemon = True
    process.start()