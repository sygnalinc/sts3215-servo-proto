"""
Scan and find all connected servo IDs.

Usage:
    python src/scan_servos.py
"""

from scservo_sdk import PortHandler, sms_sts

PORT = '/dev/tty.usbmodem5B610357991'
BAUDRATE = 1000000
SCAN_RANGE = range(1, 20)  # ID 1~19 をスキャン


def main():
    port = PortHandler(PORT)
    servo = sms_sts(port)

    if not port.openPort():
        print(f"Failed to open port: {PORT}")
        return
    port.setBaudRate(BAUDRATE)

    print(f"Scanning servo IDs {SCAN_RANGE.start} ~ {SCAN_RANGE.stop - 1}...")
    found = []

    for sid in SCAN_RANGE:
        model, result, error = servo.ping(sid)
        if result == 0:
            print(f"  [FOUND] ID={sid}, Model={model}")
            found.append(sid)

    print(f"\nTotal: {len(found)} servo(s) found -> {found}")
    port.closePort()


if __name__ == '__main__':
    main()
