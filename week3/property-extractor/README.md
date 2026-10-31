# Property Inquiry Extractor

A command-line tool for a Nairobi property agent. It reads a raw WhatsApp inquiry and extracts the key details into clean fields, so the agent no longer copies them into a spreadsheet by hand.

## What it extracts, and why each field matters

| Field | Why it matters |
|---|---|
| `property_type` | Decides which listings to show. A bedsitter and a house are completely different stock. |
| `bedrooms` | Matches size to the client's needs. A bedsitter or studio counts as 0. |
| `location` | The area drives both price and availability, so it is the first filter an agent applies. |
| `budget_kes` | Qualifies the lead and filters listings. Stored as a number (80000, not "80k") so it can be sorted in a spreadsheet. |
| `rental_or_sale` | Rentals and sales are separate listings with different processes and commissions. |

Anything the client did not say is shown as "Not specified", and the tool lists what to ask them next. It never guesses.

## Setup
1. Install Python 3.
2. Install the libraries:
   ```bash
   pip install anthropic python-dotenv
   ```
3. Get an API key from the Anthropic Console.
4. Create a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

## Usage
```bash
python week3/property-extractor/extract_inquiry.py
```
Paste an inquiry and press Enter. Type `quit` to exit.

## Example
```
Property Inquiry Extractor
Paste an inquiry, or type "quit" to exit.

Inquiry: I am looking for a 3-bedroom house in Kileleshwa, budget around 80k per month

=== Extracted inquiry ===
Property type : house
Bedrooms      : 3
Location      : Kileleshwa
Budget        : KES 80,000
Rental/Sale   : rental

Inquiry: Do you have any bedsitters near Westlands under 20k?

=== Extracted inquiry ===
Property type : bedsitter
Bedrooms      : 0
Location      : Westlands
Budget        : KES 20,000
Rental/Sale   : Not specified

Ask the client for: rental_or_sale

Inquiry: rental

=== Extracted inquiry ===
Property type : Not specified
Bedrooms      : Not specified
Location      : Not specified
Budget        : Not specified
Rental/Sale   : rental

Ask the client for: property_type, bedrooms, location, budget_kes

Inquiry: Hi, are you still available?

=== Extracted inquiry ===
Property type : Not specified
Bedrooms      : Not specified
Location      : Not specified
Budget        : Not specified
Rental/Sale   : Not specified

Ask the client for: property_type, bedrooms, location, budget_kes, rental_or_sale

Inquiry: quit 
Goodbye!
```

## How it works
A system prompt tells the model which five fields to return as JSON, gives three examples, and says to use `null` for anything missing. The code then validates the reply before showing it, because AI output cannot be trusted blindly.

## Limits
- The messages in this repo are invented. Real client messages contain personal details and are sent to the Claude API, so the agent should be comfortable with that.
- The tool can still make mistakes. Check the output before relying on it.
- It handles one message at a time and does not save to a spreadsheet yet.
- A customer message cannot change the tool's rules, but no prompt is perfectly safe against manipulation.