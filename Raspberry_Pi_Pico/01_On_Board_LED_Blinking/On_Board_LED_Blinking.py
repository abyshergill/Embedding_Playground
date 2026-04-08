from machine import Pin
import time

# "LED" is a shortcut for the onboard LED pin on the Pico
# For older Pico firmware, you might need to use Pin(25, Pin.OUT)
led = Pin("LED", Pin.OUT)

while True:
    led.toggle()      # Switches the LED state (On to Off, Off to On)
    time.sleep(0.5)   # Wait for 500 milliseconds