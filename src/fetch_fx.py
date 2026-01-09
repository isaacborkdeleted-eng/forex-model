import requests
import pandas as pd
import os
import json
import sys

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

r = requests.get(URL, timeout=30)
data = r.json()

# Handle rate limits or API errors gracefully
if "Time Series FX (60min)" not in data:
    print("Alpha Vantage did not return FX data.")
    print("Full response:")
    print(json.dumps(data, indent=2))

    # If we already have data, reuse it
    if os.path.exists("data/fx_prices.csv"):
        print("Using existing FX data.")
        sys.exit(0)
    else:
        raise RuntimeError("No FX data available and no cached file.")

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

print(f"Saved {len(df)} FX price rows")
