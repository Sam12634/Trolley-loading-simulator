from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# In-memory state
STATE = {
    "stations": ["Depot", "Warehouse", "Market"],
    "current_station_index": 0,
    "trolley": {
        "capacity": 10,
        "cargo": 0
    }
}

# Serve the HTML page
@app.route("/")
def home():
    return render_template("index.html")

# API: Get current state
@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(STATE)

# API: Move to next or previous station
@app.route("/move", methods=["POST"])
def move():
    data = request.get_json(force=True)
    direction = data.get("direction", "next")
    if direction == "next":
        STATE["current_station_index"] = (STATE["current_station_index"] + 1) % len(STATE["stations"])
    elif direction == "prev":
        STATE["current_station_index"] = (STATE["current_station_index"] - 1) % len(STATE["stations"])
    return jsonify(STATE)

# API: Load cargo
@app.route("/load", methods=["POST"])
def load():
    data = request.get_json(force=True)
    amount = int(data.get("amount", 1))
    trolley = STATE["trolley"]
    trolley["cargo"] = min(trolley["capacity"], trolley["cargo"] + amount)
    return jsonify(STATE)

# API: Unload cargo
@app.route("/unload", methods=["POST"])
def unload():
    data = request.get_json(force=True)
    amount = int(data.get("amount", 1))
    trolley = STATE["trolley"]
    trolley["cargo"] = max(0, trolley["cargo"] - amount)
    return jsonify(STATE)

if __name__ == "__main__":
    app.run(debug=True)
