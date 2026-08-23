import numpy as np
import tensorflow as tf

X = np.load("data/processed/X_windows.npy")

# Fixed normalization parameters
mean = np.load("models/feature_mean.npy")
std = np.load("models/feature_std.npy")

X = (X - mean) / std
X = X.astype(np.float32)

# -----------------------------
# Keras model
# -----------------------------

keras_model = tf.keras.models.load_model(
    "models/pump_1dcnn.keras"
)

keras_output = keras_model.predict(
    X[:100],
    verbose=0
)

# -----------------------------
# TFLite model
# -----------------------------

interpreter = tf.lite.Interpreter(
    model_path="models/pump_1dcnn.tflite"
)

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

tflite_outputs = []

for sample in X[:100]:

    sample = sample[np.newaxis, :, :]

    interpreter.set_tensor(
        input_details[0]["index"],
        sample
    )

    interpreter.invoke()

    output = interpreter.get_tensor(
        output_details[0]["index"]
    )

    tflite_outputs.append(output[0])

tflite_output = np.array(tflite_outputs)

# -----------------------------
# Compare
# -----------------------------

keras_labels = np.argmax(
    keras_output,
    axis=1
)

tflite_labels = np.argmax(
    tflite_output,
    axis=1
)

same = np.sum(
    keras_labels == tflite_labels
)

print("================================")
print("KERAS vs TFLITE")
print("================================")

print("Samples tested :", 100)
print("Same predictions:", same)
print(
    "Agreement:",
    f"{same / 100 * 100:.2f}%"
)

print()
print("First 10 predictions:")

labels = ["GOOD", "MODERATE", "BAD"]

for i in range(10):
    print(
        f"{i+1}: "
        f"Keras={labels[keras_labels[i]]} | "
        f"TFLite={labels[tflite_labels[i]]}"
    )
