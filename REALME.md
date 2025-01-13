# Wrist Rehabilitation Robot

## Overview
The Wrist Rehabilitation Robot project is designed to aid in physical therapy for wrist rehabilitation using a teleoperated system. It comprises two core systems:
- **Doctor System**: Operated by the therapist or doctor to perform controlled wrist movements.
- **Patient System**: Mimics the movements performed by the Doctor System to assist the patient's rehabilitation.

The system is built on **Current-based Position Control Mode**, ensuring precise and controlled wrist flexion and extension movements.

---

## Key Features

1. **Teleoperation**  
   - Real-time mirroring of the Doctor System's wrist movements by the Patient System, ensuring effective and synchronized rehabilitation tasks.

2. **Current-based Position Control Mode**  
   - Provides force-based control, enabling adjustable resistance or assistive torque for wrist movements.

3. **Safety Mechanisms**  
   - Built-in safety features including temperature, position, and current limits to prevent device or user harm.

4. **Customizable Motion Profiles**  
   - Smooth, precise, and controlled wrist movements with adjustable acceleration and velocity settings.

5. **Modular Design**  
   - Clear separation of hardware control (Motor), task coordination (Controller), and communication (MQTT) for scalability, maintainability, and testing.

---

## Project Structure

```
project/
│
├── Motor.py           # Low-level motor operations
├── Controller.py      # High-level task coordination for rehabilitation
├── Doctor.py          # Entrypoint for Doctor-side wrist control
├── Patient.py         # Entrypoint for Patient-side wrist control
├── config/            # Configuration files
│   ├── motor_config.py    # Motor-specific configuration values
├── Mqtt.py            # MQTT module for system communication
├── README.md          # Project overview and setup instructions
├── requirements.txt   # Dependencies and libraries required for the project
├── tests/             # Unit and integration tests
│   ├── test_motor.py      # Tests for Motor.py
│   ├── test_controller.py # Tests for Controller.py
├── data/              # Directory to store logs and calibration data
│   ├── logs/              # Log files for debugging and analysis
│       ├── controller_initialization.py
│       ├── doctor_system_execution.py
│       ├── motor_initialization.py
│       ├── mqtt_wrist_rehab.py
│       ├── patient_system_execution.py
│       ├── test_controller_operations.py
│       ├── test_motor_integration.py
├── literature/        # Documentation explaining key design and implementation decisions
└── DynamixelSDK/      # Dynamixel SDK library for motor communication

```

# Installation and Setup

## Prerequisites
Ensure you have the following installed on your system:

- **Python 3.8+**
- **DynamixelSDK** (included in the `DynamixelSDK/` directory of this project)
- **Required Python libraries** (see `requirements.txt`)

---

## Installation Steps

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Add the DynamixelSDK path to your Python environment:
   ```bash
   export PYTHONPATH="$PYTHONPATH:$(pwd)/DynamixelSDK"
   ```

4. Verify that the necessary serial ports (e.g., `/dev/ttyUSB0` on Linux) are accessible for the Dynamixel motors.

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
Log files for debugging and system analysis are stored in the `data/logs/` directory. These include system initialization details, runtime data, and error reports.

---

## Additional Resources

### Dynamixel SDK Documentation
The project utilizes the [DynamixelSDK](https://github.com/ROBOTIS-GIT/DynamixelSDK/tree/main) for motor communication.

### Literature
The `Literature/` folder contains detailed explanations of design decisions, including:
- Choice of Current-based Position Control Mode.
- Safety mechanisms and their thresholds.
- Teleoperation synchronization logic.

---

## Contribution Guidelines

Contributions are welcome! Please follow these steps:
1. Fork this repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request for review.

For any questions or feedback, please raise an issue in the repository.


---

## Step-by-Step Guide for Beginners

### How to Clone the Repository

If you're new to Git, follow these simple steps to get started:

1. **Install Git**
   - **Windows**: Download and install [Git for Windows](https://git-scm.com/downloads).
   - **Mac**: Install Git via the terminal using:
     ```bash
     brew install git
     ```
   - **Linux**: Install Git using your package manager:
     ```bash
     sudo apt update
     sudo apt install git
     ```
   - Verify Git is installed:
     ```bash
     git --version
     ```

2. **Open a Terminal or Command Prompt**
   - **Windows**: Use Git Bash.
   - **Mac/Linux**: Open the terminal application.

3. **Navigate to Your Desired Folder**
   - Use the `cd` command to navigate to the folder where you want to clone the repository:
     ```bash
     cd /path/to/your/folder
     ```

4. **Clone the Repository**
   - Copy the repository URL (replace `<repository_url>` with the actual URL) and run:
     ```bash
     git clone <repository_url>
     ```
   - Example:
     ```bash
     git clone https://github.com/YourUsername/WristRehabRobot.git
     ```

5. **Enter the Project Directory**
   ```bash
   cd WristRehabRobot