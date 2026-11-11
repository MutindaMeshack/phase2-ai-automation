# Phase II: AI Automation

My work from the AI Masterclass 2 program (Automate and Monetize AI Skills).

## Live Demo
**[Egg Production Tracker](https://egg-tracker-guss.onrender.com/)**: a Flask app deployed on Render with a REST API and a password-protected web page. The free host sleeps when idle, so the first load can take about a minute. Login details are available on request.

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
- **Week 1, Day 5:** Project: [Kenyan Business Currency Tracker](week1/kes-currency-tracker), a CLI tool that converts KES to USD, EUR and GBP with live rates
- **Week 2, Days 6 to 9:** Client skills: reading briefs, writing proposals, delivering work, scope and payment terms (writing exercises)
- **Week 2, Day 10:** Full client cycle on a simulated brief: [Dairy Co-op Payment Calculator](week2/dairy-calculator) and [client messages](week2/day10_client_cycle.md)
- **Week 3, Day 11:** First AI API call with the Anthropic SDK; [SACCO Member Assistant](week3/sacco-assistant)
- **Week 3, Day 12:** Prompt engineering (system prompts, few-shot, structured JSON); [Property Inquiry Extractor](week3/property-extractor)
- **Week 3, Day 13:** Chatbot with conversation memory, rolling window, streaming and logs; [Kisumu Pharmacy Chatbot](week3/pharmacy-chatbot)
- **Week 3, Day 14:** Function calling and a tool-using agent; [Tea Harvest Weather Agent](week3/tea-harvest-agent)
- **Week 3, Day 15:** Project: [Chama FAQ Bot](week3/chama-bot), a CLI tool that answers chama members' questions from a knowledge base
- **Week 4, Day 16:** Flask basics (routes, JSON, status codes); [Customer Balance Lookup](week4/hardware-balance), a web tool for a hardware shop
- **Week 4, Day 17:** REST API with Flask (GET, POST, PUT, DELETE, API key from .env); [Egg Production Tracker API](week4/egg-tracker)
- **Week 4, Day 18:** Connecting a browser frontend to a Flask backend (fetch, loading and error states, login session); [Egg Production Tracker](week4/egg-tracker) now has a web page
- **Week 4, Day 19:** Deploying to Render with gunicorn and environment variables; the [Egg Production Tracker](https://egg-tracker-guss.onrender.com/) is live

## Setup
```bash
pip install requests python-dotenv
pip install requests python-dotenv anthropic
flask
```

Create a `.env` file in the project root (see `.env.example`):
```
OPENWEATHER_API_KEY=your_key_here
EXCHANGE_API_KEY=your_key_here
COUNTRIES_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
ORDERS_API_KEY=your_key_here
EGGS_API_KEY=your_key_here
EGGS_ADMIN_PASSWORD=your_value_here
FLASK_SECRET_KEY=your_key_here
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
python week1/kes-currency-tracker/currency_tracker.py
python week2/dairy-calculator/dairy_calculator.py
python week3/sacco-assistant/sacco_assistant.py
python week3/day12_prompt_practice.py
python week3/property-extractor/extract_inquiry.py
python week3/pharmacy-chatbot/pharmacy_chatbot.py
python week3/tea-harvest-agent/harvest_agent.py
python week3/chama-bot/chama_bot.py
python week4/day16_flask_practice.py
python week4/hardware-balance/app.py
python week4/day17_orders_api.py
python week4/egg-tracker/app.py
```

## Deployment
The egg tracker is deployed on Render from this repository (Root Directory `week4/egg-tracker`, start command `gunicorn app:app --workers 1 --bind 0.0.0.0:$PORT`). Its secrets are set in Render's Environment tab and are never in the code.