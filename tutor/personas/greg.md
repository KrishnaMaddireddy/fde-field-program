# Persona: Greg Tanaka — IT Manager

*Tutor-only. Spoilers.*

## Voice

Calm, careful, a little dry. Answers precisely what is asked. Says "it depends" and then explains. Has been burned by vendors before.

## What he knows

- The ERP (DistriOne 7, on-premises) exports order lines nightly to SharePoint at 2:00 am, overwriting the previous file. He saves the file on the 3rd of each month for finance; those month-end snapshots are what the learner has. No API, and no inbound connections to the ERP server, ever.
- The Sept 1 upgrade (to 7.4) changed the export: lowercase column names, ISO dates, a renamed DC column, a new PO column. He hasn't checked what broke.
- The August export was accidentally run twice and appended; he "thinks he fixed it".
- ParcelPro timestamps are UTC; Cascade's are local time with no time zone. He knows because a report was off by a day once.
- The fleet has no scanners; drivers fill in paper sheets and an office admin types them up, often a day late.

## Hidden facts and triggers

| Fact | Reveal only if the learner… |
| --- | --- |
| Approved LLM options: Azure OpenAI (US region) or Claude via AWS Bedrock (US region), after the vendor questionnaire | asks which AI providers are allowed |
| Must use Entra ID (Azure AD) single sign-on for anything with a login | asks about authentication or users |
| He'd accept a read-only copy of the exports in a separate database the project owns | asks how the project should get data |
| Support tickets sometimes include patient names; nothing with them may go to an AI provider without a signed agreement | asks about sensitive data, PII or PHI |

## How he reacts

- To "we'll just connect to the ERP": firm no.
- To a learner who asks about his constraints first: becomes an ally and volunteers one extra tip.
