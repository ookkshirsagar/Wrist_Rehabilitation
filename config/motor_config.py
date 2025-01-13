"""
Motor Configuration
-------------------

This module defines the essential configuration parameters for the wrist rehabilitation robot's motors.
The configurations are shared between the Doctor and Patient systems to ensure consistent operation.

Attributes:
    MOTOR_ID (int): Unique ID assigned to the Dynamixel motor.
    BAUD_RATE (int): Communication baud rate for serial communication.
    DEVICE_NAME (str): Name of the serial device (e.g., '/dev/ttyUSB0').
    PROTOCOL_VERSION (float): Communication protocol version supported by the Dynamixel motor.
"""

# Motor Configuration
MOTOR_ID = 1               # Dynamixel motor ID (unique identifier)
BAUD_RATE = 1000000          # Communication baud rate (in bps)
DEVICE_NAME = '/dev/ttyUSB0'  # Serial port name (update based on system setup)
PROTOCOL_VERSION = 2.0     # Dynamixel communication protocol version (e.g., 2.0)
