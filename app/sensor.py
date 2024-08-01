from bme280 import BME280
from machine import I2C, Pin
import time
import socket
import network

def connect_wifi(ssid):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid)

    while not wlan.isconnected():
        print('Menghubungkan ke WiFi...')
        time.sleep(1)
    
    print('Terhubung ke WiFi:', wlan.ifconfig())

def conn_init(IP, PORT):
    addr = (IP, PORT)
    client_socket = socket.socket()
    client_socket.connect(addr)
    client_socket.send(b'pico')
    print("Connection to server established.")

    return client_socket

def send_to_server(client_socket, data):
    client_socket.send(data.encode('utf-8'))
    print(f"Sent temperature: {data}")

def get_temperature(sensor):
    temperature = sensor.values[0]
    return str(temperature)

if __name__ == "__main__":  
    sensor = BME280(i2c=I2C(1, sda=Pin(6), scl=Pin(7)))

    connect_wifi('BOE-')

    IP = "192.168.57.140"
    PORT = 65432
    client_socket = conn_init(IP, PORT)
    
    while True:
        temperature = get_temperature(sensor)
        send_to_server(client_socket, temperature)
        time.sleep(1)
