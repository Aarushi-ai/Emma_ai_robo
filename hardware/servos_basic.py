"""
servos_basic.py
---------------
Basic Servo Movement Script for Emma AI Robot.
Controls 3 servo motors (Left Arm, Right Arm, Head) via Arduino
using the cvzone SerialModule for serial communication.

Hardware: Arduino + 3x Servo Motors
Libraries: cvzone, pyserial
"""

from cvzone.SerialModule import SerialObject
from time import sleep

# ---------------------- INITIALIZATION ----------------------

# Create a Serial Object with three digit precision for sending servo angles
arduino = SerialObject(digits=3)

# Initialize last known positions: [LServo, RServo, HServo]
# Left starts at 180°, Right starts at 0°, Head starts at 90°
last_positions = [180, 0, 90]

# ---------------------- FUNCTIONS ----------------------

def move_servo(target_positions, delay=0.0001):
    """
    Moves the servos smoothly to the target positions.

    :param target_positions: List of target angles [LServo, RServo, HServo]
    :param delay: Time delay (in seconds) between each increment step
    """
    global last_positions

    max_steps = max(abs(target_positions[i] - last_positions[i]) for i in range(3))

    if max_steps == 0:  # Guard against division by zero if already at target
        return

    for step in range(max_steps):
        current_positions = [
            last_positions[i] + (step + 1) * (target_positions[i] - last_positions[i]) // max_steps
            if abs(target_positions[i] - last_positions[i]) > step else last_positions[i]
            for i in range(3)
        ]
        arduino.sendData(current_positions)
        sleep(delay)

    last_positions = target_positions[:]


# ---------------------- MAIN ----------------------

if __name__ == "__main__":
    # Move all servos to neutral (90°) position
    target_positions = [90, 90, 90]
    move_servo(target_positions)
