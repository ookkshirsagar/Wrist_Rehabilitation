# Wrist Rehabilitation Robot

## Overview
The Wrist Rehabilitation Robot project is designed to aid in physical therapy for wrist rehabilitation using a teleoperated system. It comprises two core systems:
- **Doctor System**: Operated by the therapist or doctor to perform controlled wrist movements.
- **Patient System**: Mimics the movements performed by the Doctor System to assist the patient's rehabilitation.

The system is built on **Current-based Position Control Mode**, ensuring precise and controlled wrist flexion and extension movements.

---

## Key Features

1. **Teleoperation**
   Real-time mirroring of the Doctor System's wrist movements by the Patient System, ensuring effective and synchronized rehabilitation tasks.

2. **Current-based Position Control Mode**
   Provides force-based control, enabling adjustable resistance or assistive torque for wrist movements.

3. **Safety Mechanisms**
   Built-in safety features including temperature, position, and current limits to prevent device or user harm.

4. **Customizable Motion Profiles**
   Smooth, precise, and controlled wrist movements with adjustable acceleration and velocity settings.

5. **Modular Design**
   Clear separation of hardware control (Motor), task coordination (Controller), and communication (MQTT) for scalability, maintainability, and testing.

---

## Project Structure

```
Wrist_Rehabilitation/
│
├── Motor.py            # Low-level motor operations
├── Controller.py        # High-level task coordination for rehabilitation
├── Doctor.py             # Entrypoint for Doctor-side wrist control
├── Patient.py            # Entrypoint for Patient-side wrist control
├── Mqtt.py               # MQTT module for system communication
├── config/
│   └── motor_config.py   # Motor-specific configuration values
├── tests/
│   ├── conftest.py               # Shared pytest fixtures
│   ├── test_motor.py             # Motor unit tests, mocked hardware
│   ├── test_controller.py        # PD control loop unit tests
│   ├── test_safety.py            # Doctor/Patient safety-check unit tests
│   └── hardware/                 # Manual scripts requiring real hardware
│       ├── motor_integration_check.py
│       └── controller_operations_check.py
├── literature/
│   └── literature.md     # Design decisions, control table reference, ROM values
├── .env.example           # Template for local MQTT credentials
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Test dependencies
├── pytest.ini
├── LICENSE
└── README.md
```

Logs are written at runtime to `data/logs/` (created automatically, not committed).

---

## Installation and Setup

### Prerequisites

- Python 3.8+
- A Dynamixel motor reachable over serial (e.g. `/dev/ttyUSB0` on Linux) to actually operate the hardware. The automated test suite does not require this.

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/ookkshirsagar/Wrist_Rehabilitation.git
   cd Wrist_Rehabilitation
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows PowerShell

   pip install -r requirements.txt
   ```

3. Configure MQTT credentials. The broker host, username, and password are read from the environment, never hardcoded:
   ```bash
   cp .env.example .env
   # then edit .env with your actual HiveMQ (or other broker) credentials
   ```

4. Verify that the necessary serial ports are accessible for the Dynamixel motors:
   ```bash
   sudo chmod a+rw /dev/ttyUSB0
   ```

---

## Usage Instructions

### Running the Systems
- **Doctor System**:
  ```bash
  python Doctor.py
  ```

- **Patient System**:
  ```bash
  python Patient.py
  ```

### Logs and Telemetry
Log files for debugging and system analysis are written to `data/logs/` at runtime: system initialization details, runtime data, and error reports.

---

## Running tests

The main test suite mocks the Dynamixel SDK and runs without any hardware attached:

```bash
pip install -r requirements-dev.txt
pytest -v
```

For manual checks against a real, connected motor, see `tests/hardware/`:

```bash
python tests/hardware/motor_integration_check.py
python tests/hardware/controller_operations_check.py
```

---

## Additional Resources

### Dynamixel SDK
Motor communication uses the [DynamixelSDK](https://github.com/ROBOTIS-GIT/DynamixelSDK) Python package (`dynamixel_sdk` on PyPI), installed via `requirements.txt`, not vendored in this repository.

### Literature
[`literature/literature.md`](literature/literature.md) documents the design rationale in detail, including:
- Dynamixel control table parameters used
- Choice of Current-based Position Control Mode
- Safety mechanisms and their thresholds
- Wrist range-of-motion values and their source

---

## Contribution Guidelines

Contributions are welcome. Please:
1. Fork this repository.
2. Create a new branch for your feature or fix.
3. Run `pytest -v` and make sure it passes.
4. Submit a pull request for review.

For any questions or feedback, please raise an issue in the repository.

---

## License

[MIT](LICENSE)
