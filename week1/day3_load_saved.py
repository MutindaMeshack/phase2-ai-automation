"""
Loads a saved travel result from week1/saved/ and prints it.
No API call is made, so it works offline and uses no quota.

Usage:
    python week1/day3_load_saved.py
Run day3_travel_info.py first so a saved file exists.
"""

import os
import json

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saved")

city = input("Saved city to load (e.g. Nairobi): ").strip().lower().replace(" ", "_")
path = os.path.join(SAVE_DIR, city + ".json")

try:
    with open(path, "r", encoding="utf-8") as f:
        record = json.load(f)
except FileNotFoundError:
    print("No saved file for that city. Run day3_travel_info.py first.")
    raise SystemExit(1)

weather = record["weather"]
print(f"\n=== {record['city']} (saved {record['saved_at']}) ===")
print(f"Temperature : {weather['main']['temp']}°C")
print(f"Humidity    : {weather['main']['humidity']}%")