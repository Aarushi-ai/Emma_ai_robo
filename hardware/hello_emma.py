"""
hello_emma.py
-------------
Hello Gesture Script for Emma AI Robot.

Makes Emma wave "hello" by moving the right arm servo
back and forth using smooth incremental motion.

Hardware: Arduino + 3x Servo Motors
Libraries: cvzone, pyserial
"""

from cvzone.SerialModule import SerialObject  # Serial communication with Arduino
from time import sleep  # Delays between actions

# ---------------------- INITIALIZATION ----------------------

# Create a Serial Object with three digit precision
arduino = SerialObject(digit=3)

# Initial positions: [LServo=180°, RServo=0°, HServo=90°]
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

    for step in range(max_steps):
        current_positions = [
            last_positions[i] + (step + 1) * (target_positions[i] - last_positions[i]) // max_steps
            if abs(target_positions[i] - last_positions[i]) > step else last_positions[i]
            for i in range(3)
        ]
        arduino.sendData(current_positions)
        sleep(delay)

    last_positions = target_positions[:]


def hello_gesture():
    """
    Makes Emma wave hello by moving the right servo back and forth.
    """
    global last_positions
    # Raise right arm to start waving
    move_servo([last_positions[0], 180, last_positions[2]])
    # Wave back and forth 3 times
    for _ in range(3):
        move_servo([last_positions[0], 150, last_positions[2]])  # Arm slightly down
        move_servo([last_positions[0], 180, last_positions[2]])  # Arm back up
    # Reset arm to original position
    move_servo([last_positions[0], 0, last_positions[2]])


# ---------------------- MAIN ----------------------

if __name__ == "__main__":
    hello_gesture()
