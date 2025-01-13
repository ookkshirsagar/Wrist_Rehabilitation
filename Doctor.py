"""
Doctor-Side Wrist Rehabilitation System
----------------------------------------

This script manages the Doctor-side wrist rehabilitation system using Current-Based 
Position Control with real-time feedback to ensure safety, precision, and responsiveness.

Features:
1. Monitors the Doctor's wrist movement.
2. Adapts Patient system movement using virtual spring logic.
3. Implements real-time PD control for precision and force adjustments.
4. Ensures safety through temperature and current monitoring.
5. Communicates with the Patient system via MQTT.

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
LOG_FILE = os.path.join(LOGS_DIR, "doctor_system_execution.log")

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


class DoctorSystem:
    """
    Manages the Doctor-side wrist rehabilitation system.
    """

    def __init__(self):
        """
        Initialize the Doctor system with motor, controller, and MQTT instances.
        """
        logging.info("Initializing Doctor system...")
        self.motor = Motor(MOTOR_ID, BAUD_RATE, DEVICE_NAME, PROTOCOL_VERSION)
        self.controller = Controller(self.motor)  # Use defaults from Controller.py
        self.mqtt_client = MQTTClient()

        # MQTT topics (defined in Mqtt.py)
        self.topic_doctor = self.mqtt_client.TOPIC_DOCTOR_POSITION
        self.topic_patient = self.mqtt_client.TOPIC_PATIENT_POSITION
        self.topic_status = self.mqtt_client.TOPIC_STATUS

        # Variables to store received patient position
        self.patient_position = None

        # Bind MQTT callback for receiving patient position
        self.mqtt_client.client.on_message = self.on_patient_message


    def check_safety(self, temp_limit=80, current_limit= 1500):
        """
        Check safety parameters (temperature and current).

        Returns:
            bool: True if system is safe, False otherwise.
        """
        try:
            temperature = self.motor.readRegister(1, self.motor.ADDR_PRESENT_TEMPERATURE)
            current = self.motor.readCurrent()

            if temperature > temp_limit:
                logging.warning(f"Temperature limit exceeded! Current: {temperature}°C.")
                return False

            if abs(current) > current_limit:
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

            # Subscribe to patient position topic
            self.mqtt_client.subscribe(self.topic_patient)
            logging.info("Doctor system initialized and ready.")
        except Exception as e:
            logging.error(f"Error during initialization: {e}")
            self.safety_shutdown()

    def on_patient_message(self, client, userdata, message):
        """
        Callback for processing received patient position from MQTT.

        Args:
            client: The MQTT client instance.
            userdata: The private user data provided by the client.
            message: The MQTT message instance containing topic and payload.
        """
        try:
            self.patient_position = float(message.payload.decode())
            logging.info(f"Received patient position: {self.patient_position:.2f} radians.")
        except Exception as e:
            logging.error(f"Error processing patient position message: {e}")

    def monitor_and_control(self):
        """
        Monitor Doctor's wrist movements and send position to the Patient system.
        Adjust dynamically using the virtual spring logic.
        """
        try:
            while True:
                # Read current Doctor wrist position
                doctor_position = self.motor.readPosition()

                # Publish Doctor's position to MQTT
                self.mqtt_client.publish(self.topic_doctor, str(doctor_position))
                logging.info(f"Doctor wrist position published: {doctor_position:.2f} radians.")

                # Use received patient position for control logic
                if self.patient_position is not None:
                    # Check if Patient system reached the position
                    if abs(doctor_position - self.patient_position) > 0.01:  # Example tolerance in radians
                        logging.warning("Patient system lagging behind, activating virtual spring logic.")
                        self.controller.set_target_position(self.patient_position)
                    else:
                        logging.info("Patient system synchronized with Doctor.")

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
        Main function to orchestrate the Doctor system states.
        """
        self.initialize_system()
        self.monitor_and_control()


if __name__ == "__main__":
    doctor_system = DoctorSystem()
    doctor_system.main()
