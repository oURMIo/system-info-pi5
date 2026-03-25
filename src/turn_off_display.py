import board
from adafruit_ssd1306 import SSD1306_I2C

i2c = board.I2C()
disp = SSD1306_I2C(128, 64, i2c)

disp.fill(0)
disp.show()
disp.poweroff()

print("Display turned off.")
