"""
tests/test_controller.py - Hardware-independent unit tests for Controller.

Uses a mocked Motor so the PD control loop can be tested without a
physical Dynamixel motor attached. Run with:

    pytest tests/ -v
"""

from unittest.mock import MagicMock, patch

import pytest

from Controller import Controller


@pytest.fixture
def motor():
    return MagicMock()


@pytest.fixture
def controller(motor):
    return Controller(motor, kp=1.0, kd=0.1)


class TestBoundaryCheck:
    @pytest.mark.parametrize("target", [-84, 82, 100, -200])
    def test_rejects_out_of_range_target(self, controller, motor, target):
        controller.set_target_position(target)
        motor.setGoalCurrent.assert_not_called()


class TestPDLoopConvergence:
    def test_converges_when_motor_already_at_target(self, controller, motor):
        """
        Regression test: set_target_position() used to multiply
        motor.readPosition()'s radian return value by pulses_per_degree
        (a degrees factor), inflating the position reading by ~57x and
        making the loop's error term wrong even when the motor was
        already at the target.

        45 degrees == 512 pulses (45 * 4096 / 360). motor.readPosition()
        returns radians, so we mock it to return the radian equivalent of
        512 pulses (512 * 3.14 / 2048) and expect the loop to see near-zero
        error and stop on its first iteration.
        """
        target_degrees = 45
        radians_equivalent_of_target = 512 * (3.14 / 2048)
        motor.readPosition.return_value = radians_equivalent_of_target

        sleep_calls = {"n": 0}

        def _fail_if_looping_too_long(_seconds):
            sleep_calls["n"] += 1
            if sleep_calls["n"] > 3:
                raise AssertionError(
                    "PD loop did not converge in one step for a motor already at the target; "
                    "the radians/pulses unit conversion likely regressed."
                )

        with patch("Controller.time.sleep", side_effect=_fail_if_looping_too_long):
            controller.set_target_position(target_degrees)

        assert sleep_calls["n"] == 0
        motor.setGoalCurrent.assert_called_once()
        (control_output,), _ = motor.setGoalCurrent.call_args
        assert control_output == pytest.approx(0, abs=15)


class TestStop:
    def test_sets_goal_current_to_zero(self, controller, motor):
        controller.stop()
        motor.setGoalCurrent.assert_called_once_with(0)


class TestUpdateGains:
    def test_updates_kp_and_kd(self, controller):
        controller.update_gains(kp=2.0, kd=0.5)
        assert controller.kp == 2.0
        assert controller.kd == 0.5

    def test_leaves_gains_unchanged_when_not_provided(self, controller):
        controller.update_gains()
        assert controller.kp == 1.0
        assert controller.kd == 0.1
