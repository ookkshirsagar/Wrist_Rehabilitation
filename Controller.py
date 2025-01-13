"""
Controller Module for Wrist Rehabilitation System
-------------------------------------------------

This module defines the `Controller` class, which manages high-level operations 
for the wrist rehabilitation system using Current-Based Position Control.

Features:
1. Implements PD control for smooth and precise motion.
2. Manages motor position targets and feedback loops.
3. Interfaces with the Motor module for low-level operations.
4. Supports extension and flexion movements with customizable ranges.

Note:
This module is designed to be imported and used in `Doctor.py` and `Patient.py` 
to operate the wrist rehabilitation system on both ends.

References:
- PD control selection for wrist rehab: Optimized for Current-Based Position Control.
- Dynamixel XM540-W270-T/R Control Table: https://emanual.robotis.com/docs/en/dxl/x/xm540-w270/#control-table-data-address
"""

import os
import time
import logging

# Create the log file path dynamically
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # Determine project root
LOGS_DIR = os.path.join(PROJECT_ROOT, "data", "logs")      # Define logs directory path
os.makedirs(LOGS_DIR, exist_ok=True)                      # Create logs directory if it doesn't exist
LOG_FILE = os.path.join(LOGS_DIR, "controller_intialization.log")  # Define log file path

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
class Controller:
    """
    High-level controller for the wrist rehabilitation system.

    Attributes:
        motor (Motor): An instance of the Motor class to control the actuator.
        kp (float): Proportional gain for PD control.
        kd (float): Derivative gain for PD control.
    """

    def __init__(self, motor, kp=1.0, kd=0.1):
        """
        Initializes the Controller with a motor instance and PD control gains.

        Args:
            motor (Motor): An instance of the Motor class.
            kp (float): Proportional gain for PD control.
            kd (float): Derivative gain for PD control.
        """
        self.motor = motor
        self.kp = kp
        self.kd = kd
        self.previous_error = 0
        self.previous_time = time.time()

    def set_target_position(self, target_position):
        """
        Moves the motor to the specified target position using PD control.

        Args:
            target_position (float): Desired position in degrees.
        """
        try:
            # Convert target position (degrees) to motor pulses
            pulses_per_degree = 4096 / 360
            target_pulses = int(target_position * pulses_per_degree)

            # Boundary check
            if not -83 <= target_position <= 81:
                logging.warning(f"Target position {target_position}° is out of bounds!")
                return

            # Log the target position
            logging.info(f"Setting target position to {target_position}° ({target_pulses} pulses).")

            # PD Control Loop
            while True:
                # Get current position in motor pulses
                current_position = self.motor.readPosition() * pulses_per_degree

                # Compute error and derivative
                error = target_pulses - current_position
                current_time = time.time()
                delta_time = current_time - self.previous_time
                derivative = (error - self.previous_error) / delta_time if delta_time > 0 else 0

                # PD control output
                control_output = (self.kp * error) + (self.kd * derivative)

                # Limit current output within safe range
                max_current = 1500  # Set as per motor configuration
                control_output = max(-max_current, min(max_current, control_output))

                # Apply the control output
                self.motor.setGoalCurrent(control_output)

                # Log the control loop details
                logging.info(f"Error: {error}, Derivative: {derivative:.2f}, "
                             f"Control Output: {control_output:.2f} mA, Current Position: {current_position:.2f} pulses.")

                # Break loop if error is within tolerance
                if abs(error) < 10:  # Tolerance in pulses
                    logging.info(f"Target position {target_position}° reached.")
                    break

                # Update for next loop
                self.previous_error = error
                self.previous_time = current_time

                # Small delay for stability
                time.sleep(0.01)

        except Exception as e:
            logging.error(f"Error in set_target_position: {e}")

    def stop(self):
        """
        Stops the motor by setting the current to zero.
        """
        try:
            self.motor.setGoalCurrent(0)
            logging.info("Motor stopped. Current set to 0.")
        except Exception as e:
            logging.error(f"Error stopping the motor: {e}")
    
    
    def update_gains(self, kp=None, kd=None):
        """
        Dynamically update PD control gains.
        """
        if kp is not None:
            self.kp = kp
            logging.info(f"Updated proportional gain (kp) to {kp}.")
        if kd is not None:
            self.kd = kd
            logging.info(f"Updated derivative gain (kd) to {kd}.")
