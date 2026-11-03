# Module 1 answer key (SPOILERS)

*For the AI tutor when grading. Never quote these numbers to the learner; `tools/fde.py check 01` gives them feedback.*

Exact figures: run `python3 solutions/01-discovery/reference.py` from the repo root.

## What the numbers mean

- Dana's "94%" is **shipped within 1 business day**. **Delivered by the promise date is about 75%.** Boise is worst (about 68–69%) and fell from July.
- About 13% of orders contain a backordered line, though only ~4% of lines are backordered. That's how backorders hit far more customers than "4%" suggests.
- Labelled order-status tickets are 36% of volume; the true share is closer to 42% (Renee).
- Tier 1 late credits are about $300–360K in six months, roughly $650K a year.
- Easy-path cost figure: labelled order-status tickets took about 390 agent-hours in six months (about 460 if you add the mislabelled ones), roughly a third of one support agent's time.
- Root causes of lateness: backorders (about half), Cascade Freight delays on Boise lanes, Boise's undisclosed 1 pm cutoff (Hector), and normal transit misses.

## What a strong scoping doc recommends

- **Problem:** customers aren't told about delays (mostly backorders and Cascade/Boise), which drives ~40% of support volume and ~$650K a year in Tier 1 credits, and is costing hospital accounts.
- **Phase 1 (pilot):** one trustworthy order-status view joining ERP, carriers and fleet; an internal "one screen" lookup for support agents; proactive, human-reviewed delay and backorder notices to Tier 1 customers.
- **Non-AI fixes flagged to ops:** Boise cutoff, Cascade performance. The FDE doesn't own these but must surface them.
- **Phase 2:** customer-facing chatbot, once the data behind it is right.
- **Metrics with baselines:** Tier 1 delivered on time (~74%), WISMO tickets per week, WISMO handle time (~13 min), Tier 1 credit exposure per month.
- **Risks:** data quality (fleet), PII in tickets (Greg), adoption by support (Renee), board expectations (Dana).


