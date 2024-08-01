import board
import busio
import socket
import psutil
import subprocess
import time
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL, board.SDA)
disp = SSD1306_I2C(128, 64, i2c)

disp.fill(0)
disp.show()

image = Image.new("1", (disp.width, disp.height))
draw = ImageDraw.Draw(image)

font_size = 10
font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size
)


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(("10.254.254.254", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "NO IP"
    finally:
        s.close()
    return ip


def get_cpu_temp():
    try:
        result = subprocess.run(
            ["vcgencmd", "measure_temp"], capture_output=True, text=True
        )
        temp_str = result.stdout.strip()
        temp = temp_str.split("=")[1].replace("'C", "")
    except Exception:
        temp = "N/A"
    return temp


def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    net_before = psutil.net_io_counters()
    time.sleep(1)
    net_after = psutil.net_io_counters()
    net_sent = (net_after.bytes_sent - net_before.bytes_sent) / 1024
    net_recv = (net_after.bytes_recv - net_before.bytes_recv) / 1024
    return cpu_usage, memory_usage, net_sent, net_recv


IP_DISK_UPDATE_INTERVAL = 180  # 3 min
SYSTEM_UPDATE_INTERVAL = 1  # 1 sec

last_ip_disk_update_time = time.time()
last_system_update_time = time.time()

ip_address = get_ip_address()
disk_usage = psutil.disk_usage("/").percent

while True:
    current_time = time.time()

    if current_time - last_ip_disk_update_time >= IP_DISK_UPDATE_INTERVAL:
        ip_address = get_ip_address()
        disk_usage = psutil.disk_usage("/").percent
        last_ip_disk_update_time = current_time

    if current_time - last_system_update_time >= SYSTEM_UPDATE_INTERVAL:
        cpu_usage, memory_usage, net_sent, net_recv = get_system_info()
        cpu_temp = get_cpu_temp()

        draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)

        draw.text((0, 0), f"IP: {ip_address}", font=font, fill=255)
        draw.text((0, 10), f"CPU: {cpu_usage:.1f}%", font=font, fill=255)
        draw.text((0, 20), f"RAM: {memory_usage:.1f}%", font=font, fill=255)
        draw.text((0, 30), f"Disk: {disk_usage:.1f}%", font=font, fill=255)
        draw.text((0, 40), f"Temp: {cpu_temp}C", font=font, fill=255)
        draw.text((0, 50), f"Net: {net_sent:.1f}K/{net_recv:.1f}K", font=font, fill=255)

        disp.image(image)
        disp.show()

        last_system_update_time = current_time

    time.sleep(0.05)  # Small sleep to avoid 100% CPU usage
