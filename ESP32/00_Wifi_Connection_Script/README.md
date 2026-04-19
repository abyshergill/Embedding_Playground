# 📡 ESP32 Wi-Fi Connection Script (MicroPython)

This script connects an ESP32 device to a Wi-Fi network using MicroPython. It includes a simple retry mechanism and timeout to prevent infinite connection loops.
```bash
🧾 Code
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

```
## ⚙️ How It Works
1. Initialize Modules
network: Handles Wi-Fi connectivity
time: Adds delays
machine: Interfaces with hardware
2. Reset Wi-Fi Interface

The script disables and re-enables the Wi-Fi interface to ensure a clean start:
```bash
wlan.active(False)
time.sleep(1)
wlan.active(True)
```
3. Connect to Wi-Fi

Replace the placeholders with your actual credentials:
```bash
wlan.connect('Your_wifi_name', 'wifi_password')
```
4. Connection Timeout Loop

The script waits up to 10 seconds for a connection:
```bash
timeout = 10
while not wlan.isconnected() and timeout > 0:
```
This prevents the device from getting stuck trying to connect forever.

5. Connection Status
- ✅ On success: Prints the assigned IP address
- ❌ On failure: Displays an error message
##  🛠️ Customization

Change timeout duration:
```bash
timeout = 20  # wait longer
```
Add retry logic: Wrap the connection block in a loop if needed.

Debug available networks:
```bash
print(wlan.scan())
```
## ⚠️ Notes
- Ensure your Wi-Fi:
    - Uses 2.4 GHz (ESP32 typically doesn’t support 5 GHz)
    - Has correct SSID and password
- If using a phone hotspot, verify:
    - Hotspot is active
    - Device limits are not exceeded
## 🚀 Output Example
```bsh
Scanning for networks...
Connecting...
Connecting...
Connected!
ESP32 IP Address: 192.168.1.45
```