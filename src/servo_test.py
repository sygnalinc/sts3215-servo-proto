"""
STS3215 x2 servo control example via Waveshare Bus Servo Adapter.

Usage:
    python src/servo_test.py
"""

import time
from scservo_sdk import PortHandler, sms_sts, SMS_STS_TORQUE_ENABLE

# --- Configuration ---
PORT = '/dev/tty.usbmodem5B610357991'
BAUDRATE = 1000000
SERVO_ID_1 = 1
SERVO_ID_2 = 2

# Position range: 0 ~ 4095 (center = 2048)
POS_CENTER = 2048
POS_MIN = 1024
POS_MAX = 3072
SPEED = 2000
ACC = 200


def move_sync(servo, positions):
    """Move two servos simultaneously using SyncWrite."""
    servo.groupSyncWrite.clearParam()
    for sid, pos in positions.items():
        servo.SyncWritePosEx(sid, pos, SPEED, ACC)
    servo.groupSyncWrite.txPacket()


def main():
    port = PortHandler(PORT)
    servo = sms_sts(port)

    if not port.openPort():
        print(f"Failed to open port: {PORT}")
        return
    print(f"Opened port: {PORT}")
    port.setBaudRate(BAUDRATE)

    # Ping both servos
    for sid in [SERVO_ID_1, SERVO_ID_2]:
        model, result, error = servo.ping(sid)
        if result != 0:
            print(f"Servo ID={sid} not found! Check connection and ID.")
            port.closePort()
            return
        print(f"Servo ID={sid} found! Model={model}")

    try:
        # 順番に動かすステップ: (servo_id, position)
        steps = [
            (SERVO_ID_1, POS_MIN),
            (SERVO_ID_1, POS_CENTER),
            (SERVO_ID_2, POS_MAX),
            (SERVO_ID_2, POS_CENTER),
            (SERVO_ID_1, POS_MAX),
            (SERVO_ID_1, POS_CENTER),
            (SERVO_ID_2, POS_MIN),
            (SERVO_ID_2, POS_CENTER),
        ]

        for sid, pos in steps:
            print(f"Moving ID={sid} -> {pos}")
            servo.WritePosEx(sid, pos, SPEED, ACC)
            time.sleep(0.6)

    except KeyboardInterrupt:
        print("\nStopped by user")

    finally:
        for sid in [SERVO_ID_1, SERVO_ID_2]:
            servo.write1ByteTxRx(sid, SMS_STS_TORQUE_ENABLE, 0)
        print("Torque disabled")
        port.closePort()
        print("Port closed")


if __name__ == '__main__':
    main()
