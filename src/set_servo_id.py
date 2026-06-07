"""
Change servo ID.
Connect only ONE servo at a time when running this script.

Usage:
    python src/set_servo_id.py <current_id> <new_id>

Example:
    python src/set_servo_id.py 1 2
"""

import sys
from scservo_sdk import PortHandler, sms_sts

PORT = '/dev/tty.usbmodem5B610357991'
BAUDRATE = 1000000


def main():
    if len(sys.argv) != 3:
        print("Usage: python src/set_servo_id.py <current_id> <new_id>")
        print("Example: python src/set_servo_id.py 1 2")
        sys.exit(1)

    current_id = int(sys.argv[1])
    new_id = int(sys.argv[2])

    if not (1 <= new_id <= 253):
        print("Error: ID must be between 1 and 253")
        sys.exit(1)

    port = PortHandler(PORT)
    servo = sms_sts(port)

    if not port.openPort():
        print(f"Failed to open port: {PORT}")
        return
    port.setBaudRate(BAUDRATE)

    # Ping
    model, result, error = servo.ping(current_id)
    if result != 0:
        print(f"Servo ID={current_id} not found. Check connection.")
        port.closePort()
        return
    print(f"Found servo ID={current_id}, Model={model}")

    # Change ID
    result, error = servo.write1ByteTxRx(current_id, 5, new_id)
    if result == 0:
        print(f"ID changed: {current_id} -> {new_id}")
    else:
        print(f"Failed to change ID. result={result}")

    port.closePort()


if __name__ == '__main__':
    main()
