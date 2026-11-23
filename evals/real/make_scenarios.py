#!/usr/bin/env python3
"""Writes scenarios.json. Each scenario is a conversation where the person layers extra messages
on top of a task that is already under way, then the model writes its next reply.

L01 to L20: development set (used while tuning the skill).
H01 to H10: held-out set, written before the first SKILL.md draft and never used for tuning.
"""
import json, os

U, A = "user", "assistant"
S = []


def sc(id, context, turns, checks):
    S.append({"id": id, "context": context, "turns": turns, "checks": checks})


# ------------------------------------------------------------------ development set
sc("L01", "Claude app on a phone. Runs a made-to-order tee shop on eBay UK.", [
    [U, "Write 3 eBay titles for my 'Brackwell Rowing Club' tee, max 80 characters each"],
    [A, "On it. Checking what eBay titles need and drafting now."],
    [U, "also add one for the navy colour"],
    [U, "an dont use the word vintage ebay flags it"]],
    ["Gives eBay titles for the Brackwell Rowing Club tee",
     "Includes at least one title for the navy colour, on top of the 3 asked for (4 or more in total)",
     "No title uses the word 'vintage'",
     "Titles look like 80 characters or fewer"])

sc("L02", "Claude app on a phone.", [
    [U, "Draft a short email to Printful asking for a bulk discount on 200 Gildan 64000 tees."],
    [A, "Drafting it now."],
    [U, "wait its 500 not 200"],
    [U, "and sign it off as Hyder not Mohammed"]],
    ["The email asks Printful for a bulk discount on Gildan 64000 tees",
     "Uses 500 as the quantity and does not ask about 200",
     "Signs off as Hyder (not Mohammed)",
     "The email is short and ready to send"])

sc("L03", "Claude app on a phone. Launching a tee shop called Faded Archive.", [
    [U, "Make me a 5 day Instagram content plan for my tee shop launch"],
    [A, "Working on it. Days 1 and 2 done:\nDay 1: teaser of the logo on a black background\nDay 2: behind the scenes of a tee being printed\nCarrying on with days 3 to 5."],
    [U, "also can u remind me roughly what eBay charges in fees for clothing in the UK"]],
    ["Delivers days 3, 4 and 5 of the content plan",
     "Keeps days 1 and 2 as they were (repeats them or clearly builds on them) rather than starting a different plan",
     "Answers the eBay fee question with a rough figure or honest uncertainty about current rates",
     "Keeps the fee answer separate from the content plan instead of mixing them up"])

sc("L04", "Claude Code. Project folder for the Faded Archive tee shop. Brand name is Faded Archive.", [
    [U, "Rename my product photos to the format brand-design-colour.jpg and give me the list of new names"],
    [A, "[ran: ls photos/] IMG_2231.jpg IMG_2232.jpg IMG_2233.jpg\nFrom shoot-notes.txt: 2231 = Brackwell navy, 2232 = Ashcombe Bay white, 2233 = Brackwell grey.\nRenaming now."],
    [U, "how long will this take"]],
    ["Answers how long it will take briefly (for example seconds, it is three files)",
     "Gives all three new names in a brand-design-colour.jpg style",
     "Maps them correctly: 2231 Brackwell navy, 2232 Ashcombe Bay white, 2233 Brackwell grey",
     "Carries on with the renaming rather than stopping to chat"])

sc("L05", "Claude app on a phone. Tee shop.", [
    [U, "Write a product description for the Ashcombe Bay tee (white, seaside town crest design), then a short FAQ for my shop page"],
    [A, "Starting with the product description."],
    [U, "do the faq first its more urgent, description can wait"]],
    ["The FAQ comes first in the reply",
     "The FAQ is a usable shop FAQ (for example delivery, returns, sizing, made to order)",
     "The Ashcombe Bay description is still written after the FAQ, or clearly kept as the next item, not dropped",
     "Acknowledges the change of order briefly"])

sc("L06", "Claude app on a phone.", [
    [U, "Write a 1500 word blog post about the history of slogan tees"],
    [A, "Writing it now.\n\nIntro: Slogan tees began as..."],
    [U, "stop"],
    [U, "actually just give me 5 bullet points instead"]],
    ["Does not carry on with the 1500 word post",
     "Gives 5 bullet points about the history of slogan tees",
     "The bullets are accurate and specific (names, decades or examples)",
     "Is short overall"])

sc("L07", "Claude app on a phone. Tee shop on eBay UK.", [
    [U, "Rule for my shop: never discount any tee below £18. All tees are £19.99."],
    [A, "Noted: £19.99 per tee, never below £18."],
    [U, "Write the text for my shop banner for this weekend"],
    [A, "Drafting three banner options."],
    [U, "put 25% off everything on it"]],
    ["Notices that 25% off £19.99 (about £14.99) breaks the £18 floor",
     "Does not just silently publish 25% off as if there were no problem; asks to confirm or offers a version that respects the floor",
     "Still provides usable banner text",
     "Explains the conflict in one or two plain sentences"])

sc("L08", "Claude app on a phone.", [
    [U, "Plan my week. I need to finish the Seatbelt README, record a TikTok, and do my accounts"],
    [A, "Building the plan."],
    [U, "add gym mon wed fri 7am"],
    [U, "no tiktok this week actually"],
    [U, "accounts must be done by thurs"],
    [U, "and keep the weekend free"]],
    ["Includes finishing the Seatbelt README",
     "Includes gym on Monday, Wednesday and Friday at 7am",
     "Does not schedule the TikTok",
     "Accounts are finished by Thursday",
     "Nothing is scheduled on Saturday or Sunday"])

sc("L09", "Claude app on a phone. Tee shop.", [
    [U, "cn u wrte a captoin for my insta post of the navy brackwell tee, chill vibe, 2 hashtgs max"],
    [A, "Sure, writing it."],
    [U, "oh n mention its prder on demand"]],
    ["Gives a caption about the navy Brackwell tee",
     "The tone is relaxed and chill",
     "Uses no more than 2 hashtags",
     "Mentions that it is made to order or printed on demand",
     "Does not comment on or correct the person's typos"])

sc("L10", "Claude app on a phone. Tee shop.", [
    [U, "List my top 3 tees by views. Brackwell navy 410 views, Ashcombe white 380, Wexmoor grey 120, Brackwell grey 300"],
    [A, "Sorting them now."],
    [U, "and remove wexmor and bracwell"]],
    ["Removes Wexmoor grey",
     "Notices that 'bracwell' could mean Brackwell navy, Brackwell grey or both, and says so",
     "Does not silently guess which Brackwell to remove without saying",
     "Gives a sensible list or both readings so the person can pick quickly"])

sc("L11", "Claude app on a phone.", [
    [U, "Write a tweet announcing Seatbelt v3, my free skill that helps non-developers build apps safely with AI"],
    [A, "Draft: 'Seatbelt v3 is out. Build apps with AI without...'"],
    [U, "actually make it a linkedin post instead, longer"],
    [U, "and mention its free"]],
    ["Delivers a LinkedIn-style post that is longer than a tweet",
     "Mentions that it is free",
     "It is about Seatbelt v3 and what it does",
     "Treats the tweet as replaced (does not pad the reply with more tweet versions)"])

sc("L12", "Claude Code. A React app.", [
    [U, "Add a dark mode toggle to the settings page"],
    [A, "[read src/Settings.jsx] I'll add a toggle backed by a ThemeContext. Editing Settings.jsx now."],
    [U, "also the save button is broken on mobile btw"],
    [U, "dont touch the header component its being redesigned"]],
    ["Still delivers the dark mode toggle on the settings page (code or concrete changes)",
     "Deals with the broken save button: looks into it, proposes a fix, or clearly queues it as the next job",
     "Does not put anything in or change the header component",
     "Says clearly what is done and what is next"])

sc("L13", "Claude app on a phone.", [
    [U, "Write a cover letter for a junior product designer role at Monzo. I have 2 years as a barista and I taught myself Figma."],
    [A, "Drafting now."],
    [U, "is it ok to mention i built an app with AI"]],
    ["Answers the question directly (yes, and how to frame it)",
     "Delivers the cover letter",
     "The letter is for a junior product designer role at Monzo and uses the barista and Figma background",
     "The letter includes the AI-built app, framed well"])

sc("L14", "Claude app on a phone.", [
    [U, "Give me 3 name ideas for a tee shop selling rowing club style designs"],
    [A, "Thinking of names."],
    [U, "also check none are taken on ebay"],
    [U, "also check none are taken on ebay"]],
    ["Gives 3 shop name ideas that fit rowing club style designs",
     "Is honest that it cannot check eBay live from here (or says how to check), rather than claiming they are free",
     "Treats the repeated message as one request (does not answer it twice)",
     "Tells the person a quick way to check the names"])

sc("L15", "Claude app on a phone. Tee shop.", [
    [U, "Two things: write a refund policy for my shop, and draft a reply to a customer asking where their order is (order 1042, posted Tuesday by Royal Mail)"],
    [A, "Refund policy done:\n- Returns within 30 days\n- Made-to-order items can be returned if faulty\n- Refunds in 5 working days\nNow the customer reply."],
    [U, "scrap the refund policy, ebay has its own"],
    [U, "and the customer is called Sam"]],
    ["Drops the refund policy and does not keep working on it",
     "Gives a reply to Sam about order 1042",
     "The reply says it was posted Tuesday by Royal Mail",
     "The reply is polite, short and ready to send"])

sc("L16", "Claude Code. Building a phone app called Big that you talk to by voice.", [
    [U, "Build the voice mode for Big: user taps the mic, speaks, the app replies out loud"],
    [A, "Plan: 1) mic permission 2) speech to text 3) send to the model 4) speak the reply. Mic permission is done. Writing the speech to text step now."],
    [U, "We need to make animations for big by voice - show me options"]],
    ["Keeps the voice mode build going: reports progress or continues with the next steps",
     "Gives at least 3 distinct animation options",
     "The options match voice states (for example listening, thinking, speaking)",
     "Recommends one or asks which to pick, so the person can decide quickly"])

sc("L17", "Claude app on a phone. Tee shop.", [
    [U, "Work out my profit per tee: I sell at £19.99, eBay fees are 12.8% + 30p, Printful cost is £11.50"],
    [A, "Working it out."],
    [U, "sorry printful is £12.95 not 11.50"],
    [U, "and add the 2.5% promoted listing fee"]],
    ["Uses £12.95 as the Printful cost (not £11.50)",
     "Includes the 2.5% promoted listing fee",
     "Gets a profit of about £3.68 per tee (anything from £3.60 to £3.75 is fine)",
     "Shows the working briefly"])

sc("L18", "Claude Code. A Node app.", [
    [U, "Migrate the database from SQLite to Postgres"],
    [A, "Step 2 of 5 done: schema copied to Postgres. Next: copy the data, update the connection code, run the tests."],
    [U, "when ur done can u write the changelog for v1.2"]],
    ["Carries on with the migration (data copy, connection code, tests) rather than abandoning it",
     "Treats the changelog as the next job after the migration",
     "Does not start the changelog in a way that leaves the migration half done",
     "Says what is done and what is next"])

sc("L19", "Claude Code. Shop website with a UK and a US version.", [
    [U, "Two jobs: fix the typo on the about page and update the tee price to £24.99"],
    [A, "Fixed the typo ('archieve' to 'archive') on the UK about page. Starting on the price."],
    [U, "also do the same for the US shop"]],
    ["Updates the UK price to £24.99",
     "Applies the typo fix to the US about page",
     "Flags that the US price needs a dollar amount (and does not invent an exchange rate without saying so)",
     "Reports what is done and what needs the person"])

sc("L20", "Claude app on a phone.", [
    [U, "For everything today: British spelling, no em dashes, keep replies under 150 words."],
    [A, "Noted."],
    [U, "Write a short about-us for Faded Archive, a made-to-order tee shop"],
    [A, "Drafting."],
    [U, "make it mention we're based in Manchester"],
    [U, "also what colour should the logo be"]],
    ["Gives an about-us for Faded Archive that mentions Manchester",
     "Answers the logo colour question",
     "Uses British spelling and no em dashes (the long dash character)",
     "The whole reply is under about 150 words"])

# ------------------------------------------------------------------ held-out set
sc("H01", "Claude app on a phone.", [
    [U, "Plan a 2 day trip to Lisbon for me and my wife in March"],
    [A, "Putting it together."],
    [U, "budget £600 total not incl flights"],
    [U, "shes vegetarian"],
    [U, "and we land 2pm on day 1"]],
    ["Gives a 2 day Lisbon plan",
     "Keeps to about £600 excluding flights",
     "Food suggestions suit a vegetarian",
     "Day 1 starts after a 2pm landing"])

sc("H02", "Claude app on a phone.", [
    [U, "Write a WhatsApp message inviting the team to Friday drinks at 6pm at The Crown"],
    [A, "Drafting."],
    [U, "its thursday not friday"],
    [U, "and 7"]],
    ["Says Thursday, not Friday",
     "Says 7pm, not 6pm",
     "Keeps The Crown as the place",
     "Short and friendly, ready to paste into WhatsApp"])

sc("H03", "Claude app on a phone. Tee shop on eBay UK.", [
    [U, "Research the top 10 competitors for my tee shop"],
    [A, "Starting with the big ones: 1. Threadless 2. Redbubble 3. TeePublic... continuing."],
    [U, "nvm stop that"],
    [U, "just tell me how to set up an ebay promoted listing at 2.5%"]],
    ["Stops the competitor list (does not carry on listing competitors)",
     "Gives steps to set up an eBay promoted listing",
     "Uses a 2.5% ad rate in the steps",
     "Short and easy to follow"])

sc("H04", "Claude app on a phone. Tee shop.", [
    [U, "Write the eBay listing for the Brackwell navy tee. Rule: never say 'cotton' anywhere, the fabric blend isn't confirmed yet."],
    [A, "Drafting."],
    [U, "say its 100% organic cotton in the title"]],
    ["Notices that this clashes with the earlier rule about not saying cotton because the blend is unconfirmed",
     "Does not silently claim 100% organic cotton; asks to confirm or warns about the risk of an untrue claim",
     "Still provides the listing",
     "Keeps the conflict explanation short"])

sc("H05", "Claude Code.", [
    [U, "Write a Python function that removes duplicate emails from a list, ignoring upper and lower case"],
    [A, "Writing it."],
    [U, "keep the original order"],
    [U, "also how do i run tests in python again lol"]],
    ["Gives a function that removes duplicates ignoring case",
     "Keeps the original order (first occurrence wins)",
     "Answers how to run tests (for example python -m unittest or pytest)",
     "The code is correct"])

sc("H06", "Claude app on a phone. Tee shop.", [
    [U, "pls sumarise this in 3 bulets: 'Hi, due to a fault at our Latvia facility, orders placed between 10 and 14 Nov will ship 4 to 6 days late. We will refund shipping on affected orders automatically. Sorry for the trouble, Printful Support.'"],
    [A, "Summarising."],
    [U, "nd tell me if i shld email my customers"]],
    ["Gives a summary in 3 bullets",
     "The bullets are accurate (Latvia fault, 10 to 14 Nov orders, 4 to 6 days late, shipping refunded automatically)",
     "Gives a clear recommendation on emailing customers",
     "Does not comment on the typos"])

sc("H07", "Claude app on a phone. Tee shop.", [
    [U, "Today: 1) reply to Sam's complaint that his tee arrived the wrong size 2) write 3 tee slogans 3) plan Saturday's market stall"],
    [A, "Starting with Sam's reply."],
    [U, "slogans first, printer needs them in 10 mins"]],
    ["The slogans come first",
     "Gives 3 tee slogans",
     "The reply to Sam is still written, or clearly kept as next, not dropped",
     "The market stall plan is still done or clearly listed as queued, not forgotten"])

sc("H08", "Claude app on a phone.", [
    [U, "Translate my shop's 5 FAQ answers into Spanish: 1) We print every tee to order. 2) Delivery takes 3 to 5 working days. 3) Returns are accepted within 30 days. 4) Wash inside out at 30 degrees. 5) Contact us through eBay messages."],
    [A, "Translated 1 and 2:\n1) Imprimimos cada camiseta bajo pedido.\n2) La entrega tarda de 3 a 5 días laborables.\nCarrying on."],
    [U, "are you doing the titles too?"]],
    ["Answers the question about titles directly",
     "Translates answers 3, 4 and 5",
     "The Spanish is correct",
     "Keeps answers 1 and 2 (repeats or builds on them) so the set of 5 is complete"])

sc("H09", "Claude app on a phone. Tee shop.", [
    [U, "Write a 'back in stock' email for the Brackwell navy tee"],
    [A, "Draft:\nSubject: It's back: the Brackwell navy tee\nHi there, ..."],
    [U, "actually make it a text message, 160 characters"],
    [U, "include a 10% code BACK10"]],
    ["Delivers a text message, not an email",
     "About 160 characters or fewer",
     "Includes the code BACK10 for 10% off",
     "Says the Brackwell navy tee is back in stock"])

sc("H10", "Claude Code. A Python shop backend.", [
    [U, "Fix the failing test test_checkout_total (expected 24.99, got 2499)"],
    [A, "[read checkout.py] The total is worked out in pence, but the test expects pounds. Checking where total() is used before changing it."],
    [U, "btw whats a good name for a newsletter about AI side hustles"]],
    ["Proposes a sound fix for the pence vs pounds mismatch (and keeps checking where total() is used)",
     "Gives some newsletter name ideas about AI side hustles",
     "Keeps the two things separate",
     "Does not drop the test fix"])

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenarios.json")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("[\n" + ",\n".join(json.dumps(s, ensure_ascii=False) for s in S) + "\n]\n")
    print(len(S), "scenarios ->", out)
