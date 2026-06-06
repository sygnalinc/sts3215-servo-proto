"""
STS3215 Servo basic control example via Waveshare Bus Servo Adapter.

Usage:
    python src/servo_test.py
"""

import time
from scservo_sdk import PortHandler, PacketHandler, COMM_SUCCESS

# --- Configuration ---
PORT = '/dev/tty.usbserial-XXXX'  # Change to your actual port
BAUDRATE = 1000000
SERVO_ID = 1

# STS3215 Register addresses
ADDR_TORQUE_ENABLE = 40
ADDR_GOAL_POSITION = 42
ADDR_PRESENT_POSITION = 56

# Position range: 0 ~ 4095 (center = 2048)
POS_CENTER = 2048
POS_MIN = 1024
POS_MAX = 3072


def main():
    port = PortHandler(PORT)
    packet = PacketHandler(0)  # STS series uses protocol 0

    if not port.openPort():
        print(f"Failed to open port: {PORT}")
        return
    print(f"Opened port: {PORT}")

    if not port.setBaudRate(BAUDRATE):
        print(f"Failed to set baudrate: {BAUDRATE}")
        port.closePort()
        return
    print(f"Baudrate: {BAUDRATE}")

    # Enable torque
    packet.write1ByteTxRx(port, SERVO_ID, ADDR_TORQUE_ENABLE, 1)
    print("Torque enabled")

    try:
        positions = [POS_CENTER, POS_MIN, POS_CENTER, POS_MAX, POS_CENTER]
        for pos in positions:
            print(f"Moving to position: {pos}")
            packet.write2ByteTxRx(port, SERVO_ID, ADDR_GOAL_POSITION, pos)
            time.sleep(1.5)

            # Read current position
            result, _, _ = packet.read2ByteTxRx(port, SERVO_ID, ADDR_PRESENT_POSITION)
            print(f"  Current position: {result}")

    except KeyboardInterrupt:
        print("\nStopped by user")

    finally:
        # Disable torque
        packet.write1ByteTxRx(port, SERVO_ID, ADDR_TORQUE_ENABLE, 0)
        print("Torque disabled")
        port.closePort()
        print("Port closed")


if __name__ == '__main__':
    main()
