import serial
import numpy as np
import tensorflow as tf
import time

PORT = "/dev/ttyACM0"
BAUD = 115200

MODEL = "models/pump_1dcnn.tflite"
MEAN = "models/feature_mean.npy"
STD = "models/feature_std.npy"

labels = ["GOOD", "MODERATE", "BAD"]

mean = np.load(MEAN).astype(np.float32)
std = np.load(STD).astype(np.float32)

interpreter = tf.lite.Interpreter(model_path=MODEL)
interpreter.allocate_tensors()

inp = interpreter.get_input_details()[0]
out = interpreter.get_output_details()[0]

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

buffer = []

print("================================")
print(" HYDROGUARD AI LIVE INFERENCE")
print("================================")
print("Waiting for sensor data...\n")

try:
    while True:

        line = ser.readline().decode(
            errors="ignore"
        ).strip()

        if not line:
            continue

        if line.startswith("timestamp_ms"):
            continue

        parts = line.split(",")

        if len(parts) != 7:
            continue

        try:
            temperature = float(parts[1])
            pressure = float(parts[2])
            pressure_voltage = float(parts[3])
            vibration = float(parts[5])
            current = float(parts[6])
        except ValueError:
            continue

        sample = [
            temperature,
            pressure,
            pressure_voltage,
            vibration,
            current
        ]

        buffer.append(sample)

        if len(buffer) < 32:
            print(
                f"Collecting window: "
                f"{len(buffer)}/32"
            )
            continue

        window = np.array(
            buffer[-32:],
            dtype=np.float32
        )

        window = (
            window - mean
        ) / (std + 1e-8)

        window = window.reshape(
            1, 32, 5
        ).astype(np.float32)

        interpreter.set_tensor(
            inp["index"],
            window
        )

        interpreter.invoke()

        probabilities = interpreter.get_tensor(
            out["index"]
        )[0]

        prediction = int(
            np.argmax(probabilities)
        )

        confidence = (
            probabilities[prediction] * 100
        )

        print(
            f"\nTemperature : {temperature:.2f} C"
        )
        print(
            f"Pressure    : {pressure:.2f} kPa"
        )
        print(
            f"Vibration   : {vibration:.3f} m/s²"
        )
        print(
            f"Current     : {current:.3f} A"
        )
        print(
            f"AI Prediction: {labels[prediction]}"
        )
        print(
            f"Confidence   : {confidence:.2f}%"
        )

        # Keep last 32 samples
        buffer = buffer[-32:]

except KeyboardInterrupt:
    print("\nAI inference stopped.")

finally:
    ser.close()
