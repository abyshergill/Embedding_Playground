import socket
import network
from machine import Pin

# 1. Setup Hardware
led = Pin(2, Pin.OUT)

# 2. Connect to WiFi
ssid = 'HMD CREST'
password = 'aby123456'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

print("Connecting to WiFi...")

while not station.isconnected():
    pass

print("Connection successful!")
ip_address = station.ifconfig()[0]
port = 80
print(f"Web Server is active at: http://{ip_address}:{port}")

# 3. Web Page Template with Dynamic Status
def web_page():
    # Check current LED state
    state = "ON" if led.value() == 1 else "OFF"
    # Dynamic color based on state
    status_color = "#4CAF50" if state == "ON" else "#f44336"
    
    html = f"""<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>ESP32 Web Server</title>
        <style>
            body {{ font-family: Arial; text-align: center; margin-top: 50px; }}
            .button {{ padding: 20px; font-size: 20px; text-decoration: none; color: white; border-radius: 5px; display: inline-block; width: 120px; }}
            .on {{ background-color: #4CAF50; }}
            .off {{ background-color: #f44336; }}
            .status-box {{ font-size: 24px; font-weight: bold; color: {status_color}; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>ESP32 Control Center</h1>
        <div class="status-box">Current Status: {state}</div>
        <p><a href="/?led=on" class="button on">Turn ON</a></p>
        <p><a href="/?led=off" class="button off">Turn OFF</a></p>
    </body>
    </html>"""
    return html

# 4. Start Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))
s.listen(5)

while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()
        
        # 1. Ignore empty requests or favicon requests
        if not request or 'favicon.ico' in request:
            conn.close()
            continue

        # 2. Only change the LED if the specific string is in the URL
        if '/?led=on' in request:
            led.value(1)
        elif '/?led=off' in request:
            led.value(0)
            
        # 3. Generate and send response
        response = web_page()
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
        conn.sendall(response)
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        try: conn.close()
        except: pass
