# Phase II: AI Automation

My work from the AI Masterclass 2 program (Automate and Monetize AI Skills).

## Projects

### Travel Weather Tool (Week 1, Day 3)
**The problem:** A traveller wants the weather and basic country facts for a city in one place, instead of checking several sites.

**What it does:** Takes a city name, fetches live weather (OpenWeatherMap), then uses the country code from that result to fetch country details (REST Countries v5): region, population and currency. It prints a clean summary and saves the data to a JSON file.

### Country Info Web Page (Week 1, Day 4)
**The problem:** Data from an API is useless to most people unless it appears on a page they can read.

**What it does:** A browser page where you type a country and see live results. It uses JavaScript `fetch()` with `async/await`, shows a "Loading..." state while waiting, and shows a clear error message if the search fails.

## Progress
- **Week 1, Day 1:** What APIs are, first API call with Python `requests` (Open-Meteo weather)
- **Week 1, Day 2:** API keys, `.env` files, error handling (OpenWeatherMap, ExchangeRate-API)
- **Week 1, Day 3:** Command-line tool chaining two APIs, saving responses to JSON
- **Week 1, Day 4:** Fetch API in JavaScript, async/await, loading and error states in the browser

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
start week1/day4_fetch.html
```