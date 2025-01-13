# Literature: Wrist Rehabilitation Robot

This document provides a detailed explanation of the key decisions, parameters, and control methodologies employed in the **Wrist Rehabilitation Robot** project. It serves as a reference for understanding the system's design rationale and implementation details.

---

## Control Table Parameters for XM540-W270-R

Link to the E-manual: [XM540-W270-R Control Table](https://emanual.robotis.com/docs/en/dxl/x/xm540-w270/#control-table-data-address)

### Key Parameters

1. **ID (Address: 7)**
   - **Description:** Identifies the motor on the communication bus.
   - **Purpose:** Ensures that each actuator has a unique ID for communication.
   - **Default Value:** 1
   - **Range:** 0 ~ 252

2. **Operating Mode (Address: 11)**
   - **Description:** Sets the operating mode of the motor.
   - **Purpose:** Enables Current-based Position Control Mode.
   - **Required Value:** 5 (for Current-based Position Control Mode)
   - **Range:** 0 ~ 16

3. **Temperature Limit (Address: 31)**
   - **Description:** Sets the maximum allowable temperature before the motor shuts down.
   - **Purpose:** Protects the motor from overheating.
   - **Default Value:** 80 °C
   - **Range:** 0 ~ 100 °C

4. **Current Limit (Address: 38)**
   - **Description:** Sets the maximum allowable current to control torque.
   - **Purpose:** Ensures safe force application and protects the motor from overcurrent.
   - **Default Value:** 2047 (maximum)
   - **Range:** 0 ~ 2047

5. **Max Position Limit (Address: 48)**
   - **Description:** Sets the maximum position limit in terms of motor pulses.
   - **Purpose:** Prevents overextension of the wrist.
   - **Default Value:** 4095
   - **Range:** 0 ~ 4095

6. **Min Position Limit (Address: 52)**
   - **Description:** Sets the minimum position limit in terms of motor pulses.
   - **Purpose:** Prevents over-flexion of the wrist.
   - **Default Value:** 0
   - **Range:** 0 ~ 4095

7. **Shutdown (Address: 63)**
   - **Description:** Configures conditions to shut down the motor in case of critical errors.
   - **Purpose:** Ensures safety by stopping the motor during overheating, overcurrent, or voltage issues.
   - **Default Value:** 52 (overheating and overcurrent protection)

8. **Torque Enable (Address: 64)**
   - **Description:** Enables or disables the motor torque.
   - **Purpose:** Activates the motor for operation or disables it for manual adjustments.
   - **Default Value:** 0 (disabled)
   - **Range:**
     - 0: Torque Disabled
     - 1: Torque Enabled

9. **Status Return Level (Address: 68)**
   - **Description:** Configures the return level of status packets from the motor.
   - **Purpose:** Determines the communication feedback behavior.
   - **Default Value:** 2 (return for READ and PING instructions)
   - **Range:**
     - 0: No return response.
     - 1: Return for PING instruction.
     - 2: Return for READ and PING instructions.

10. **Position P Gain (Address: 84)**
    - **Description:** Proportional gain of the position control loop.
    - **Purpose:** Adjusts the responsiveness and accuracy of position control.
    - **Default Value:** 800
    - **Range:** 0 ~ 16,383

11. **Profile Acceleration (Address: 108)**
    - **Description:** Sets the acceleration profile for position control.
    - **Purpose:** Controls the rate of change in speed for smooth motion.
    - **Default Value:** 0 (no profile applied)
    - **Range:** 0 ~ 32,767

12. **Profile Velocity (Address: 112)**
    - **Description:** Sets the velocity profile for position control.
    - **Purpose:** Limits the maximum speed during motion for smooth operation.
    - **Default Value:** 0 (no profile applied)
    - **Range:** 0 ~ 32,767

13. **Goal Position (Address: 116)**
    - **Description:** Target position for the actuator in terms of pulses.
    - **Purpose:** Sets the desired position the motor should reach.
    - **Default Value:** 0
    - **Range:** 0 ~ 4,095 (depends on Max and Min Position Limits)

14. **Present Current (Address: 126)**
    - **Description:** Current electrical load on the motor.
    - **Purpose:** Monitors the torque output by measuring current.
    - **Range:** 0 ~ 2,047 (2.69 mA per unit)

15. **Present Position (Address: 132)**
    - **Description:** Current position of the actuator in terms of pulses.
    - **Purpose:** Provides feedback on the motor's position.
    - **Range:** 0 ~ 4,095 (depends on Max and Min Position Limits)

16. **Present Temperature (Address: 146)**
    - **Description:** Current internal temperature of the motor.
    - **Purpose:** Provides real-time thermal monitoring for safety.
    - **Range:** 0 ~ 100 °C

---

## MQTT for Teleoperation

## What is MQTT?

**Message Queuing Telemetry Transport (MQTT)** is a lightweight messaging protocol designed for low-bandwidth, high-latency networks. It uses a publish/subscribe model, making it ideal for applications requiring real-time data exchange.

### Key Features of MQTT:
1. **Lightweight and Efficient**: Minimal overhead, making it suitable for resource-constrained devices.
2. **Scalable**: Handles multiple clients, enabling multi-device communication.
3. **Real-Time Communication**: Low latency ensures responsiveness.
4. **Quality of Service (QoS)**: Guarantees message delivery with three levels of reliability.
5. **Topic-Based Communication**: Hierarchical topic structure allows targeted message exchange.
6. **Cloud Compatibility**: Integrates easily with IoT platforms like AWS or Google Cloud.

### MQTT in Wrist Rehabilitation Robot
In this project, MQTT facilitates communication between the **Doctor System** and the **Patient System**, ensuring synchronized movements and providing feedback.

### Pros

1. **Lightweight and Efficient:** Designed for low-bandwidth networks, making it ideal for cloud-based communication.
2. **Scalable:** Supports multiple clients, enabling control of multiple robots simultaneously.
3. **Real-Time Communication:** Provides low latency, ideal for responsive control.
4. **Quality of Service (QoS):** Ensures reliable message delivery with adjustable levels of guarantee.
5. **Cloud Compatibility:** Integrates easily with services like AWS IoT or Google Cloud IoT.
6. **Decoupled Architecture:** Allows flexibility by separating publishers and subscribers.
7. **Topic-Based Communication:** Facilitates specific control using hierarchical topics.

### Cons

1. **Latency in Network Issues:** Dependence on internet connectivity can cause delays.
2. **Security Concerns:** Requires additional measures like TLS encryption and authentication.
3. **Complexity in Real-Time Control:** Fine-grained control may be challenging compared to local solutions.
4. **Message Overhead:** High-frequency updates in large-scale deployments can saturate bandwidth.
5. **Limited Local Fallback:** Connectivity loss disrupts operations unless fallback mechanisms are implemented.

---

## Current-Based Position Control Mode

This mode combines current feedback to maintain specific torque, ensuring smooth, precise, and adaptive wrist motion.

### Pros
1. **Precise Force Control:** Essential for gradual force adjustments in rehabilitation.
2. **Smooth Motion:** Minimizes jerky movements for a safer experience.
3. **Load Adaptability:** Adjusts to resistance for adaptive rehab protocols.
4. **Reduced Motor Stress:** Optimizes torque to extend motor life.
5. **Patient Safety:** Limits applied force, reducing injury risks.
6. **Progress Monitoring:** Provides valuable feedback on resistance and range of motion.

### Cons
1. **Complex Calibration:** Requires precise tuning for accuracy.
2. **Higher Processing Demands:** Increases the load on control hardware.
3. **Sensitivity to Noise:** Electrical noise can affect current measurements.
4. **Limited Speed Control:** Focuses on force rather than speed.
5. **Wear and Tear:** Prolonged high-current operation increases component wear.
6. **Firmware Dependence:** Requires specific motor settings, limiting flexibility.

---

## PD Control for Wrist Rehabilitation

**Why PD Control?**
PD control is ideal for wrist rehabilitation as it balances simplicity, responsiveness, and stability.

### Advantages
1. **Smooth and Stable Movements:** Combines proportional action for responsiveness and derivative action to dampen oscillations.
2. **Quick Response:** Predicts and stabilizes dynamic changes, essential for resistance training.
3. **Reduced Overshoot:** Prevents movements beyond safe limits.

### Why Not Other Controls?
1. **P Control:** Simple but prone to steady-state errors and oscillations.
2. **PI Control:** Eliminates errors but introduces overshoot and slower response.
3. **PID Control:** Comprehensive but complex, often unnecessary for rehab tasks.

### Benefits in Current-Based Position Control Mode
- **Force Feedback:** Maintains smooth transitions without force fluctuations.
- **Simpler Tuning:** Requires only two parameters (proportional and derivative gains).
- **Patient Safety:** Minimizes unintended movements and excessive forces.

---

## Python Code Snippet: Control Table Constants

```python
# Control Table Address Constants for XM540-W270-T/R

# Motor Identification
ADDR_ID = 7

# Operating Mode
ADDR_OPERATING_MODE = 11

# Safety Limits
ADDR_TEMPERATURE_LIMIT = 31
ADDR_CURRENT_LIMIT = 38
ADDR_MAX_POSITION_LIMIT = 48
ADDR_MIN_POSITION_LIMIT = 52
ADDR_SHUTDOWN = 63

# Torque Control
ADDR_TORQUE_ENABLE = 64

# Status Feedback
ADDR_STATUS_RETURN_LEVEL = 68

# Control Gains
ADDR_POSITION_P_GAIN = 84

# Motion Profiles
ADDR_PROFILE_ACCELERATION = 108
ADDR_PROFILE_VELOCITY = 112

# Position Control
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132

# Current Feedback
ADDR_PRESENT_CURRENT = 126

# Temperature Monitoring
ADDR_PRESENT_TEMPERATURE = 146
```

---

## Recommendation for Wrist Rehab Robots

### Recommended Modes
1. **Current-Based Position Control Mode (Best Overall):** Combines position accuracy and adaptive force control.
2. **Position Control Mode (0 ~ 360° or Extended Multi-Turn):** Ideal for ROM-focused exercises.
3. **Current Control Mode:** Suitable for resistance training.

### Modes to Avoid
- **Velocity Control Mode:** No position/force control.
- **PWM Control Mode:** Complex and unnecessary for rehab tasks.

---

This document provides a comprehensive understanding of the control methodologies and design rationale for the Wrist Rehabilitation Robot.
