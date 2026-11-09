"""
CORS practice (Day 18)
----------------------
A tiny API on port 5000. A page served from port 8000 tries to call it.

Run:
    python week4/day18_cors_practice/api.py
"""

from flask import Flask, jsonify

# Step B: remove the # from the next two lines, save, and restart this server
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://127.0.0.1:8000"])  # one named origin, never "*"

@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from the API on port 5000"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)