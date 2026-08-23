#include <Arduino.h>
#include "sensors.h"

void setup()
{
    Serial.begin(115200);

    delay(1000);

    pressureBegin();
    temperatureBegin();
    currentBegin();
    vibrationBegin();

    Serial.println("HydroGuard AI - Pump Monitoring");
    Serial.println("Pressure_kPa,Temperature_C,Current_A,Vibration");
}

void loop()
{
    updateTemperature();

    float pressure = readPressureKPa();
    float temperature = readTemperatureC();
    float current = readCurrentA();
    int vibration = readVibrationRaw();

    Serial.print(pressure, 2);
    Serial.print(",");
    Serial.print(temperature, 2);
    Serial.print(",");
    Serial.print(current, 3);
    Serial.print(",");
    Serial.println(vibration);

    delay(500);
}
