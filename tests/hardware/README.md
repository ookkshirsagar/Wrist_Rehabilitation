# Hardware checks

These scripts require a real Dynamixel motor connected over serial. They are
not run by `pytest` or CI, run them manually against real hardware:

```bash
python tests/hardware/motor_integration_check.py
python tests/hardware/controller_operations_check.py
```

For automated, hardware-independent tests, see the `test_*.py` files in
`tests/`, which mock the DynamixelSDK.
