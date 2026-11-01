"""
Kisumu Pharmacy Chatbot
-----------------------
A command-line chatbot that pharmacy staff use to answer common customer
questions consistently. It remembers earlier turns in the conversation.
All pharmacy facts below are FICTIONAL demo data: replace them with the
real pharmacy's facts before real use.

Usage:
    python week3/pharmacy-chatbot/pharmacy_chatbot.py
Type "exit" to quit. The conversation is saved to the logs folder.

Requires ANTHROPIC_API_KEY in the .env file in the project root.
"""

import json
import os
from datetime import datetime

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-5-5"
MAX_INPUT_LENGTH = 1000
HISTORY_WINDOW = 9  # odd number, so the window always starts with a user message
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

SYSTEM_PROMPT = """You are the assistant for Kisumu Pharmacy. Pharmacy staff use you
to answer customer questions quickly and consistently. Keep answers short, clear
and friendly. Reply in the language the person uses (English or Swahili).

PHARMACY FACTS
- Name: Kisumu Pharmacy
- Opening hours: Monday to Saturday 8am to 8pm. Sunday 10am to 4pm.
- Services: prescription dispensing, repeat prescriptions, over-the-counter
  medicines, blood pressure checks, blood sugar testing, first-aid supplies,
  baby care products.
- Prescription time: a new prescription usually takes 15 to 20 minutes and a
  repeat prescription about 10 minutes. It can take longer at busy times.
- Repeat prescription documents: the previous prescription or the empty medicine
  box or label, a valid ID, and the name of the doctor or clinic that prescribed it.
- Items usually kept on the shelf: paracetamol, oral rehydration salts, plasters,
  antiseptic, hand sanitiser, baby nappies. Staff should still check the shelf.

RULES
- Use only the facts above. If something is not covered, say you do not have that
  information and ask the customer to speak to a pharmacist at the counter.
- Never confirm that a prescription medicine is in stock. A pharmacist must check.
- Never give medical advice: no diagnosis, no doses, and no advice to start, stop
  or change a medicine. Refer the person to a pharmacist.
- If someone describes an emergency (for example chest pain, trouble breathing,
  a severe allergic reaction, or a possible overdose), tell them to call 999 or
  112 or go to the nearest hospital immediately.
- Remember what was said earlier in this conversation and use it. If someone says
  they have a prescription and later asks how long it will take, they mean that
  prescription."""

client = None
history = []


def report_error(err):
    if isinstance(err, anthropic.AuthenticationError):
        print("API key is wrong or expired. Check your .env file.")
    elif isinstance(err, anthropic.NotFoundError):
        print("Model not found. Check the model name in the Anthropic docs.")
    elif isinstance(err, anthropic.RateLimitError):
        print("Too many requests. Wait 60 seconds and try again.")
    elif isinstance(err, anthropic.APIConnectionError):
        print("No internet connection. Check your connection and try again.")
    elif isinstance(err, anthropic.APIStatusError):
        print(f"The API returned an error (status {err.status_code}). Check your billing.")
    else:
        print("Something went wrong talking to the AI service.")


def ask(question):
    """Stream the reply as it is written. Returns usage or None."""
    history.append({"role": "user", "content": question})
    print("\nAssistant: ", end="", flush=True)
    parts = []
    try:
        with client.messages.stream(
            model=MODEL,
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=history[-HISTORY_WINDOW:],
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                parts.append(text)
            final = stream.get_final_message()
    except anthropic.AnthropicError as err:
        print()
        report_error(err)
        history.pop()
        return None

    answer = "".join(parts).strip()
    if not answer:
        print("(no text came back)")
        history.pop()
        return None

    history.append({"role": "assistant", "content": answer})
    print()
    return final.usage


def save_log():
    if not history:
        return
    os.makedirs(LOG_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(LOG_DIR, f"chat_{stamp}.json")
    log = {"date": datetime.now().isoformat(timespec="seconds"), "messages": history}
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
        print(f"Conversation saved to logs/chat_{stamp}.json")
    except OSError:
        print("Could not save the conversation log.")


def main():
    global client

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("No API key found. Add ANTHROPIC_API_KEY to your .env file.")
        return
    client = anthropic.Anthropic(api_key=api_key)

    print("Kisumu Pharmacy Assistant (demo). Type 'exit' to quit.\n")

    try:
        while True:
            try:
                question = input("You: ").strip()
            except EOFError:
                break
            if question.lower() in ("exit", "quit"):
                break
            if not question:
                continue
            if len(question) > MAX_INPUT_LENGTH:
                print(f"That message is too long (limit {MAX_INPUT_LENGTH} characters).")
                continue

            usage = ask(question)
            if usage:
                print(f"[{usage.input_tokens} tokens in, {usage.output_tokens} out]\n")
    except KeyboardInterrupt:
        print()
    finally:
        save_log()


if __name__ == "__main__":
    main()