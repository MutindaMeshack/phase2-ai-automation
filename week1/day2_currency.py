import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("EXCHANGE_API_KEY")
if not api_key:
    print("No API key found. Check EXCHANGE_API_KEY in your .env file.")
    raise SystemExit(1)

base = input("Convert from (e.g. USD): ").strip().upper()
target = input("Convert to (e.g. KES): ").strip().upper()
amount_text = input("Amount: ").strip()

try:
    amount = float(amount_text)
except ValueError:
    print("Amount must be a number, for example 100 or 25.5")
    raise SystemExit(1)

url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base}/{target}/{amount}"

try:
    response = requests.get(url, timeout=10)
except requests.exceptions.RequestException:
    print("Could not connect. Check your internet and try again.")
    raise SystemExit(1)

try:
    data = response.json()
except ValueError:
    data = {}

error_type = data.get("error-type")

if response.status_code == 200 and data.get("result") == "success":
    rate = data["conversion_rate"]
    result = data["conversion_result"]
    print("\n=== Currency Conversion ===")
    print(f"Amount:   {amount:,.2f} {base}")
    print(f"Rate:     1 {base} = {rate:,.4f} {target}")
    print(f"Result:   {result:,.2f} {target}")
elif error_type == "invalid-key":
    print("Invalid API key. Check EXCHANGE_API_KEY in your .env file.")
elif error_type == "unsupported-code":
    print(f"Unsupported currency code: {base} or {target}. Use codes like USD, KES, EUR.")
elif error_type == "quota-reached" or response.status_code == 429:
    print("Request limit reached. Wait before trying again.")
elif error_type == "inactive-account":
    print("Account not active. Confirm your email address first.")
elif response.status_code >= 500:
    print("Server error on their side. Try again later.")
else:
    print(f"Unexpected error. Status: {response.status_code}, type: {error_type}")