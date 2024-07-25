import socket
import random
import time

server_ip = '192.168.56.68'  # Gantilah dengan IP server jika berbeda
server_port = 400

while True:
    try:
        # Membuat koneksi ke server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        # Mengirim data
        data = str(random.randint(0, 100))
        print(data)
        client_socket.send(data.encode('utf-8'))

        # Menutup koneksi
        client_socket.close()

        # Menunggu beberapa detik sebelum mengirim data lagi
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)