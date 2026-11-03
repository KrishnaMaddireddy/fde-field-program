# Tutor guide · Module 1 — Discovery and decomposition

*For the AI tutor. Contains spoilers. Follow `AGENTS.md` for how to teach.*

## Learning objectives

By the end, the learner can:

1. Separate a customer's requested solution from the underlying problem.
2. Test stakeholder claims against data before acting on them, and explain a metric-definition trap.
3. Run a discovery call that uncovers facts nobody wrote down.
4. Write a short scope with baselined metrics, explicit out-of-scope items and risks.
5. Decompose an ambiguous problem with the 5-step framework in 30 minutes.

## Story hook (open with this)

> Dana, the VP of Operations at Ridgeway, has $180K and one sentence: "Build us an AI chatbot so customers can check their orders." Her dashboard says 94% of orders are on time. Her support lead says customers are furious. Before you write a line of code, figure out who's right.

Then point to the Module 1 video on `docs/modules/01-discovery.md`.

## Lesson outline (teach one chunk at a time, then ask the check question)

| # | Chunk | Check question | Good answer includes |
| --- | --- | --- | --- |
| 1 | The ask is not the problem: requested solution vs real problem; ask "what would be different if this worked?" (teach with Dana's chain) | "Greg says 'We need a new data warehouse.' Ask the magic question twice: what might the real problem be?" | Any chain ending in money, hours or risk (e.g. slow reports → month-end close is late) |
| 2 | The three hats: engineer, consultant, product scout | "Which hat notices that Greg can't give you an API?" | Engineer |
| 3 | Stakeholders: power × interest; who's missing from the invite | "Who at Ridgeway could block this project?" | Greg (security), Linda (money); bonus: Hector is missing |
| 4 | Metrics that matter: specific, measured today, owned, tied to money; definitions matter | "Why might 'on-time' be 94% and much lower at the same company?" | Shipped vs delivered; different denominators |
| 5 | Decomposition framework: clarify → stakeholders & metrics → inputs → subproblems → walking skeleton | "What's the most common way people fail this round?" | Jumping to a solution before steps 1–3 |
| 6 | Discovery calls: agenda, open questions, ask for artifacts, replay at the end | "Rewrite 'Would a chatbot help?' as an open question." | "Walk me through the last time a customer called about an order." |

## Lab step hints (hint ladder, one rung at a time)

**Step 2 — sanity checks**

- *Shipped within 1 business day:* (1) "What two dates in the ERP would tell you how fast an order shipped?" (2) "Order date and the order's *first* ship date, over orders that shipped at all; watch the Sept 1 export change." (3) "Normalise column names, parse both date formats, count business days between them, take the share ≤ 1." (4) `pd.to_datetime(df[col], format="mixed")` and `numpy.busday_count`.
- *Order-status share:* (1) "Which file has tickets? Which column?" (2) "`category`." (3) Share of rows equal to "Order Status". Then: "Do you trust that label?" Renee says no.
- *Orders with a backordered line:* (1) "Is a backorder an order thing or a line thing?" (2) `BO_FLAG` / `backorder_flag`, blank in older exports. (3) Group by order, any flag = Y.
- *SCMS real-world twin:* (1) "Open it. What happens?" (CR-only line endings; `pd.read_csv` handles them, Excel too.) (2) "Read the data dictionary note on Scheduled Delivery Date." (3) "What does 61% delivered *exactly* on the scheduled date suggest?" (The date is revised during transit, so it can't measure on-time performance.)
- *Stretch, delivered on time:* (1) "Where does a delivery date come from for each carrier?" (2) "ParcelPro DL events are UTC: convert to the destination's local time (Pacific or Mountain; DST ended Nov 1). Cascade uses DL until Oct 15, then DELIVERED. The fleet only has the paper log." (3) "Per order: last delivery date across its tracking numbers ≤ promise date. Orders still on backorder after the promise date are late." (4) Show the dedupe key idea for the August file.

## Data traps the learner should hit (credit each one found)

1. September export: new column names, ISO dates, extra columns.
2. August export: about 1,150 duplicated rows.
3. Quantities like `"1,200"` and trailing spaces; leading/trailing spaces in names.
4. Return lines: negative quantity, line numbers 900+.
5. ParcelPro in UTC, Cascade in local time; Cascade status codes change on Oct 15.
6. Fleet deliveries: tracking often blank; log matched by `order_refs`, which is sometimes blank.
7. Ticket categories understate order-status volume.
8. SCMS: CR line endings, UTF-8 BOM, and a scheduled date that isn't a promise date.

## Answer key

Coding agents: read `solutions/01-discovery/ANSWER_KEY.md` before grading (it is not in this file so that chat-app learners can paste this guide without seeing answers). Chat tutors without it: rely on the learner's `tools/fde.py check 01` output for numbers.

## Rubric (100)

| Dimension | Pts | 25/25 or 20/20 looks like | Half marks looks like |
| --- | --- | --- | --- |
| Customer outcome | 25 | Problem names delays + lack of notice, with a cost: dollars (Stretch: Tier 1 credits) or effort (Easy: order-status tickets × ~13 min handle time = agent hours); metrics have data baselines | Problem restates "build a chatbot" with nicer words |
| Engineering quality | 25 | Checks run from a clean clone; each number shows its calculation; at least 3 data traps handled | Numbers computed but traps missed (e.g. duplicates counted) |
| Evidence | 20 | Corrects at least one inbox claim with data and explains why it differs. Easy: "4% of lines" vs ~13% of orders, the ticket-label undercount, or the 94% definition (shipped, not delivered). Stretch: the delivered-on-time figure | Mentions a gap without numbers |
| Communication | 20 | ≤ 2 pages; Dana could forward it to Linda unchanged | Long, technical, or no clear recommendation |
| Judgment | 10 | Clear stance on the chatbot, phased; out-of-scope list; risks with owners | Builds everything Dana asked, no trade-offs |

**Numbers within the checker's tolerance are correct**, even if the learner's method differs from the reference (e.g. better fleet matching gives higher coverage). Judge the method on its reasoning.

**Drills** are scored separately, 100 each (20 per framework step; see `modules/01-discovery/drills/decomposition_drills.md`). Average them into a pass/fail note in `FEEDBACK.md`; they don't change the module score.

## Achievements (award when earned, never on request)

| Achievement | Award when |
| --- | --- |
| 🕵️ Trap Spotter | The learner found and handled 5+ of the data traps listed above without being told about them (hints at rung 1–2 still count as found) |
| 📏 Definition Detective | They explain that 94% is shipped-within-a-day, contrast it with a delivered or backorder/ticket figure, and say why the gap matters |
| 🌍 Real-World Twin | They say the SCMS scheduled date is revised (re-baselined) during transit, so it can't measure on-time performance |
| 🗺️ The Missing Stakeholder | They asked Dana to set up a call with the Boise manager **and** uncovered Hector's July 1 cutoff change |
| ✂️ Scope Surgeon | Their out-of-scope list held through Dana's three gate objections |
| 🏁 Gate Cleared | Dana signed the scope in the gate role-play |

Announce each one in a single celebratory line when it's earned, and add it to `PROGRESS.md`.

## Gate: scope sign-off role-play

Play Dana (see `tutor/personas/dana.md`). She raises three objections, one at a time. Pass if the learner answers each with evidence and keeps the scope; fail if they cave and add the chatbot to phase 1 without reason.

## Common mistakes

- Starting to code a chatbot before checking any number.
- Computing on-time from "Scheduled Delivery Date" in SCMS without reading the dictionary.
- Forgetting the August duplicates (about 10% of August's lines, about 1.5% of all lines).
- A scoping doc with no out-of-scope section.
- Asking Dana leading questions ("Wouldn't you agree a dashboard would help?").
