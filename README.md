<a name="top"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/hero-dark.svg">
  <img src="assets/readme/hero-light.svg" alt="Juggle: layer messages on your AI. Nothing gets dropped. A free skill that keeps every request, applies your corrections and flags real clashes." width="100%">
</picture>

<p align="center">
  <a href="#install"><b>Install</b></a> &nbsp;·&nbsp;
  <a href="#how-it-sorts-your-messages">How it sorts</a> &nbsp;·&nbsp;
  <a href="#how-it-works">How it works</a> &nbsp;·&nbsp;
  <a href="#see-it-in-action">See it in action</a> &nbsp;·&nbsp;
  <a href="#tested-not-guessed">Results</a> &nbsp;·&nbsp;
  <a href="#faq">FAQ</a>
</p>

<p align="center">You type fast and think of things mid-task. <b>Juggle makes your AI keep up.</b></p>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/specs-dark.svg">
  <img src="assets/readme/specs-light.svg" alt="At a glance: 93% on held-out tests vs 76% with no skill; 92% on development tests vs 77%; 95% of layering checks passed on held-out vs 78%; 9 kinds of message sorted; 30 test chats, 10 held out; 23 automated tests; works in 6 places; free, MIT licence." width="100%">
</picture>

<br>

## Install

Pick the tool you use. Every option is free.

<table>
<tr>
<td width="50%" valign="top">

<img src="assets/readme/badge-claude-code.svg" height="30" alt="Claude Code">

Type these two lines into Claude Code:

```
/plugin marketplace add HYDERMAA/juggle
/plugin install juggle@juggle
```

</td>
<td width="50%" valign="top">

<img src="assets/readme/badge-agents.svg" height="30" alt="Codex, Cursor and other agents">

Any app that reads skills. One command:

```
npx skills add HYDERMAA/juggle
```

</td>
</tr>
<tr>
<td width="50%" valign="top">

<img src="assets/readme/badge-claude-ai.svg" height="30" alt="Claude.ai">

Web or desktop chat. Three steps:

1. Download [`juggle.zip`](https://github.com/HYDERMAA/juggle/releases/latest). Do not unzip it.
2. Turn on **Settings > Capabilities > Code execution**.
3. Upload the zip under **Plugins** (once called **Customize**).

</td>
<td width="50%" valign="top">

<img src="assets/readme/badge-chat-apps.svg" height="30" alt="ChatGPT, Gemini or any chat app">

One copy and paste:

Copy the box in [`paste-into-chat.md`](paste-into-chat.md) into your app's custom instructions. It fits ChatGPT's 1,500 character limit.

</td>
</tr>
</table>

<details>
<summary><b>Other ways: by hand, Cursor rule, AGENTS.md</b></summary>

<br>

**By hand, for any skill-aware agent**

```bash
git clone https://github.com/HYDERMAA/juggle.git
mkdir -p ~/.claude/skills
cp -r juggle/skills/juggle ~/.claude/skills/
```

Codex and other agents read `~/.agents/skills/` instead.

**Cursor:** copy [`.cursor/rules/juggle.mdc`](.cursor/rules/juggle.mdc) into your project's `.cursor/rules/` folder.

**Codex, Cursor, Aider and others:** copy [`AGENTS.md`](AGENTS.md) into your project's main folder.

</details>

<br>

## The problem

You ask for one thing. While the AI works, you remember three more, spot a mistake, or change your mind. So you send more, or queue them in Claude Code. Too often the AI answers only your last message, keeps the old number, or quietly forgets what you first asked for.

That is not just you. A 2026 study of 15 models found the same thing at scale:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/stats-dark.svg">
  <img src="assets/readme/stats-light.svg" alt="The research: a 39% average drop in quality when a request arrives over several messages; 95% of single-message quality kept when the pieces are joined into one brief first; and models become about twice as unreliable in multi-turn chats. Source: Laban et al., LLMs Get Lost in Multi-Turn Conversation, ICLR 2026." width="100%">
</picture>

<sub>Source: Laban, Hayashi, Zhou and Neville, <a href="https://arxiv.org/abs/2505.06120">LLMs Get Lost in Multi-Turn Conversation</a> (ICLR 2026). Juggle's core habit, rebuilding the brief before every reply, is the "join the pieces" fix from that paper, done by the AI itself.</sub>

<br>

## How it sorts your messages

Every new message is one of nine kinds, and each kind has its own rule.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/kinds-dark.svg">
  <img src="assets/readme/kinds-light.svg" alt="Nine kinds of message. Addition, like 'also add navy': merged into the job now. Correction, like 'its 500 not 200': applied, old value gone. Replacement, like 'make it a post instead': only the new version. New task, like 'btw what are the fees': kept separate, done after. Question, like 'how long will this take': short answer, keeps going. Do this first: reordered, nothing dropped. Stop, like 'nvm scrap that': stopped at once. Sent twice: answered once. Standing rule, like 'never below £18': applies to everything." width="100%">
</picture>

<br>

## How it works

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/flow-dark.svg">
  <img src="assets/readme/flow-light.svg" alt="Five steps: a message arrives, it is sorted into one of nine kinds, the conversation is rebuilt into one up-to-date brief where the newest wish wins, the finished work is delivered urgent first, then a short check shows what is done, next and waiting on you. A real clash gets a safe version now plus a one-word override." width="100%">
</picture>

<br>

### What a reply looks like

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/anatomy-dark.svg">
  <img src="assets/readme/anatomy-light.svg" alt="A reply has three parts: one line up front showing it caught your new messages; the finished work, urgent first; and a short Done, Next, Needs you check when you asked for two or more things." width="100%">
</picture>

<br>

## See it in action

Real replies from the held-out test, before and after. Same model, same messages. Trimmed for length; full text in [`evals/real/runs/`](evals/real/runs/).

<table>
<tr><th width="30%">You sent</th><th width="35%">No skill</th><th width="35%">With Juggle</th></tr>
<tr>
<td valign="top">

1. Fix the failing test `test_checkout_total` (expected 24.99, got 2499)
2. *AI starts reading the code*
3. btw whats a good name for a newsletter about AI side hustles

</td>
<td valign="top">

> Here are a handful of snappy, memorable names that hint at both AI and the "side-hustle" vibe: … HustleBytes … Prompt Profits …

In all three tries, the failing test is never mentioned again.

</td>
<td valign="top">

> Fixed the `checkout.total()` to return pounds instead of pence, and here are a few catchy newsletter name ideas.
>
> **1. Fix for `test_checkout_total`** … `return total_pence / 100.0` …
>
> **2. Newsletter names** …

Both done, kept separate, in all three tries.

</td>
</tr>
<tr>
<td valign="top">

1. Today: reply to Sam's wrong-size complaint, write 3 tee slogans, plan Saturday's market stall
2. *AI starts on Sam's reply*
3. slogans first, printer needs them in 10 mins

</td>
<td valign="top">

> **T-shirt slogans (ready for printing in 10 min):** 1… 2… 3…
>
> Feel free to give me a … font choice, and I'll send a final pixel-perfect asset file …

In all three tries, Sam and the market stall are gone.

</td>
<td valign="top">

> **Slogans (first, in 10 min)** 1… 2… 3…
>
> **Reply to Sam (done)** Hi Sam, I'm really sorry to hear that the tee arrived in the wrong size …
>
> **Saturday market stall plan (next)** …

Urgent first, nothing dropped. (Best of three tries. The other two did the slogans first and listed the rest as next, though one forgot the stall plan.)

</td>
</tr>
</table>

<br>

## Tested, not guessed

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/results-dark.svg">
  <img src="assets/readme/results-light.svg" alt="Results on gpt-oss-20b, graded blind: held-out tests 93% with Juggle vs 76% with no skill; development tests 92% vs 77%; layering checks on held-out 95% vs 78%; layering checks on development 95% vs 82%." width="100%">
</picture>

| | No skill | With Juggle |
| --- | --- | --- |
| **Held-out chats** (10, never used for tuning) | 76% | **93%** |
| **Development chats** (20, used while writing the skill) | 77% | **92%** |
| Layering checks only, held-out | 78% | **95%** |
| Held-out, using only the short [chat paste-in](paste-into-chat.md) | 76% | **94%** |

- **30 realistic chats**, each a first request, the AI starting work, then one to four layered messages: corrections, extras, questions, a stop, "do this first", a clash with an earlier rule, typo-heavy phone messages and the same message sent twice.
- **The held-out 10 were written and committed before the first line of the skill**, and a test makes sure none of their wording ever appears in the skill.
- **Model:** `gpt-oss-20b`, a small open model on a free endpoint, with and without the skill. **Judge:** the same model, twice per reply, blind to which version wrote it.
- **Honest limits:** small numbers (3 replies per chat), a lenient judge, and a small model, not Claude. Full method and per-chat tables: [`evals/real/README.md`](evals/real/README.md).

<br>

## With Juggle, and without

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/compare-dark.svg">
  <img src="assets/readme/compare-light.svg" alt="Your AI on its own versus with Juggle: answering the whole request is left to chance versus rebuilding the brief; corrections, priority changes, rule clashes and honesty about checks are left to chance versus built-in rules; stopping and reading phone typing usually work on their own and are made reliable with Juggle; a done, next and waiting-on-you check comes with every multi-ask reply." width="100%">
</picture>

<br>

## For coding agents: the ledger file

In Claude Code, Codex or Cursor, when work runs over several turns or three or more requests are open, Juggle keeps the list in `.juggle/ledger.md`, plain Markdown you can open any time. It survives long runs and compaction.

```bash
python3 scripts/ledger.py add "Dark mode toggle on settings" --kind original   # R1 (doing)
python3 scripts/ledger.py add "Save button broken on mobile"                    # R2 (next)
python3 scripts/ledger.py add "Do not touch the header" --kind rule             # R3 (active)
python3 scripts/ledger.py set R1 done --note "Settings.jsx, header untouched"
python3 scripts/ledger.py check    # exit 1 while anything is still doing or next
```

<details>
<summary><b>What the ledger file looks like</b></summary>

<br>

```markdown
| # | Request | Kind | Status | Note |
|---|---|---|---|---|
| R1 | Dark mode toggle on settings | original | done | Settings.jsx, header untouched |
| R2 | Save button broken on mobile | task | doing |  |
| R3 | Do not touch the header | rule | active |  |
```

Statuses: `doing`, `next`, `done`, `changed`, `cancelled`, `needs-you`, and `active` for standing rules. A request sent twice is recorded once. IDs are never reused. One Python file, standard library only.

</details>

<br>

## FAQ

<details>
<summary><b>What does "layering" or "queueing" a message mean?</b></summary>

<br>

Sending another message while the AI is still working on the last one. In Claude Code, press **Enter** while Claude works and the message is queued; Claude Code hands it over as soon as the current tool calls finish, in the same turn ([docs](https://code.claude.com/docs/en/interactive-mode)). On the phone you see **Queue for after this turn**. In chat apps it is simply several messages in a row.

</details>

<details>
<summary><b>Will it make every reply longer?</b></summary>

<br>

No. For a single simple request nothing changes. When you asked for two or more things, it adds one line up front and a check at the end of five lines or fewer.

</details>

<details>
<summary><b>Will it keep asking me to confirm things?</b></summary>

<br>

Rarely. Most "clashes" are just corrections, and the newest message wins. It only asks when a new message breaks a rule you set earlier and getting it wrong would cost something, like a discount below your price floor. Even then it does the safe version straight away and lets you override with one word.

</details>

<details>
<summary><b>I type badly on my phone. Will it nag me?</b></summary>

<br>

Never. It reads for what you meant and never comments on spelling. It only checks with you when a word could mean two different things that lead to different results, like two products with the same name.

</details>

<details>
<summary><b>How is this different from other ledger or to-do skills?</b></summary>

<br>

Most keep a list of tasks across sessions. Juggle is about the moment a new message lands: what kind it is, whether to merge, queue, reorder or stop, how to protect the original request, and how to spot a clash with your own earlier rules. The list is a small part of it, and it is optional.

</details>

<details>
<summary><b>Does it work with Seatbelt?</b></summary>

<br>

Yes. [Seatbelt](https://github.com/HYDERMAA/seatbelt) keeps the building safe, Juggle keeps your requests intact. They do not overlap.

</details>

<details>
<summary><b>Is anything sent anywhere?</b></summary>

<br>

No. The skill is text, and the ledger script writes one local file. No accounts, no installs, nothing leaves your computer.

</details>

<br>

<p align="center">
  <img src="assets/readme/footer.svg" alt="Juggle. Free and open source under the MIT licence. Made by Hyder." width="100%">
</p>

<p align="center"><a href="#top">Back to top</a> &nbsp;·&nbsp; <a href="LICENSE">MIT licence</a> &nbsp;·&nbsp; <a href="evals/real/README.md">How it is tested</a></p>
