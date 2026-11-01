"""
Function calling practice
-------------------------
Two tools for Kamau Stores (stock level and price). The model decides which
tool to call, and the loop sends each result back so it can answer.

Usage:
    python week3/day14_tool_practice.py
Type "exit" to quit.

Requires ANTHROPIC_API_KEY in the .env file in the project root.
"""

import os
import re


import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-5-5"
MAX_STEPS = 5

inventory = {"maize flour": 120, "wheat flour": 85, "rice": 200, "sugar": 0, "cooking oil": 45}
prices = {"maize flour": 2800, "wheat flour": 3200, "rice": 4500}

SYSTEM_PROMPT = """You are an assistant for Kamau Stores, a wholesale distributor in Nairobi.
Use the tools to check stock and prices. Never guess a stock level or a price.
If a tool says a product is not found, say so. Prices are in KES. Be brief."""

NOISE = re.compile(
    r"^(?:(?:a|an|the|some|\d+)\s+)*(?:bags?|sacks?|packets?|bottles?|litres?|liters?|kgs?|kilos?)(?:\s+of)?\s+"
)

def find_product(text, catalog):
    """Clean up a product name like 'bag of rice'. Returns the catalog name, or None."""
    text = NOISE.sub("", str(text).strip().lower())
    return text if text in catalog else None


def get_stock_level(product_name):
    product = find_product(product_name, inventory)
    if product is None:
        return f"Product '{product_name}' not found in the system."
    qty = inventory[product]
    if qty == 0:
        return f"{product}: currently out of stock."
    return f"{product}: {qty} units in stock."


def get_price(product_name):
    product = find_product(product_name, prices)
    if product:
        return f"{product}: KES {prices[product]:,} per bag"
    if find_product(product_name, inventory):
        return f"'{product_name}' is stocked but has no price on file."
    return f"Price not found for '{product_name}'."


TOOLS = [
    {
        "name": "get_stock_level",
        "description": "The product name only, for example 'rice' or 'maize flour'. Leave out quantities, units and words like 'bag of'. Known products: maize flour, wheat flour, rice, sugar, cooking oil.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {"type": "string", "description": "The name of the product to check"}
            },
            "required": ["product_name"],
        },
    },
    {
        "name": "get_price",
        "description": "Get the price in KES for a product at Kamau Stores.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {"type": "string", "description": "The name of the product"}
            },
            "required": ["product_name"],
        },
    },
]

FUNCTIONS = {"get_stock_level": get_stock_level, "get_price": get_price}


def run_tool(name, tool_input):
    """Run one tool. Returns (result_text, is_error)."""
    func = FUNCTIONS.get(name)
    if func is None:
        return f"Unknown tool: {name}", True
    try:
        return func(**tool_input), False
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
                    result, is_error = run_tool(block.name, block.input)
                    print(f"  [tool] {block.name}({block.input}) -> {result}")
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

    print("Kamau Stores assistant with tools. Type 'exit' to quit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
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