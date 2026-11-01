# Tea Harvest Weather Agent

A command-line assistant for a field supervisor at a tea estate in Kericho. The supervisor asks a question such as "Is today good for harvesting?". If the answer depends on the weather, the AI calls a weather tool, then gives a plain recommendation: GOOD, MARGINAL or NOT RECOMMENDED, with the reasons.

## How it works (the function-calling loop)
1. The question is sent to Claude together with a description of the weather tool.
2. If the question needs the weather, Claude asks for the tool to be run.
3. The script fetches live weather from Open-Meteo (no key needed) and sends it back.
4. Claude applies the estate's harvest rules and answers.

Questions that do not need the weather (for example tea terms) are answered directly, without calling the tool.

## Harvest rules in the prompt
- **NOT RECOMMENDED:** raining now, or above 28°C
- **GOOD:** no rain expected in 6 hours, 15 to 25°C, humidity 80% or below
- **MARGINAL:** everything in between

These are demo values. The estate's agronomist should confirm them.

## Setup
1. Install Python 3.
2. Install the libraries:
   ```bash
   pip install anthropic python-dotenv requests
   ```
3. Create a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

## Usage
```bash
python week3/tea-harvest-agent/harvest_agent.py
```

## Example
```
Kericho Tea Estate: Harvest Assistant (demo)
Ask a question, or type "exit" to quit.

Supervisor: Is today good for harvesting?
  [tool called: get_harvest_weather {'hours_ahead': 6}]

Assistant: **MARGINAL.** It is dry now at 23.7 °C with 51% humidity, but rain is likely from about 1:00 pm, with 75% chance at 2:00 pm and 94% chance at 3:00 pm. Pluck now and finish before about 1:00 pm, since the heaviest rain (3.3 mm) is expected at 3:00 pm. Forecasts can change, so make the final call in the field.
[1 tool call(s), 2963 tokens in, 536 out in total]

Supervisor: Mvua itanyesha leo?
  [tool called: get_harvest_weather {'hours_ahead': 12}]

Assistant: Ndiyo, mvua inatarajiwa leo alasiri. Kwa sasa haijanyesha (23.7 °C, unyevu 51%). Uwezekano wa mvua ni 75% saa 2:00 pm, na ni mkubwa zaidi kati ya 3:00 pm na 4:00 pm (hadi 94–96%). Mvua inaweza kuendelea hadi takriban 7:00 pm, na baada ya hapo uwezekano unashuka hadi karibu 0% kufikia 9:00 pm.
[1 tool call(s), 3267 tokens in, 896 out in total]

Supervisor: Is it raining in Nairobi right now?

Assistant: I can't check Nairobi. My weather data covers only the Kericho estate. I can check conditions there if you need them for harvesting or field work.
[0 tool call(s), 1326 tokens in, 158 out in total]

Supervisor: quit
Goodbye!
```

## Limits
- The location is fixed to the Kericho area. Replace the coordinates with the estate's own.
- Forecasts can be wrong, and the supervisor makes the final decision.
- It checks the weather only and does not know about the estate's leaf, labour or machinery.
- Each question can need two AI calls, so it costs more than a plain chatbot.