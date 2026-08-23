#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define TEMP_PIN D4

OneWire oneWire(TEMP_PIN);
DallasTemperature temperatureSensor(&oneWire);

float temperatureC = NAN;

void temperatureBegin()
{
    temperatureSensor.begin();

    Serial.println("DS18B20 initialized");

    int count = temperatureSensor.getDeviceCount();

    Serial.print("DS18B20 devices: ");
    Serial.println(count);

    if (count == 0)
    {
        Serial.println("DS18B20 NOT DETECTED!");
    }
}

void updateTemperature()
{
    temperatureSensor.requestTemperatures();

    float temp = temperatureSensor.getTempCByIndex(0);

    if (temp != DEVICE_DISCONNECTED_C &&
        temp >= -55.0 &&
        temp <= 125.0)
    {
        temperatureC = temp;
    }
}

float readTemperatureC()
{
    if (isnan(temperatureC))
    {
        return NAN;
    }

    return temperatureC;
}
