import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL, board.SDA)

text = "Hello World"

disp = SSD1306_I2C(128, 64, i2c)

disp.fill(0)
disp.show()

image = Image.new("1", (disp.width, disp.height))

draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)

draw.text((0, 0), text, font=font, fill=255)

disp.image(image)
disp.show()
