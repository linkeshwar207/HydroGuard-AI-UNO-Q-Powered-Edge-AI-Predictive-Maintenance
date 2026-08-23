#include <Arduino.h>
#include "sensors.h"

namespace
{
    constexpr int PRESSURE_PIN = A0;

    // UNO Q ADC
    constexpr float ADC_REFERENCE = 3.3f;
    constexpr int ADC_MAX = 16383;

    // GZP6847A 0-40 kPa, 5 V version
    constexpr float SENSOR_V_MIN = 0.5f;
    constexpr float SENSOR_V_MAX = 4.5f;

    constexpr float PRESSURE_MIN_KPA = 0.0f;
    constexpr float PRESSURE_MAX_KPA = 40.0f;

    // Set this to 1.0 if OUT is connected directly.
    // If you later add a voltage divider, change this
    // to the divider compensation factor.
    constexpr float VOLTAGE_DIVIDER_FACTOR = 1.0f;
}

void pressureBegin()
{
    pinMode(PRESSURE_PIN, INPUT);

    // UNO Q: 14-bit ADC = 0 to 16383
    analogReadResolution(14);
}

float readPressureVoltage()
{
    int raw = analogRead(PRESSURE_PIN);

    float adcVoltage =
        (static_cast<float>(raw) * ADC_REFERENCE) /
        static_cast<float>(ADC_MAX);

    // Recover actual sensor output voltage
    float sensorVoltage =
        adcVoltage * VOLTAGE_DIVIDER_FACTOR;

    return sensorVoltage;
}

float readPressureKPa()
{
    float voltage = readPressureVoltage();

    // 0.5 V = 0 kPa
    // 4.5 V = 40 kPa
    float pressure =
        (voltage - SENSOR_V_MIN) *
        (PRESSURE_MAX_KPA - PRESSURE_MIN_KPA) /
        (SENSOR_V_MAX - SENSOR_V_MIN) +
        PRESSURE_MIN_KPA;

    // Prevent negative values
    if (pressure < PRESSURE_MIN_KPA)
    {
        pressure = PRESSURE_MIN_KPA;
    }

    // Prevent values above sensor range
    if (pressure > PRESSURE_MAX_KPA)
    {
        pressure = PRESSURE_MAX_KPA;
    }

    return pressure;
}
