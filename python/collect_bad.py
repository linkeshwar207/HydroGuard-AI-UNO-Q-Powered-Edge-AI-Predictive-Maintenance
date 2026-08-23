import csv
import os
import time
import serial

PORT = "/dev/ttyACM0"
BAUD = 115200
OUTPUT = "data/fresh/bad.csv"

os.makedirs("data/fresh", exist_ok=True)

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

new_file = not os.path.exists(OUTPUT) or os.path.getsize(OUTPUT) == 0

with open(OUTPUT, "a", newline="") as f:
    writer = csv.writer(f)

    if new_file:
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

    print("\n================================")
    print("BAD DATA COLLECTION")
    print("================================")
    print("Collecting BAD readings...")
    print("Press Ctrl+C when finished.\n")

    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()

            if not line or line.startswith("timestamp_ms"):
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

            writer.writerow(parts + ["BAD"])
            f.flush()

            count += 1

            print(
                f"{count:4d} | "
                f"{parts[1]} C | "
                f"P={parts[2]} | "
                f"VIB={parts[4]} ({parts[5]}) | "
                f"I={parts[6]} | BAD"
            )

    except KeyboardInterrupt:
        print("\n\nBAD collection stopped.")

ser.close()

print("BAD rows saved:", count)
print("File:", OUTPUT)
