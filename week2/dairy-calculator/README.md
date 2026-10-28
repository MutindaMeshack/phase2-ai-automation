# Dairy Co-op Payment Calculator

A simple tool for a dairy co-op. A farmer enters their name and the litres of milk they supplied, and the tool shows how much the co-op owes them at the current buying price.

## Setup
1. Install Python 3 from python.org (one time only).
2. Download this project.

## Updating the weekly price
Open `price.txt`, replace the number with the new price per litre in KES, and save. Nothing else needs to change.

## Usage
```bash
python week2/dairy-calculator/dairy_calculator.py
```

## Example output
```
Kiambu Dairy Co-op Payment Calculator
--------------------------------------
Current buying price: KES 55.00 per litre

Farmer name: Meshack
Litres supplied today: 279

Farmer : Meshack
Litres : 279.00
Price  : KES 55.00 per litre
Total  : KES 15,345.00
```

## Notes
- If `price.txt` is missing or does not contain a valid number, the tool shows a message and stops, so nobody is paid at the wrong price.
- The tool does not keep a history of payments.