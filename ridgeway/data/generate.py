#!/usr/bin/env python3
"""
Ridgeway Medical Supply -- simulated client data generator.

Ridgeway is a FICTIONAL company. Every name, number and record here is invented
for the FDE Field Program. The data is deliberately messy, the way real client
exports are: inconsistent names, mixed date formats, schema drift, duplicates,
missing keys, and two carriers that disagree on how to report time.

Usage:
    python3 generate.py                # writes ./raw/...
    python3 generate.py --out DIR      # writes DIR/...
    python3 generate.py --truth        # also writes the instructor answer key

Standard library only. Deterministic: same seed -> same files.
"""
import argparse
import csv
import datetime as dt
import json
import os
import random

SEED = 20261102
START = dt.date(2026, 5, 1)
END = dt.date(2026, 10, 31)
HOLIDAYS = {dt.date(2026, 5, 25), dt.date(2026, 7, 3), dt.date(2026, 9, 7)}
CASCADE_CODE_CHANGE = dt.date(2026, 10, 15)   # carrier switches status codes
ERP_SCHEMA_CHANGE = dt.date(2026, 9, 1)       # ERP upgrade renames columns
BOI_EARLY_CUTOFF_FROM = dt.date(2026, 7, 1)   # Boise staffing change
DATA_PULLED = dt.datetime(2026, 11, 6, 17, 0)  # Greg pulled carrier, fleet and ticket data (story "today" is Mon Nov 9)
DST_ENDS_UTC = dt.datetime(2026, 11, 1, 9, 0)  # 2 am Pacific / 1 am Mountain on Nov 1, 2026, roughly
MOUNTAIN = {"ID", "UT", "MT"}


def utc_offset(state, local_dt):
    """Hours to add to UTC to get local time at a destination in `state` (US DST rules, 2026)."""
    std = -7 if state in MOUNTAIN else -8
    return std + (1 if local_dt < dt.datetime(2026, 11, 1, 2, 0) else 0)

DCS = {
    "PDX": {"city": "Portland", "states": ["OR", "WA"]},
    "SMF": {"city": "Sacramento", "states": ["CA", "NV"]},
    "BOI": {"city": "Boise", "states": ["ID", "UT", "MT"]},
}
CITIES = {
    "OR": ["Portland", "Salem", "Eugene", "Bend", "Medford", "Corvallis", "Gresham"],
    "WA": ["Vancouver", "Spokane", "Yakima", "Kennewick", "Olympia"],
    "CA": ["Sacramento", "Roseville", "Chico", "Redding", "Stockton", "Davis", "Modesto"],
    "NV": ["Reno", "Carson City", "Sparks"],
    "ID": ["Boise", "Nampa", "Meridian", "Idaho Falls", "Pocatello", "Twin Falls"],
    "UT": ["Ogden", "Logan"],
    "MT": ["Missoula", "Bozeman"],
}
SAINTS = ["Mary's", "Joseph's", "Luke's", "Vincent's", "Anne's", "Francis", "Alphonsus", "Charles"]
WORDS = ["Valley", "Riverside", "Summit", "Cascade", "Pinecrest", "Lakeview", "Harbor", "Mesa",
         "Cedar", "Willow", "Granite", "Sunrise", "Northgate", "Evergreen", "Highland", "Meadow",
         "Sagebrush", "Ridgecrest", "Bayside", "Foothill", "Canyon", "Prairie", "Silver Creek"]

CATEGORIES = {
    # category: (n_skus, price range, hazmat share)
    "Gloves": (40, (6, 28), 0.0),
    "Sutures": (45, (18, 140), 0.0),
    "IV Therapy": (40, (2, 45), 0.0),
    "Wound Care": (50, (3, 60), 0.0),
    "PPE": (35, (4, 40), 0.0),
    "Catheters": (30, (5, 90), 0.0),
    "Antiseptics": (25, (3, 25), 0.6),   # alcohol-based -> hazmat
    "Diagnostics": (35, (10, 220), 0.1),
}


def bday_add(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in HOLIDAYS:
            n -= 1
    return d


def is_bday(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def next_bday(d):
    return bday_add(d, 1)


def messy_name(rng, name):
    """How a carrier or a support agent might write the same customer."""
    v = name.upper().replace("'", "").replace(".", "").replace(",", "")
    v = v.replace("SAINT ", "ST ").replace("MEDICAL CENTER", "MED CTR").replace("HOSPITAL", "HOSP")
    v = v.replace("SURGERY CENTER", "SURG CTR").replace("CLINIC", "CLN")
    if rng.random() < 0.15:
        v = v.replace("ST ", "SAINT ")
    if rng.random() < 0.1:
        v = v + " - RECEIVING"
    return v


def build_customers(rng):
    customers = []
    cid = 10001
    plan = [("Hospital", 1, 1, 120), ("Surgery Center", 2, 2, 260),
            ("Clinic", 2, 2, 260), ("Clinic", 3, 3, 440), ("Long-Term Care", 3, 3, 320)]
    used = set()
    for ctype, tier, sla, n in plan:
        for _ in range(n):
            dc = rng.choices(["PDX", "SMF", "BOI"], weights=[42, 38, 20])[0]
            state = rng.choice(DCS[dc]["states"])
            city = rng.choice(CITIES[state])
            for _try in range(20):
                if ctype == "Hospital":
                    base = rng.choice([f"Saint {rng.choice(SAINTS)} Medical Center",
                                       f"{city} General Hospital", f"{rng.choice(WORDS)} Regional Medical Center",
                                       f"{rng.choice(WORDS)} Community Hospital"])
                elif ctype == "Surgery Center":
                    base = f"{rng.choice(WORDS)} Surgery Center"
                elif ctype == "Clinic":
                    base = rng.choice([f"{rng.choice(WORDS)} Family Clinic", f"{rng.choice(WORDS)} Urgent Care",
                                       f"{city} Pediatrics", f"{rng.choice(WORDS)} Orthopedic Clinic",
                                       f"{rng.choice(WORDS)} Dermatology"])
                else:
                    base = f"{rng.choice(WORDS)} {rng.choice(['Care Center', 'Senior Living', 'Rehabilitation'])}"
                name = base if base not in used else f"{base} - {city}"
                if name not in used:
                    break
            used.add(name)
            customers.append({
                "customer_id": f"C{cid}", "name": name, "type": ctype, "tier": tier,
                "contract_sla_bdays": sla, "city": city, "state": state, "home_dc": dc,
                "order_weight": {"Hospital": 9, "Surgery Center": 3}.get(ctype, 1.2 if tier == 2 else 0.7),
                "po_required": ctype in ("Hospital", "Surgery Center") or rng.random() < 0.2,
            })
            cid += 1
    return customers


def build_products(rng):
    products = []
    n = 1
    for cat, (k, (lo, hi), hz) in CATEGORIES.items():
        for _ in range(k):
            products.append({"sku": f"RMS-{cat.replace(' ', '')[:3].upper()}-{n:04d}", "category": cat,
                             "description": f"{cat} item {n:04d}",
                             "unit_price": round(rng.uniform(lo, hi), 2), "hazmat": rng.random() < hz})
            n += 1
    return products


def order_time(rng, day):
    hour = rng.choices(range(6, 19), weights=[2, 6, 9, 11, 12, 10, 8, 11, 12, 9, 6, 3, 1])[0]
    return dt.datetime.combine(day, dt.time(hour, rng.randrange(60), rng.randrange(60)))


def simulate(rng, customers, products):
    weights = [c["order_weight"] for c in customers]
    orders = []
    so = 400001
    day = START
    while day <= END:
        n = rng.randint(130, 170) if is_bday(day) else rng.randint(8, 25)
        for _ in range(n):
            c = rng.choices(customers, weights=weights)[0]
            ts = order_time(rng, day)
            dc = c["home_dc"] if rng.random() > 0.07 else rng.choice([d for d in DCS if d != c["home_dc"]])
            channel = rng.choices(["EDI", "Portal", "Phone", "Email/Fax"], weights=[35, 30, 20, 15])[0]
            nlines = rng.choices(range(1, 11), weights=[18, 20, 17, 13, 10, 8, 6, 4, 2, 2])[0]
            lines = []
            for ln, p in enumerate(rng.sample(products, nlines), start=1):
                qty = rng.choice([1, 2, 4, 5, 10, 12, 20, 24, 50, 100]) if p["category"] != "Gloves" else rng.choice([10, 20, 50, 100, 200, 1000, 1200])
                bo_rate = 0.035 + (0.06 if p["category"] == "Gloves" and dt.date(2026, 8, 1) <= day <= dt.date(2026, 9, 30) else 0)
                lines.append({"line_no": ln, "sku": p["sku"], "qty": qty, "unit_price": p["unit_price"],
                              "backorder": rng.random() < bo_rate, "cancelled": rng.random() < 0.006})
            # --- promise per contract: 3pm local cutoff, then SLA business days
            contract_day = day if (is_bday(day) and ts.hour < 15) else next_bday(day) if is_bday(day) else next_bday(day)
            promise = bday_add(contract_day, c["contract_sla_bdays"])
            # --- actual warehouse cutoff
            cutoff = 13 if (dc == "BOI" and day >= BOI_EARLY_CUTOFF_FROM) else 15
            pick_day = day if (is_bday(day) and ts.hour < cutoff) else next_bday(day)
            if rng.random() < 0.025:  # picking backlog / short staff
                pick_day = next_bday(pick_day)
            # --- carrier choice
            big = nlines >= 6 or sum(l["qty"] for l in lines) >= 600
            if c["type"] == "Hospital" and dc == c["home_dc"] and rng.random() < 0.9:
                carrier = "RMS Fleet"
            elif big:
                carrier = "Cascade Freight"
            else:
                carrier = "ParcelPro"
            any_bo = any(l["backorder"] for l in lines)
            split = any_bo and rng.random() < 0.55
            hold_days = rng.randint(2, 7) if any_bo else 0
            shipments = []
            def transit(carrier_):
                if carrier_ == "RMS Fleet":
                    return 1 if rng.random() < 0.97 else 2, None
                if carrier_ == "ParcelPro":
                    t = rng.choices([1, 2, 3, 4], weights=[80, 16, 3, 1])[0]
                    return t, ("WEATHER" if t >= 3 and rng.random() < 0.5 else "ADDRESS" if t >= 3 else None)
                t = rng.choices([2, 3, 4], weights=[60, 30, 10])[0]
                exc = None
                if dc == "BOI" and rng.random() < 0.18:
                    t += rng.randint(1, 3); exc = rng.choice(["MISSED LINEHAUL", "TERMINAL DELAY", "APPT REQUIRED"])
                elif rng.random() < 0.05:
                    t += 1; exc = "TERMINAL DELAY"
                return t, exc
            live = [l for l in lines if not l["cancelled"]]
            if not live:
                orders.append(dict(so=f"SO-{so}", customer=c, ts=ts, dc=dc, channel=channel, lines=lines,
                                   promise=promise, pick_day=pick_day, shipments=[], carrier=carrier, cutoff=cutoff))
                so += 1
                continue
            groups = []
            if not any_bo:
                groups.append((live, pick_day))
            elif split:
                groups.append(([l for l in live if not l["backorder"]], pick_day))
                groups.append(([l for l in live if l["backorder"]], bday_add(pick_day, hold_days)))
            else:
                groups.append((live, bday_add(pick_day, hold_days)))
            for g_lines, ship_day in groups:
                if not g_lines:
                    continue
                t, exc = transit(carrier)
                deliver_day = bday_add(ship_day, t)
                shipments.append({"lines": [l["line_no"] for l in g_lines], "ship_day": ship_day,
                                  "deliver_day": deliver_day, "exception": exc, "carrier": carrier,
                                  "tracking": None})
            orders.append(dict(so=f"SO-{so}", customer=c, ts=ts, dc=dc, channel=channel, lines=lines,
                               promise=promise, pick_day=pick_day, shipments=shipments, carrier=carrier,
                               cutoff=cutoff, po=(f"PO{rng.randint(10000, 99999)}" if c["po_required"] else "")))
            so += 1
        day += dt.timedelta(days=1)
    # tracking numbers
    for o in orders:
        for s in o["shipments"]:
            if s["carrier"] == "ParcelPro":
                s["tracking"] = "1PP" + "".join(rng.choice("0123456789ABCDEFGHJKLMNPRSTUVWXYZ") for _ in range(13))
            elif s["carrier"] == "Cascade Freight":
                s["tracking"] = f"CF{rng.randint(10**8, 10**9 - 1)}"
            else:
                s["tracking"] = f"FLT-{rng.randint(100000, 999999)}"
    return orders


def snapshot_day(month):
    """Greg saved the nightly export on the 3rd of the following month."""
    first = dt.date.fromisoformat(month + "-01")
    return (first.replace(day=28) + dt.timedelta(days=4)).replace(day=3)


def fmt_old(ts):
    return ts.strftime("%m/%d/%Y %H:%M")


def write_erp(rng, orders, out):
    os.makedirs(os.path.join(out, "erp"), exist_ok=True)
    by_month = {}
    for o in orders:
        by_month.setdefault(o["ts"].strftime("%Y-%m"), []).append(o)
    for month, os_ in sorted(by_month.items()):
        new_schema = dt.date.fromisoformat(month + "-01") >= ERP_SCHEMA_CHANGE
        if new_schema:
            header = ["order_no", "order_datetime", "customer_no", "customer_name", "po_number",
                      "fulfillment_ctr", "order_channel", "line_no", "sku", "qty", "unit_price",
                      "line_status", "backorder_flag", "ship_date", "tracking_no", "promise_date"]
        else:
            header = ["ORDER_NO", "ORDER_DATE", "CUST_NO", "CUST_NAME", "SHIP_DC", "CHANNEL",
                      "LINE_NO", "SKU", "QTY", "UNIT_PRICE", "LINE_STATUS", "BO_FLAG", "SHIP_DATE",
                      "TRACKING_NO", "PROMISE_DATE"]
        rows = []
        for o in os_:
            ship_of = {}
            for s in o["shipments"]:
                for ln in s["lines"]:
                    ship_of[ln] = s
            cname = o["customer"]["name"]
            if rng.random() < 0.08:
                cname = "  " + cname + " "
            for l in o["lines"]:
                s = ship_of.get(l["line_no"])
                export_cutoff = snapshot_day(month)
                if l["cancelled"]:
                    status, ship, trk = "CANCELLED", "", ""
                elif s and s["ship_day"] <= export_cutoff:
                    status, ship, trk = "SHIPPED", s["ship_day"], s["tracking"]
                    if s["carrier"] == "RMS Fleet" and rng.random() < 0.12:
                        trk = ""  # drivers often don't scan
                else:
                    status, ship, trk = "BACKORDER", "", ""
                qty = l["qty"]
                qty_s = f"{qty:,}" if qty >= 1000 and rng.random() < 0.5 else str(qty)
                if rng.random() < 0.01:
                    qty_s = qty_s + " "
                if new_schema:
                    row = [o["so"], o["ts"].isoformat(timespec="seconds"), o["customer"]["customer_id"], cname,
                           o.get("po", ""), o["dc"], o["channel"], l["line_no"], l["sku"], qty_s,
                           f"{l['unit_price']:.2f}", status, "Y" if l["backorder"] else "N",
                           ship.isoformat() if ship else "", trk, o["promise"].isoformat()]
                else:
                    row = [o["so"], fmt_old(o["ts"]), o["customer"]["customer_id"], cname, o["dc"],
                           o["channel"], l["line_no"], l["sku"], qty_s, f"{l['unit_price']:.2f}", status,
                           "Y" if l["backorder"] else "", ship.strftime("%m/%d/%Y") if ship else "", trk,
                           o["promise"].strftime("%m/%d/%Y")]
                rows.append(row)
        # returns: negative qty lines appended later in month
        for o in rng.sample(os_, k=max(1, len(os_) // 60)):
            l = rng.choice(o["lines"])
            q = -rng.randint(1, max(1, min(l["qty"], 20)))
            if new_schema:
                rows.append([o["so"], o["ts"].isoformat(timespec="seconds"), o["customer"]["customer_id"],
                             o["customer"]["name"], o.get("po", ""), o["dc"], o["channel"], 900 + l["line_no"], l["sku"], str(q),
                             f"{l['unit_price']:.2f}", "RETURN", "N", "", "", ""])
            else:
                rows.append([o["so"], fmt_old(o["ts"]), o["customer"]["customer_id"], o["customer"]["name"],
                             o["dc"], o["channel"], 900 + l["line_no"], l["sku"], str(q),
                             f"{l['unit_price']:.2f}", "RETURN", "", "", "", ""])
        if month == "2026-08":  # a re-run export appended part of the file twice
            rows += rows[2000:3150]
        with open(os.path.join(out, "erp", f"erp_order_lines_{month}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)


def write_carriers(rng, orders, out):
    os.makedirs(os.path.join(out, "carrier"), exist_ok=True)
    os.makedirs(os.path.join(out, "fleet"), exist_ok=True)
    pp, cf, fleet = [], [], []
    for o in orders:
        dc_state = {"PDX": "OR", "SMF": "CA", "BOI": "ID"}[o["dc"]]
        dest_state = o["customer"]["state"]
        for s in o["shipments"]:
            consignee = messy_name(rng, o["customer"]["name"])
            dest = f"{o['customer']['city'].upper()}, {o['customer']['state']}"
            pick_local = dt.datetime.combine(s["ship_day"], dt.time(rng.randint(15, 18), rng.randrange(60)))
            del_local = dt.datetime.combine(s["deliver_day"], dt.time(rng.randint(8, 16), rng.randrange(60)))
            if s["carrier"] == "ParcelPro":
                def utc(x, state):
                    return (x - dt.timedelta(hours=utc_offset(state, x))).strftime("%Y-%m-%dT%H:%M:%SZ")
                ev = [("PU", pick_local, DCS[o["dc"]]["city"].upper(), dc_state),
                      ("IT", pick_local + dt.timedelta(hours=6), "HUB", dc_state)]
                if s["exception"]:
                    ev.append(("EX", pick_local + dt.timedelta(hours=20), "HUB", dc_state))
                ev += [("OFD", del_local.replace(hour=7, minute=10), dest, dest_state), ("DL", del_local, dest, dest_state)]
                for code, t, loc, st in ev:
                    if t > DATA_PULLED:
                        continue
                    rec = {"tracking_number": s["tracking"], "status_code": code, "event_time": utc(t, st),
                           "location": loc, "consignee": consignee}
                    if code == "EX":
                        rec["exception_reason"] = s["exception"]
                    pp.append(rec)
            elif s["carrier"] == "Cascade Freight":
                new = s["ship_day"] >= CASCADE_CODE_CHANGE
                code_map = {"PU": "PICKED_UP", "IT": "IN_TRANSIT", "EX": "DELAY", "OFD": "OUT_FOR_DELIVERY", "DL": "DELIVERED"} if new else {}
                ev = [("PU", pick_local, f"{DCS[o['dc']]['city'].upper()} TERMINAL"),
                      ("IT", pick_local + dt.timedelta(hours=10), "LINEHAUL")]
                if s["exception"]:
                    ev.append(("EX", pick_local + dt.timedelta(hours=30), "LINEHAUL"))
                ev += [("OFD", del_local.replace(hour=6, minute=45), dest), ("DL", del_local, dest)]
                for code, t, loc in ev:
                    if t > DATA_PULLED:
                        continue
                    rec = {"pro_number": s["tracking"], "status": code_map.get(code, code),
                           "status_date": t.strftime("%Y-%m-%d %H:%M"),  # local time, no zone
                           "terminal": loc, "shipper_ref": o["so"] if rng.random() < 0.7 else (o.get("po") or ""),
                           "consignee_name": consignee, "pieces": len(s["lines"])}
                    if code == "EX":
                        rec["remarks"] = s["exception"]
                    cf.append(rec)
            else:
                if del_local > DATA_PULLED:
                    continue
                fleet.append({"delivery_date": s["deliver_day"].strftime("%m/%d/%y"),
                              "route": f"{o['dc']}-R{rng.randint(1, 9)}",
                              "stop_name": consignee.title() if rng.random() < 0.6 else o["customer"]["name"],
                              "signed_by": rng.choice(["J. RAMOS", "dock", "K LEE", "recv", "M.Ortiz", "", "SMITH"]),
                              "order_refs": o["so"] if rng.random() < 0.8 else "",
                              "time_delivered": del_local.strftime("%I:%M %p"),
                              "notes": rng.choice(["", "", "", "left at dock", "partial - see BO", "call ahead"])})
    rng.shuffle(pp)
    with open(os.path.join(out, "carrier", "parcelpro_events.jsonl"), "w") as f:
        for r in pp:
            f.write(json.dumps(r) + "\n")
    cf.sort(key=lambda r: r["status_date"])
    with open(os.path.join(out, "carrier", "cascade_freight_events.jsonl"), "w") as f:
        for r in cf:
            f.write(json.dumps(r) + "\n")
    with open(os.path.join(out, "fleet", "fleet_delivery_log.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fleet[0].keys()))
        w.writeheader()
        w.writerows(fleet)


WISMO_SUBJECTS = ["Where is my order?", "Order status", "RE: missing delivery", "Still waiting on supplies",
                  "URGENT - OR supplies not here", "tracking?", "Shipment late again", "When will this arrive"]
WISMO_BODIES = [
    "Hi, we placed order {ref} on {day} and it still hasn't arrived. Can you tell me when to expect it?",
    "Our {cat} order from {day} is not here. We were told next day. Please advise. {ref}",
    "This is the third time this month a delivery has been late. Order {ref}. Who can I talk to?",
    "Can I get tracking for {ref}? The portal just says shipped.",
    "We are almost out of {cat} in the OR. The order from {day} ({ref}) needs to arrive today.",
    "Hello - checking on our order from {day}. I don't have the order number handy, it was for {cat}.",
    "Part of our order came but the {cat} were missing. {ref}",
]
OTHER = {
    "Returns": (["Return request", "RMA for damaged box", "Wrong item shipped"],
                ["We received the wrong {cat}, need to return. {ref}", "Box arrived crushed, requesting RMA for {ref}."]),
    "Billing": (["Invoice question", "Credit memo?", "Pricing discrepancy"],
                ["Invoice for {ref} shows the wrong price on {cat}.", "We were double billed for {ref}."]),
    "Product": (["Substitute for backordered item?", "Latex-free options", "Product spec sheet"],
                ["Is there a substitute for the {cat} on backorder?", "Do you carry latex-free {cat}?"]),
    "Account": (["Update ship-to address", "Add a new buyer", "Portal login"],
                ["Please add our new purchasing contact to the account.", "I can't log into the portal."]),
}


def write_tickets(rng, orders, products_by_sku, out):
    os.makedirs(os.path.join(out, "support"), exist_ok=True)
    tickets = []
    tid = 70001
    agents = ["Priya", "Marcus", "Jen", "Tomas", "Aisha", "Ben"]
    for o in orders:
        if not o["shipments"]:
            continue
        last = max(s["deliver_day"] for s in o["shipments"])
        late = last > o["promise"]
        p = 0.36 if late else 0.025
        if rng.random() < p:
            when = o["promise"] if late else o["pick_day"]
            created = dt.datetime.combine(when, dt.time(rng.randint(8, 16), rng.randrange(60)))
            if late and rng.random() < 0.4:
                created = dt.datetime.combine(bday_add(o["promise"], 1), dt.time(rng.randint(7, 11), rng.randrange(60)))
            r = rng.random()
            ref = o["so"] if r < 0.55 else (o.get("po") or "") if r < 0.72 else ""
            if ref and rng.random() < 0.08:
                ref = ref.replace("SO-", rng.choice(["SO ", "#", "so"]))
            cat = products_by_sku[o["lines"][0]["sku"]]["category"].lower()
            body = rng.choice(WISMO_BODIES).format(ref=ref or "", day=o["ts"].strftime("%A"), cat=cat).replace("  ", " ")
            category = "Order Status" if rng.random() < 0.85 else rng.choice(["General", "Shipping", "Other"])
            tickets.append([f"T-{tid}", created.isoformat(timespec="minutes"),
                            rng.choice(["Email", "Email", "Phone", "Portal"]),
                            o["customer"]["name"] if rng.random() < 0.7 else messy_name(rng, o["customer"]["name"]).title(),
                            rng.choice(WISMO_SUBJECTS), body, category, rng.choice(agents),
                            max(3, int(rng.gauss(13, 5))), o["so"]])
            tid += 1
        if rng.random() < 0.15:
            kind = rng.choices(list(OTHER), weights=[30, 25, 25, 20])[0]
            subj, bodies = OTHER[kind]
            created = dt.datetime.combine(bday_add(o["pick_day"], rng.randint(1, 8)), dt.time(rng.randint(8, 16), rng.randrange(60)))
            cat = products_by_sku[o["lines"][0]["sku"]]["category"].lower()
            tickets.append([f"T-{tid}", created.isoformat(timespec="minutes"),
                            rng.choice(["Email", "Phone", "Portal"]), o["customer"]["name"], rng.choice(subj),
                            rng.choice(bodies).format(ref=o["so"] if rng.random() < 0.6 else "", cat=cat).replace("  ", " "),
                            kind, rng.choice(agents), max(2, int(rng.gauss(8, 4))), o["so"]])
            tid += 1
    tickets = [t for t in tickets if t[1] <= DATA_PULLED.isoformat(timespec="minutes")]
    tickets.sort(key=lambda t: t[1])
    with open(os.path.join(out, "support", "tickets.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ticket_id", "created_at", "channel", "requester_org", "subject", "body", "category",
                    "assigned_agent", "handle_minutes"])
        w.writerows(t[:-1] for t in tickets)
    return tickets


def write_master(customers, products, out):
    os.makedirs(os.path.join(out, "crm"), exist_ok=True)
    os.makedirs(os.path.join(out, "catalog"), exist_ok=True)
    with open(os.path.join(out, "crm", "customers.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["customer_id", "name", "type", "tier", "contract_sla_business_days", "city", "state",
                    "home_dc", "po_required"])
        for c in customers:
            w.writerow([c["customer_id"], c["name"], c["type"], c["tier"], c["contract_sla_bdays"],
                        c["city"], c["state"], c["home_dc"], "Y" if c["po_required"] else "N"])
    with open(os.path.join(out, "catalog", "products.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sku", "category", "description", "unit_price", "hazmat"])
        for p in products:
            w.writerow([p["sku"], p["category"], p["description"], p["unit_price"], "Y" if p["hazmat"] else "N"])


def write_truth(orders, out):
    os.makedirs(os.path.join(out, "_truth"), exist_ok=True)
    with open(os.path.join(out, "_truth", "orders_truth.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["order_no", "customer_id", "tier", "dc", "order_ts", "promise", "warehouse_cutoff",
                    "pick_day", "first_ship", "last_delivery", "carrier", "n_shipments", "backorder",
                    "exception", "on_time"])
        for o in orders:
            if not o["shipments"]:
                continue
            last = max(s["deliver_day"] for s in o["shipments"])
            w.writerow([o["so"], o["customer"]["customer_id"], o["customer"]["tier"], o["dc"],
                        o["ts"].isoformat(), o["promise"], o["cutoff"], o["pick_day"],
                        min(s["ship_day"] for s in o["shipments"]), last, o["carrier"], len(o["shipments"]),
                        any(l["backorder"] for l in o["lines"]),
                        "|".join(s["exception"] for s in o["shipments"] if s["exception"]), last <= o["promise"]])


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--out", default=os.path.join(here, "raw"))
    ap.add_argument("--truth", action="store_true")
    a = ap.parse_args()
    rng = random.Random(SEED)
    customers = build_customers(rng)
    products = build_products(rng)
    orders = simulate(rng, customers, products)
    # Only orders up to "today" can have shipped; drop deliveries in the future handled in writers.
    write_master(customers, products, a.out)
    write_erp(rng, orders, a.out)
    write_carriers(rng, orders, a.out)
    tickets = write_tickets(rng, orders, {p["sku"]: p for p in products}, a.out)
    if a.truth:
        write_truth(orders, a.out)
        with open(os.path.join(a.out, "_truth", "ticket_orders.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ticket_id", "order_no"])
            w.writerows([t[0], t[-1]] for t in tickets)
    print(f"customers={len(customers)} products={len(products)} orders={len(orders)} tickets={len(tickets)} -> {a.out}")


if __name__ == "__main__":
    main()
