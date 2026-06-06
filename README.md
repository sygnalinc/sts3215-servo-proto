# sts3215-servo-proto

STS3215 serial bus servo prototype controller via Waveshare Bus Servo Adapter on Mac.

## Hardware

- [Feetech STS3215](https://www.feetechrc.com/sts3215.html) - Serial bus servo
- [Waveshare Bus Servo Adapter](https://www.waveshare.com/bus-servo-adapter-a.htm) - USB adapter

## Requirements

- Python 3.8+
- macOS

## Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

### Driver Installation

The Waveshare Bus Servo Adapter uses a CH343P chip. Install the driver:

```bash
brew install --cask wch-ch34x-usb-serial-driver
```

Or download from [WCH official site](https://www.wch-ic.com/downloads/CH343SER_MAC_ZIP.html).

### Check Connection

After connecting the adapter via USB:

```bash
ls /dev/tty.*
# Should show: /dev/tty.usbserial-XXXX or /dev/tty.wchusbserial-XXXX
```

## Usage

```bash
python src/servo_test.py
```

## Project Structure

```
sts3215-servo-proto/
├── src/
│   └── servo_test.py   # Basic servo control example
├── requirements.txt
└── README.md
```
