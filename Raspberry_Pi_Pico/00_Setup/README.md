# 🛠 Raspberry Pi Pico MicroPython Setup Guide

## 1. Download MicroPython Firmware
- Visit the official Raspberry Pi Pico documentation: [Pico Series Documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#pico2).
- Download the latest **UF2 firmware file** for MicroPython (specific to your Pico model, e.g., Pico or Pico W).

## 2. Connect Pico to Your Computer
- Hold down the **BOOTSEL** button on the Pico.
- While holding, plug the Pico into your computer via micro‑USB.
- The Pico will appear as a **USB mass storage device** named `RPI-RP2`.

## 3. Flash MicroPython Firmware
- Drag and drop the downloaded **UF2 file** onto the `RPI-RP2` drive.
- The Pico will reboot automatically and is now running MicroPython.

## 4. Install a Python Editor
You need an editor to write and upload MicroPython code:
- **Thonny IDE** (recommended for beginners):
  - Download from [Thonny.org](https://thonny.org).
  - Install it on your computer (Windows, macOS, or Linux).
- Alternatives: Mu Editor, or VS Code with MicroPython plugins.

## 5. Configure Thonny for Pico
- Open **Thonny**.
- Go to **Tools → Options → Interpreter**.
- Select **MicroPython (Raspberry Pi Pico)**.
- Choose the correct **COM port** (Windows) or device path (macOS/Linux).
- Click **OK**.

## 6. Test Your Setup
Paste the following code into Thonny:

```python
from machine import Pin, Timer

led = Pin("LED", Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
