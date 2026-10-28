# Day 10: Client Messages (Kiambu Dairy Co-op Price Checker)

*Practice exercise using a simulated brief.*

---

## Message 1: Reply to your brief

Hello Kiambu Dairy Co-op team,

Thank you for your message. Here is what I understood, so you can correct me if I have got anything wrong.

Every week the buying price per litre changes, and your staff have to call or WhatsApp about 30 farmers to tell each one what they are owed. You would like a simple program where a farmer enters their name and the litres they supplied, and it shows the total amount owed at the current price. You do not have a website, so something simple is fine. Your budget is KES 8,000 and you need it by the end of this week.

To meet that deadline, I can deliver by Friday 30 October, as long as the deposit clears by Wednesday 28 October. If it clears later, the delivery date moves by the same number of days.

I have one question before I send you my full proposal:

Where is the current buying price recorded today? If it is in a spreadsheet, I can read it directly. If someone writes or types it each week, I will put it in a one-line file that your manager edits.

If I do not hear from you, I will assume the price can be kept in a simple text file. If it lives in a database or another system, I would need 1 extra working day.

Regards,
Meshack Mutinda.

---

## Message 2: My proposal

Hello Kiambu Dairy Co-op team,

Your farmers should not have to wait for a call or WhatsApp to find out what they are owed.

I will build a simple program for you. A farmer enters their name and the litres they supplied, and instantly sees the total you owe them at this week's price per litre. Your manager updates the price by editing one small file.

I am assuming the weekly price can be kept in a simple text file. If it lives in a database or another system, I will need 1 extra working day.

**What you will receive**
- The working program
- A README with step-by-step instructions for updating the weekly price
- A 20-minute handover call to show your team how to use it

**Included**
- A program where you enter a name and litres and get the total owed
- The weekly price kept in an editable file (price.txt)
- Clear messages if a number is typed wrongly or the price file is missing
- A README with setup and price-update instructions
- A 20-minute handover call

**Not included**
- A history or log of payments
- A website or phone app
- Sending SMS or M-Pesa payments
- Support or changes after delivery

**Price and timeline**
KES 8,000. Delivery in 2 working days after your deposit clears.

**Payment terms**
- KES 4,000 deposit before work begins
- KES 4,000 within 2 business days of you confirming delivery in writing
- Work starts once the deposit clears

Could you tell me whether the price is recorded in a spreadsheet or written down each week? Once you confirm the scope above and send the deposit, I will start straight away.

Regards,
Meshack Mutinda.

---

## Message 3: Deposit request

Hello Kiambu Dairy Co-op team,

Thank you for confirming the scope. Please send KES 4,000 (50% deposit) to Mpesa Number: 0799660xxx. Work starts once the deposit clears, and delivery is 2 working days after that date.

Regards,
Meshack Mutinda.

---

## Message 4: Delivery

Hello Kiambu Dairy Co-op team,

The Dairy Co-op Payment Calculator is ready. Here is what I have delivered:

- A program where a farmer enters their name and litres supplied and sees the total owed at the current price
- A price file (price.txt) that your manager edits each week, with step-by-step instructions in the README
- Clear messages if a number is entered wrongly or the price file is missing

To try it, follow the Setup steps in the README, then run:
`python week2/dairy-calculator/dairy_calculator.py`

Try 12.5 litres and compare the total with your own calculation at the current price.

This covers everything we agreed: name and litres in, total out, with a price your manager can change every week.

Please review it over the next two business days. If everything works as agreed, reply to confirm and I will send the invoice for the remaining KES 4,000. If something does not work, tell me what you typed and what you saw, and I will fix it the same day.

Regards,
Meshack Mutinda.

---

## Message 5: Reply to your request for a payment log

You wrote: *"This is great! Can we also add a feature where it keeps a log of every farmer's payment so we can see the history at the end of the month?"*

Hello Kiambu Dairy Co-op team,

Thank you, I am glad it works for you. A payment log is a good idea and would make month-end much easier.

A log was not part of our original agreement (payment history was listed under "Not included"), so I would quote it separately. It would save each farmer's name, litres, price and date to a file that you can open in Excel.

The price for that is KES 2,500, delivered in 1 working day after you confirm the quote and pay a 50% deposit of KES 1,250.

The current program is working as agreed. Please reply to confirm delivery of the original scope, and I will send the invoice for the remaining KES 4,000.

Regards,
Meshack Mutinda.

---

## Message 6: If a bug is reported

Hello [Name], received. I will look at this and get back to you by end of day.

---

## Message 7: Late payment follow-up

Hello Kiambu Dairy Co-op team, I am following up on the balance of KES 4,000 for the Dairy Calculator project. You confirmed delivery on 30th October, 2026. If there is anything about the work that needs attention before you can pay, please tell me and I will fix it. Otherwise, payment to Mpesa Number: 0799660xxx would be great. Thank you.

---

## Notes to myself

- **A revision** on this project would look like: the total is calculated wrongly, or the program crashes when a farmer types a normal number.
- **A new feature** would look like: keeping a payment log, sending an SMS to the farmer, or checking names against a member list.