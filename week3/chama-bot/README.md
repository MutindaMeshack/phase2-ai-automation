# Chama FAQ Bot

A command-line tool for a chama secretary. She types a member's question, and the bot answers from the chama's own rules (contributions, meeting schedule, fines, loans, welfare). If the answer is not in the rules, it says so and points to the right official.

## What it does
- Answers from a knowledge base file that the secretary can edit, with no coding
- Says "I do not have that information" instead of guessing
- Never gives balances or loan status (it has no member records) and never waives fines
- Answers in English or Swahili

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
Interactive:
```bash
python week3/chama-bot/chama_bot.py
```
One question:
```bash
python week3/chama-bot/chama_bot.py "When is the next meeting?"
```

## Changing the rules
Open `knowledge_base.md`, edit the text, and save it. No code changes are needed. The demo file contains invented data.

## Example interaction
```
PowerLeaders Chama FAQ Bot. Type the member's question, or 'exit' to quit.

Question: How much do I pay every month and by when?

Each member contributes KES 2,000 per month, due by the 5th of the month. You can pay by M-Pesa to the chama paybill (the treasurer will give you the number) or in cash to the treasurer at the meeting.

[1262 tokens in, 74 out]
Question: Who can take a loan, and how much interest?

Here is what the chama rules say:

**Who can apply:** A member can apply for a loan after 6 months of membership, with no more than 1 late contribution in the last 6 months. Each loan needs one guarantor, who must be another member.

**Interest:** The interest is 10% flat, and the loan must be repaid within 3 months. The maximum loan is 3 times the member's total savings.

To apply, contact the treasurer. The committee decides at the monthly meeting.

[1264 tokens in, 154 out]
Question: quit
Goodbye!
```

## Cost
Each question sends the whole knowledge base plus the question, and Claude sends an answer back. The tool prints the token counts. With the Claude Haiku 5.5 prices (USD 0.10 per million input tokens and 0.50 per million output tokens, as listed in Anthropic's docs when this was written), my test runs cost: [FILL IN FROM YOUR OWN TOKEN COUNTS]. A longer knowledge base costs more on every question.

## Limits
- It answers only from the knowledge base. It can be wrong, so the secretary should check anything important.
- The wording can differ from run to run.
- It has no member records and does not remember earlier questions.
- The knowledge base is sent to the Claude API with every question. Do not put member names, phone numbers or balances in it.
- Knowledge bases longer than about 20,000 characters need a different approach (retrieval).