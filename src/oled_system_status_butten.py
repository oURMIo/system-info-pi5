import socket
import subprocess
import time

import board
import digitalio
import psutil
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

WIDTH = 128
HEIGHT = 64
LINE_HEIGHT = 10
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 10

BUTTON_PIN = board.D17
DEBOUNCE_TIME = 0.3

SYSTEM_UPDATE_INTERVAL = 1
SLOW_UPDATE_INTERVAL = 180


def init_display():
    i2c = board.I2C()
    display = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    display.fill(0)
    display.show()
    return display


def init_button():
    button = digitalio.DigitalInOut(BUTTON_PIN)
    button.direction = digitalio.Direction.INPUT
    return button


def create_canvas(display):
    image = Image.new("1", (display.width, display.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    return image, draw, font


def get_ip_address():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0)
            s.connect(("10.254.254.254", 1))
            return s.getsockname()[0]
    except Exception:
        return "NO IP"


def get_cpu_temp():
    try:
        result = subprocess.run(
            ["vcgencmd", "measure_temp"], capture_output=True, text=True
        )
        return result.stdout.strip().split("=")[1].replace("'C", "")
    except Exception:
        return "N/A"


def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    net_before = psutil.net_io_counters()
    time.sleep(1)
    net_after = psutil.net_io_counters()

    net_sent = (net_after.bytes_sent - net_before.bytes_sent) / 1024
    net_recv = (net_after.bytes_recv - net_before.bytes_recv) / 1024

    return cpu, ram, net_sent, net_recv


def render(draw, font, lines):
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    for i, line in enumerate(lines):
        draw.text((0, i * LINE_HEIGHT), line, font=font, fill=255)


def turn_off(display):
    display.fill(0)
    display.show()
    display.poweroff()


def turn_on(display):
    display.poweron()


def button_pressed(button, prev_state):
    current = button.value
    pressed = current and not prev_state
    return pressed, current


def main():
    display = init_display()
    button = init_button()
    image, draw, font = create_canvas(display)

    display_on = True
    prev_button = button.value

    ip = get_ip_address()
    disk = psutil.disk_usage("/").percent
    last_slow_update = time.time()

    while True:
        pressed, prev_button = button_pressed(button, prev_button)

        if pressed:
            display_on = not display_on
            if display_on:
                turn_on(display)
            else:
                turn_off(display)
            time.sleep(DEBOUNCE_TIME)
            continue

        if not display_on:
            time.sleep(0.05)
            continue

        now = time.time()

        if now - last_slow_update >= SLOW_UPDATE_INTERVAL:
            ip = get_ip_address()
            disk = psutil.disk_usage("/").percent
            last_slow_update = now

        cpu, ram, net_sent, net_recv = get_system_stats()
        temp = get_cpu_temp()

        lines = [
            f"IP: {ip}",
            f"CPU: {cpu:.1f}%",
            f"RAM: {ram:.1f}%",
            f"Disk: {disk:.1f}%",
            f"Temp: {temp}C",
            f"Net: {net_sent:.1f}K/{net_recv:.1f}K",
        ]

        render(draw, font, lines)
        display.image(image)
        display.show()


if __name__ == "__main__":
    main()
