# Phase II: AI Automation

My work from the AI Masterclass 2 program (Automate and Monetize AI Skills).

## Progress
- **Week 1, Day 1:** What APIs are, first API call with Python `requests` (Open-Meteo weather)
- **Week 1, Day 2:** API keys, `.env` files, error handling (OpenWeatherMap, ExchangeRate-API)

## Setup
```bash
pip install requests python-dotenv
```

Create a `.env` file in the project root (see `.env.example`):
```
OPENWEATHER_API_KEY=your_key_here
EXCHANGE_API_KEY=your_key_here
```

## Run
```bash
python week1/day1_weather.py
python week1/day2_weather.py
python week1/day2_currency.py
```