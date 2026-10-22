# Kenyan Business Currency Tracker

A command-line tool that converts a price in Kenyan shillings (KES) into US dollars, euros and British pounds using live exchange rates. Built for businesses that quote clients abroad.

## The problem
Exchange rates change daily. Looking them up and calculating by hand is slow and error-prone when you are preparing a quote for a foreign client.

## How it works
1. You enter a price in KES.
2. The tool fetches live rates from ExchangeRate-API (one API call).
3. It prints the converted amounts, the rate used for each, and when the rates were last updated.

## Setup
1. Clone the repo.
2. Install the libraries:
```bash
   pip install requests python-dotenv
```
3. Get a free API key at [exchangerate-api.com](https://www.exchangerate-api.com).
4. Create a `.env` file in the project root:
```
   EXCHANGE_API_KEY=your_key_here
```

## Usage
From the project root:
```bash
python week1/kes-currency-tracker/currency_tracker.py
```

## Example output
```
PASTE YOUR REAL TERMINAL OUTPUT HERE
```

## Error handling
Handles invalid input, a bad or inactive API key, a reached request limit, server errors and no internet, with a clear message instead of a crash.

## Notes
Rates are indicative. Confirm with your bank before invoicing.