# Mission 1 · The chatbot that wasn't

<div class="fde-mission" markdown>
**Module 1: Discovery and decomposition**<br>
<span class="fde-meta"><span class="fde-pill">6–10 hours</span><span class="fde-pill">Easy + Stretch paths</span><span class="fde-pill">Gate: scope signed off</span></span>
</div>

<figure class="fde-video" markdown>
<video controls preload="metadata" poster="../../assets/videos/01-the-ask-is-not-the-problem.jpg">
  <source src="../../assets/videos/01-the-ask-is-not-the-problem.mp4" type="video/mp4">
</video>
<figcaption>Watch first (2½ minutes): the ask is not the problem.</figcaption>
</figure>

## Your first email from the client

<div class="fde-email" markdown>
<div class="fde-head">From: Dana Okafor, VP Operations · Subject: Kickoff — AI for fulfillment</div>

Our support team is drowning in "where's my order?" calls. What I'm picturing is an **AI chatbot on our customer portal** that answers order-status questions 24/7… Operationally we're in decent shape. **We ship about 94% of orders on time.** We have $180K approved. I'd like to see something working before Thanksgiving.
</div>

Ten minutes later, a Slack message from Renee, who runs support:

<div class="fde-email" markdown>
<div class="fde-head">Renee Alvarez · Slack</div>

a chatbot isn't going to fix this. people don't call because they can't find tracking. they call because the order is LATE and nobody told them.
</div>

**Your mission:** before anyone writes a line of code, find out who's right, uncover what's really going on, and write a scope that Ridgeway's VP will sign.

By the end you'll be able to:

- separate what a customer *asks for* from the problem they *have*
- test claims against data before you build on them
- run a discovery call that surfaces facts nobody wrote down
- write a short scope with measurable goals
- break any vague problem into a plan in 30 minutes (a classic FDE interview round)

---

## Lesson

!!! tutor "Learning with an AI agent?"
    Say **"Teach me Module 1"** and your tutor walks you through this lesson one piece at a time, with a quick question after each. Prefer reading? Everything is below.

### 1. The ask is not the problem

Customers describe a **solution** they've imagined: "We want a chatbot." Behind it is a **problem**: too many "where's my order?" calls (logistics people call them **WISMO**), late orders, lost customers. Your job is to find the problem first, then decide whether their solution is the best first move.

The question that gets you there: **"If this worked perfectly, what would be different?"** Keep asking until the answer is measured in money, hours or risk.

> Dana: "A chatbot." → *What would be different?* → "Fewer where's-my-order calls." → *Why do they call?* → "Orders are late and nobody tells them." → *What does that cost?* → "Credits we pay hospitals, and hospitals that leave."

That last answer is the problem. The chatbot was one possible fix.

??? question "Check yourself: Greg from IT says \"We need a new data warehouse.\" Ask the magic question twice. What might the real problem be?"
    For example: *What would be different?* "Reports would be faster." *Why does that matter?* "Finance can't close the month on time." The real problem might be the month-end close, and a warehouse is one possible fix. Any chain that ends in money, hours or risk is a good answer.

### 2. Wear three hats

| Hat | Asks | Forget it and… |
| --- | --- | --- |
| **Engineer** | Can we build it, with this data, in this environment? | You promise something the client's systems can't support |
| **Consultant** | Is this the right problem, and who must say yes? | You build the sponsor's idea and nobody uses it |
| **Product scout** | What here should become part of our product? | Every project is a one-off and your company can't scale |

??? question "Check yourself: Greg from IT says there's no API to the ERP, only nightly CSV files. Which hat cares most?"
    The engineer hat. It changes what you can build and how fresh the data can be.

### 3. Map the people

For each person, ask two things: **can they stop or fund this?** (power) and **does it change their day?** (interest).

- **Dana** (VP) has power: she owns the budget.
- **Renee** (support) has interest: her team lives with the result.
- **Greg** (IT) can veto anything that fails security.
- **Linda** (CFO) decides whether there's a phase 2.
- And watch for who's **missing from the invite list**. Boise's warehouse has been "rough since summer"; nobody invited its manager.

??? question "Check yourself: who could quietly kill this project even if Dana loves it?"
    Greg (fails the security review) or Linda (no phase-2 money). Renee too, if her team simply doesn't use what you build.

### 4. Pick metrics that matter, and check their definitions

A good success metric is **specific, measured today, owned by someone, and tied to money**.

- ❌ "Improve customer experience"
- ✅ "Raise hospital (Tier 1) delivered-on-time from today's baseline to 85% by March, measured from carrier delivery scans, owned by Dana"

Now the trap. **"On time" can mean very different things:**

| Definition | Measures | Can look like |
| --- | --- | --- |
| Shipped within 1 business day of the order | The warehouse | 94% 🎉 |
| Delivered by the date we promised | The customer's experience | …you'll find out in the lab |

Same company, same week, very different story. **Always ask how a number is calculated before you build on it.**

??? question "Check yourself: why might a company honestly report 94% on time while customers are angry?"
    It's measuring when orders *leave the warehouse*, not when they *arrive*. Delays after shipping (carriers, backorders shipped later) never show up in that number.

### 5. Decompose before you solve

This five-step framework is how FDEs attack vague problems, and it's also an interview round at companies like Palantir, where many candidates fail by jumping to a solution.

1. **Clarify the goal.** Restate it. Ask what success looks like, and by when.
2. **Stakeholders and metrics.** Who wins, who loses, who decides. How it's measured today.
3. **Inputs.** What data exists, who owns it, how fresh and how messy it is, how you get access.
4. **Subproblems.** Break it into 4–7 pieces. Order them by *value × confidence ÷ effort*, riskiest assumption first.
5. **Walking skeleton.** The thinnest end-to-end version that proves value in days. Then how it grows.

Say your assumptions out loud. Name what could go wrong. **Never jump to step 5 before steps 1–3.**

??? question "Check yourself: what's the most common way people fail a decomposition interview?"
    Jumping straight to a technical solution ("I'd build a RAG pipeline…") before clarifying the goal, the people and the data.

### 6. Run a good discovery call

- **Open** with the agenda and the outcome you want from the call.
- **Ask open questions.** Not "Would a dashboard help?" but "Walk me through the last time a hospital called about a late order."
- **Ask for artifacts**: the spreadsheet, the screenshot, the email thread. They beat opinions.
- **Close** by replaying what you heard, the next step, and who owns it.

??? question "Check yourself: rewrite this leading question as an open one: 'Would a chatbot reduce your call volume?'"
    For example: "What are customers trying to find out when they call?" or "Walk me through the last five calls your team took."

---

## Real-world twin: when the data dictionary warns you

Before you look at Ridgeway, try the same trap on **real data**. `real-data/scms/` holds USAID's delivery history for HIV/AIDS medicines shipped to 43 countries (2006–2015), unmodified.

Its data dictionary says the `Scheduled Delivery Date` column "should not be used to determine on-time performance." Calculate the on-time rate with it anyway, and also the share of shipments delivered *exactly* on the scheduled date. Then ask yourself why the second number is so high, and what that means for the first.

!!! tip "Hint"
    The file has old-style carriage-return line endings and a byte-order mark. `pd.read_csv(path, encoding="utf-8-sig")` handles both.

---

## Lab

Everything lives in `modules/01-discovery/`. You write only in `submission/`.

### Step 1 · Read the inbox · 30 min

Read the five messages in `inbox/` and `ridgeway/CLIENT_PROFILE.md`. For each person, jot down what they want and where they disagree with someone else.

### Step 2 · Check the numbers before the call · 1–2 hours

FDEs don't walk into a kickoff blind. Copy `templates/answers.json` to `submission/answers.json`, fill in the Easy keys (and the Stretch keys if you take that path; leave the rest `null`), and keep your code in `submission/sanity_checks.py` (or `.ipynb` / `.sql`). Write it to run from the repo root, e.g. `python3 modules/01-discovery/submission/sanity_checks.py`, so anyone can re-run it on a fresh copy.

Business days, holidays and the 3 pm cutoff are defined in `ridgeway/CLIENT_PROFILE.md`.

=== "Easy path"

    1. **Dana's 94%.** Of the orders that shipped, what share had their *first* shipment within 1 business day of the order date? (Use the calendar date the order was placed; ignore the 3 pm cutoff for this check.) Does it match her number?
    2. **Ticket mix.** What share of all support tickets are labelled "Order Status"? Do you trust that label? (Re-read Renee's message.)
    3. **Backorders.** Purchasing says about 4% of *lines* are backordered. Counting a line as backordered if its backorder flag is `Y`, and ignoring returned and cancelled lines, what share of *orders* contain at least one backordered line? Why are the two numbers so different?
    4. **Real-world twin.** The two SCMS numbers from the section above.

=== "Stretch path"

    Everything in Easy, plus:

    5. **Delivered on time.** What share of orders were fully delivered by their promise date? You'll need all three delivery sources: ParcelPro, Cascade Freight and the fleet log. Two rules, as an FDE would agree them with the client:
        - Judge only orders whose outcome you can determine, and note your **coverage** (the share of orders you could judge). An order you can't match to any delivery is "unknown", not late.
        - An order that still had a line on backorder in its snapshot (taken on the 3rd of the next month), after its promise date had passed, is late even without a delivery record.
    6. **Boise.** The same, for orders from the Boise warehouse. When did it get worse?
    7. **Money.** Hospital (Tier 1) contracts give a 2% credit on late orders. What did that cost Ridgeway in six months?

!!! warning "The data fights back"
    This is a client's real-world export, so expect mess. Nobody will tell you what's wrong with it. Finding the traps is part of the job, and part of your grade.

Check yourself any time:

```bash
python3 tools/fde.py check 01
```

It tells you which numbers are right, and for wrong ones whether you're too high or too low, with a hint. It never shows the answer.

### Step 3 · Prepare the kickoff · 20 min

Copy `templates/discovery_notes.md` to `submission/discovery_notes.md`. Write your agenda, what the data told you, and your **top 10 questions, in order**.

### Step 4 · Run the kickoff call · 30 min · role-play

Say to your AI tutor: **"Start the kickoff call with Dana."**

Dana has 45 minutes and strong opinions. She answers only what you ask. Some of what she believes is wrong, and one key fact is held by someone who wasn't invited. You can ask her to bring in Renee, Greg or Linda.

Take notes in `submission/discovery_notes.md` as you go. When the call ends, your tutor steps out of character and debriefs you.

### Step 5 · Write the scope · 2–3 hours

Copy `templates/scoping_doc.md` to `submission/scoping_doc.md`. **Two pages maximum.** It needs:

- [ ] the problem in one sentence
- [ ] your recommendation, including what you'd do **instead of or alongside** the chatbot, and why
- [ ] success metrics with **baselines from the data**
- [ ] in scope and **out of scope**
- [ ] a data inventory
- [ ] a 4-week plan with something demo-able each week
- [ ] risks, each with an owner

### Step 6 · Two decomposition drills · 2 × 30 min

Pick two of the three cases in `drills/decomposition_drills.md`. Set a 30-minute timer for each and save them as `submission/drill_1.md` and `drill_2.md`. Or say **"Give me a drill"** and your tutor invents a fresh client.

### Step 7 · The gate · 10 min · role-play

Say **"Grade Module 1"** for your rubric score, then **"Present the scope to Dana."** She'll push back three times. Hold your ground with evidence and she signs.

---

## Rubric

| Dimension | Points | Full marks looks like |
| --- | --- | --- |
| Customer outcome | 25 | The problem names what's really driving the calls, with a cost (dollars or support hours); metrics have baselines |
| Engineering quality | 25 | Your checks run from a fresh copy; each number shows how it was calculated; you caught the data traps |
| Evidence | 20 | You corrected at least one claim from the inbox with data, in plain words |
| Communication | 20 | Dana could forward your scope to the CFO unchanged; two pages max |
| Judgment | 10 | A clear call on the chatbot, explicit out-of-scope items, risks with owners |

Both paths can earn full marks: on the Easy path, use cost in support hours instead of dollars, and correct a claim like the backorder rate or the ticket labels.

The two **decomposition drills** get separate feedback (20 points for each step of the framework). They're required, but they don't change your module score.

**70 passes.** Pass the gate role-play too, and you're ready for Mission 2.

## Achievements

Your tutor awards these when you earn them, and records them in `PROGRESS.md`. No partial credit, no asking for them.

| Achievement | How to earn it |
| --- | --- |
| 🕵️ **Trap Spotter** | Find and handle at least five problems in Ridgeway's data, unprompted |
| 📏 **Definition Detective** | Explain, with numbers, why Dana's 94% isn't what she thinks it is |
| 🌍 **Real-World Twin** | Explain why so many USAID shipments arrive "exactly" on schedule |
| 🗺️ **The Missing Stakeholder** | Get the person who wasn't invited on a call, and learn what they know |
| ✂️ **Scope Surgeon** | Write an out-of-scope list that survives Dana's pushback |
| 🏁 **Gate Cleared** | Dana signs your scope |

## Words you met

| Term | Meaning |
| --- | --- |
| **FDE** | Forward Deployed Engineer: an engineer embedded with a customer to scope, build and ship what they need |
| **WISMO** | "Where is my order?", the most common support question in logistics |
| **Backorder** | An item ordered but out of stock, shipped later |
| **SLA / promise date** | The delivery date the contract commits to |
| **Walking skeleton** | The thinnest version of a system that works end to end |
| **Tier 1** | Ridgeway's hospital customers, promised next-day delivery |
