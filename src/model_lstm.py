import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras  import layers
import matplotlib.pyplot as plt

#cargad datos de csv
df = pd.read_csv("data/BTC-USD_features.csv", parse_dates=["time"])

n = len(df)
i_train = int(n * 0.7)
i_value = int(n * 0.85)

train = df.iloc[:i_train]
val = df.iloc[i_train:i_value]
test = df.iloc[i_value:]

# Verification of the dimension
print(f"train: {len(train)} rows | {train['time'].min()} - {train['time'].max()}")
print(f"val: {len(val)} filas | {val['time'].min()} - {val['time'].max()}")
print(f"test: {len(test)} filas | {test['time'].min()} - {test['time'].max()}")


features_columns = ["sma_24", "rsi_14", "ema_24", "macd", "macd_signal", "macd_diff"]
target_column = ["label"]

X_train = train[features_columns]
y_train = train[target_column]


X_vale = value[features_columns]
y_value = value[target_column]

X_test = test[features_columns]
y_test = test[features_columns]

print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
print(f"X_val:   {X_val.shape}, y_val:   {y_val.shape}")
print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")

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


