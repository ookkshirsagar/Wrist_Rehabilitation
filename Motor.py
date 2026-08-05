"""
Motor Control Module for Wrist Rehabilitation Robot
---------------------------------------------------

This module defines a `Motor` class that interfaces with Dynamixel motors 
using the DynamixelSDK to perform operations required for wrist rehabilitation. 

Key Features:
1. Initializes the motor for Current-based Position Control Mode.
2. Configures safety limits, including temperature and position constraints.
3. Configures motion profiles for smooth and controlled movements.
4. Monitors motor performance, including position, current, and safety conditions.
5. Provides centralized initialization for convenience and modular methods for flexibility.

References:
- Dynamixel XM540-W270-T/R Control Table: https://emanual.robotis.com/docs/en/dxl/x/xm540-w270/#control-table-data-address
- Normal wrist ROM values:
  73° flexion, 71° extension 
  Source: https://pubmed.ncbi.nlm.nih.gov/24322647/#:~:text=Results%3A%20Normal%20values%20for%20wrist,and%2060%20degrees%20of%20pronation
- Choosen wrsit ROM values:
  83° flexion, 81° extension; considering Safety
"""

from dynamixel_sdk import *
import logging

# -------Configure logging-----------------------------------------
"""
Configure logging to save logs into a structured directory (data/logs)
with a dynamically determined filename.
"""

import os

# Create the log file path dynamically
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # Determine project root
LOGS_DIR = os.path.join(PROJECT_ROOT, "data", "logs")      # Define logs directory path
os.makedirs(LOGS_DIR, exist_ok=True)                      # Create logs directory if it doesn't exist
LOG_FILE = os.path.join(LOGS_DIR, "motor_initialization.log")  # Define log file path

# Reset existing logging configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging to write logs to the specified file
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    filemode='w'  # Overwrite the log file on each run
)


class Motor:
    """
    A class for controlling Dynamixel motors using the Dynamixel SDK.

    Attributes:
        dxl_id (int): ID of the Dynamixel motor.
        baud_rate (int): Baud rate for communication.
        device_name (str): Name of the device/port (e.g., '/dev/ttyUSB0').
        protocol_version (float): Protocol version for communication.
    """

    # Control Table Addresses
    ADDR_ID = 7
    ADDR_OPERATING_MODE = 11
    ADDR_TEMPERATURE_LIMIT = 31
    ADDR_CURRENT_LIMIT = 38
    ADDR_MAX_POSITION_LIMIT = 48
    ADDR_MIN_POSITION_LIMIT = 52
    ADDR_SHUTDOWN = 63
    ADDR_TORQUE_ENABLE = 64
    ADDR_STATUS_RETURN_LEVEL = 68
    ADDR_POSITION_P_GAIN = 84
    ADDR_GOAL_CURRENT = 102
    ADDR_PROFILE_ACCELERATION = 108
    ADDR_PROFILE_VELOCITY = 112
    ADDR_GOAL_POSITION = 116
    ADDR_PRESENT_CURRENT = 126
    ADDR_PRESENT_POSITION = 132
    ADDR_PRESENT_TEMPERATURE = 146


    # ---------- Initialization Methods ----------
    def __init__(self, dxl_id, baud_rate, device_name, protocol_version):
        """
        Initializes the Motor object.

        Args:
            dxl_id (int): Motor ID.
            baud_rate (int): Communication baud rate.
            device_name (str): Device port name (e.g., '/dev/ttyUSB0').
            protocol_version (float): Protocol version (e.g., 2.0).
        """
        self.dxl_id = dxl_id
        self.baud_rate = baud_rate
        self.device_name = device_name
        self.protocol_version = protocol_version
        self.portHandler = PortHandler(device_name)
        self.packetHandler = PacketHandler(protocol_version)

    def openPort(self):
        """Opens the communication port for the motor."""
        if self.portHandler.openPort():
            logging.info("Successfully opened the port.")
        else:
            logging.error("Failed to open the port. Check device connection.")

    def setBaudRate(self):
        """Sets the communication baud rate."""
        if self.portHandler.setBaudRate(self.baud_rate):
            logging.info("Successfully set the baudrate.")
        else:
            logging.error("Failed to set the baudrate. Check configuration.")

    # ---------- Utility Methods ----------
    @staticmethod
    def twosComplement(num_bytes, decNumber):
        """Converts a number to its two's complement representation."""
        if num_bytes == 2:
            return decNumber - (0x10000 if decNumber > 0xFFFF // 2 else 0)
        elif num_bytes == 4:
            return decNumber - (0x100000000 if decNumber > 0xFFFFFFFF // 2 else 0)

    @staticmethod
    def intToHex(num_bytes, decNumber):
        """Converts a decimal number to its hexadecimal representation."""
        decNumber = int(decNumber)
        if num_bytes == 2:
            return decNumber & 0xFFFF
        elif num_bytes == 4:
            return decNumber & 0xFFFFFFFF

    # ---------- Register Read/Write Methods ----------
    def writeRegister(self, num_bytes, address, data):
        """Writes data to a register."""
        try:
            if num_bytes == 1:
                self.packetHandler.write1ByteTxRx(self.portHandler, self.dxl_id, address, data)
            elif num_bytes == 2:
                self.packetHandler.write2ByteTxRx(self.portHandler, self.dxl_id, address, data)
            elif num_bytes == 4:
                self.packetHandler.write4ByteTxRx(self.portHandler, self.dxl_id, address, data)
            logging.info(f"Successfully wrote to register at address {address}.")
        except Exception as e:
            logging.error(f"Error writing to register: {e}")

    def readRegister(self, num_bytes, address):
        """Reads data from a register."""
        try:
            if num_bytes == 1:
                return self.packetHandler.read1ByteTxRx(self.portHandler, self.dxl_id, address)[0]
            elif num_bytes == 2:
                return self.packetHandler.read2ByteTxRx(self.portHandler, self.dxl_id, address)[0]
            elif num_bytes == 4:
                return self.packetHandler.read4ByteTxRx(self.portHandler, self.dxl_id, address)[0]
        except Exception as e:
            logging.error(f"Error reading from register: {e}")

    # ---------- Configuration Methods ----------
    def initializeCurrentBasedPositionControl(self):
        """
        Initializes the motor for Current-based Position Control Mode.
        Ensures proper mode and configurations for rehabilitation tasks.
        """
        # Set Operating Mode to Current-based Position Control (5)
        current_mode = self.readRegister(1, self.ADDR_OPERATING_MODE)
        if current_mode != 5:
            logging.info("Setting Operating Mode to Current-based Position Control Mode (5).")
            self.setMode(5)
        else:
            logging.info("Operating Mode is already set to Current-based Position Control Mode.")

        # Set Current Limit to 1500 (approx. 4.03A)
        max_current_limit = 1500  # Example value for wrist rehab; adjust as needed
        self.writeRegister(2, self.ADDR_CURRENT_LIMIT, max_current_limit)
        logging.info(f"Set Current Limit to {max_current_limit} (approx. 4.03A).")

        # Enable Torque
        self.setTorque(1)
        logging.info("Torque Enabled for Current-based Position Control Mode.")

    def configureSafetyLimits(self, temp_limit=80):
        """
        Configures safety parameters such as temperature and position limits for the wrist rehabilitation robot.

        Args:
            temp_limit (int): Maximum temperature limit in °C.
        """
        # Set Temperature Limit
        self.writeRegister(1, self.ADDR_TEMPERATURE_LIMIT, temp_limit)
        logging.info(f"Temperature limit set to {temp_limit} °C.")

        # Calculate Position Limits for Wrist ROM
        pulses_per_degree = 4096 / 360
        max_pos = int(2048 + (81 * pulses_per_degree))  # Extension (+81°)
        min_pos = int(2048 - (83 * pulses_per_degree))  # Flexion (-83°)

        # Set Max and Min Position Limits
        self.writeRegister(4, self.ADDR_MAX_POSITION_LIMIT, max_pos)
        logging.info(f"Maximum position limit set to {max_pos} pulses (approx. +81°).")
        
        self.writeRegister(4, self.ADDR_MIN_POSITION_LIMIT, min_pos)
        logging.info(f"Minimum position limit set to {min_pos} pulses (approx. -83°).")

    def configureMotionProfiles(self, acceleration=100, velocity=200):
        """
        Configures motion profiles for smooth movement.

        Args:
            acceleration (int): Acceleration profile value.
            velocity (int): Velocity profile value.
        """
        self.writeRegister(4, self.ADDR_PROFILE_ACCELERATION, acceleration)
        logging.info(f"Acceleration profile set to {acceleration}.")

        self.writeRegister(4, self.ADDR_PROFILE_VELOCITY, velocity)
        logging.info(f"Velocity profile set to {velocity}.")

    # ---------- Monitoring Methods ----------
    def readPosition(self):
        """
        Reads the current position of the motor.

        Returns:
            float: Motor position in radians.
        """
        pos = self.readRegister(4, self.ADDR_PRESENT_POSITION)
        position_in_radians = self.twosComplement(4, pos) * (3.14 / 2048)
        logging.info(f"Current position: {position_in_radians:.2f} radians.")
        return position_in_radians

    def readCurrent(self):
        """
        Reads the current consumption of the motor.

        Returns:
            int: Current value in milliamps.
        """
        current = self.readRegister(2, self.ADDR_PRESENT_CURRENT)
        current_mA = self.twosComplement(2, current) * (5.5 / 2047)
        logging.info(f"Current consumption: {current_mA:.2f} mA.")
        return current_mA

    def monitorShutdownConditions(self):
        """
        Monitors the shutdown register for safety-critical conditions.
        """
        shutdown_conditions = self.readRegister(1, self.ADDR_SHUTDOWN)
        logging.info(f"Current shutdown conditions: {bin(shutdown_conditions)}")
        return shutdown_conditions

    # ---------- Control Methods ----------
    def setMode(self, mode):
        """Sets the operating mode of the motor."""
        self.writeRegister(1, self.ADDR_OPERATING_MODE, mode)

    def setTorque(self, enable_flag):
        """Enables or disables the motor torque."""
        self.writeRegister(1, self.ADDR_TORQUE_ENABLE, enable_flag)

    def setPosition(self, desired_position):
        """
        Sets the motor to the desired position.

        Args:
            desired_position (int): Desired position in pulses.
        """
        self.writeRegister(4, self.ADDR_GOAL_POSITION, desired_position)
        logging.info(f"Goal position set to {desired_position} pulses.")

    def setGoalCurrent(self, desired_current):
        """
        Sets the goal current for the motor.

        Args:
            desired_current (float): Desired current in milliamps.
        """
        current_value = int(self.intToHex(2, desired_current * (2047 / 5500)))  # Scaling factor
        self.writeRegister(2, self.ADDR_GOAL_CURRENT, current_value)
        logging.info(f"Goal current set to {desired_current:.2f} mA.")

    # ---------- Centralized Initialization ----------
    def initializeWristRehabRobot(self, temp_limit=80, acceleration=100, velocity=200):
        """
        Initializes the wrist rehabilitation robot by setting up communication, safety parameters, 
        and motion profiles.

        Args:
            temp_limit (int): Maximum temperature limit in °C.
                Default: 80°C
            acceleration (int): Acceleration profile value.
                Recommended:
                    - For smooth, gradual motion: 50 ~ 150
                    - For faster, responsive motion: 150 ~ 500
                Default: 100
            velocity (int): Velocity profile value.
                Recommended:
                    - For slow movements: 50 ~ 200
                    - For moderate speed: 200 ~ 500
                    - For high speed: 500 ~ 1000
                Default: 200
        """
        logging.info("Initializing wrist rehabilitation robot...")

        # Step 1: Open communication port
        self.openPort()

        # Step 2: Set baud rate
        self.setBaudRate()

        # Step 3: Set operating mode and current limit for Current-based Position Control
        self.initializeCurrentBasedPositionControl()

        # Step 4: Configure safety parameters
        self.configureSafetyLimits(temp_limit=temp_limit)

        # Step 5: Configure motion profiles
        self.configureMotionProfiles(acceleration=acceleration, velocity=velocity)

        logging.info("Wrist rehabilitation robot initialization complete.")
