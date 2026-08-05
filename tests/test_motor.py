"""
tests/test_motor.py - Hardware-independent unit tests for Motor.

Mocks Motor.writeRegister/readRegister so these run without a physical
Dynamixel motor attached. Run with:

    pytest tests/ -v
"""

from unittest.mock import MagicMock, patch

import pytest

from Motor import Motor


@pytest.fixture
def motor():
    return Motor(dxl_id=1, baud_rate=1_000_000, device_name="/dev/ttyUSB0", protocol_version=2.0)


class TestTwosComplement:
    def test_positive_value_unchanged(self):
        assert Motor.twosComplement(2, 100) == 100

    def test_negative_2byte_value(self):
        # 0xFFFF (65535) as a signed 2-byte value is -1
        assert Motor.twosComplement(2, 0xFFFF) == -1

    def test_negative_4byte_value(self):
        assert Motor.twosComplement(4, 0xFFFFFFFF) == -1


class TestIntToHex:
    def test_masks_to_2_bytes(self):
        assert Motor.intToHex(2, 0x1FFFF) == 0xFFFF

    def test_masks_to_4_bytes(self):
        assert Motor.intToHex(4, 0x1FFFFFFFF) == 0xFFFFFFFF


class TestSetGoalCurrent:
    def test_writes_to_goal_current_address(self, motor):
        """
        Regression test: setGoalCurrent previously raised AttributeError
        because ADDR_GOAL_CURRENT was never defined on Motor.
        """
        with patch.object(motor, "writeRegister") as mock_write:
            motor.setGoalCurrent(1000)
        mock_write.assert_called_once()
        num_bytes, address, _value = mock_write.call_args[0]
        assert address == Motor.ADDR_GOAL_CURRENT
        assert num_bytes == 2


class TestConfigureSafetyLimits:
    def test_writes_expected_position_bounds(self, motor):
        with patch.object(motor, "writeRegister") as mock_write:
            motor.configureSafetyLimits(temp_limit=80)

        calls = {addr: value for (_n, addr, value) in (c.args for c in mock_write.call_args_list)}

        pulses_per_degree = 4096 / 360
        expected_max = int(2048 + (81 * pulses_per_degree))
        expected_min = int(2048 - (83 * pulses_per_degree))

        assert calls[Motor.ADDR_TEMPERATURE_LIMIT] == 80
        assert calls[Motor.ADDR_MAX_POSITION_LIMIT] == expected_max
        assert calls[Motor.ADDR_MIN_POSITION_LIMIT] == expected_min


class TestReadPosition:
    def test_converts_pulses_to_radians(self, motor):
        with patch.object(motor, "readRegister", return_value=2048):
            position = motor.readPosition()
        assert position == pytest.approx(2048 * (3.14 / 2048))

    def test_handles_negative_pulses(self, motor):
        with patch.object(motor, "readRegister", return_value=0xFFFFFFFF):  # -1 pulse
            position = motor.readPosition()
        assert position == pytest.approx(-1 * (3.14 / 2048))


class TestReadCurrent:
    def test_converts_to_milliamps(self, motor):
        with patch.object(motor, "readRegister", return_value=1000):
            current = motor.readCurrent()
        assert current == pytest.approx(1000 * (5.5 / 2047))


class TestInitializeCurrentBasedPositionControl:
    def test_sets_mode_when_not_already_current_based(self, motor):
        with patch.object(motor, "readRegister", return_value=0), patch.object(
            motor, "writeRegister"
        ) as mock_write, patch.object(motor, "setMode") as mock_set_mode, patch.object(
            motor, "setTorque"
        ) as mock_set_torque:
            motor.initializeCurrentBasedPositionControl()

        mock_set_mode.assert_called_once_with(5)
        mock_set_torque.assert_called_once_with(1)
        mock_write.assert_any_call(2, Motor.ADDR_CURRENT_LIMIT, 1500)

    def test_skips_mode_change_when_already_current_based(self, motor):
        with patch.object(motor, "readRegister", return_value=5), patch.object(
            motor, "writeRegister"
        ), patch.object(motor, "setMode") as mock_set_mode, patch.object(motor, "setTorque"):
            motor.initializeCurrentBasedPositionControl()

        mock_set_mode.assert_not_called()
