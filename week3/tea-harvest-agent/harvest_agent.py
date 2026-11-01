"""
Tea Harvest Weather Agent
-------------------------
A field supervisor in Kericho asks a question. If it depends on the weather,
the AI calls a weather tool (Open-Meteo, no key needed) and gives a plain
recommendation using the estate's harvest rules.

Usage:
    python week3/tea-harvest-agent/harvest_agent.py
Type "exit" to quit.

Requires ANTHROPIC_API_KEY in the .env file in the project root.
Harvest thresholds below are demo values: the estate's agronomist must confirm them.
"""

import os

import anthropic
import requests
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-5-5"
MAX_STEPS = 5
MAX_QUESTION_LENGTH = 500

LATITUDE = -0.37   # Kericho area: replace with the estate's coordinates
LONGITUDE = 35.28
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

SYSTEM_PROMPT = """You help a field supervisor at a tea estate in Kericho, Kenya.
Keep answers short, practical and in plain language.

LANGUAGE AND STYLE
- Reply in the language the supervisor writes in. If they write in English, reply
  in English, including the first line. Use Swahili only if they write in Swahili
  or ask for a message in Swahili.
- When asked to write a message for workers, give only the message, ready to send.
  No introduction, no offers of extra help.
- Write times exactly as given, using the normal clock (for example "6:30 am").
  Never convert them to Swahili clock time unless asked.
- Do not add details that were not asked for, such as items to bring or weather
  remarks, unless the supervisor asks.
- Check times and numbers before you answer. Give only the final answer, with no
  corrections or second thoughts in the reply.

WHEN TO USE THE TOOL
- Use get_harvest_weather whenever the answer depends on current or coming
  conditions at the estate: harvesting, plucking, field work, rain, temperature.
- For other questions (for example tea terms, or writing a short message), answer
  directly without the tool.
- The tool covers Kericho only and gives current and short-term conditions. If
  asked about another place or past weather, say you cannot check that.
- Never state weather figures you did not get from the tool. If the tool returns
  an error, say you could not get the weather and ask the supervisor to check
  conditions in the field. Never guess.

HARVEST RULES (demo values: the estate's agronomist should confirm them)
- NOT RECOMMENDED: rain is falling now (recent rain above 0 mm) or temperature
  is above 28 C.
- Otherwise, if rain is expected in the next 6 hours (any hour with a rain
  chance of 40% or more, or more than 0.1 mm forecast): MARGINAL.
- Otherwise GOOD if temperature is 15 to 25 C and humidity is 80% or below.
- Everything else is MARGINAL (for example 25 to 28 C, below 15 C, or humidity
  above 80%).

ANSWER FORMAT for harvest questions
Start with GOOD, MARGINAL or NOT RECOMMENDED. Then give 2 or 3 short sentences
using the actual numbers (temperature, humidity, rain chance), and one practical
suggestion, such as when the next dry period starts. Forecasts can be wrong, and
the supervisor makes the final decision."""

TOOLS = [
    {
        "name": "get_harvest_weather",
        "description": (
            "Get the current weather and an hourly forecast for the tea estate in Kericho: "
            "temperature (C), humidity (%), recent rain (mm), and for each coming hour the "
            "temperature, rain chance (%) and expected rain (mm). Use it for harvesting, "
            "plucking and other outdoor work questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "hours_ahead": {
                    "type": "integer",
                    "description": "How many hours ahead to include, from 1 to 12. Default 6.",
                }
            },
        },
    }
]


def get_harvest_weather(hours_ahead=6):
    """Fetch current weather and an hourly forecast for the estate."""
    try:
        hours = int(hours_ahead)
    except (TypeError, ValueError):
        hours = 6
    hours = max(1, min(12, hours))  # the model's argument is untrusted: keep it in range

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "temperature_2m,relative_humidity_2m,precipitation",
        "hourly": "temperature_2m,precipitation_probability,precipitation",
        "forecast_hours": hours,
        "timezone": "Africa/Nairobi",
    }
    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
    except requests.exceptions.RequestException:
        return "ERROR: the weather service could not be reached.", True
    if response.status_code != 200:
        return f"ERROR: the weather service returned status {response.status_code}.", True

    try:
        data = response.json()
        now = data["current"]
        hourly = data["hourly"]
        lines = [
            f"Now ({now['time']}, Kericho local time): temperature {now['temperature_2m']} C, "
            f"humidity {now['relative_humidity_2m']}%, recent rain {now['precipitation']} mm.",
            f"Next {hours} hours:",
        ]
        for t, temp, prob, mm in zip(
            hourly["time"],
            hourly["temperature_2m"],
            hourly["precipitation_probability"],
            hourly["precipitation"],
        ):
            lines.append(f"- {t[-5:]}: {temp} C, rain chance {prob}%, expected rain {mm} mm")
    except (ValueError, KeyError, TypeError):
        return "ERROR: the weather service sent data in an unexpected format.", True

    return "\n".join(lines), False


FUNCTIONS = {"get_harvest_weather": get_harvest_weather}


def run_tool(name, tool_input):
    """Run one tool. Returns (result_text, is_error)."""
    func = FUNCTIONS.get(name)
    if func is None:
        return f"Unknown tool: {name}", True
    try:
        return func(**tool_input)
    except TypeError:
        return "The tool was called with the wrong arguments.", True


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


def run_agent(client, question):
    """Run the tool loop for one question. Returns (answer, tokens_in, tokens_out, calls)."""
    messages = [{"role": "user", "content": question}]
    tokens_in = tokens_out = calls = 0

    for _ in range(MAX_STEPS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        tokens_in += response.usage.input_tokens
        tokens_out += response.usage.output_tokens

        # Send the whole reply back unchanged (thinking blocks included)
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "tool_use":
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    calls += 1
                    print(f"  [tool called: {block.name} {block.input}]")
                    result, is_error = run_tool(block.name, block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                        "is_error": is_error,
                    })
            messages.append({"role": "user", "content": results})
            continue

        text = "".join(b.text for b in response.content if b.type == "text").strip()
        if response.stop_reason == "max_tokens":
            text += "\n(The answer was cut off.)"
        return text or "(no answer came back)", tokens_in, tokens_out, calls

    return "Stopped: too many tool steps.", tokens_in, tokens_out, calls


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("No API key found. Add ANTHROPIC_API_KEY to your .env file.")
        return
    client = anthropic.Anthropic(api_key=api_key)

    print("Kericho Tea Estate: Harvest Assistant (demo)")
    print('Ask a question, or type "exit" to quit.\n')

    while True:
        question = input("Supervisor: ").strip()
        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not question:
            continue
        if len(question) > MAX_QUESTION_LENGTH:
            print(f"That question is too long (limit {MAX_QUESTION_LENGTH} characters).")
            continue

        try:
            answer, t_in, t_out, calls = run_agent(client, question)
        except anthropic.AnthropicError as err:
            report_error(err)
            continue

        print(f"\nAssistant: {answer}")
        print(f"[{calls} tool call(s), {t_in} tokens in, {t_out} out in total]\n")


if __name__ == "__main__":
    main()