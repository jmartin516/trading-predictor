from modulefinder import test

import pandas as pd 
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
'''
df = pd.read_csv("data/BTC-USD_1h.csv", parse_dates=["time"])

df["future_close"] = df["close"].shift(-24) #el close dentro de 24h columna auxiliar

df = df.dropna() #eliminar filas sin future_close

df["label"] = (df["future_close"] > df["close"]).astype(int) #1 si sube 0 si baja

df["sma_24"] = df["close"].rolling(window=24).mean() #media movil de 24h

df["rsi_14"] = RSIIndicator(df["close"], window=14).rsi() #RSI de 14h

df["ema_24"] = EMAIndicator(df["close"], window=24).ema_indicator() #EMA de 24h

macd = MACD(close=df["close"])
df["macd"] = macd.macd()
df["macd_signal"] = macd.macd_signal()
df["macd_diff"] = macd.macd_diff()

df = df.dropna()


print(df.tail(150))

print(df["label"].value_counts())

'''

def build_features(pair):
    print(f"building features for the pair {pair}")
    df = pd.read_csv(f"data/{pair}_1h.csv", parse_dates=["time"])

    #1 step
    df["future_close"] = df["close"].shift(-24)
    df["label"] = (df["future_close"] > df["close"]).astype(int)
   

    #2 step
    df["sma_24"] = df["close"].rolling(window=24).mean()
    df["rsi_14"] = RSIIndicator(df["close"], window=14).rsi()
    df["ema_24"] = EMAIndicator(df["close"], window=24).ema_indicator()
    macd = MACD(close=df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_diff"] = macd.macd_diff()

    #3 step - eliminate NA values
    df = df.dropna()
    df = df.drop(columns=["future_close"])

    #4 step save
    df.to_csv(f"data/{pair}_features.csv", index=False)


pares = ["BTC-USD", "ETH-USD", "LTC-USD"]
for par in pares:
    build_features(par)


