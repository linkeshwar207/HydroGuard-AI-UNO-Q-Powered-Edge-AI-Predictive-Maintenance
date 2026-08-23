import numpy as np
import tensorflow as tf

MODEL = "models/pump_1dcnn.keras"

model = tf.keras.models.load_model(MODEL)

X = np.load("data/processed/X_windows.npy")
y = np.load("data/processed/y_windows.npy")

# Same normalization used during training
mean = X.mean(axis=(0, 1), keepdims=True)
std = X.std(axis=(0, 1), keepdims=True) + 1e-8

X = (X - mean) / std

labels = ["GOOD", "MODERATE", "BAD"]

pred = model.predict(X[:10], verbose=0)

for i, p in enumerate(pred):
    result = labels[np.argmax(p)]
    confidence = np.max(p) * 100

    print(
        f"Window {i+1}: {result} "
        f"({confidence:.2f}%)"
    )
