# Egg Production Tracker API

A small REST API for a poultry farmer with three sheds. He logs each shed's daily egg count and reads the totals at the end of the week, instead of adding up WhatsApp messages by hand.

## Endpoints
Both need the header `X-API-Key`.

| Method | URL | What it does |
|---|---|---|
| POST | `/api/eggs` | Log a day's count: `{"shed": "Shed A", "date": "2026-11-02", "count": 420}` |
| GET | `/api/eggs` | All records, each with a running total, plus the grand total and totals by shed |
| GET | `/api/eggs?from=2026-11-02&to=2026-11-08` | The same, for one week |

Errors return JSON with a message: 400 (bad data), 401 (wrong key), 404, 405, and 409 (a record for that shed and date already exists).

## Setup
1. Install Python 3.
2. Install the libraries:
   ```bash
   pip install flask python-dotenv requests
   ```
3. Create a `.env` file in the project root with a long random key:
   ```
   EGGS_API_KEY=your_key_here
   ```

## Run
```bash
python week4/egg-tracker/app.py
```
In a second terminal, run the checks:
```bash
python week4/egg-tracker/test_api.py
```

## Example response
```
--- Valid records ---
[ok  ] Shed A yesterday: expected 201, got 201
       {"count":420,"date":"2026-11-08","id":1,"shed":"Shed A"}
[ok  ] Shed B yesterday: expected 201, got 201
       {"count":385,"date":"2026-11-08","id":2,"shed":"Shed B"}
[ok  ] Shed A today: expected 201, got 201
       {"count":410,"date":"2026-11-09","id":3,"shed":"Shed A"}
[ok  ] Shed B today: expected 201, got 201
       {"count":395,"date":"2026-11-09","id":4,"shed":"Shed B"}
[ok  ] Zero eggs is valid (Shed C): expected 201, got 201
       {"count":0,"date":"2026-11-09","id":5,"shed":"Shed C"}
```

## Limits
- Records are kept in memory and are lost when the server stops. A real deployment needs a database.
- The shed names in `app.py` are examples. Replace them with the farmer's real names.
- A farmer cannot use an API directly. He needs a simple page or chat front end on top.
- There is no way yet to correct or delete a wrong record.
- One shared API key, with no individual logins. It travels unencrypted unless the server uses HTTPS.
- The built-in Flask server is for development only.

## Price
- **Build and deploy:** KES 30,000 one-off. Includes the API, saving records permanently in a database (not just in memory), a simple weekly-summary page, deployment, and a one-hour handover.
- **Monthly:** KES 2,500. Includes hosting, daily backups, and support within 2 working days.