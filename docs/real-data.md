# Real data

Ridgeway is fictional so the story can be consistent from Mission 1 to Mission 8. To keep it honest, every mission also has a **real-world twin**: the same kind of problem on a real public dataset. If your method works on both, it works.

| Dataset | Publisher | What's in it | Used in | License |
| --- | --- | --- | --- | --- |
| SCMS Delivery History | USAID (PEPFAR) | 10,324 shipment lines of HIV/AIDS medicines and test kits to 43 countries, 2006–2015 | Missions 1–2 | CC BY-ND 4.0 |

The files sit unmodified in `real-data/`, each with a `SOURCE.md` that records its origin, license and checksum.

## Why SCMS is a great teacher

Its own data dictionary says the `Scheduled Delivery Date` column "should not be used to determine on-time performance". Yet it's the first column almost everyone reaches for. In Mission 1 you'll see what that does to an on-time number.

??? note "Spoiler: why (read after Mission 1)"
    The scheduled date is the *current* expected date, and it gets revised along the way. Measure against it and late shipments look on time, which is why so many are delivered "exactly" on schedule. It's the same trap as Dana's 94%.
