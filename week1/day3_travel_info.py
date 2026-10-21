"""
Travel Weather Tool
-------------------
Shows live weather and country information for any city.
Chains two APIs: OpenWeatherMap (weather) and REST Countries v5 (country data).
Saves each result to week1/saved/ as a JSON file.

Usage:
    python week1/day3_travel_info.py

Requirements:
    pip install requests python-dotenv
    A .env file in the project root containing:
        OPENWEATHER_API_KEY=your_key
        COUNTRIES_API_KEY=your_key
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

weather_key = os.getenv("OPENWEATHER_API_KEY")
countries_key = os.getenv("COUNTRIES_API_KEY")

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saved")


def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": weather_key, "units": "metric"}
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException:
        print("Could not connect to the weather service. Check your internet.")
        return None

    if response.status_code == 200:
        return response.json()
    if response.status_code == 401:
        print("Weather API key is invalid or not active. Check .env.")
    elif response.status_code == 404:
        print(f"City '{city}' not found. Check the spelling.")
    elif response.status_code == 429:
        print("Too many weather requests. Wait and try again.")
    else:
        print(f"Weather service error: {response.status_code}")
    return None


def get_country_info(country_code):
    url = f"https://api.restcountries.com/countries/v5/codes.alpha_2/{country_code}"
    params = {"response_fields": "names.common,region,population,currencies"}
    headers = {"Authorization": f"Bearer {countries_key}"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        print("Could not reach the country data service.")
        return None

    if response.status_code == 200:
        objects = response.json().get("data", {}).get("objects", [])
        return objects[0] if objects else None
    if response.status_code == 401:
        print("Country API key is invalid. Check COUNTRIES_API_KEY in .env.")
    elif response.status_code == 403:
        print("Country API limit reached or account frozen.")
    elif response.status_code == 429:
        print("Too many country requests. Wait and try again.")
    else:
        print(f"Country service error: {response.status_code}")
    return None


def format_currencies(raw):
    if isinstance(raw, dict):
        return ", ".join(raw.keys())
    if isinstance(raw, list):
        parts = []
        for item in raw:
            if isinstance(item, dict):
                parts.append(str(item.get("code") or item.get("name") or item))
            else:
                parts.append(str(item))
        return ", ".join(parts)
    return str(raw) if raw else "Unknown"


def save_to_file(city, weather_data, country_data):
    os.makedirs(SAVE_DIR, exist_ok=True)
    filename = city.strip().lower().replace(" ", "_") + ".json"
    path = os.path.join(SAVE_DIR, filename)
    record = {
        "city": city.title(),
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "weather": weather_data,
        "country": country_data,
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        print(f"\nData saved to week1/saved/{filename}")
    except OSError:
        print("\nCould not save the data file.")


def run_tool():
    if not weather_key:
        print("No weather key found. Check OPENWEATHER_API_KEY in your .env file.")
        return

    city = input("Enter a city name (e.g. Nairobi, Lagos): ").strip()
    if not city:
        print("No city entered.")
        return

    print(f"\nFetching data for {city}...")

    weather_data = get_weather(city)
    if not weather_data:
        return

    country_code = weather_data["sys"]["country"]

    print(f"\n=== {city.title()}, {country_code} ===")
    print(f"Temperature : {weather_data['main']['temp']}°C")
    print(f"Condition   : {weather_data['weather'][0]['description'].title()}")
    print(f"Humidity    : {weather_data['main']['humidity']}%")
    print(f"Wind        : {weather_data['wind']['speed']} m/s")

    if not countries_key:
        print("\nCountry info skipped: COUNTRIES_API_KEY not found in .env.")
        save_to_file(city, weather_data, None)
        return

    country_data = get_country_info(country_code)

    if country_data:
        population = country_data.get("population")
        population_text = f"{population:,}" if isinstance(population, (int, float)) else "N/A"
        region = country_data.get("region", "Unknown")
        currencies = format_currencies(country_data.get("currencies"))

        print("\n=== Country Info ===")
        print(f"Region      : {region}")
        print(f"Population  : {population_text}")
        print(f"Currency    : {currencies}")
    else:
        print("\nCountry info is not available right now.")

    save_to_file(city, weather_data, country_data)


if __name__ == "__main__":
    print("Travel Weather Tool")
    print("-------------------")
    while True:
        run_tool()
        again = input("\nSearch another city? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
        print()