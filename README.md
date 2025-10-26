# Raspberry Pi Demo Projects

This is a collection of Raspberry Pi sensor demo projects, including human body detection, light detection, email alert, collision detection, and integrated sensor detection.

**Note: The current code is developed and tested based on Raspberry Pi 3 Model B**

## Project Structure

```
raspberry-pi-demo/
├── setup.py
├── README.md
├── README_en.md         # English version README
├── requirements.txt     # Project dependencies list
├── venv/               # Python virtual environment
├── __init__.py
├── sensor_detection.log     # Sensor detection log file
├── src/
│   ├── __init__.py
│   ├── body_detect.py       # Human body detection module, using infrared sensor to detect human activity and send email alerts
│   ├── smartlite.py         # Light detection module, detecting environmental light changes
│   ├── email_alarm.py       # Email alert module, independent email sending function
│   ├── collision_detection.py   # Collision detection module, using infrared obstacle avoidance sensor to detect obstacles
│   └── sensor_integration.py    # Integrated sensor detection module, simultaneously detecting human body and collision
├── tests/
└── docs/
    └── collision_detection_design.md  # Collision detection design document
```

## Features

### Human Body Detection (src/body_detect.py)
- Uses GPIO 18 to connect to human body infrared sensor
- Sends email alert when human activity is detected
- Emails are sent via SMTP protocol

### Light Detection (src/smartlite.py)
- Uses GPIO 3 to detect environmental light changes
- Outputs timestamp and notification when light changes are detected

### Email Alert (src/email_alarm.py)
- Independent email sending module
- Can be called by other modules to send alert emails

### Collision Detection (src/collision_detection.py)
- Uses infrared obstacle avoidance sensor to detect obstacles ahead
- Detectable distance range: 2-30cm (adjustable)
- Real-time detection with output results

### Integrated Sensor Detection (src/sensor_integration.py)
- Simultaneously detects human body sensor (GPIO18) and collision sensor (GPIO4)
- Buzzer sounds continuously when human body is detected (GPIO17), LED lights up when obstacle is detected (GPIO23)
- Real-time polling detection with logging
- Supports dual logging to file and console

## Hardware Connections

- Human body infrared sensor connected to GPIO 18
- Light sensor connected to GPIO 3
- Infrared obstacle avoidance sensor connected to GPIO 4
- Buzzer connected to GPIO 17
- LED connected to GPIO 23

## Installation

1. Clone the project:
   ```bash
   git clone https://codeup.aliyun.com/67fa7122c3ce52a957f12f24/Default/raspberry_demo.git
   cd raspberry-pi-demo
   ```

2. Create virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/MacOS
   # Or use venv\Scripts\activate on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set environment variables:
   ```bash
   export MAIL_HOST=smtp.yeah.net
   export MAIL_USER=your_username
   export MAIL_PASS=your_password
   export SENDER=your_email@yeah.net
   export RECEIVERS=recipient1@domain.com,recipient2@domain.com
   ```

2. Run the programs:
   ```bash
   python src/body_detect.py
   python src/smartlite.py
   python src/email_alarm.py
   python src/collision_detection.py
   python src/sensor_integration.py
   ```

## Notes

1. Raspberry Pi hardware environment is required to run (developed and tested based on Raspberry Pi 3 Model B)
2. Sensors need to be properly connected to the hardware
3. Email alert function requires correct email configuration

## Security Notice

All sensitive information (email passwords, etc.) has been removed from the code and needs to be configured through environment variables:
1. Email server information (MAIL_HOST, MAIL_USER, MAIL_PASS)
2. Sender email (SENDER)
3. Recipient email list (RECEIVERS)

Please protect these environment variables and do not commit them to the code repository.