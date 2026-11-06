# Customer Balance Lookup

A small web tool for a hardware shop that sells on credit. The owner types a customer's name and sees how much they owe, instead of searching through a notebook.

## What it does
- A web page with a search box (`/`)
- A JSON API (`/api/balance?name=...`) that returns one customer's balance
- Clear messages for a missing name (400) or an unknown customer (404)

## Setup
1. Install Python 3.
2. Install Flask:
   ```bash
   pip install flask
   ```

## Run
```bash
python week4/hardware-balance/app.py
```
Open http://127.0.0.1:5000 in your browser. Press Ctrl+C in the terminal to stop it.

## Example
Page: type `Kiprop Rotich` and press Search.

API:
```
{
  "balance_kes": 12500,
  "currency": "KES",
  "customer": "Kiprop Rotich"
}
```

## Limits
- All customers and balances are fictional demo data, kept in a Python dictionary. Balances are not saved or edited anywhere yet.
- There is no login. Run it only on the owner's computer.
- Customers are found by exact full name, so two customers with the same name would need an ID or phone number.
- The built-in Flask server is for development. A real deployment needs a proper server, HTTPS and a login.
- Customer debts are personal information. The shop owner should check their data-protection obligations (I am not a lawyer).

## Price
PRICE LINE GOES HERE