"""
Shared pytest fixtures.

Sets dummy MQTT credentials before any test module is collected, so
importing Mqtt.py (and anything that imports it, like Doctor.py/Patient.py)
doesn't fail just because a real .env isn't present in CI or on a dev
machine that hasn't configured one yet.
"""

import os

os.environ.setdefault("MQTT_BROKER", "test-broker.invalid")
os.environ.setdefault("MQTT_USERNAME", "test-user")
os.environ.setdefault("MQTT_PASSWORD", "test-password")
