import requests
import pandas as pd
import os

API_KEY = "HPDY217FM61W6DOD"
PAIR_FROM = "USD"
PAIR_TO = "PLN"

URL = (
    "https://www.alphavantage.co/query"
    "?function=FX_INTRADAY"
    "&from_symbol={}"
    "&to_symbol={}"
    "&interval=60min"
    "&outputsize=full"
    "&apikey={}"
).format(PAIR_FROM, PAIR_TO, API_KEY)

r = requests.get(URL)
data = r.json()

if "Time Series FX (60min)" not in data:
    raise RuntimeError("FX data not returned")

rows = []
for t, v in data["Time Series FX (60min)"].items():
    rows.append({
        "time": t,
        "price": float(v["4. close"])
    })

df = pd.DataFrame(rows)
df["time"] = pd.to_datetime(df["time"])
df.sort_values("time", inplace=True)

os.makedirs("data", exist_ok=True)
df.to_csv("data/fx_prices.csv", index=False)

print("FX prices saved")

