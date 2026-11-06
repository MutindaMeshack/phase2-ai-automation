"""
Flask practice (Day 16)
-----------------------
Routes, JSON, URL parameters, status codes and one POST route for a fictional
Kamau Stores.

Run:
    python week4/day16_flask_practice.py
Then open http://127.0.0.1:5000
Stop the server with Ctrl+C.
"""

from flask import Flask, jsonify, request
from markupsafe import escape

app = Flask(__name__)

inventory = {
    "maize flour": {"price": 2800, "stock": 120},
    "wheat flour": {"price": 3200, "stock": 85},
    "rice": {"price": 4500, "stock": 200},
    "cooking oil": {"price": 1800, "stock": 45},
}
orders = []  # kept in memory only: it is cleared when the server restarts


@app.route("/")
def home():
    return "Kamau Stores API is running."


@app.route("/products")
def products():
    return "Maize flour, wheat flour, rice, cooking oil"


@app.route("/products/<name>")
def product_detail(name):
    # escape() stops a typed name from running as HTML or a script
    return f"You asked about: {escape(name)}"


@app.route("/api/products")
def get_products():
    max_price = request.args.get("max_price")
    items = inventory
    if max_price is not None:
        try:
            limit = int(max_price)
        except ValueError:
            return jsonify({"error": "max_price must be a whole number, for example 3000"}), 400
        items = {name: item for name, item in inventory.items() if item["price"] <= limit}
    return jsonify(items)


@app.route("/api/products/<product_name>")
def get_product(product_name):
    key = product_name.strip().lower()
    if key not in inventory:
        return jsonify({"error": f"Product '{product_name}' not found"}), 404
    return jsonify({**inventory[key], "name": key})  # a copy: inventory is not changed


@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": 'Send JSON like {"product": "rice", "quantity": 5}'}), 400

    product = str(data.get("product", "")).strip().lower()
    quantity = data.get("quantity")
    if product not in inventory:
        return jsonify({"error": f"Product '{product}' not found"}), 404
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        return jsonify({"error": "quantity must be a whole number of 1 or more"}), 400

    order = {
        "id": len(orders) + 1,
        "product": product,
        "quantity": quantity,
        "total": inventory[product]["price"] * quantity,
    }
    orders.append(order)
    return jsonify(order), 201


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "That API route does not exist"}), 404
    return "Page not found", 404


if __name__ == "__main__":
    # Bound to this computer only. debug=True is for learning: turn it off before any deployment.
    app.run(host="127.0.0.1", port=5000, debug=True)