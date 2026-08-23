import numpy as np
import tensorflow as tf

MODEL = "models/pump_1dcnn.tflite"

interpreter = tf.lite.Interpreter(model_path=MODEL)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input shape :", input_details[0]["shape"])
print("Output shape:", output_details[0]["shape"])

X = np.load("data/processed/X_windows.npy")

# Same normalization used during training
mean = X.mean(axis=(0, 1), keepdims=True)
std = X.std(axis=(0, 1), keepdims=True) + 1e-8

X = (X - mean) / std

labels = ["GOOD", "MODERATE", "BAD"]

for i in range(10):
    sample = X[i:i+1].astype(np.float32)

    interpreter.set_tensor(
        input_details[0]["index"],
        sample
    )

    interpreter.invoke()

    output = interpreter.get_tensor(
        output_details[0]["index"]
    )[0]

    prediction = np.argmax(output)
    confidence = output[prediction] * 100

    print(
        f"Window {i+1}: "
        f"{labels[prediction]} "
        f"({confidence:.2f}%)"
    )
