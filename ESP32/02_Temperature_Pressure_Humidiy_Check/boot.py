# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
from machine import Pin, I2C
import bme280
import time

# Initialize I2C (ESP32 Default: SCL=Pin 22, SDA=Pin 21)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

def scan_i2c():
    devices = i2c.scan()
    if not devices:
        print("No I2C device found! Check your wiring.")
        return None
    else:
        print(f"I2C device(s) found at: {[hex(d) for d in devices]}")
        return devices

def read_sensor():
    try:
        # Address is usually 0x76 or 0x77
        sensor = bme280.BME280(i2c=i2c, address=0x76)
        
        while True:
            # The library returns a tuple: (temp, pressure, humidity)
            # Example format: ('23.50C', '1013.25hPa', '50.00%')
            reading = sensor.values
            
            print(f"Temp: {reading[0]} | Pressure: {reading[1]} | Humidity: {reading[2]}")
            time.sleep(2)
            
    except Exception as e:
        print(f"Error reading sensor: {e}")

# Check connection then start loop
if scan_i2c():
    read_sensor()


