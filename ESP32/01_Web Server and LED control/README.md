# ESP32 Web Server: Onboard LED Control (MicroPython)
This project is a dedicated module within my Embedding Playground for testing MicroPython-based network interactions. It demonstrates how to create a lightweight socket server on the ESP32 to control hardware via a web browser.

## Purpose
- **Prototyping:** Validating MicroPython's network and usocket modules.
- **Code Reference:** A master script for copy-pasting stable Wi-Fi connection routines and HTML string handling.
- **Logic Testing: Testing how Python’s interpreted nature handles real-time GPIO requests compared to compiled code.

## Features
- **Socket-Based Server:** Uses Python's socket library to listen for HTTP GET requests.
- **Dynamic HTML:** Serves a UI that changes based on the LED's current physical state.
- **REPL Feedback:** Real-time logging of client IP addresses and request headers to the terminal.

## Hardware Requirements
- **Board:** ESP32 with MicroPython firmware installed.
- **Onboard LED:** Usually mapped to Pin 2 in MicroPython (machine.Pin(2, machine.Pin.OUT)).

## Software & Environment
- **Firmware:** MicroPython for ESP32 (v1.19 or later recommended).
- **IDE:** Thonny, Mu, or VS Code (with Pymakr extension).
- **Language:** Python 3 (MicroPython flavor).

## Setup Instructions
- Open main.py (or the script file in this folder).
- Modify the Wi-Fi configuration section with your credentials:
```Python
ssid = 'YOUR_WIFI_NAME'
password = 'YOUR_WIFI_PASSWORD'
```
- Upload the script to your ESP32.
- Run the script. The Serial REPL will display: Connection established and the IP Address.
- Open your browser and navigate to that IP address to toggle the LED.