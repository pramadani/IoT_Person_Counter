import network
import usocket as socket
import time
from machine import I2C, Pin
from bme280 import * # type: ignore

# Fungsi untuk menghubungkan ke WiFi
def connect_wifi(ssid):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid)

    while not wlan.isconnected():
        print('Menghubungkan ke WiFi...')
        time.sleep(1)
    
    print('Terhubung ke WiFi:', wlan.ifconfig())
    return wlan

# Informasi WiFi
ssid = 'BOE-'

# Menghubungkan ke WiFi
wlan = connect_wifi(ssid)

# Informasi IP dan port
server_ip = '192.168.58.17'
server_port = 400

# Membuat socket dan menghubungkan ke server
# try:
#     s = socket.socket()
#     s.connect((server_ip, server_port))
#     print('Terhubung ke server pada IP {} dan port {}'.format(server_ip, server_port))
# except Exception as e:
#     print('Gagal menghubungkan ke server:', e)

# Inisialisasi I2C dan BME280
i2c = I2C(1)
bme = BME280(i2c=i2c) # type: ignore

# Loop untuk membaca data dari sensor dan mengirim ke server setiap detik
try:
    while True:
        s = socket.socket()
        s.connect((server_ip, server_port))
        temp = bme.formated_values[0][:5]
        print('Mengirim data:', temp)

        s.send(temp.encode())

        time.sleep(1)
        s.close()
except KeyboardInterrupt:
    print('Koneksi socket ditutup')
