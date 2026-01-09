import requests
import pandas as pd
import os
from datetime import datetime, timedelta

BASE = "USD"
QUOTE = "PLN"

end = datetime.utcnow().date()
start = end - timedelta(days=365)

url = (
    "https://api.exchangerate.host/timeseries"
    f"?start_date={start}"
    f"&end_date={end}"
    f"&base={BASE}"
    f"&symbols={QUOTE}"
)

r = requests.get(url, timeout=30)
data = r.json()

if not data.get("success"):
    raise RuntimeError("FX API failed")

rows = []
for date, rates in data["rates"].items():
    rows.append({
        "time": date,
        "price": rates[QUOTE]
    })

df = pd.DataFrame(rows)
df["time"] = pd.to_datetime(df["time"])
df.sort_values("time", inplace=True)

os.makedirs("data", exist_ok=True)
df.to_csv("data/fx_prices.csv", index=False)

print(f"Saved {len(df)} daily FX rows")

