"""
Kenyan Business Currency Tracker
--------------------------------
Problem:    A Kenyan business quoting a client abroad needs to know what a
            KES price is worth in USD, EUR and GBP right now.
Input:      A price in KES.
Processing: Fetches live rates from ExchangeRate-API (one call for all
            currencies) and converts the price.
Output:     A quote with the converted amounts, the rates used, and the
            time the rates were last updated.

Usage:
    python week1/kes-currency-tracker/currency_tracker.py

Requirements:
    pip install requests python-dotenv
    EXCHANGE_API_KEY in a .env file in the project root
"""

import math
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_CURRENCY = "KES"
TARGET_CURRENCIES = ["USD", "EUR", "GBP"]


def get_rates():
    """Fetch rates from KES to all currencies. Returns the response data, or None."""
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        print("Could not connect. Check your internet and try again.")
        return None

    try:
        data = response.json()
    except ValueError:
        data = {}

    if response.status_code == 200 and data.get("result") == "success":
        return data

    error_type = data.get("error-type")
    if error_type == "invalid-key":
        print("Invalid API key. Check EXCHANGE_API_KEY in your .env file.")
    elif error_type == "inactive-account":
        print("Account not active. Confirm your email address with ExchangeRate-API.")
    elif error_type == "quota-reached" or response.status_code == 429:
        print("Monthly request limit reached. Try again later.")
    elif response.status_code >= 500:
        print("The exchange rate service is having problems. Try again later.")
    else:
        print(f"Could not get rates (status {response.status_code}, type {error_type}).")
    return None


def read_amount():
    """Ask for a KES amount. Returns a positive number, or None if invalid."""
    text = input("Price in KES (e.g. 15000): ").strip().replace(",", "")
    try:
        amount = float(text)
    except ValueError:
        print("Please enter a number, for example 15000 or 2,500.50")
        return None
    if not math.isfinite(amount) or amount <= 0:
        print("The price must be greater than zero.")
        return None
    return amount


def print_quote(amount, data):
    rates = data["conversion_rates"]

    print(f"\n=== Quote for KES {amount:,.2f} ===")
    for code in TARGET_CURRENCIES:
        rate = rates.get(code)
        if not rate:
            print(f"{code}: rate not available")
            continue
        converted = amount * rate
        print(f"{code}  {converted:>14,.2f}   (1 {code} = {1 / rate:,.2f} KES)")

    print(f"\nRates last updated: {data.get('time_last_update_utc', 'unknown')}")
    print("Rates are indicative. Confirm with your bank before invoicing.")


def main():
    print("Kenyan Business Currency Tracker")
    print("--------------------------------")

    if not API_KEY:
        print("No API key found. Add EXCHANGE_API_KEY to your .env file.")
        return

    data = get_rates()  # one call, reused for every quote this session
    if not data:
        return

    while True:
        amount = read_amount()
        if amount is not None:
            print_quote(amount, data)
        again = input("\nQuote another price? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()