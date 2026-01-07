import pandas as pd
import json

df = pd.read_csv("data/fx_prices.csv", parse_dates=["time"])
df.sort_values("time", inplace=True)

current_price = df.iloc[-1]["price"]
price_2h = df.iloc[-3]["price"]

year_ago = df[df["time"] >= df["time"].max() - pd.Timedelta(days=365)]
two_months = df[df["time"] >= df["time"].max() - pd.Timedelta(days=60)]

year_trend = year_ago.iloc[-1]["price"] - year_ago.iloc[0]["price"]
avg_2m = two_months["price"].mean()

with open("data/weather.json") as f:
    weather = json.load(f)

# Weather impact (completely arbitrary, as requested)
weather_bias = (
    (20 - weather["temperature"]) * 0.01 +
    (weather["cloudcover"] / 100) * 0.02
)

indicators = {
    "current_price": current_price,
    "price_2h": price_2h,
    "year_trend": year_trend,
    "avg_2m": avg_2m,
    "weather_bias": weather_bias
}

with open("data/indicators.json", "w") as f:
    json.dump(indicators, f, indent=2)

print("Indicators computed")

