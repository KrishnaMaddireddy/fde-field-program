"""
SPOILER: one way a learner might do Module 1's Easy-path sanity checks with pandas.
Run from the repo root:  python3 solutions/01-discovery/sanity_checks_pandas.py
"""
import glob

import numpy as np
import pandas as pd

HOLIDAYS = ["2026-05-25", "2026-07-03", "2026-09-07"]

# --- 1. Load every ERP export into one table --------------------------------------
# The Sept 1 upgrade renamed columns, so map the old names onto the new ones.
OLD_TO_NEW = {"ORDER_NO": "order_no", "ORDER_DATE": "order_datetime", "CUST_NO": "customer_no",
              "CUST_NAME": "customer_name", "SHIP_DC": "fulfillment_ctr", "CHANNEL": "order_channel",
              "LINE_NO": "line_no", "SKU": "sku", "QTY": "qty", "UNIT_PRICE": "unit_price",
              "LINE_STATUS": "line_status", "BO_FLAG": "backorder_flag", "SHIP_DATE": "ship_date",
              "TRACKING_NO": "tracking_no", "PROMISE_DATE": "promise_date"}
frames = [pd.read_csv(f, dtype=str).rename(columns=OLD_TO_NEW)
          for f in sorted(glob.glob("ridgeway/data/raw/erp/erp_order_lines_*.csv"))]
erp = pd.concat(frames, ignore_index=True)

before = len(erp)
erp = erp.drop_duplicates()                      # the August export was appended twice
print(f"Dropped {before - len(erp)} duplicate rows")

erp = erp[~erp["line_status"].isin(["RETURN", "CANCELLED"])]
erp["order_datetime"] = pd.to_datetime(erp["order_datetime"], format="mixed")
erp["ship_date"] = pd.to_datetime(erp["ship_date"], format="mixed")

# --- 2. Dana's "on time": shipped within 1 business day ---------------------------
orders = erp.groupby("order_no").agg(order_day=("order_datetime", "min"), first_ship=("ship_date", "min"),
                                     any_backorder=("backorder_flag", lambda s: (s == "Y").any()))
shipped = orders.dropna(subset=["first_ship"])
bdays = np.busday_count(shipped["order_day"].values.astype("datetime64[D]"),
                        shipped["first_ship"].values.astype("datetime64[D]"), holidays=HOLIDAYS)
print(f"Shipped within 1 business day: {100 * (bdays <= 1).mean():.1f}%")

# --- 3. Backorders are per line, but customers feel them per order ----------------
print(f"Orders with a backordered line: {100 * orders['any_backorder'].mean():.1f}%")

# --- 4. Ticket mix -----------------------------------------------------------------
tickets = pd.read_csv("ridgeway/data/raw/support/tickets.csv")
print(f"Tickets labelled 'Order Status': {100 * (tickets['category'] == 'Order Status').mean():.1f}%")

# --- 5. Real-world twin: USAID SCMS ------------------------------------------------
scms = pd.read_csv("real-data/scms/SCMS_Delivery_History_Dataset.csv", encoding="utf-8-sig")
sched = pd.to_datetime(scms["Scheduled Delivery Date"], format="%d-%b-%y")
deliv = pd.to_datetime(scms["Delivered to Client Date"], format="%d-%b-%y")
print(f"SCMS delivered on/before scheduled: {100 * (deliv <= sched).mean():.1f}%")
print(f"SCMS delivered exactly on scheduled: {100 * (deliv == sched).mean():.1f}%  <- suspicious!")
