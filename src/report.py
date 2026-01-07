import json

with open("state.json") as f:
    state = json.load(f)

with open("data/indicators.json") as f:
    ind = json.load(f)

total_value = state["usd"] + state["pln"] * ind["current_price"]

html = f"""
<html>
<head><title>USD/PLN Bot</title></head>
<body>
<h1>USD/PLN Trading Bot</h1>

<p><b>Last action:</b> {state.get("last_action")}</p>
<p><b>USD:</b> {state["usd"]:.2f}</p>
<p><b>PLN:</b> {state["pln"]:.2f}</p>
<p><b>Total value (USD):</b> {total_value:.2f}</p>

<h2>Indicators</h2>
<pre>{json.dumps(ind, indent=2)}</pre>

</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)

print("Report generated")

