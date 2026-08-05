"""
tests/test_safety.py - Hardware-independent unit tests for the
Doctor/Patient systems' check_safety() logic.

Run with:

    pytest tests/ -v
"""

from unittest.mock import patch

import pytest

from Doctor import DoctorSystem
from Patient import PatientSystem


@pytest.fixture
def doctor_system():
    return DoctorSystem()


@pytest.fixture
def patient_system():
    return PatientSystem()


class TestDoctorCheckSafety:
    def test_true_when_within_limits(self, doctor_system):
        with patch.object(doctor_system.motor, "readRegister", return_value=40), patch.object(
            doctor_system.motor, "readCurrent", return_value=500
        ):
            assert doctor_system.check_safety() is True

    def test_false_when_temperature_exceeds_limit(self, doctor_system):
        with patch.object(doctor_system.motor, "readRegister", return_value=90), patch.object(
            doctor_system.motor, "readCurrent", return_value=500
        ):
            assert doctor_system.check_safety(temp_limit=80) is False

    def test_false_when_current_exceeds_limit(self, doctor_system):
        with patch.object(doctor_system.motor, "readRegister", return_value=40), patch.object(
            doctor_system.motor, "readCurrent", return_value=2000
        ):
            assert doctor_system.check_safety(current_limit=1500) is False


class TestPatientCheckSafety:
    """
    Regression coverage: check_safety() used to read
    self.motor.temp_limit / self.motor.current_limit, attributes that
    Motor never sets, so every call raised AttributeError internally.
    Because check_safety() wraps its body in a broad try/except, that
    didn't crash the process, it made check_safety() always return
    False regardless of actual temperature/current, so the Patient
    system could never pass its own safety check.
    """

    def test_true_when_within_limits(self, patient_system):
        with patch.object(patient_system.motor, "readRegister", return_value=40), patch.object(
            patient_system.motor, "readCurrent", return_value=500
        ):
            assert patient_system.check_safety() is True

    def test_false_when_temperature_exceeds_limit(self, patient_system):
        with patch.object(patient_system.motor, "readRegister", return_value=90), patch.object(
            patient_system.motor, "readCurrent", return_value=500
        ):
            assert patient_system.check_safety(temp_limit=80) is False

    def test_false_when_current_exceeds_limit(self, patient_system):
        with patch.object(patient_system.motor, "readRegister", return_value=40), patch.object(
            patient_system.motor, "readCurrent", return_value=2000
        ):
            assert patient_system.check_safety(current_limit=1500) is False
