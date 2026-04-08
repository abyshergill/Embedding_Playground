from machine import Pin
import time
# We use 15 because we plugged it into GP15
external_led = Pin(15, Pin.OUT) 

while True:
    external_led.toggle()      # Switches the LED state (On to Off, Off to On)
    time.sleep(0.5)
#external_led.value(1) # Turn it on