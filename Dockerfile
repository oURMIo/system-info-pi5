FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    i2c-tools \
    fonts-dejavu-core \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/oled_system_status_butten.py .

CMD ["python", "-u", "oled_system_status_butten.py"]
