"""
Egg Production Tracker (web page + API)
---------------------------------------
A poultry farmer's manager logs in, records the eggs collected from each shed
each day, and sees all records and totals on one page, without reloading it.

Pages:
    /login       password form
    /            the tracker page (needs login)
API (needs a login session OR an X-API-Key header):
    POST /api/eggs   {"shed": "Shed A", "date": "2026-11-02", "count": 420}
    GET  /api/eggs   all records with running totals
                     Optional filters: ?from=2026-11-02&to=2026-11-08

Run:
    python week4/egg-tracker/app.py
Then open http://127.0.0.1:5000. Stop the server with Ctrl+C.

Requires in the .env file in the project root:
    EGGS_API_KEY, EGGS_ADMIN_PASSWORD, FLASK_SECRET_KEY
Records are kept in memory and are lost when the server stops.
The shed names below are examples: replace them with the farmer's real names.
"""

import hmac
import os
import re
import time
from datetime import date
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

load_dotenv()

API_KEY = os.getenv("EGGS_API_KEY")
ADMIN_PASSWORD = os.getenv("EGGS_ADMIN_PASSWORD")
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

missing = [
    name
    for name, value in (
        ("EGGS_API_KEY", API_KEY),
        ("EGGS_ADMIN_PASSWORD", ADMIN_PASSWORD),
        ("FLASK_SECRET_KEY", SECRET_KEY),
    )
    if not value
]
if missing:
    raise SystemExit("Add these to your .env file: " + ", ".join(missing))

SHEDS = ["Shed A", "Shed B", "Shed C"]
MAX_COUNT = 20000

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config.update(
    MAX_CONTENT_LENGTH=10_000,  # reject very large request bodies
    SESSION_COOKIE_HTTPONLY=True,  # page JavaScript cannot read the cookie
    SESSION_COOKIE_SAMESITE="Lax",  # the cookie is not sent on cross-site POSTs
)

records = []
next_id = 1


def normalise(text):
    return " ".join(str(text).split()).lower()


SHED_LOOKUP = {normalise(name): name for name in SHEDS}


def fail(message, status):
    return jsonify({"error": message}), status


def has_access():
    """True for a logged-in browser session, or a request with the right API key."""
    if session.get("admin"):
        return True
    supplied = request.headers.get("X-API-Key", "")
    return hmac.compare_digest(supplied.encode("utf-8"), API_KEY.encode("utf-8"))


def require_access(view):
    @wraps(view)  # keeps each route's function name unique, which Flask needs
    def wrapper(*args, **kwargs):
        if not has_access():
            return fail("Not logged in, or invalid API key", 401)
        return view(*args, **kwargs)

    return wrapper


def parse_date(value):
    """Accept only YYYY-MM-DD. Returns a date, or None."""
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value.strip()):
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


@app.after_request
def no_store(response):
    response.headers["Cache-Control"] = "no-store"  # do not keep records in the browser cache
    return response


@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(413)
def http_error(error):
    return jsonify({"error": error.description}), error.code


# ---------- Pages ----------

@app.route("/")
def home():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("index.html", sheds=SHEDS)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        supplied = request.form.get("password", "")
        if hmac.compare_digest(supplied.encode("utf-8"), ADMIN_PASSWORD.encode("utf-8")):
            session.clear()
            session["admin"] = True
            return redirect(url_for("home"))
        time.sleep(1)  # slows down password guessing
        error = "Wrong password."
    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- API ----------

@app.route("/api/eggs", methods=["POST"])
@require_access
def log_eggs():
    global next_id
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return fail('Send JSON like {"shed": "Shed A", "date": "2026-11-02", "count": 420}', 400)

    shed = SHED_LOOKUP.get(normalise(data.get("shed", "")))
    if shed is None:
        return fail("Unknown shed. Use one of: " + ", ".join(SHEDS), 400)

    day = parse_date(data.get("date"))
    if day is None:
        return fail("date must look like 2026-11-02 (year-month-day)", 400)
    if day > date.today():
        return fail("date cannot be in the future", 400)

    count = data.get("count")
    if isinstance(count, bool) or not isinstance(count, int) or not 0 <= count <= MAX_COUNT:
        return fail(f"count must be a whole number from 0 to {MAX_COUNT}", 400)

    if any(r["shed"] == shed and r["date"] == day.isoformat() for r in records):
        return fail(f"{shed} already has a record for {day.isoformat()}", 409)

    record = {"id": next_id, "shed": shed, "date": day.isoformat(), "count": count}
    next_id += 1
    records.append(record)
    return jsonify(record), 201


@app.route("/api/eggs", methods=["GET"])
@require_access
def list_eggs():
    start = end = None
    if "from" in request.args:
        start = parse_date(request.args["from"])
        if start is None:
            return fail("from must look like 2026-11-02 (year-month-day)", 400)
    if "to" in request.args:
        end = parse_date(request.args["to"])
        if end is None:
            return fail("to must look like 2026-11-02 (year-month-day)", 400)
    if start and end and start > end:
        return fail("from must not be later than to", 400)

    rows = [
        r for r in records
        if (start is None or r["date"] >= start.isoformat())
        and (end is None or r["date"] <= end.isoformat())
    ]
    rows.sort(key=lambda r: (r["date"], r["id"]))

    running = 0
    output = []
    by_shed = {}
    for r in rows:
        running += r["count"]
        output.append({**r, "running_total": running})
        by_shed[r["shed"]] = by_shed.get(r["shed"], 0) + r["count"]

    return jsonify({
        "records": output,
        "record_count": len(output),
        "total_eggs": running,
        "totals_by_shed": by_shed,
    })


if __name__ == "__main__":
    # Bound to this computer only. Debug mode is off because this app holds a password and data.
    app.run(host="127.0.0.1", port=5000, debug=False)