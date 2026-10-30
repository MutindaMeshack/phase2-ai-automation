"""
First AI API call
-----------------
Asks Claude a question and prints the answer with token usage.

Usage:
    python week3/day11_first_call.py

Requires ANTHROPIC_API_KEY in the .env file in the project root.
"""

import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-5-5"
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("No API key found. Add ANTHROPIC_API_KEY to your .env file.")
    raise SystemExit(1)

client = anthropic.Anthropic(api_key=api_key)

question = input("Ask me anything: ").strip()
if not question:
    print("No question entered.")
    raise SystemExit(1)

try:
    message = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": question}],
    )
except anthropic.AuthenticationError:
    print("API key is wrong or expired. Check your .env file.")
    raise SystemExit(1)
except anthropic.NotFoundError:
    print("Model not found. Check the model name in the Anthropic docs.")
    raise SystemExit(1)
except anthropic.RateLimitError:
    print("Too many requests. Wait 60 seconds and try again.")
    raise SystemExit(1)
except anthropic.APIConnectionError:
    print("No internet connection. Check your connection and try again.")
    raise SystemExit(1)
except anthropic.APIStatusError as e:
    print(f"The API returned an error (status {e.status_code}). Check your billing and credit balance.")
    raise SystemExit(1)

print("\nAnswer:", message.content[0].text)
if message.stop_reason == "max_tokens":
    print("(The answer was cut off. Raise max_tokens if you need more.)")
print(f"\nTokens used: {message.usage.input_tokens} in, {message.usage.output_tokens} out")