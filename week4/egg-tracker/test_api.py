"""
Tests the Egg Tracker API. Start the server first, in another terminal:
    python week4/egg-tracker/app.py
Then run:
    python week4/egg-tracker/test_api.py

The server keeps records in memory, so restart it before running this again.
"""

import os
from datetime import date, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

URL = "http://127.0.0.1:5000/api/eggs"
KEY = os.getenv("EGGS_API_KEY")
GOOD = {"X-API-Key": KEY}

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)


def send(label, expect, method="POST", headers=None, **kwargs):
    headers = GOOD if headers is None else headers
    try:
        response = requests.request(method, URL, headers=headers, timeout=10, **kwargs)
    except requests.exceptions.RequestException:
        print(f"[FAIL] {label}: could not reach the server. Is it running?")
        return None
    mark = "ok  " if response.status_code == expect else "FAIL"
    print(f"[{mark}] {label}: expected {expect}, got {response.status_code}")
    print(f"       {response.text.strip()[:300]}")
    return response


def log(shed, day, count):
    return {"shed": shed, "date": day.isoformat(), "count": count}


if not KEY:
    raise SystemExit("Add EGGS_API_KEY to your .env file.")

print("--- Valid records ---")
send("Shed A yesterday", 201, json=log("Shed A", yesterday, 420))
send("Shed B yesterday", 201, json=log("Shed B", yesterday, 385))
send("Shed A today", 201, json=log("Shed A", today, 410))
send("Shed B today", 201, json=log("Shed B", today, 395))
send("Zero eggs is valid (Shed C)", 201, json=log("Shed C", today, 0))

print("\n--- Bad data ---")
send("Duplicate shed and date", 409, json=log("Shed A", today, 100))
send("Unknown shed", 400, json=log("Shed Z", today, 100))
send("Negative count", 400, json=log("Shed C", yesterday, -5))
send("Decimal count", 400, json=log("Shed C", yesterday, 12.5))
send("Text count", 400, json=log("Shed C", yesterday, "many"))
send("Boolean count", 400, json={"shed": "Shed C", "date": yesterday.isoformat(), "count": True})
send("Bad date format", 400, json={"shed": "Shed C", "date": "02/11/2026", "count": 10})
send("Future date", 400, json=log("Shed C", tomorrow, 10))
send("Body is not JSON", 400, data="hello")

print("\n--- Security and methods ---")
send("No API key", 401, headers={}, json=log("Shed C", yesterday, 10))
send("Wrong API key", 401, headers={"X-API-Key": "wrong"}, json=log("Shed C", yesterday, 10))
send("Wrong method (DELETE)", 405, method="DELETE")

print("\n--- Reading ---")
everything = send("GET everything", 200, method="GET")
send("GET only yesterday", 200, method="GET",
     params={"from": yesterday.isoformat(), "to": yesterday.isoformat()})
send("GET with a bad date", 400, method="GET", params={"from": "tomorrow"})

if everything is not None and everything.status_code == 200:
    data = everything.json()
    print("\nChecks on the totals:")
    print("  total_eggs is 1610:", data["total_eggs"] == 1610)
    print("  Shed A is 830, Shed B is 780:", data["totals_by_shed"].get("Shed A") == 830
          and data["totals_by_shed"].get("Shed B") == 780)
    print("  last running_total is 1610:", data["records"][-1]["running_total"] == 1610)