# HydroGuard AI – UNO Q Powered Edge AI Predictive Maintenance

## Project Overview

HydroGuard AI is an edge-AI based predictive maintenance system for monitoring a DC water pump using Arduino UNO Q.

The system monitors pressure, temperature, current and vibration to identify pump operating conditions.

## Hardware

- Arduino UNO Q
- 9V DC Water Pump
- GZP6847A040KPP50 Pressure Sensor
- DS18B20 Waterproof Temperature Sensor
- INA291 Current Sensor
- Piezoelectric Vibration Sensor
- Water Pipes

## Software

- Arduino App Lab
- Arduino Sketch
- Python
- 1D-CNN AI
- Digital Twin
- CSV Data Logging
- Monitoring Dashboard

## Architecture

Sensors
→ STM32 MCU
→ Arduino Bridge
→ UNO Q Linux MPU
→ 1D-CNN
→ Pump Condition Prediction

## Sensors

### Pressure Sensor
GZP6847A040KPP50 measures pump pressure.

### Temperature Sensor
DS18B20 measures pump temperature.

### Current Sensor
INA291 monitors pump current.

### Vibration Sensor
Piezoelectric vibration sensor monitors pump vibration.

## AI

A 1D-CNN model is used for pump condition analysis.

The AI processes time-series sensor data and identifies:

- HEALTHY
- WARNING
- FAULT

## Digital Twin

The Digital Twin represents the real-time operating condition of the physical pump using the sensor measurements and AI prediction.

## Data Logging

Sensor readings are collected and stored in CSV format for analysis and machine-learning training.

## Code Structure

```text
sketch/
├── sketch.ino
├── sensors.h
├── pressure_sensor.cpp
├── temperature_sensor.cpp
├── current_sensor.cpp
└── vibration_sensor.cpp

python/
├── main.py
├── data_logger.py
├── digital_twin.py
├── ml_model.py
├── dashboard.py
└── requirements.txt
