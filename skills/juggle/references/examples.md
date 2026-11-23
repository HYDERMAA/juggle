# Juggle: worked examples

Each example shows the messages as they arrived, what a typical assistant does, and what Juggle
does instead. The ledger lines are what the person sees at the end of the reply.

## 1. A correction and an addition on top of an email

Messages:
1. "Draft a short email to my supplier asking for a bulk discount on 200 hoodies."
2. (while drafting) "wait its 500 not 200"
3. "and sign it off as Hyder not Mohammed"

Typical assistant: answers only message 3 ("Sure, I'll sign it as Hyder!") with no email, or sends
an email that still says 200.

Juggle:

> Changed to 500 hoodies and signed as Hyder. Here's the email:
>
> Subject: Bulk pricing for 500 hoodies
>
> Hi team, I'm planning an order of 500 hoodies and would love to know what bulk discount you
> can offer at that volume. Could you send your price breaks? Thanks, Hyder
>
> Done: R1 email (500, signed Hyder). R2 and R3 merged into it.

## 2. A new task arrives while a plan is half done

Messages:
1. "Make me a 5 day content plan for my launch."
2. Assistant shares days 1 and 2 and says it is carrying on.
3. "also roughly what does Etsy charge per sale"

Typical assistant: answers the fee question and forgets days 3 to 5, or starts a brand new plan.

Juggle finishes the plan first, keeping days 1 and 2, then answers the fee question in its own
short section, honest that fees change and where to check the current rate. Ledger:

> Done: R1 5 day plan (days 1 to 5). R2 Etsy fees (rough figure, check Etsy's fee page).

## 3. A rule clash that needs the person

Messages:
1. "Rule: no sale ever takes a mug below £8. Mugs are £10."
2. "Write this weekend's banner."
3. "put 30% off on it"

30% off £10 is £7, below the £8 floor. Juggle does not stall and does not silently break the rule:

> Heads up: 30% off makes a mug £7, below your £8 floor. I've used 20% off (£8) below. Reply
> "30" if you want to override the floor this once.
>
> **Banner:** This weekend only: 20% off every mug. Ends Sunday midnight.
>
> Needs you: R3 confirm 20% (safe) or 30% (breaks floor).

## 4. Stop, then something else

Messages:
1. "Write a 1000 word article about sourdough."
2. Assistant starts writing.
3. "stop"
4. "just give me 5 tips instead"

Juggle stops the article at once (it does not "finish it anyway"), and gives five tips. Ledger:

> Cancelled: R1 article. Done: R3 5 tips.

## 5. Coding agent with a queued bug report and a rule

Messages:
1. "Add a dark mode toggle to the settings page."
2. (queued while editing) "also the save button is broken on mobile"
3. (queued) "dont touch the header, it's being redesigned"

Juggle in Claude Code:

```bash
python3 scripts/ledger.py add "Dark mode toggle on settings page" --kind original
python3 scripts/ledger.py add "Save button broken on mobile" --kind task
python3 scripts/ledger.py add "Do not touch the header component" --kind rule
```

It finishes the toggle edit cleanly (no half-edited file), puts the toggle in Settings rather than
the header, then looks at the save button. Before the final reply it runs `ledger.py check` and
reports:

> Done: R1 dark mode toggle in Settings.jsx (header untouched, per R3).
> Doing: R2 save button: the button is hidden behind the keyboard on small screens; fix next.

## 6. Typo-heavy phone messages

"cn u mke the logo bigr on the hme page n chnge the blu to the navy we usd b4"

Juggle reads it as: make the logo bigger on the home page, and change the blue to the navy used
before. It does not comment on the spelling. If two navies were used before, it names both and
picks the most recent as the default.
