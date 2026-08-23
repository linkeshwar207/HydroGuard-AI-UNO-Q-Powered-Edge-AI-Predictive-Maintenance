import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

INPUT = "data/training/pump_training_data_combined.csv"
OUTPUT_DIR = "data/processed"

WINDOW_SIZE = 32

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------
# 1. Load dataset
# -------------------------------------------------

df = pd.read_csv(INPUT)

original_rows = len(df)

# -------------------------------------------------
# 2. Remove invalid GOOD pump-OFF samples
# -------------------------------------------------

df = df[
    ~(
        (df["label"] == "GOOD") &
        (df["pressure_kpa"] == 0) &
        (df["current_a"] == 0)
    )
].copy()

df = df.dropna().reset_index(drop=True)

# -------------------------------------------------
# 3. Features
# -------------------------------------------------

features = [
    "temperature_c",
    "pressure_kpa",
    "pressure_voltage",
    "vibration_level",
    "current_a"
]

X_raw = df[features].values.astype(np.float32)

# -------------------------------------------------
# 4. Labels
# -------------------------------------------------

label_map = {
    "GOOD": 0,
    "MODERATE": 1,
    "BAD": 2
}

y_raw = df["label"].map(label_map).values

# Remove unknown labels if any
valid = ~pd.isna(y_raw)

X_raw = X_raw[valid]
y_raw = y_raw[valid].astype(np.int64)

# -------------------------------------------------
# 5. Normalize
# -------------------------------------------------

scaler = StandardScaler()
X = scaler.fit_transform(X_raw).astype(np.float32)

joblib.dump(
    scaler,
    "data/processed/scaler.pkl"
)

# Save mean/std for TFLite validation/deployment
np.save(
    "models/feature_mean.npy",
    scaler.mean_.astype(np.float32)
)

np.save(
    "models/feature_std.npy",
    scaler.scale_.astype(np.float32)
)

# -------------------------------------------------
# 6. Create 32-sample overlapping windows
# -------------------------------------------------

X_windows = []
y_windows = []

for i in range(len(X) - WINDOW_SIZE + 1):

    window = X[i:i + WINDOW_SIZE]
    labels = y_raw[i:i + WINDOW_SIZE]

    # Majority label
    label = np.bincount(
        labels,
        minlength=3
    ).argmax()

    X_windows.append(window)
    y_windows.append(label)

X_windows = np.asarray(
    X_windows,
    dtype=np.float32
)

y_windows = np.asarray(
    y_windows,
    dtype=np.int64
)

# -------------------------------------------------
# 7. Save complete window dataset
# -------------------------------------------------

np.save(
    "data/processed/X_windows.npy",
    X_windows
)

np.save(
    "data/processed/y_windows.npy",
    y_windows
)

# -------------------------------------------------
# 8. Train/test split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_windows,
    y_windows,
    test_size=0.20,
    random_state=42,
    stratify=y_windows
)

np.save(
    "data/processed/X_train.npy",
    X_train
)

np.save(
    "data/processed/X_test.npy",
    X_test
)

np.save(
    "data/processed/y_train.npy",
    y_train
)

np.save(
    "data/processed/y_test.npy",
    y_test
)

# -------------------------------------------------
# 9. Report
# -------------------------------------------------

print()
print("====================================")
print("DATASET PREPARATION COMPLETE")
print("====================================")

print("Original rows       :", original_rows)
print("Rows after cleaning :", len(df))
print("Window size         :", WINDOW_SIZE)

print()
print("Window dataset:")
print("X_windows:", X_windows.shape)
print("y_windows:", y_windows.shape)

print()
print("Window classes:")
print("GOOD     :", int((y_windows == 0).sum()))
print("MODERATE :", int((y_windows == 1).sum()))
print("BAD      :", int((y_windows == 2).sum()))

print()
print("Training windows:", len(X_train))
print("Testing windows :", len(X_test))

print()
print("Scaler saved:")
print("data/processed/scaler.pkl")

print()
print("====================================")


