import pandas as pd
import numpy as np
import os

INPUT = "data/training/pump_training_data.csv"
OUT = "data/processed"

WINDOW = 32

features = [
    "temperature_c",
    "pressure_kpa",
    "pressure_voltage",
    "vibration_level",
    "current_a"
]

label_map = {
    "GOOD": 0,
    "MODERATE": 1,
    "BAD": 2
}

df = pd.read_csv(INPUT)

# Remove GOOD pump-OFF samples
df = df[
    ~(
        (df["label"] == "GOOD") &
        (df["pressure_kpa"] == 0) &
        (df["current_a"] == 0)
    )
].reset_index(drop=True)

X = df[features].values.astype(np.float32)
y = df["label"].map(label_map).values

# Create consecutive windows
Xw = []
yw = []

for i in range(len(X) - WINDOW + 1):
    window = X[i:i + WINDOW]

    # Use majority label of the window
    labels = y[i:i + WINDOW]
    label = np.bincount(labels).argmax()

    Xw.append(window)
    yw.append(label)

Xw = np.array(Xw, dtype=np.float32)
yw = np.array(yw, dtype=np.int64)

os.makedirs(OUT, exist_ok=True)

np.save(f"{OUT}/X_windows.npy", Xw)
np.save(f"{OUT}/y_windows.npy", yw)

print("================================")
print("WINDOW CREATION COMPLETE")
print("================================")
print("Window size:", WINDOW)
print("Features:", len(features))
print("X shape:", Xw.shape)
print("y shape:", yw.shape)

print()
print("GOOD:", np.sum(yw == 0))
print("MODERATE:", np.sum(yw == 1))
print("BAD:", np.sum(yw == 2))
