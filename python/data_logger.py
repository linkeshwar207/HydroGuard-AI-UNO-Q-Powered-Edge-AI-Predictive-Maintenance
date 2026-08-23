import serial
import csv
import os

# ==============================
# UNO Q SERIAL SETTINGS
# ==============================

PORT = "/dev/ttyACM0"
BAUD = 115200

# ==============================
# ASK FOR DATASET LABEL
# ==============================

print()
print("================================")
print("   HYDROGUARD DATA COLLECTION")
print("================================")
print()
print("Select dataset label:")
print("1 = GOOD")
print("2 = MODERATE")
print("3 = BAD")
print()

choice = input("Enter choice (1/2/3): ").strip()

labels = {
    "1": "GOOD",
    "2": "MODERATE",
    "3": "BAD"
}

if choice not in labels:
    print("Invalid choice.")
    raise SystemExit

LABEL = labels[choice]

print()
print("Selected label:", LABEL)
print()

# ==============================
# CSV FILE
# ==============================

CSV_FILE = os.path.expanduser(
    "~/HydroGuardAI/data/raw/sensor_data.csv"
)

os.makedirs(
    os.path.dirname(CSV_FILE),
    exist_ok=True
)

# ==============================
# CONNECT TO UNO Q
# ==============================

print("Connecting to Arduino UNO Q...")

try:
    ser = serial.Serial(
        PORT,
        BAUD,
        timeout=1
    )

except Exception as e:
    print("ERROR: Could not connect to UNO Q")
    print(e)
    raise SystemExit

print("UNO Q connected successfully!")
print("Saving to:")
print(CSV_FILE)
print()
print("LABEL:", LABEL)
print("Waiting for sensor data...")
print("Press Ctrl+C to stop.")
print()

# ==============================
# OPEN CSV
# ==============================

with open(
    CSV_FILE,
    "a",
    newline=""
) as file:

    writer = csv.writer(file)

    try:

        while True:

            line = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not line:
                continue

            # Ignore Arduino diagnostic messages
            if not line[0].isdigit():
                continue

            values = line.split(",")

            # We expect 7 sensor values
            if len(values) != 7:
                continue

            # Add the selected label
            values.append(LABEL)

            # Save row
            writer.writerow(values)

            file.flush()

            # Display
            print(",".join(values))

    except KeyboardInterrupt:

        print()
        print("Data collection stopped.")

    finally:

        ser.close()

        print()
        print("UNO Q serial connection closed.")
        print("CSV saved at:")
        print(CSV_FILE)
