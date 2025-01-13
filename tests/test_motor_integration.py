"""
Motor Integration Test
----------------------

This script tests the integration of the Motor class with the configuration 
defined in `motor_config.py`. It verifies that the motor can be initialized 
successfully with the provided configuration values.

Usage:
------
Run the following command from the project root directory:

    python tests/test_motor_integration.py

Make sure the `config/` and `Motor.py` modules are accessible from the project root.
"""

import sys
import os
import logging

# Add the project root directory to the Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


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


# Import Motor and configuration
try:
    from Motor import Motor
    from config.motor_config import MOTOR_ID, BAUD_RATE, DEVICE_NAME, PROTOCOL_VERSION
except ImportError as e:
    logging.error(f"ImportError: {e}")
    raise

# Configure logging for the test
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def test_motor_integration():
    """
    Tests the initialization of the Motor class using configuration values.

    Logs the result of the test and any encountered errors, including whether the motor is connected.
    """
    try:
        # Initialize the motor using configuration values
        motor = Motor(MOTOR_ID, BAUD_RATE, DEVICE_NAME, PROTOCOL_VERSION)
        logging.info("Motor initialized successfully.")
        logging.info(f"Configuration Details:\n"
                     f" - Motor ID: {MOTOR_ID}\n"
                     f" - Baud Rate: {BAUD_RATE}\n"
                     f" - Device Name: {DEVICE_NAME}\n"
                     f" - Protocol Version: {PROTOCOL_VERSION}")

        # Verify motor connection by pinging the motor
        dxl_model_number, dxl_comm_result, dxl_error = motor.packetHandler.ping(motor.portHandler, MOTOR_ID)

        if dxl_comm_result == 0 and dxl_error == 0:
            logging.info(f"Motor connected successfully. Model Number: {dxl_model_number}")
        else:
            logging.warning("Failed to verify motor connection. Check wiring and configuration.")

    except Exception as e:
        logging.error(f"Error during motor initialization or connection test: {e}")

if __name__ == "__main__":
    test_motor_integration()
