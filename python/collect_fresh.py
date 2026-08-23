import csv
import os
import time
import serial

PORT = "/dev/ttyACM0"
BAUD = 115200
OUTPUT = "data/fresh/fresh_sensor_data.csv"

print("\n================================")
print(" HYDROGUARD AI FRESH DATA")
print("================================")
print("1 = GOOD")
print("2 = MODERATE")
print("3 = BAD")
print("q = EXIT")
print("================================")

choice = input("Select condition: ").strip()

labels = {
    "1": "GOOD",
    "2": "MODERATE",
    "3": "BAD"
}

if choice not in labels:
    print("Exiting.")
    exit()

label = labels[choice]

os.makedirs("data/fresh", exist_ok=True)

file_exists = os.path.exists(OUTPUT) and os.path.getsize(OUTPUT) > 0

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except Exception as e:
    print("Serial error:", e)
    print("Available ports:")
    os.system("ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")
    exit()

time.sleep(2)

with open(OUTPUT, "a", newline="") as f:

    writer = csv.writer(f)

    if not file_exists:
        writer.writerow([
            "timestamp_ms",
            "temperature_c",
            "pressure_kpa",
            "pressure_voltage",
            "vibration_raw",
            "vibration_level",
            "current_a",
            "label"
        ])
        f.flush()

    print("\nCollecting:", label)
    print("Press Ctrl+C when you have enough readings.\n")

    count = 0

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
                float(parts[0])
                float(parts[1])
                float(parts[2])
                float(parts[3])
                int(parts[4])
                float(parts[5])
                float(parts[6])
            except ValueError:
                continue

            writer.writerow(parts + [label])
            f.flush()

            count += 1

            print(
                f"{count:4d} | "
                f"{parts[1]} C | "
                f"P={parts[2]} | "
                f"VIB={parts[4]} ({parts[5]}) | "
                f"I={parts[6]} | "
                f"{label}"
            )

    except KeyboardInterrupt:
        print("\n\nCollection stopped.")

ser.close()

print("Label :", label)
print("New rows:", count)
print("File:", OUTPUT)
