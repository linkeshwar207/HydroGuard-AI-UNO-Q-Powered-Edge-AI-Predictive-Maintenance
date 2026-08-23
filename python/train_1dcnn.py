import os
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix

# --------------------------------------------------
# Paths
# --------------------------------------------------

X_FILE = "data/processed/X_windows.npy"
Y_FILE = "data/processed/y_windows.npy"
MODEL_FILE = "models/pump_1dcnn.keras"

# --------------------------------------------------
# Load newly prepared combined dataset
# --------------------------------------------------

X = np.load(X_FILE)
y = np.load(Y_FILE)

print("Dataset shape:", X.shape)
print("Labels shape :", y.shape)

# --------------------------------------------------
# Split dataset
# --------------------------------------------------

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

print("Train:", X_train.shape)
print("Validation:", X_val.shape)
print("Test:", X_test.shape)

# --------------------------------------------------
# Class weights
# --------------------------------------------------

classes = np.unique(y_train)

weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)

class_weights = dict(
    zip(classes, weights)
)

print("Class weights:", class_weights)

# --------------------------------------------------
# Model
# --------------------------------------------------

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X.shape[1], X.shape[2])),

    tf.keras.layers.Conv1D(
        32,
        3,
        activation="relu"
    ),

    tf.keras.layers.MaxPooling1D(2),

    tf.keras.layers.Conv1D(
        64,
        3,
        activation="relu"
    ),

    tf.keras.layers.MaxPooling1D(2),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(
        64,
        activation="relu"
    ),

    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(
        3,
        activation="softmax"
    )
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# --------------------------------------------------
# Training
# --------------------------------------------------

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=8,
        restore_best_weights=True
    )
]

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=32,
    class_weight=class_weights,
    callbacks=callbacks,
    verbose=1
)

# --------------------------------------------------
# Test
# --------------------------------------------------

loss, accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=0
)

print("\n================================")
print("1D-CNN TEST RESULT")
print("================================")

print(
    "Test accuracy:",
    f"{accuracy * 100:.2f}%"
)

print(
    "Test loss:",
    f"{loss:.4f}"
)

# --------------------------------------------------
# Classification report
# --------------------------------------------------

pred = np.argmax(
    model.predict(X_test, verbose=0),
    axis=1
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        pred,
        labels=[0, 1, 2],
        target_names=[
            "GOOD",
            "MODERATE",
            "BAD"
        ],
        zero_division=0
    )
)

print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        pred,
        labels=[0, 1, 2]
    )
)

# --------------------------------------------------
# Save
# --------------------------------------------------

os.makedirs("models", exist_ok=True)

model.save(MODEL_FILE)

print("\nModel saved:")
print(MODEL_FILE)
