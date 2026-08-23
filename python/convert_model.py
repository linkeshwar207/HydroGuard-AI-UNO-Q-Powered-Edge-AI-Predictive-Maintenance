import tensorflow as tf

model = tf.keras.models.load_model(
    "models/pump_1dcnn.keras"
)

converter = tf.lite.TFLiteConverter.from_keras_model(model)

tflite_model = converter.convert()

with open("models/pump_1dcnn.tflite", "wb") as f:
    f.write(tflite_model)

print("TFLite model created:")
print("models/pump_1dcnn.tflite")
