import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

CSV = "data/fresh/fresh_sensor_data.csv"
MODEL = "models/pump_1dcnn.tflite"

FEATURES = [
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

df = pd.read_csv(CSV)

X = df[FEATURES].to_numpy(dtype=np.float32)
y = df["label"].map(label_map).to_numpy()

mean = np.load("models/feature_mean.npy").reshape(1, -1)
std = np.load("models/feature_std.npy").reshape(1, -1)

X = (X - mean) / (std + 1e-8)

# Create OVERLAPPING 32-sample windows
Xw = []
yw = []

for i in range(len(X) - 32 + 1):
    Xw.append(X[i:i+32])

    # Majority label of each window
    labels = y[i:i+32]
    yw.append(np.bincount(labels, minlength=3).argmax())

Xw = np.asarray(Xw, dtype=np.float32)
yw = np.asarray(yw, dtype=np.int32)

print("\n================================")
print("FRESH TFLITE VALIDATION")
print("================================")
print("Raw rows:", len(df))
print("Windows :", len(Xw))

interpreter = tf.lite.Interpreter(model_path=MODEL)
interpreter.allocate_tensors()

inp = interpreter.get_input_details()[0]
out = interpreter.get_output_details()[0]

pred = []

for window in Xw:

    interpreter.set_tensor(
        inp["index"],
        window[np.newaxis, :, :]
    )

    interpreter.invoke()

    result = interpreter.get_tensor(out["index"])

    pred.append(int(np.argmax(result[0])))

pred = np.array(pred)

print("\nAccuracy:",
      f"{accuracy_score(yw, pred) * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        yw,
        pred,
        labels=[0, 1, 2],
        target_names=["GOOD", "MODERATE", "BAD"],
        zero_division=0
    )
)

print("Confusion Matrix:")
print(confusion_matrix(yw, pred, labels=[0, 1, 2]))

print("\nPrediction counts:")
for i, name in enumerate(["GOOD", "MODERATE", "BAD"]):
    print(name, ":", int(np.sum(pred == i)))
