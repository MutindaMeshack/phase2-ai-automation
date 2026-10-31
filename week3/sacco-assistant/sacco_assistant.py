"""
SACCO Member Assistant
----------------------
Answers common member questions for a Matatu SACCO in Thika using Claude.
The facts the assistant may use are written in SYSTEM_PROMPT below.
All names and amounts here are FICTIONAL demo data.

Usage:
    python week3/sacco-assistant/sacco_assistant.py
Type "quit" to exit.

Requires ANTHROPIC_API_KEY in the .env file in the project root.
"""

import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-5-5"

SYSTEM_PROMPT = """You are the member assistant for Thika Matatu SACCO.
Answer members' questions in short, friendly, clear language. Reply in the
language the member writes in (English or Swahili).

Use ONLY the facts below. If the answer is not in them, say you do not have
that information and ask the member to contact the SACCO secretary.
Never guess or invent amounts, dates or rules.

FACTS
- Next meeting: Saturday 7 November 2026, 10:00 am, at the SACCO office in Thika.
- Membership fee: KES 1,000 per year.
- Monthly savings contribution: KES 2,000, due by the 5th of each month.
- Member balances as at 31 October 2026:
    Member 001, Wanjiru Kamau: KES 48,500
    Member 002, Peter Otieno: KES 31,200
    Member 003, Amina Hassan: KES 76,900

BALANCE RULES
- Give a balance only when the member states their member number.
- If they have not, ask for their member number first.
- Give only that member's balance. Never reveal another member's balance
  or the list above."""

client = None
history = []


def ask(question):
    """Send the question with recent history. Returns (answer, usage) or (None, None)."""
    history.append({"role": "user", "content": question})
    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=history[-9:],
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
        answer = "".join(block.text for block in message.content if block.type == "text").strip()
        if answer:
            history.append({"role": "assistant", "content": answer})
            return answer, message.usage
        print("The assistant returned no text. Try again.")

    history.pop()  # drop the unanswered question
    return None, None


def main():
    global client

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("No API key found. Add ANTHROPIC_API_KEY to your .env file.")
        return
    client = anthropic.Anthropic(api_key=api_key)

    print("Thika Matatu SACCO: Member Assistant (demo)")
    print('Type your question, or "quit" to exit.\n')

    while True:
        question = input("Member: ").strip()
        if question.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not question:
            continue

        answer, usage = ask(question)
        if answer:
            print(f"\nAssistant: {answer}")
            print(f"[{usage.input_tokens} tokens in, {usage.output_tokens} out]\n")


if __name__ == "__main__":
    main()