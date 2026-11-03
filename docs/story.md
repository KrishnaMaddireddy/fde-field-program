# Meet Ridgeway

!!! info "Fictional client, real problems"
    Ridgeway Medical Supply and everyone in it are invented for this course. The problems are ones FDEs meet every week, and each mission pairs Ridgeway with a real public dataset (its *real-world twin*).

**Ridgeway Medical Supply** distributes gloves, sutures, IV sets, wound care and other supplies to about 1,400 hospitals, surgery centers, clinics and care homes across the Pacific Northwest and Mountain West. It runs three warehouses, in **Portland, Sacramento and Boise**, and roughly 800 orders leave them every business week.

Hospitals are promised next-day delivery. Lately, many aren't getting it, and two hospital accounts have walked away this year. The VP of Operations has a budget, a board that wants "an AI story", and you.

## The cast

<div class="fde-cast" markdown>

<div class="fde-person" markdown>
<div class="fde-avatar" style="background:#0f5257">DO</div>
<div markdown><strong>Dana Okafor</strong><span>VP Operations · your sponsor. Confident, busy, has promised the board a chatbot.</span></div>
</div>

<div class="fde-person" markdown>
<div class="fde-avatar" style="background:#e8833a">RA</div>
<div markdown><strong>Renee Alvarez</strong><span>Support lead · team of 6. Overloaded, blunt, allergic to chatbots.</span></div>
</div>

<div class="fde-person" markdown>
<div class="fde-avatar" style="background:#5b6c8f">GT</div>
<div markdown><strong>Greg Tanaka</strong><span>IT manager · team of 2. Careful, protective of the ERP, burned by vendors before.</span></div>
</div>

<div class="fde-person" markdown>
<div class="fde-avatar" style="background:#8a5a83">LM</div>
<div markdown><strong>Linda Marsh</strong><span>CFO. Polite, precise, believes numbers, not adjectives.</span></div>
</div>

<div class="fde-person" markdown>
<div class="fde-avatar" style="background:#6f7d3c">HR</div>
<div markdown><strong>Hector Ruiz</strong><span>Boise warehouse manager. Not on the invite list. Knows something important.</span></div>
</div>

</div>

## Their systems

| System | What it holds | How you get the data |
| --- | --- | --- |
| DistriOne 7 (ERP) | Orders, lines, promise and ship dates, tracking numbers | Month-end snapshots of a nightly CSV export. The format changed on Sept 1. |
| ParcelPro | Parcel tracking events | JSON lines, timestamps in UTC |
| Cascade Freight | Freight tracking events | JSON lines, local time, codes changed mid-October |
| RMS Fleet | Ridgeway's own trucks to hospitals | A typed-up paper log |
| CRM | Customers, tiers, home warehouse | CSV |
| Help desk | Support tickets | CSV with free text |

All of it lives in `ridgeway/data/raw/`: six months, about 20,000 orders and 5,200 tickets, with the mess you'd expect from a real client.
