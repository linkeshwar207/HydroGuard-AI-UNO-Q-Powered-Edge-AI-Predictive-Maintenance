#include <Arduino.h>
#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <math.h>

#include "sensors.h"

namespace
{
    MPU6050 mpu;

    bool mpuReady = false;

    float vibrationLevel = 0.0f;
    int vibrationRaw = 0;
}

void vibrationBegin()
{
    Wire.begin();

    mpu.initialize();

    if (mpu.testConnection())
    {
        mpuReady = true;
        Serial.println("MPU6050 OK");
    }
    else
    {
        mpuReady = false;
        Serial.println("MPU6050 ERROR");
    }
}

int readVibrationRaw()
{
    if (!mpuReady)
    {
        vibrationRaw = 0;
        vibrationLevel = 0.0f;
        return 0;
    }

    int16_t ax;
    int16_t ay;
    int16_t az;

    // Read ONE MPU6050 sample
    mpu.getAcceleration(
        &ax,
        &ay,
        &az
    );

    // MPU6050 default ±2g:
    // 16384 counts = 1g
    float ax_g =
        static_cast<float>(ax) / 16384.0f;

    float ay_g =
        static_cast<float>(ay) / 16384.0f;

    float az_g =
        static_cast<float>(az) / 16384.0f;

    float magnitude =
        sqrt(
            ax_g * ax_g +
            ay_g * ay_g +
            az_g * az_g
        );

    // Remove static gravity
    float dynamic_g =
        fabs(magnitude - 1.0f);

    // Convert g → m/s²
    vibrationLevel =
        dynamic_g * 9.80665f;

    // Store raw value from THE SAME sample
    vibrationRaw =
        static_cast<int>(
            vibrationLevel * 1000.0f
        );

    return vibrationRaw;
}

float readVibrationLevel()
{
    // IMPORTANT:
    // Do NOT read the MPU6050 again.
    // Return the level calculated from the
    // same sample used by readVibrationRaw().
    return vibrationLevel;
}
