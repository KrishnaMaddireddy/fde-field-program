#!/usr/bin/env python3
"""
SPOILER: reference answers for Module 1, computed only from files a learner has.

The checker (`python tools/fde.py check 01`) imports `compute()` from here, so
the answer key is never hard-coded: it is always recomputed from the raw data.

Standard library only, so the checker runs anywhere. Learners usually solve this
with pandas or DuckDB instead; see sanity_checks_pandas.py for that version.
"""
import csv
import datetime as dt
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "ridgeway", "data", "raw")
SCMS = os.path.join(ROOT, "real-data", "scms", "SCMS_Delivery_History_Dataset.csv")
HOLIDAYS = {dt.date(2026, 5, 25), dt.date(2026, 7, 3), dt.date(2026, 9, 7)}
MOUNTAIN = {"ID", "UT", "MT"}   # everything else Ridgeway serves is Pacific time


def utc_to_local(utc, state):
    """Convert a UTC timestamp to local time at the destination (DST ends 2026-11-01)."""
    std = -7 if state in MOUNTAIN else -8
    dst_end_utc = dt.datetime(2026, 11, 1, 9 if std == -8 else 8)
    return utc + dt.timedelta(hours=std + (1 if utc < dst_end_utc else 0))


def business_days_between(a, b):
    """Business days from date a to date b (0 if same day)."""
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in HOLIDAYS:
            n += 1
    return n


def parse_date(s):
    s = s.strip()
    for fmt in ("%m/%d/%Y %H:%M", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(s)


def load_erp():
    """Order lines from all monthly exports, normalised to one schema, de-duplicated."""
    rename = {"ORDER_NO": "order_no", "ORDER_DATE": "order_datetime", "CUST_NO": "customer_no",
              "CUST_NAME": "customer_name", "SHIP_DC": "fulfillment_ctr", "CHANNEL": "order_channel",
              "LINE_NO": "line_no", "SKU": "sku", "QTY": "qty", "UNIT_PRICE": "unit_price",
              "LINE_STATUS": "line_status", "BO_FLAG": "backorder_flag", "SHIP_DATE": "ship_date", "TRACKING_NO": "tracking_no",
              "PROMISE_DATE": "promise_date"}
    seen, lines = set(), []
    for path in sorted(glob.glob(os.path.join(RAW, "erp", "erp_order_lines_*.csv"))):
        for row in csv.DictReader(open(path, newline="")):
            row = {rename.get(k, k): v for k, v in row.items()}
            key = (row["order_no"], row["line_no"], row["line_status"], row["qty"])
            if key in seen:            # the August export was appended twice
                continue
            seen.add(key)
            lines.append(row)
    return lines


def build_orders(lines):
    orders = {}
    for r in lines:
        if r["line_status"] in ("RETURN", "CANCELLED"):
            continue
        o = orders.setdefault(r["order_no"], {
            "order_dt": parse_date(r["order_datetime"]), "dc": r["fulfillment_ctr"],
            "customer_no": r["customer_no"], "promise": parse_date(r["promise_date"]).date(),
            "ship_dates": [], "tracking": set(), "backorder_lines": 0, "ever_backordered": 0,
            "value": 0.0, "lines": 0})
        o["lines"] += 1
        o["value"] += float(r["qty"].replace(",", "").strip()) * float(r["unit_price"])
        if r["line_status"] == "BACKORDER":
            o["backorder_lines"] += 1
        if r["backorder_flag"] == "Y":    # old export leaves it blank instead of "N"
            o["ever_backordered"] += 1
        if r["ship_date"]:
            o["ship_dates"].append(parse_date(r["ship_date"]).date())
        if r["tracking_no"]:
            o["tracking"].add(r["tracking_no"])
    return orders


def delivery_dates(orders, customers):
    """tracking/order -> local delivery date, from all three carrier sources."""
    by_tracking = {}
    for line in open(os.path.join(RAW, "carrier", "parcelpro_events.jsonl")):
        e = json.loads(line)
        if e["status_code"] == "DL":
            by_tracking[e["tracking_number"]] = dt.datetime.strptime(e["event_time"], "%Y-%m-%dT%H:%M:%SZ")
    for line in open(os.path.join(RAW, "carrier", "cascade_freight_events.jsonl")):
        e = json.loads(line)
        if e["status"] in ("DL", "DELIVERED"):           # codes changed on Oct 15
            by_tracking[e["pro_number"]] = ("local", dt.datetime.strptime(e["status_date"], "%Y-%m-%d %H:%M"))
    fleet_by_order = {}
    for r in csv.DictReader(open(os.path.join(RAW, "fleet", "fleet_delivery_log.csv"), newline="")):
        if r["order_refs"].strip():
            d = dt.datetime.strptime(r["delivery_date"], "%m/%d/%y").date()
            for ref in r["order_refs"].split(";"):
                fleet_by_order[ref.strip()] = max(d, fleet_by_order.get(ref.strip(), d))
    result = {}
    for no, o in orders.items():
        dates, known = [], True
        for t in o["tracking"]:
            v = by_tracking.get(t)
            if isinstance(v, tuple):
                dates.append(v[1].date())
            elif v is not None:   # ParcelPro is UTC: convert to the destination's local date
                dates.append(utc_to_local(v, customers[o["customer_no"]]["state"]).date())
            elif t.startswith("FLT-") and no in fleet_by_order:
                dates.append(fleet_by_order[no])
            else:
                known = False
        if not o["tracking"] and no in fleet_by_order:
            dates.append(fleet_by_order[no])
        elif not o["tracking"]:
            known = False
        result[no] = (max(dates) if dates else None, known)
    return result


def compute():
    lines = load_erp()
    orders = build_orders(lines)
    customers = {r["customer_id"]: r for r in csv.DictReader(open(os.path.join(RAW, "crm", "customers.csv")))}
    deliveries = delivery_dates(orders, customers)
    # Each monthly file is the nightly export Greg saved on the 3rd of the following month.
    export_day = {m: dt.date(2026, m + 1, 3) for m in range(5, 11)}

    shipped = [o for o in orders.values() if o["ship_dates"]]
    within_1 = sum(business_days_between(o["order_dt"].date(), min(o["ship_dates"])) <= 1 for o in shipped)

    # Delivered on time = every line delivered on or before the promise date.
    # Late for sure if a line was still on backorder when the export ran after the promise date.
    judged = {}
    for no, o in orders.items():
        last, known = deliveries[no]
        if o["backorder_lines"] and o["promise"] < export_day[o["order_dt"].month]:
            judged[no] = False
        elif known and last:
            judged[no] = last <= o["promise"]
    on_time = sum(judged.values())
    by_dc = {}
    for no, ok in judged.items():
        by_dc.setdefault(orders[no]["dc"], []).append(ok)
    t1_late_value = sum(orders[no]["value"] for no, ok in judged.items()
                        if not ok and customers[orders[no]["customer_no"]]["tier"] == "1")

    tickets = list(csv.DictReader(open(os.path.join(RAW, "support", "tickets.csv"), newline="")))
    status = sum(t["category"] == "Order Status" for t in tickets)

    # Real data: USAID SCMS delivery history (CR line endings, UTF-8 with BOM).
    scms = list(csv.DictReader(open(SCMS, newline="", encoding="utf-8-sig")))
    def d(s):
        return dt.datetime.strptime(s, "%d-%b-%y").date()
    sched_ok = sum(d(r["Delivered to Client Date"]) <= d(r["Scheduled Delivery Date"]) for r in scms)
    exact = sum(d(r["Delivered to Client Date"]) == d(r["Scheduled Delivery Date"]) for r in scms)

    return {
        "shipped_within_1_business_day_pct": round(100 * within_1 / len(shipped), 1),
        "order_status_ticket_share_pct": round(100 * status / len(tickets), 1),
        "orders_with_backorder_line_pct": round(100 * sum(o["ever_backordered"] > 0 for o in orders.values()) / len(orders), 1),
        "delivered_on_time_pct": round(100 * on_time / len(judged), 1),
        "boise_delivered_on_time_pct": round(100 * sum(by_dc["BOI"]) / len(by_dc["BOI"]), 1),
        "tier1_late_credit_usd_6mo": round(0.02 * t1_late_value, -3),
        "scms_on_or_before_scheduled_pct": round(100 * sched_ok / len(scms), 1),
        "scms_delivered_exactly_on_scheduled_pct": round(100 * exact / len(scms), 1),
        "_coverage_orders_judged_pct": round(100 * len(judged) / len(orders), 1),
    }


if __name__ == "__main__":
    print(json.dumps(compute(), indent=2))
