**From:** Greg Tanaka, IT Manager
**Subject:** Data access + ground rules

Hi — a few things before we start.

1. **ERP.** DistriOne 7 runs on-prem. There is no API we'll expose. The ERP writes a CSV export of order lines every night, overwriting the last one. I save a copy on the 3rd of each month for finance, so you get six of those month-end snapshots (each one covers orders placed that month, with statuses as of the 3rd of the next month). We upgraded to 7.4 on Sept 1 and the export layout changed; I haven't had time to check what broke downstream.
2. **Carriers.** ParcelPro and Cascade both give us event feeds; I've dumped six months of each. Our own fleet (RMS Fleet) doesn't have tracking. Drivers fill in a sheet and the office types it up.
3. **Support tickets.** Export from the shared inbox tool. Free text, so there may be patient-adjacent info in there occasionally. Treat it as sensitive.
4. **Security.** We're a Microsoft shop (M365, Entra ID). Anything customer-facing or touching the ERP needs to pass our vendor security questionnaire. Customer data can't leave the US. I need to know which LLM provider you'd use and where it runs.
5. **Capacity.** It's me and one other person. Whatever you build, we can't babysit it. If it needs a person to restart it at 2 am, it won't survive.

Everything is in the shared folder (`ridgeway/data/raw/`): orders placed May 1 – Oct 31, and carrier events, fleet logs and tickets up to Friday Nov 6, when I pulled them.

Greg
