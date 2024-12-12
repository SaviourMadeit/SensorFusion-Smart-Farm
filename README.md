# SensorFusion Smart Farm

The `SensorFusion Smart Farm` is a Raspberry Pi Pico W-based IoT project that integrates multiple sensors and actuators to monitor and manage a smart farming environment. The system leverages environmental data and user-defined crop parameters to automate irrigation, lighting, ventilation, and heating, ensuring optimal crop growth conditions at various growth stages.

## Features

- **Environmental Monitoring**:
  - Soil moisture, light intensity, and soil temperature sensors.
  - DHT11 for air temperature and humidity measurement.

- **Actuator Control**:
  - Water pump for irrigation.
  - Artificial lamp for supplemental lighting.
  - Ventilation fan for air regulation.
  - A heating device for temperature control.

- **User-defined Crop Parameters**:
  - Configurable light intensity, soil moisture, air temperature, and humidity thresholds for different growth stages (seedling, vegetative, flowering).

- **Wi-Fi Connectivity**:
  - Supports remote monitoring and control via the Blynk IoT platform.

- **Data Logging**:
  - Stores sensor data in a local CSV file for analysis.

## Hardware Requirements

- Raspberry Pi Pico W
- Sensors:
  - DHT11 (air temperature and humidity)
  - ADC-compatible soil moisture sensor
  - ADC-compatible soil temperature sensor
  - ADC-compatible light intensity sensor
- Actuators:
  - Water pump
  - Artificial lamp
  - Ventilation fan
  - Heating device
- LCD Display (16x2)

## Software Requirements

- Micropython firmware
- Libraries:
  - `machine` (for GPIO control)
  - `time` (for timing)
  - `BlynkLib` (for Blynk server interaction)
  - `network` (for Wi-Fi connectivity)
  - `DHT` (for DHT11 sensor)
  - `os` (for file operations)

## Setup and Installation

1. **Flash Micropython onto Raspberry Pi Pico W**:
   - Download the Micropython firmware from the official [MicroPython website](https://micropython.org/download/).
   - Flash the firmware using tools like `Thonny IDE` or `esptool.py`.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/sensorfusion_smart_farm.git
   ```

3. **Upload Files to Raspberry Pi Pico W**:
   - Use `Thonny IDE` or any file upload utility to transfer the project files to your Raspberry Pi Pico W.

4. **Connect Hardware**:
   - Follow the GPIO pin assignments in the code to connect the sensors and actuators to the Raspberry Pi Pico W.

5. **Configure Wi-Fi and Blynk**:
   - Edit the `wifi_credentials.txt` file with your Wi-Fi SSID and password.
   - Replace `BLYNK_AUTH` with your Blynk authentication token in the code.

6. **Run the Program**:
   - Open the main script in your Python IDE and execute it.

## Usage

### Crop Data Input

You can define crop-specific parameters by entering the following details:
- Ideal light intensity (percentage)
- Ideal soil moisture level (percentage)
- Minimum and maximum soil temperature (°C)
- Minimum and maximum air temperature (°C)
- Minimum and maximum air humidity (percentage)

### Automated Control

The system will:
- Turn the water pump ON/OFF based on soil moisture levels.
- Control the artificial lamp based on light intensity.
- Adjust ventilation and heating based on air and soil temperature.

### Remote Monitoring

Monitor and control the smart farm via the Blynk app:
- View real-time sensor readings.
- Receive notifications for any critical environmental conditions.

## Example Sensor Readings
```python
Moisture Level: 42.5% (ADC Value: 27891)
Light Intensity: 76.3%
Soil Temperature: 22.4°C
Temp: 25°C, Humidity: 60%
Pump ON
Lamp OFF
```

## Troubleshooting

- **Wi-Fi Connection Issues**:
  - Ensure the SSID and password in `wifi_credentials.txt` are correct.
  - Verify your router supports 2.4GHz Wi-Fi.

- **Sensor Readings Incorrect**:
  - Check the sensor connections.
  - Calibrate the sensors if required.

- **Actuators Not Working**:
  - Ensure proper GPIO pin assignments.
  - Verify the power supply to the actuators.

## Future Enhancements

- Integration with additional sensors (CO2, soil pH, NPK).
- Machine learning for predictive crop health analysis.
- Enhanced visualization with web dashboards.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
