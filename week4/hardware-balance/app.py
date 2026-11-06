"""
Customer Balance Lookup
-----------------------
A small Flask web tool for a hardware shop that sells on credit. The owner types
a customer's name and sees how much they owe.

Routes:
    /                      web page with a search form
    /api/balance?name=...  JSON balance for one customer

Run:
    python week4/hardware-balance/app.py
Then open http://127.0.0.1:5000
"""

from flask import Flask, jsonify, render_template, request

SHOP_NAME = "Eldoret Hardware"
MAX_NAME_LENGTH = 60

CUSTOMER_LIST = [
    ("Kiprop Rotich", 12500),
    ("Chebet Koech", 0),
    ("Wanjiru Njoroge", 4800),
    ("Emmanuel Wafula", 31250),
    ("Faith Jepkemboi", 8900),
    ("Hassan Abdi", 2150),
]

app = Flask(__name__)


def normalise(name):
    """Lower-case a name and collapse extra spaces, so matching ignores them."""
    return " ".join(str(name).split()).lower()


CUSTOMERS = {
    normalise(name): {"name": name, "balance": balance} for name, balance in CUSTOMER_LIST
}


def json_response(payload, status=200):
    response = jsonify(payload)
    response.status_code = status
    response.headers["Cache-Control"] = "no-store"  # do not keep balances in the browser cache
    return response


@app.route("/")
def home():
    return render_template("index.html", shop_name=SHOP_NAME)


@app.route("/api/balance")
def balance():
    name = normalise(request.args.get("name", ""))

    if not name:
        return json_response(
            {"error": "Please give a customer name, for example /api/balance?name=Kiprop Rotich"}, 400
        )
    if len(name) > MAX_NAME_LENGTH:
        return json_response({"error": f"Names are limited to {MAX_NAME_LENGTH} characters."}, 400)

    customer = CUSTOMERS.get(name)
    if customer is None:
        return json_response(
            {"error": f"No customer found with the exact name '{name}'. Check the spelling."}, 404
        )

    return json_response(
        {"customer": customer["name"], "balance_kes": customer["balance"], "currency": "KES"}
    )


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return json_response({"error": "That API route does not exist"}, 404)
    return "Page not found", 404


if __name__ == "__main__":
    # Bound to this computer only. debug=True is for learning: turn it off before any deployment.
    app.run(host="127.0.0.1", port=5000, debug=True)