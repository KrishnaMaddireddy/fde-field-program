<p align="center"><img src="docs/assets/img/logo.svg" width="72" alt=""></p>

<h1 align="center">FDE Field Program</h1>

<p align="center"><b>Learn to be a Forward Deployed Engineer by running one client engagement, with any AI agent as your tutor.</b><br>
Free · open source · basic Python is enough to start</p>

---

A **Forward Deployed Engineer (FDE)** sits with a customer, works out what they actually need, and ships software that solves it, in their messy environment. This course teaches the job the way it's done: one client, one story, eight missions, from the first vague email to a production handover.

Your client is **Ridgeway Medical Supply** (fictional). Its VP wants "an AI chatbot" and says 94% of orders are on time. Its support lead says customers are furious. You'll find out who's right, then build what Ridgeway actually needs. Every mission also has a **real-world twin** on real public data.

## Start in 5 minutes

```bash
git clone https://github.com/KrishnaMaddireddy/fde-field-program && cd fde-field-program
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 tools/fde.py doctor
```

Then open the folder in your AI agent (Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI…) and say:

> **Start the course**

The agent reads [`AGENTS.md`](AGENTS.md) and becomes your **teacher** (lessons in small pieces), your **client** (role-plays with five characters who have secrets) and your **reviewer** (auto-checks plus rubric grading). It gives hints, not answers. No coding agent? See [Learn with an AI tutor](docs/ai-tutor.md) for a prompt that works in any chat app.

## The missions

| # | Mission | Status |
| --- | --- | --- |
| 1 | [Discovery and decomposition](docs/modules/01-discovery.md): the chatbot that wasn't | ✅ Available |
| 2 | Data integration: one table you'd bet your job on | 🚧 In progress |
| 3 | Week-one prototype | Planned |
| 4 | RAG over customer documents | Planned |
| 5 | Agents and tool use | Planned |
| 6 | Evals and observability | Planned |
| 7 | Production deployment | Planned |
| 8 | Handover and capstone | Planned |

Each mission has a short video, a lesson, a lab with **Easy** and **Stretch** paths, a real-world twin, an auto-checker and a rubric.

## Read it as a website

```bash
mkdocs serve      # http://127.0.0.1:8000
```

## Repository map

| Path | What it is |
| --- | --- |
| `docs/` | The course website: lessons and labs |
| `modules/` | Lab files; learners write only in each `submission/` folder |
| `ridgeway/` | The fictional client and its deterministic data generator |
| `real-data/` | Real public datasets, unmodified, each with a `SOURCE.md` |
| `tutor/` | Guides and role-play personas for the AI tutor (spoilers) |
| `solutions/` | Reference solutions (spoilers) |
| `tools/fde.py` | `doctor`, `status` and `check` |
| `videos/` | Video source code and narration scripts |

## Contributing and license

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). Course content is [CC BY 4.0](LICENSE-CONTENT.md); code is [MIT](LICENSE); datasets keep their own licenses. Ridgeway Medical Supply and its people are fictional.
