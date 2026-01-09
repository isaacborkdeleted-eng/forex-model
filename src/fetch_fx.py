import requests
import pandas as pd
import os
from datetime import datetime, timedelta

BASE = "USD"
QUOTE = "PLN"

end = datetime.utcnow().date()
start = end - timedelta(days=365)

url = (
    f"https://www.frankfurter.app/{start}..{end}"
    f"?from={BASE}&to={QUOTE}"
)

r = requests.get(url, timeout=30)
data = r.json()

if "rates" not in data:
    raise RuntimeError(f"FX API failed: {data}")

rows = []
for date, rates in data["rates"].items():
    if QUOTE in rates:
        rows.append({
            "time": date,
            "price": rates[QUOTE]
        })

if not rows:
    raise RuntimeError("No FX price data returned")

df = pd.DataFrame(rows)
df["time"] = pd.to_datetime(df["time"])
df.sort_values("time", inplace=True)

os.makedirs("data", exist_ok=True)
df.to_csv("data/fx_prices.csv", index=False)

print(f"Saved {len(df)} daily FX rows")


