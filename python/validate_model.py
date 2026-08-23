import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

CSV = "data/test/fresh_test_synthetic.csv"
MODEL = "models/pump_1dcnn.tflite"

FEATURES = [
    "temperature_c",
    "pressure_kpa",
    "pressure_voltage",
    "vibration_level",
    "current_a"
]

LABELS = ["GOOD", "MODERATE", "BAD"]
LABEL_MAP = {"GOOD": 0, "MODERATE": 1, "BAD": 2}

WINDOW = 32

# Load data
df = pd.read_csv(CSV)

X = df[FEATURES].values.astype(np.float32)
y = df["label"].map(LABEL_MAP).values

# Fixed normalization from training
mean = np.load("models/feature_mean.npy").reshape(1, -1)
std = np.load("models/feature_std.npy").reshape(1, -1)

X = (X - mean) / std

# Create windows without crossing class boundaries
Xw = []
yw = []

start = 0

while start < len(X):
    label = y[start]
    end = start

    while end < len(X) and y[end] == label:
        end += 1

    for i in range(start, end - WINDOW + 1):
        Xw.append(X[i:i + WINDOW])
        yw.append(label)

    start = end

Xw = np.asarray(Xw, dtype=np.float32)
yw = np.asarray(yw)

print("================================")
print("VALIDATION DATA")
print("================================")
print("Windows:", len(Xw))

# TFLite
interpreter = tf.lite.Interpreter(model_path=MODEL)
interpreter.allocate_tensors()

inp = interpreter.get_input_details()[0]
out = interpreter.get_output_details()[0]

pred = []

for sample in Xw:
    sample = sample[np.newaxis, :, :].astype(np.float32)

    interpreter.set_tensor(inp["index"], sample)
    interpreter.invoke()

    output = interpreter.get_tensor(out["index"])[0]
    pred.append(np.argmax(output))

pred = np.asarray(pred)

print()
print("Accuracy:", f"{accuracy_score(yw, pred) * 100:.2f}%")

print()
print("Classification Report:")
print(classification_report(
    yw,
    pred,
    labels=[0, 1, 2],
    target_names=LABELS,
    zero_division=0
))

print("Confusion Matrix:")
print(confusion_matrix(
    yw,
    pred,
    labels=[0, 1, 2]
))
