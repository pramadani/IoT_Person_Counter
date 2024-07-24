import socket
import threading

global_data = "No data received"

def socket_server():
    global global_data
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 400))
    server_socket.listen(5)
    print("Socket server started, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            if data == 'REQUEST_DATA':
                client_socket.sendall(global_data.encode('utf-8'))
            else:
                global_data = data

        client_socket.close()

if __name__ == "__main__":
    thread = threading.Thread(target=socket_server)
    thread.daemon = True
    thread.start()
    while True:
        pass
