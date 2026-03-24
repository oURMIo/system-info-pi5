import board
from adafruit_ssd1306 import SSD1306_I2C

WIDTH = 128
HEIGHT = 64

print("Initializing I2C...")
i2c = board.I2C()

print("Scanning I2C bus...")
while not i2c.try_lock():
    pass

devices = i2c.scan()
i2c.unlock()

if not devices:
    print("No I2C devices found. Check wiring.")
else:
    print(f"I2C devices found at addresses: {[hex(d) for d in devices]}")

print("Initializing SSD1306 OLED display...")
try:
    disp = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    disp.fill(0)
    disp.show()
    disp.fill(1)
    disp.show()
    disp.fill(0)
    disp.show()
    print("Display connection successful!")
except Exception as e:
    print(f"Display connection failed: {e}")
