"""
Controller Operations Test
--------------------------

This script tests the integration and functionality of the `Controller` class,
which manages high-level operations for the wrist rehabilitation system.

Features:
1. Initializes the Controller class with a Motor instance.
2. Tests the PD control logic by moving to a target position.
3. Verifies logging of controller operations.

Usage:
------
Run the following command from the project root directory:

    python tests/test_controller_operations.py

Make sure the `Motor.py`, `Controller.py`, and `config/motor_config.py` modules are accessible from the project root.
"""

import os
import sys
import logging
import time

# Add the project root directory to the Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Import Controller, Motor, and configuration
try:
    from Controller import Controller
    from Motor import Motor
    from config.motor_config import MOTOR_ID, BAUD_RATE, DEVICE_NAME, PROTOCOL_VERSION
except ImportError as e:
    logging.error(f"ImportError: {e}")
    raise

# Dynamically create log file path
LOGS_DIR = os.path.join(PROJECT_ROOT, "data", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)  # Create the logs directory if it doesn't exist
LOG_FILE = os.path.join(LOGS_DIR, f"{os.path.splitext(os.path.basename(__file__))[0]}.log")

# Reset existing logging configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging to write to the dynamically determined log file
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    filemode='w'  # Overwrite the log file on each run
)

def test_controller_operations():
    """
    Tests the Controller class functionality.

    - Initializes a Motor instance.
    - Creates a Controller instance with PD gains.
    - Moves the motor to a target position and logs results.
    """
    try:
        # Step 1: Initialize Motor
        motor = Motor(MOTOR_ID, BAUD_RATE, DEVICE_NAME, PROTOCOL_VERSION)
        motor.openPort()
        motor.setBaudRate()
        motor.initializeWristRehabRobot()

        logging.info("Motor initialized successfully for Controller test.")

        # Step 2: Initialize Controller
        controller = Controller(motor, kp=1.0, kd=0.1)
        logging.info("Controller initialized with PD gains: Kp=1.0, Kd=0.1")

        # Step 3: Test Target Position
        target_position = 30  # Move to 30° as a test
        logging.info(f"Testing Controller: Moving to target position {target_position}°")
        controller.set_target_position(target_position)

        # Step 4: Stop Motor
        controller.stop()
        logging.info("Controller test completed successfully.")

    except Exception as e:
        logging.error(f"Error during controller operations test: {e}")

if __name__ == "__main__":
    test_controller_operations()
