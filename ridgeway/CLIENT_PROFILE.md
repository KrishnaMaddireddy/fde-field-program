# Ridgeway Medical Supply — client profile

*Fictional company. Prepared by your account team before the engagement. Everything here is what Ridgeway told sales; not all of it has been verified.*

## The company

- Regional distributor of medical and surgical supplies, founded 1994, privately held.
- About 1,400 customer accounts in OR, WA, CA, NV, ID, UT and MT: hospitals, surgery centers, clinics and long-term care facilities.
- 3 distribution centers (DCs): **Portland (PDX)**, **Sacramento (SMF)**, **Boise (BOI)**.
- Around 300 active SKUs across gloves, sutures, IV therapy, wound care, PPE, catheters, antiseptics and diagnostics.
- Roughly 800 orders per business week.

## Service promise (from the standard customer contract)

| Customer tier | Typical customer | Delivery promise |
| --- | --- | --- |
| Tier 1 | Hospitals | Next business day |
| Tier 2 | Surgery centers, most clinics | 2 business days |
| Tier 3 | Smaller clinics, long-term care | 3 business days |

Orders received by **3:00 pm local time** count as received that business day. Business days are Monday–Friday, except Ridgeway's holidays in this period: **May 25, July 3 and September 7, 2026**. Tier 1 contracts include a **late-delivery credit of 2% of order value**.

## People you will meet

| Name | Role | What sales heard from them |
| --- | --- | --- |
| Dana Okafor | VP Operations, your sponsor | Wants "an AI answer" to fulfillment problems; owns the budget |
| Renee Alvarez | Customer Support Lead (team of 6) | Overloaded; skeptical of chatbots |
| Greg Tanaka | IT Manager (team of 2) | Protective of the ERP; worried about security reviews |
| Linda Marsh | CFO | Signs off on spend; wants ROI in dollars |
| Hector Ruiz | Boise DC Manager | Not on the kickoff invite |

## Systems

| System | What it holds | How you get data |
| --- | --- | --- |
| DistriOne 7 (ERP, on-premises) | Orders, lines, promise dates, ship dates, tracking numbers | Nightly CSV export, no API. You get month-end snapshots saved on the 3rd of the next month. Upgraded Sept 1. |
| ParcelPro (parcel carrier) | Parcel tracking events | JSON event feed |
| Cascade Freight (LTL carrier) | Freight tracking events | JSON event feed |
| RMS Fleet (own trucks) | Hospital deliveries in metro areas | Drivers' paper logs, typed into a spreadsheet |
| Customer list (CRM) | Accounts, tiers, home DC | CSV export |
| Shared help-desk inbox | Support tickets | CSV export |
| SharePoint | SOPs, contracts, policies | Arrives in Module 4 |

Everything in `data/raw/` is what Greg exported for you: orders placed May 1 – Oct 31, 2026, plus carrier events, fleet logs and tickets up to Friday, November 6, when he pulled them. The engagement kicks off on Monday, November 9.
