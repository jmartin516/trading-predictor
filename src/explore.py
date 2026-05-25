import pandas as pd


"""df = pd.read_csv("data/BTC-USD_1h.csv", parse_dates=["time"])
print(df)
df.info()
print(df.describe())

diferencias = df["time"].diff()
print(diferencias.value_counts())

huecos = df[diferencias > pd.Timedelta(hours=1)]
print(huecos)
"""

def explore(pair):
    print(f"exploring {pair}")
    df = pd.read_csv(f"data/{pair}_1h.csv", parse_dates=["time"])
    df.info()
    print(df.describe())

    diferencias = df["time"].diff()
    print(diferencias.value_counts())

    huecos = df[diferencias > pd.Timedelta(hours=1)]
    print(huecos)

pares = ["BTC-USD", "ETH-USD", "LTC-USD"]

for par in pares:
    explore(par)