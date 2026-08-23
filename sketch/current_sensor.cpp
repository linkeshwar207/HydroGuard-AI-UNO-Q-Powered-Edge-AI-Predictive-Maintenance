#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include "sensors.h"

namespace
{
    Adafruit_INA219 ina219;
    bool ina219OK = false;
}

void currentBegin()
{
    delay(100);

    Serial.println("Checking INA219...");

    if (ina219.begin())
    {
        ina219OK = true;
        Serial.println("INA219 CONNECTED");
    }
    else
    {
        ina219OK = false;
        Serial.println("INA219 NOT DETECTED!");
    }
}

float readCurrentA()
{
    if (!ina219OK)
    {
        return 0.0f;
    }

    float current_mA = ina219.getCurrent_mA();

    if (!isfinite(current_mA))
    {
        return 0.0f;
    }

    return current_mA / 1000.0f;
}
