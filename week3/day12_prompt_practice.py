"""
Prompt engineering practice
---------------------------
Try three system prompts from the lesson:
  1. Kamau Stores customer service assistant
  2. Message classifier (few-shot)
  3. Order extractor (JSON output)

Usage:
    python week3/day12_prompt_practice.py

Requires ANTHROPIC_API_KEY in the .env file in the project root.
"""

import json
import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-5-5"

STORE_PROMPT = """You are a customer service assistant for Kamau Stores,
a wholesale distributor in Nairobi.

Your rules:
- Only answer questions about orders, pricing, and delivery
- All prices are in KES. Never mention USD.
- Delivery covers Nairobi, Mombasa, Kisumu, and Nakuru only
- You have no price list. Never state or guess a price.
- If a question is outside your scope, say: "Please call our office
  on 0799 660 888 for that."
- Always be polite and professional. End with "Asante kwa kuwasiliana."
"""

CLASSIFIER_PROMPT = """You classify customer messages as: ORDER, COMPLAINT, or INQUIRY.

Examples:
User: "I need 50 bags of maize flour"
Answer: ORDER

User: "My delivery was 2 days late and items were damaged"
Answer: COMPLAINT

User: "Do you stock Pembe flour?"
Answer: INQUIRY

Reply with only the category. No explanation."""

ORDER_PROMPT = """Extract the order details from the customer message.
Return ONLY valid JSON in this format:
{"product": "...", "quantity": ..., "urgency": "normal" or "urgent"}
No explanation. No markdown. Just the JSON."""

PROMPTS = {
    "1": ("Kamau Stores assistant", STORE_PROMPT),
    "2": ("Message classifier", CLASSIFIER_PROMPT),
    "3": ("Order extractor", ORDER_PROMPT),
}


def get_text(message):
    return "".join(b.text for b in message.content if b.type == "text").strip()


def ask(client, system_prompt, user_message):
    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
    except anthropic.AuthenticationError:
        print("API key is wrong or expired. Check your .env file.")
    except anthropic.NotFoundError:
        print("Model not found. Check the model name in the Anthropic docs.")
    except anthropic.RateLimitError:
        print("Too many requests. Wait 60 seconds and try again.")
    except anthropic.APIConnectionError:
        print("No internet connection. Check your connection and try again.")
    except anthropic.APIStatusError as e:
        print(f"The API returned an error (status {e.status_code}). Check your billing.")
    else:
        return get_text(message)
    return None


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("No API key found. Add ANTHROPIC_API_KEY to your .env file.")
        return
    client = anthropic.Anthropic(api_key=api_key)

    print("Prompt practice")
    for key, (name, _) in PROMPTS.items():
        print(f"  {key}. {name}")
    choice = input("Choose 1, 2 or 3: ").strip()
    if choice not in PROMPTS:
        print("Please choose 1, 2 or 3.")
        return

    name, system_prompt = PROMPTS[choice]
    print(f'\n{name}. Type "quit" to exit.\n')

    while True:
        text = input("You: ").strip()
        if text.lower() in ("quit", "exit"):
            break
        if not text:
            continue

        answer = ask(client, system_prompt, text)
        if not answer:
            continue
        print(f"\nAI: {answer}")

        if choice == "3":
            try:
                print("Parsed as JSON:", json.loads(answer))
            except json.JSONDecodeError:
                print("This was NOT valid JSON, so code could not read it.")
        print()


if __name__ == "__main__":
    main()