# Phase II: AI Automation

My work from the AI Masterclass 2 program (Automate and Monetize AI Skills).

## Projects

### Travel Weather Tool (Week 1, Day 3)
**The problem:** A traveller wants the weather and basic country facts for a city in one place, instead of checking several sites.

**What it does:** Takes a city name, fetches live weather (OpenWeatherMap), then uses the country code from that result to fetch country details (REST Countries v5): region, population and currency. It prints a clean summary and saves the data to a JSON file.


## Progress
- **Week 1, Day 1:** What APIs are, first API call with Python `requests` (Open-Meteo weather)
- **Week 1, Day 2:** API keys, `.env` files, error handling (OpenWeatherMap, ExchangeRate-API)
- **Week 1, Day 3:** Command-line tool chaining two APIs, saving responses to JSON

## Setup
```bash
pip install requests python-dotenv
```

Create a `.env` file in the project root (see `.env.example`):
```
OPENWEATHER_API_KEY=your_key_here
EXCHANGE_API_KEY=your_key_here
COUNTRIES_API_KEY=your_key_here
```
Free keys: openweathermap.org, exchangerate-api.com, restcountries.com

## Run
```bash
python week1/day1_weather.py
python week1/day2_weather.py
python week1/day2_currency.py
python week1/day3_travel_info.py
python week1/day3_load_saved.py
```