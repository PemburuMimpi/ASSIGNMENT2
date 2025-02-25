import network
import time 
from time import sleep
import dht
from machine import ADC, Pin 
import urequests

#IDENTITAS WIFI YANG DIGUNAKAN
SSID = "Sylus"
PASSWORD = "syluscakep"

#ALAMAT WEB API URL
API_URL = "http://192.168.251.60:5000/api/dht"

#UNTUK MENGHUBUNGKAN WIFI
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        pass

    print("Connected to WiFi:", wlan.ifconfig())

connect_wifi()

#KONVERSI NILAI INTENSITAS CAHAYA MENJADI BENTUK PERSENTASE
def map_value(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) // (from_high - from_low) + to_low

#INISIASI SENSOR DHT DAN LDR
sensor = dht.DHT11(Pin(33))
ldr = ADC(Pin(32))
ldr.atten(ADC.ATTN_11DB)

#MEMBACA DAN MENGIRIM DATA
def send_data():
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        light_value = ldr.read()
        
        #KONVERSI NILAI INTENSITAS CAHAYA MENJADI BENTUK PERSENTASE
        light_percentage = map_value(light_value, 0, 4095, 0, 100)
        
        #UNTUK MENAMPILKAN WAKTU DAN TANGGAL
        year, month, day, hour, minute, second, _, _ = time.localtime()
        timestamp = f"{day:02d}-{month:02d}-{year} {hour:02d}:{minute:02d}:{second:02d}"
        
        #UNTUK MENAMPILKAN DATA: SUHU, KELEMBABAN, WAKTU, INTENSITAS CAHAYA 
        print(f"Temperature: {temp}, Humidity: {hum}, Timestamp: {timestamp}")
        print("Light Intensity:", light_value)
        data = {"temperature": temp, "humidity": hum, "light_value": light_value, "timestamp": timestamp}
        response = urequests.post(API_URL, json=data)
        print("Response:", response.content)
        response = None
        
    except Exception as e:
        print("Error:", e)

#PENGIRIMAN DATA SETIAP 5 DETIK
while True:
    send_data()
    sleep(5)
    