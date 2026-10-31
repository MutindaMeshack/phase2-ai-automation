# SACCO Member Assistant

A command-line tool for a Matatu SACCO secretary in Thika. Members' common questions (balance, next meeting, fees) are answered automatically using Claude, so the secretary spends less time on repeated WhatsApp messages.

## How it works
The SACCO's facts are written in a system prompt. Each question is sent to the Claude API together with those facts, and the assistant answers only from them. If the answer is not there, it says so.

## Setup
1. Install Python 3.
2. Install the libraries:
   ```bash
   pip install anthropic python-dotenv
   ```
3. Get an API key from the Anthropic Console.
4. Created a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

## Usage
```bash
python week3/sacco-assistant/sacco_assistant.py
```
Type a question. Type `quit` to exit.

## Example
```
Thika Matatu SACCO: Member Assistant (demo)
Type your question, or "quit" to exit.

Member: What is my balance?

Assistant: I'd be happy to help you check your balance. Could you please share your member number first? Once I have it, I can give you your balance as at 31 October 2026.
[379 tokens in, 49 out]

Member: Member 001, how much do I have?

Assistant: Thank you! Your balance as at 31 October 2026 is **KES 48,500**, Wanjiru.

If you have any other questions, feel free to ask.
[441 tokens in, 54 out]

Member: quit
Goodbye!
```

## Cost
Each question costs a small amount, based on tokens sent and received. The tool prints the token count after each answer.

## Limits
- All names and balances in this repo are fictional demo data.
- The tool cannot verify who is asking. Anyone can type any member number, so a real version needs a verified login.
- Balances are written into the prompt by hand. A real version would read them from the SACCO's records.
- Member data is sent to the Claude API, so the SACCO should be comfortable with that.