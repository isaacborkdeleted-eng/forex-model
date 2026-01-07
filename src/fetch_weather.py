import requests
import json
from datetime import datetime

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=52.52"
    "&longitude=13.41"
    "&hourly=temperature_2m,cloudcover"
    "&timezone=UTC"
)

r = requests.get(URL)
data = r.json()

now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
times = data["hourly"]["time"]

idx = times.index(now.strftime("%Y-%m-%dT%H:00"))

weather = {
    "temperature": data["hourly"]["temperature_2m"][idx],
    "cloudcover": data["hourly"]["cloudcover"][idx]
}

with open("data/weather.json", "w") as f:
    json.dump(weather, f, indent=2)

print("Weather saved")

