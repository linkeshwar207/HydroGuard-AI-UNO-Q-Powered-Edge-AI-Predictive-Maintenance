#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

void pressureBegin();
void temperatureBegin();
void currentBegin();
void vibrationBegin();

void updateSensors();
void updateTemperature();

float readPressureVoltage();
float readPressureKPa();

float readTemperatureC();

float readCurrentVoltage();
float readCurrentA();

int readVibrationRaw();
float readVibrationLevel();

void printSensorData();

#endif
