"""
REST API practice (Day 17)
--------------------------
An orders API for a wholesaler. Every route needs an X-API-Key header.
All data is invented and kept in memory (it resets when the server restarts).

Run:
    python week4/day17_orders_api.py
Stop the server with Ctrl+C.

Requires ORDERS_API_KEY in the .env file in the project root.
"""

import hmac
import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

API_KEY = os.getenv("ORDERS_API_KEY")
if not API_KEY:
    raise SystemExit("Add ORDERS_API_KEY to your .env file (see the roadmap for how to make one).")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10_000  # reject very large request bodies

ORDER_STATUSES = {"pending", "delivered", "cancelled"}

orders = [
    {"id": 1, "customer": "Hassan Traders", "product": "maize flour", "qty": 50, "status": "pending"},
    {"id": 2, "customer": "Otieno Wholesale", "product": "rice", "qty": 30, "status": "delivered"},
]
next_id = 3  # only ever goes up, so an ID is never reused


def fail(message, status):
    return jsonify({"error": message}), status


def require_api_key(view):
    @wraps(view)  # keeps each route's function name unique, which Flask needs
    def wrapper(*args, **kwargs):
        supplied = request.headers.get("X-API-Key", "")
        if not hmac.compare_digest(supplied.encode("utf-8"), API_KEY.encode("utf-8")):
            return fail("Invalid or missing API key", 401)
        return view(*args, **kwargs)

    return wrapper


def clean_text(value, max_length=60):
    """Return tidy text, or None if it is not text or is empty or too long."""
    if not isinstance(value, str):
        return None
    text = " ".join(value.split())
    return text if 0 < len(text) <= max_length else None


def find_order(order_id):
    return next((o for o in orders if o["id"] == order_id), None)


@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(413)
def http_error(error):
    return jsonify({"error": error.description}), error.code


@app.route("/api/orders", methods=["GET"])
@require_api_key
def get_orders():
    return jsonify(orders)


@app.route("/api/orders", methods=["POST"])
@require_api_key
def create_order():
    global next_id
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return fail('Send JSON like {"customer": "Baraka Stores", "product": "sugar", "qty": 20}', 400)

    customer = clean_text(data.get("customer"))
    product = clean_text(data.get("product"))
    if customer is None or product is None:
        return fail("customer and product are required (text, up to 60 characters)", 400)

    qty = data.get("qty", 1)
    if isinstance(qty, bool) or not isinstance(qty, int) or not 1 <= qty <= 100000:
        return fail("qty must be a whole number from 1 to 100000", 400)

    order = {"id": next_id, "customer": customer, "product": product, "qty": qty, "status": "pending"}
    next_id += 1
    orders.append(order)
    return jsonify(order), 201


@app.route("/api/orders/<int:order_id>", methods=["GET"])
@require_api_key
def get_order(order_id):
    order = find_order(order_id)
    if order is None:
        return fail("Order not found", 404)
    return jsonify(order)


@app.route("/api/orders/<int:order_id>/status", methods=["PUT"])
@require_api_key
def update_status(order_id):
    order = find_order(order_id)
    if order is None:
        return fail("Order not found", 404)

    data = request.get_json(silent=True)
    status = data.get("status") if isinstance(data, dict) else None
    if not isinstance(status, str) or status not in ORDER_STATUSES:
        return fail("status must be one of: " + ", ".join(sorted(ORDER_STATUSES)), 400)

    order["status"] = status
    return jsonify(order)


@app.route("/api/orders/<int:order_id>", methods=["DELETE"])
@require_api_key
def delete_order(order_id):
    order = find_order(order_id)
    if order is None:
        return fail("Order not found", 404)
    orders.remove(order)
    return jsonify({"deleted": order_id})


if __name__ == "__main__":
    # Bound to this computer only. debug=True is for learning: never use it on a public server.
    app.run(host="127.0.0.1", port=5000, debug=True)