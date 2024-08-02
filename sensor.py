from bme280 import BME280  # type: ignore
from machine import I2C, Pin  # type: ignore
import time
import socket
import network  # type: ignore

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Connecting to WiFi...')
        time.sleep(1)
    
    print('Connected:', wlan.ifconfig())

def conn_init(ip, port):
    addr = (ip, port)
    client_socket = socket.socket()
    client_socket.connect(addr)
    print("Connection to server established.")

    return client_socket

def send_to_server(client_socket, data):
    client_socket.send(data.encode('utf-8'))
    print(f"Sent temperature: {data}")

def get_temperature(sensor):
    temperature = sensor.temperature
    return str(temperature)

if __name__ == "__main__":
    i2c = I2C(1, sda=Pin(6), scl=Pin(7))
    sensor = BME280(i2c=i2c)

    ssid = 'BOE-'
    password = ''
    connect_wifi(ssid, password)

    ip = "192.168.57.140"
    port = 65432

    while True:
        try:
            client_socket = conn_init(ip, port)
            
            while True:
                temperature = get_temperature(sensor)
                try:
                    send_to_server(client_socket, temperature)
                except:
                    break
                time.sleep(1)
        except:
            print("Error connecting to server. Retrying in 5 seconds.")
            time.sleep(5)