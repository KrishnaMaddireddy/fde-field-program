# USAID SCMS Delivery History Dataset

**Real data.** 10,324 shipment line items of HIV/AIDS medicines and test kits delivered to 43 countries between 2006 and 2015 under the U.S. President's Emergency Plan for AIDS Relief (PEPFAR), through USAID's Supply Chain Management System (SCMS).

| | |
| --- | --- |
| Publisher | U.S. Agency for International Development (USAID) |
| Original title | Supply Chain Shipment Pricing Data |
| Original landing page | https://data.usaid.gov/d/a3rc-nmf6 (data.usaid.gov was unreachable when this course was built, Nov 2026) |
| Catalog record | https://data.amerigeoss.org/dataset/supply-chain-shipment-pricing-data |
| License (per catalog record) | [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/) |
| Files here | `SCMS_Delivery_History_Dataset.csv` (MD5 `75ada24f6df3870fda5fde6a2e24cdad`), `SCMS_Delivery_History_Data_Dictionary.csv` |

## How we use it

The files are included **unmodified**, as the license permits, with attribution to USAID. All cleaning happens in your own code, never in these files. Don't commit modified copies of them to this repository.

Because data.usaid.gov is offline, the copy here came from public GitHub mirrors of the original export. Four mirrors listed the same file size, and the two we downloaded were byte-identical (same MD5 as above).

## Why it's in the course

It is the real-world twin of Ridgeway's problems:

- **Module 1:** the data dictionary warns that `Scheduled Delivery Date` "should not be used to determine on-time performance", yet it's the obvious column to use. It's a real metric-definition trap, just like Dana's 94%.
- **Module 2:** carriage-return-only line endings, a UTF-8 byte-order mark, three date columns, and numeric columns that sometimes hold text such as `Freight Included in Commodity Cost` or `See ASN-608 (ID#:…)`.

Suggested citation: *USAID, Supply Chain Management System (SCMS) Delivery History Dataset, PEPFAR, 2006–2015.*
