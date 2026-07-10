import network
import time
import machine

# Give the hardware a second to breathe
time.sleep(1)

wlan = network.WLAN(network.STA_IF)

# Force a reset of the Wi-Fi radio
wlan.active(False)
time.sleep(1)
wlan.active(True)

print("Scanning for networks...")
wlan.connect('Your_wifi_name', 'wifi_password')

# Wait for connection with a timeout (so it doesn't loop forever)
timeout = 10
while not wlan.isconnected() and timeout > 0:
    print("Connecting...")
    time.sleep(1)
    timeout -= 1

if wlan.isconnected():
    print("Connected!")
    print("ESP32 IP Address:", wlan.ifconfig()[0])
else:
    print("Failed to connect. Check your Password or Phone Hotspot settings.")
