import csv
import time
import serial

PORT = "/dev/ttyACM0"
BAUD = 115200
OUT = "data/fresh/good.csv"

ser = serial.Serial(PORT, BAUD, timeout=2)
time.sleep(2)

with open(OUT, "w", newline="") as f:
    writer = csv.writer(f)

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

    count = 0

    print("GOOD DATA COLLECTION STARTED")
    print("Keep the pump in NORMAL/GOOD condition.")
    print("Collecting 150 readings...")

    while count < 150:
        line = ser.readline().decode(errors="ignore").strip()

        if not line:
            continue

        if line.startswith("timestamp_ms"):
            continue

        parts = line.split(",")

        if len(parts) != 7:
            continue

        try:
            float(parts[1])
            float(parts[2])
            float(parts[3])
            int(parts[4])
            float(parts[5])
            float(parts[6])
        except ValueError:
            continue

        writer.writerow(parts + ["GOOD"])
        f.flush()

        count += 1

        print(f"{count}/150  {line},GOOD")

ser.close()

print("\nGOOD COLLECTION COMPLETE")
print("Saved:", OUT)
