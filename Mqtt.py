"""
MQTT Module for Wrist Rehabilitation System
-------------------------------------------

This module handles all MQTT-related operations for the wrist rehabilitation system,
allowing seamless communication between Doctor and Patient systems.

Features:
1. Secure TLS connection for encrypted communication.
2. Modular functions for publishing, subscribing, and handling received messages.
3. Integration-ready design for `Doctor.py` and `Patient.py`.

References:
- Paho MQTT with MQTT v5: https://pypi.org/project/paho-mqtt/
"""

import os
import threading
import logging
import ssl
import paho.mqtt.client as paho

# Configure logging
LOGS_DIR = os.path.join(os.getcwd(), "data", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, "mqtt_wrist_rehab.log")

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

# MQTT Configuration
BROKER = "f40d1650f9db422da8bc00193d76e58a.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "imek_wrist_rehab"
PASSWORD = "#Imek@21073"




class MQTTClient:
    """
    Handles MQTT connection, publishing, and subscribing for the Wrist Rehabilitation System.

    Attributes:
        client (paho.Client): The MQTT client instance.
    """

    # Class-level attributes for MQTT topics
    TOPIC_DOCTOR_POSITION = "wrist_rehab/doctor/position"
    TOPIC_PATIENT_POSITION = "wrist_rehab/patient/position"
    TOPIC_STATUS = "wrist_rehab/system/status"

    
    def __init__(self):
        """
        Initializes the MQTT client and sets up callbacks.
        """
        self.client = paho.Client(client_id="", protocol=paho.MQTTv5)
        self.client.username_pw_set(USERNAME, PASSWORD)
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)

        # Bind callback functions
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

    def connect(self):
        """
        Establishes a connection to the MQTT broker.
        """
        try:
            self.client.connect(BROKER, PORT)
            logging.info("Connected to MQTT broker.")
        except Exception as e:
            logging.error(f"Failed to connect to MQTT broker: {e}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        """
        Callback for when the client connects to the broker.
        """
        if rc == 0:
            logging.info("Successfully connected to the MQTT broker.")
        else:
            logging.error(f"Connection failed with return code {rc}.")

    def on_publish(self, client, userdata, mid, properties=None):
        """
        Callback for when a message is published.
        """
        logging.info(f"Message with mid {mid} published successfully.")

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        """
        Callback for when the client subscribes to a topic.
        """
        logging.info(f"Subscribed to topic with mid {mid}. Granted QoS: {granted_qos}.")

    def on_message(self, client, userdata, message):
        """
        Callback for when a message is received.
        Logs and decodes the received message.
        """
        logging.info(f"Received message from topic {message.topic}: {message.payload.decode()}")

    def subscribe(self, topic):
        """
        Subscribes to a given MQTT topic.

        Args:
            topic (str): The topic to subscribe to.
        """
        try:
            self.client.subscribe(topic, qos=1)
            logging.info(f"Subscribed to topic: {topic}")
        except Exception as e:
            logging.error(f"Failed to subscribe to topic {topic}: {e}")

    def publish(self, topic, message):
        """
        Publishes a message to a given MQTT topic.

        Args:
            topic (str): The topic to publish to.
            message (str): The message payload to send.
        """
        try:
            self.client.publish(topic, payload=message, qos=1)
            logging.info(f"Published message to topic {topic}: {message}")
        except Exception as e:
            logging.error(f"Failed to publish message to topic {topic}: {e}")

    def start_loop(self):
        """
        Starts the MQTT client loop in a separate thread.
        """
        loop_thread = threading.Thread(target=self.client.loop_forever)
        loop_thread.daemon = True
        loop_thread.start()
