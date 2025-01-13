"""
Patient-Side Wrist Rehabilitation System
----------------------------------------

This script manages the Patient-side wrist rehabilitation system using Current-Based 
Position Control with real-time feedback to ensure safety, precision, and responsiveness.

Features:
1. Synchronizes with the Doctor's wrist movement.
2. Adjusts its position dynamically using virtual spring logic.
3. Implements real-time PD control for precision and force adjustments.
4. Ensures safety through temperature and current monitoring.
5. Communicates with the Doctor system via MQTT.

Requirements:
- Motor.py and Controller.py for low-level and high-level control, respectively.
- Configurations defined in config/motor_config.py.
- Mqtt.py for MQTT-based communication.
"""

import time
import logging
import os
from Motor import Motor
from Controller import Controller
from config.motor_config import MOTOR_ID, BAUD_RATE, DEVICE_NAME, PROTOCOL_VERSION
from Mqtt import MQTTClient

# Configure logging
LOGS_DIR = os.path.join(os.getcwd(), "data", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, "patient_system_execution.log")

# Reset existing logging configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging to write logs to the specified file 
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    filemode="w",  # Overwrite the log file on each run
)


class PatientSystem:
    """
    Manages the Patient-side wrist rehabilitation system.
    """

    def __init__(self):
        """
        Initialize the Patient system with motor, controller, and MQTT instances.
        """
        logging.info("Initializing Patient system...")
        self.motor = Motor(MOTOR_ID, BAUD_RATE, DEVICE_NAME, PROTOCOL_VERSION)
        self.controller = Controller(self.motor)  # Use defaults from Controller.py
        self.mqtt_client = MQTTClient()

        # MQTT topics (defined in Mqtt.py)
        self.topic_doctor = self.mqtt_client.TOPIC_DOCTOR_POSITION
        self.topic_patient = self.mqtt_client.TOPIC_PATIENT_POSITION
        self.topic_status = self.mqtt_client.TOPIC_STATUS

        # Variables to store received doctor position
        self.doctor_position = None

        # Bind MQTT callback for receiving doctor position
        self.mqtt_client.client.on_message = self.on_doctor_message

    def check_safety(self, temp_limit=80, current_limit= 1500):
        """
        Check safety parameters (temperature and current).

        Returns:
            bool: True if system is safe, False otherwise.
        """
        try:
            temperature = self.motor.readRegister(1, self.motor.ADDR_PRESENT_TEMPERATURE)
            current = self.motor.readCurrent()

            if temperature > self.motor.temp_limit:
                logging.warning(f"Temperature limit exceeded! Current: {temperature}°C.")
                return False

            if abs(current) > self.motor.current_limit:
                logging.warning(f"Current limit exceeded! Current: {current:.2f} mA.")
                return False

            return True
        except Exception as e:
            logging.error(f"Error during safety check: {e}")
            return False

    def safety_shutdown(self):
        """
        Safely shut down the system by stopping the motor and disconnecting MQTT.
        """
        try:
            self.controller.stop()
            self.mqtt_client.client.disconnect()
            logging.info("System shut down safely.")
        except Exception as e:
            logging.error(f"Error during safety shutdown: {e}")

    def initialize_system(self):
        """
        Initialize the motor, controller, and MQTT client.
        """
        try:
            # Step 1: Initialize the motor with default safety and motion settings
            self.motor.initializeWristRehabRobot()

            # Step 2: Dynamically update PD gains (if needed)
            self.controller.update_gains(kp=None, kd=None)  # Use default values

            # Step 3: Connect and start MQTT client
            self.mqtt_client.connect()
            self.mqtt_client.start_loop()

            # Subscribe to Doctor position topic
            self.mqtt_client.subscribe(self.topic_doctor)
            logging.info("Patient system initialized and ready.")
        except Exception as e:
            logging.error(f"Error during initialization: {e}")
            self.safety_shutdown()

    def on_doctor_message(self, client, userdata, message):
        """
        Callback for processing received doctor position from MQTT.

        Args:
            client: The MQTT client instance.
            userdata: The private user data provided by the client.
            message: The MQTT message instance containing topic and payload.
        """
        try:
            self.doctor_position = float(message.payload.decode())
            logging.info(f"Received doctor position: {self.doctor_position:.2f} radians.")
        except Exception as e:
            logging.error(f"Error processing doctor position message: {e}")

    def monitor_and_control(self):
        """
        Monitor the Doctor's position and dynamically adjust the Patient's wrist position.
        """
        try:
            while True:
                # Use received Doctor position for control logic
                if self.doctor_position is not None:
                    patient_position = self.motor.readPosition()

                    # Check if Patient system lags behind the Doctor
                    if abs(patient_position - self.doctor_position) > 0.01:  # Example tolerance in radians
                        logging.warning("Patient lagging behind, activating virtual spring logic.")
                        self.controller.set_target_position(self.doctor_position)
                    else:
                        logging.info("Patient system synchronized with Doctor.")

                    # Publish Patient's position to MQTT
                    self.mqtt_client.publish(self.topic_patient, str(patient_position))
                    logging.info(f"Patient position published: {patient_position:.2f} radians.")

                # Monitor safety
                if not self.check_safety():
                    self.safety_shutdown()
                    break

                # Small delay for stability
                time.sleep(0.01)

        except KeyboardInterrupt:
            logging.info("Process interrupted by user. Shutting down...")
            self.safety_shutdown()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.safety_shutdown()

    def main(self):
        """
        Main function to orchestrate the Patient system states.
        """
        self.initialize_system()
        self.monitor_and_control()


if __name__ == "__main__":
    patient_system = PatientSystem()
    patient_system.main()
