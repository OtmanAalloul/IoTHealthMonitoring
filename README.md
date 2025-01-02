# IoT Health Monitoring Dashboard

## Description
This project is an **IoT-based Health Monitoring Dashboard** that collects, analyzes, and displays data for three critical health parameters:
- **Temperature (°C)**
- **Heart Rate (BPM)**
- **SpO2 (%)**

It features real-time data visualization, anomaly detection, and a user-friendly interface built with Flask, Chart.js, and Bootstrap. Additionally, the project integrates with Proteus for hardware simulation and uses **Virtual Serial Port Emulator (VSPE)** to establish communication between Proteus and the MQTT broker.

## Features
- **Real-time Monitoring:** Live updates of health parameters displayed on graphs.
- **Key Statistics Cards:** Displays the latest values of each parameter.
- **Anomaly Detection:** Detects and highlights abnormal values, with a dedicated table for anomalies.
- **Historical Data:** Keeps track of the last 10 readings in a table.
- **Sound Alerts:** Plays specific sounds for normal and anomalous values.
- **Proteus Simulation:** Integration with Proteus for hardware simulation of sensors.
- **Dark Mode:** Toggle between light and dark themes for better user experience.

## Technologies Used
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Bootstrap, Chart.js
- **MQTT Broker:** paho-mqtt (for communication with IoT devices)
- **Proteus:** For hardware simulation
- **VSPE:** Virtual Serial Port Emulator for connecting Proteus to MQTT
- **Data Analysis:** Python scripts for anomaly detection

## Prerequisites
- Python 3.x
- MQTT broker (e.g., Mosquitto)
- Proteus software for simulation
- VSPE for creating virtual serial ports
- Required Python libraries:
  ```bash
  pip install flask paho-mqtt
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your MQTT broker:
   - Update the MQTT broker details (e.g., `localhost`, port) in `main.py` and `serial_to_mqtt.py`.
4. Set up VSPE:
   - Create a virtual serial port pair (e.g., COM1 and COM2).
   - Configure Proteus to use one of the ports (e.g., COM1).
   - Configure the `serial_to_mqtt.py` script to use the other port (e.g., COM2).

## Usage
1. **Start the MQTT broker** (if not already running).
   ```bash
   mosquitto
   ```
2. **Open Proteus simulation:**
   - Load the provided Proteus file in the `proteus_config/` folder.
   - Ensure the sensors and Arduino are correctly connected.
3. **Run the Python script to handle MQTT communication:**
   ```bash
   python serial_to_mqtt.py
   ```
4. **Run the Flask server:**
   ```bash
   python main.py
   ```
5. Open the dashboard in your web browser:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure
```
├── arduino_code/         # Arduino sketches for sensors
├── proteus_config/       # Proteus simulation files
├── static/
│   ├── audio/            # Sound files for normal and anomaly alerts
│   ├── css/              # Additional CSS files (if any)
├── templates/
│   └── index.html        # HTML for the dashboard
├── main.py               # Flask application to serve the dashboard
├── serial_to_mqtt.py     # Reads data from Proteus via serial and publishes to MQTT broker
├── heartrate.py          # Analyzes heart rate data
├── spo2.py               # Analyzes SpO2 data
├── temperature.py        # Analyzes temperature data
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

## How It Works
1. **Proteus Simulation:**
   - Simulates sensors (e.g., LM35 for temperature, Heartbeat Sensor, etc.) connected to an Arduino Uno.
   - The Arduino sends data to the virtual COM port using the `COM1` port.

2. **VSPE Configuration:**
   - VSPE creates a virtual COM port pair (e.g., COM1 and COM2).
   - The data sent by Proteus on COM1 is received by the `serial_to_mqtt.py` script on COM2.

3. **MQTT Communication:**
   - The script reads data from the serial port and publishes it to MQTT topics:
     - `iot/temperature`
     - `iot/heartrate`
     - `iot/spo2`

4. **Flask Backend:**
   - Subscribes to MQTT topics and receives data in real-time.
   - Performs anomaly detection and serves the data to the frontend.

5. **Frontend Dashboard:**
   - Displays real-time data in graphs and cards.
   - Highlights anomalies in a table and plays sound alerts.

## Customization
- **MQTT Topics:** Update the topics in `main.py` and `serial_to_mqtt.py` to match your IoT device setup.
- **Anomaly Thresholds:** Modify thresholds in `temperature.py`, `heartrate.py`, and `spo2.py`.
- **Sound Alerts:** Replace the `.mp3` files in `static/audio/` to use your preferred sounds.

## Future Enhancements
- Add support for more health parameters.
- Implement database storage for long-term historical data.
- Add advanced data analysis and reporting capabilities.
- Automate the Proteus simulation start/stop process.

