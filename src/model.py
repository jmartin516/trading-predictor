"""
n = len(df)              # número total de filas
i_train = int(n * 0.70)  # índice donde acaba train
i_val   = int(n * 0.85)  # índice donde acaba val (70%+15%)

train = df.iloc[:i_train]         # de 0 a 70%
val   = df.iloc[i_train:i_val]    # de 70% a 85%
test  = df.iloc[i_val:]           # de 85% al final
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt


# Carga de datos
df = pd.read_csv("data/BTC-USD_features.csv", parse_dates=["time"])

#split temporal
n = len(df)              # número total de filas
i_train = int(n * 0.7)
i_value = int(n * 0.85)

train = df.iloc[:i_train]
val = df.iloc[i_train:i_value]
test = df.iloc[i_value:]

# Verificacion de tamaños de rangos
print(f"train: {len(train)} filas | {train['time'].min()} - {train['time'].max()}")
print(f"val: {len(val)} filas | {val['time'].min()} - {val['time'].max()}")
print(f"test: {len(test)} filas | {test['time'].min()} - {test['time'].max()}")


features_columns = ["sma_24", "rsi_14", "ema_24", "macd", "macd_signal", "macd_diff"]
target_column = "label"

X_train = train[features_columns]
y_train = train[target_column]

X_val = val[features_columns]
y_val = val[target_column]

X_test = test[features_columns]
y_test = test[target_column]

# Verification
print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
print(f"X_val:   {X_val.shape}, y_val:   {y_val.shape}")
print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")


#crear el scaler
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print("train(deber ser media p y std 1):")
print(f"media: {X_train_scaled.mean(axis=0).round(3)}")
print(f"std: {X_train_scaled.std(axis=0).round(3)}")
print("\nval (NO sera media 0/std 1 - usamos params de train):")
print(f"media: {X_val_scaled.mean(axis=0).round(3)}")
print(f"std:   {X_val_scaled.std(axis=0).round(3)}")

model = keras.Sequential([
    layers.Input(shape=(X_train_scaled.shape[1],)),
    layers.Dense(32, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

model.summary()

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    X_train_scaled, y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=30,
    batch_size=32,
    verbose=1
)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

#grafico del loss
ax1.plot(history.history["loss"],     label="train")
ax1.plot(history.history["val_loss"], label="val")
ax1.set_title("Loss por epoch")
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Loss")
ax1.legend()

#grafico de accuracy
ax2.plot(history.history["accuracy"],     label="train")
ax2.plot(history.history["val_accuracy"], label="val")
ax2.set_title("Accuracy por epoch")
ax2.set_xlabel("Epoch")
ax2.set_ylabel("Accuracy")
ax2.legend()

plt.tight_layout()
plt.savefig("models/train_curves.png")
plt.show()