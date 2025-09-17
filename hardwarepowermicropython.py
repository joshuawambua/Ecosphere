import network
import urequests
import ujson
import time
from machine import Pin, ADC

# ---------- WiFi Configuration ----------
WIFI_SSID = "YourWiFiSSID"
WIFI_PASS = "YourWiFiPassword"

# ---------- Firebase Configuration ----------
FIREBASE_URL = "https://your-project-id.firebaseio.com/sensordata.json"

# ---------- Connect to WiFi ----------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            pass
    print("Connected to WiFi:", wlan.ifconfig())

# ---------- Read Example Sensor (MQ135 or Analog) ----------
adc = ADC(Pin(34))  # Example analog pin for gas/PM sensor
adc.atten(ADC.ATTN_11DB)  # Full 0-3.3V range

def read_sensor():
    value = adc.read()
    # You can calibrate this to real units (ppm, µg/m³, etc.)
    return {"gas_value": value, "timestamp": time.time()}

# ---------- Send Data to Firebase ----------
def send_to_firebase(data):
    try:
        response = urequests.post(FIREBASE_URL, data=ujson.dumps(data))
        print("Data sent:", response.text)
        response.close()
    except Exception as e:
        print("Error:", e)

# ---------- Main Loop ----------
connect_wifi()

while True:
    sensor_data = read_sensor()
    send_to_firebase(sensor_data)
    time.sleep(10)  # Send every 10 seconds
