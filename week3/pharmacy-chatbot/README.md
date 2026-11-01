# Kisumu Pharmacy Chatbot

A command-line chatbot that helps pharmacy staff answer the same customer questions consistently: opening hours, services, how long prescriptions take, and what to bring for a repeat prescription. It remembers what was said earlier in the conversation.

## What it does
- Answers from the pharmacy's facts, which are written into the system prompt
- Remembers earlier turns, so "how long will it take?" refers to the prescription mentioned before
- Never gives medical advice, never confirms prescription stock, and sends emergencies to 999 or 112
- Saves each conversation to a log file

## Setup
1. Install Python 3.
2. Install the libraries:
   ```bash
   pip install anthropic python-dotenv
   ```
3. Create a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

## Usage
```bash
python week3/pharmacy-chatbot/pharmacy_chatbot.py
```
Type a question. Type `exit` to quit.

## Example conversation
```
Kisumu Pharmacy Assistant (demo). Type 'exit' to quit.

You: What time do you open on Sunday?

Assistant: We open on Sundays at 10am and close at 4pm.
[662 tokens in, 21 out]

You: Do you have paracetamol?

Assistant: Yes, paracetamol is usually kept on our shelves. Our staff will still check the shelf for you when you visit, so it's best to come in or ask at the counter to confirm it's available.
[695 tokens in, 62 out]

You: What’s the weather in Kisumu?

Assistant: I'm sorry, I don't have information about the weather. For that, you could check a weather app or local news. If you need anything from the pharmacy, I'm happy to help with that.
[772 tokens in, 56 out]

You: quit
Conversation saved.
```

## How the memory works
The model has no memory between calls. The script keeps the conversation in a list and sends the recent part with every question. Only the last 9 messages are sent, to keep costs down, so very old details are forgotten.

## Limits
- The pharmacy facts here are invented demo data. The real pharmacy must replace them.
- The chatbot is not a pharmacist. Staff should check anything important.
- Conversations are sent to the Claude API. Logs may contain health information, so they are kept on the local computer and are not committed to Git. The pharmacy should check its data-protection obligations (I am not a lawyer).
- The bot cannot check real stock levels.