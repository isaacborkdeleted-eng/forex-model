import json
from iddfs import iddfs

with open("data/indicators.json") as f:
    indicators = json.load(f)

try:
    with open("state.json") as f:
        state = json.load(f)
except FileNotFoundError:
    state = {
        "usd": 20000.0,
        "pln": 0.0,
        "history": []
    }

action = iddfs(state, indicators)

price = indicators["current_price"]
fee = 0.05

if action == "BUY" and state["usd"] > fee:
    amount = (state["usd"] - fee) / price
    state["pln"] += amount
    state["usd"] = 0

elif action == "SELL" and state["pln"] > 0:
    state["usd"] += state["pln"] * price - fee
    state["pln"] = 0

state["last_action"] = action

with open("state.json", "w") as f:
    json.dump(state, f, indent=2)

print("Action:", action)

