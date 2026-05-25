import requests
import pandas as pd 
from datetime import datetime, timedelta
import time
"""
url = "https://api.exchange.coinbase.com/products/BTC-USD/candles"
params = {"granularity": 3600}
respuesta = requests.get(url, params=params)
datos = respuesta.json()
print(datos[:2])

df = pd.DataFrame(datos, columns=["time", "low", "high", "open", "close", "volume"])
print(df)
print(df["close"]) 

df["time"] = pd.to_datetime(df["time"], unit="s") #convertir a segundos

df = df.sort_values("time").reset_index(drop=True) #Ordenar en forma descendente

print(df)

df.to_csv("data/BTC-USD_1h.csv", index=False)
print("data for Bitcoin stored")

end = datetime.now()
start = end - timedelta(hours=300)

params = {
    "granularity": 3600,
    "start": start.isoformat(),    # el isoformat para convertir la fecha al texto que coinbase espera
    "end": end.isoformat(),
}
"""

def get_candles(pair, start, end):
    url = f"https://api.exchange.coinbase.com/products/{pair}/candles"
    print(f"la descargade datos para {pair} ha mepezado")
    params = {
        "granularity": 3600,
        "start": start.isoformat(),
        "end": end.isoformat(),
    }
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    df = pd.DataFrame(datos, columns=["time", "low", "high", "open", "close", "volume"])
    return df


def download_history(pair):
    todos = []
    end = datetime.now()
    objetivo = end - timedelta(days=365*2)

    while end > objetivo:
        start = end - timedelta(hours=300)
        trozo = get_candles(pair, start, end)
        todos.append(trozo)
        end = start
        time.sleep(0.5)

    df = pd.concat(todos, ignore_index=True)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df.sort_values("time").reset_index(drop=True)
    print(df)
    print(f"data for {pair} stored, {len(df)} rows")
    df.to_csv(f"data/{pair}_1h.csv", index=False)

pares = ["BTC-USD", "ETH-USD", "LTC-USD"]
for par in pares:
    download_history(par)




