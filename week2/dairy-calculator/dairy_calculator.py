"""
Dairy Co-op Payment Calculator
-------------------------------
A farmer enters their name and the litres they supplied. The tool shows
the total amount owed at the current buying price.

Usage:
    python week2/dairy-calculator/dairy_calculator.py

Weekly price update:
    Open price.txt (in the same folder as this script), replace the number
    with the new price per litre in KES, and save the file.
"""

import math
import os

PRICE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "price.txt")


def get_current_price():
    """Read the price per litre from price.txt. Returns None if it is missing or invalid."""
    try:
        with open(PRICE_FILE, "r") as f:
            price = float(f.read().strip())
    except FileNotFoundError:
        print("price.txt was not found. Ask the manager to create it with the current price.")
        return None
    except ValueError:
        print("price.txt must contain only a number, for example 55")
        return None

    if not math.isfinite(price) or price <= 0:
        print("The price in price.txt must be greater than zero.")
        return None
    return price


def calculate_payment(litres, price_per_litre):
    return litres * price_per_litre


def read_litres():
    text = input("Litres supplied today: ").strip().replace(",", "")
    try:
        litres = float(text)
    except ValueError:
        print("Please enter a number for litres, for example 12.5")
        return None
    if not math.isfinite(litres) or litres <= 0:
        print("Litres must be greater than zero.")
        return None
    return litres


def main():
    print("Kiambu Dairy Co-op Payment Calculator")
    print("--------------------------------------")

    price = get_current_price()
    if price is None:
        return

    print(f"Current buying price: KES {price:,.2f} per litre\n")

    name = input("Farmer name: ").strip()
    if not name:
        print("Name is required.")
        return

    litres = read_litres()
    if litres is None:
        return

    total = calculate_payment(litres, price)

    print()
    print(f"Farmer : {name}")
    print(f"Litres : {litres:,.2f}")
    print(f"Price  : KES {price:,.2f} per litre")
    print(f"Total  : KES {total:,.2f}")


if __name__ == "__main__":
    main()