import network
import usocket as socket
import time
from machine import I2C, Pin
from bme280 import * # type: ignore

def connect_wifi(ssid):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid)

    while not wlan.isconnected():
        print('Menghubungkan ke WiFi...')
        time.sleep(1)
    
    print('Terhubung ke WiFi:', wlan.ifconfig())
    return wlan

ssid = 'BOE-'

wlan = connect_wifi(ssid)

server_ip = '192.168.58.17'
server_port = 65432

i2c = I2C(1)
bme = BME280(i2c=i2c) # type: ignore

s = socket.socket()
s.connect((server_ip, server_port))
s.send(b'pico')

while True:
    temp = bme.formated_values[0][:5]
    print(temp)
    s.send(temp.encode())
    time.sleep(1)
