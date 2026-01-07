ACTIONS = ["BUY", "SELL", "HOLD"]

def evaluate(state, indicators):
    value = state["usd"] + state["pln"] * indicators["current_price"]

    # Long-term trend dominates
    value += indicators["year_trend"] * 10

    # Penalize overtrading
    value -= len(state["history"]) * 0.01

    return value

def dfs(state, indicators, depth):
    if depth == 0:
        return evaluate(state, indicators), []

    best_score = -1e9
    best_path = []

    for action in ACTIONS:
        new_state = simulate(state, indicators, action)
        score, path = dfs(new_state, indicators, depth - 1)

        if score > best_score:
            best_score = score
            best_path = [action] + path

    return best_score, best_path

def iddfs(state, indicators, max_depth=3):
    best_action = "HOLD"
    best_score = -1e9

    for depth in range(1, max_depth + 1):
        score, path = dfs(state, indicators, depth)
        if score > best_score:
            best_score = score
            best_action = path[0]

    return best_action

def simulate(state, indicators, action):
    state = {
        "usd": state["usd"],
        "pln": state["pln"],
        "history": list(state["history"])
    }

    price = indicators["current_price"]
    fee = 0.05

    if action == "BUY" and state["usd"] > fee:
        amount = (state["usd"] - fee) / price
        state["pln"] += amount
        state["usd"] = 0
    elif action == "SELL" and state["pln"] > 0:
        state["usd"] += state["pln"] * price - fee
        state["pln"] = 0

    state["history"].append(action)
    return state

