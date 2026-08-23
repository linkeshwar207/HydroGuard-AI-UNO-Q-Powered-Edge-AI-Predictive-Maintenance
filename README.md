# HydroGuard AI – UNO Q Powered Edge AI Predictive Maintenance

## Project Overview

HydroGuard AI is an edge-AI based predictive maintenance system for monitoring a DC water pump.

The system monitors:

- Pressure
- Temperature
- Current
- Vibration

The Arduino UNO Q acquires the sensor data and performs 1D-CNN based edge AI inference on its Linux MPU.

## Hardware

- Arduino UNO Q
- 9V DC Water Pump
- GZP6847A040KPP50 Pressure Sensor
- DS18B20 Waterproof Temperature Sensor
- INA291 Current Sensor
- Piezoelectric Vibration Sensor
- Water Pipes
- 9V Power Supply

## Software

- Arduino App Lab
- Arduino Sketch
- Python
- 1D-CNN
- ONNX Runtime
- Digital Twin
- CSV Data Logging
- Dashboard

## System Architecture

Sensors → STM32 MCU → Arduino Bridge → UNO Q Linux MPU → 1D-CNN → Prediction

## AI Output

The 1D-CNN classifies pump condition as:

- HEALTHY
- WARNING
- FAULT

## Data Flow

Sensor readings are collected continuously and stored as CSV data for training and analysis.

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
