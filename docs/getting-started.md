# Getting started

Five minutes to set up, then your AI tutor takes over.

## 1. Get the course

Clone or download the course repository, then open a terminal in its folder.

```bash
git clone https://github.com/KrishnaMaddireddy/fde-field-program
cd fde-field-program
```

## 2. Install Python packages

You need Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Check your setup

```bash
python3 tools/fde.py doctor
```

It checks your Python version and packages, and builds Ridgeway's data if it's missing. The data generator is deterministic: everyone gets byte-for-byte the same files, so your numbers can be checked automatically.

## 4. Open the folder in your AI agent and say "Start the course"

=== "Claude Code"

    ```bash
    claude
    ```
    Then type: `Start the course`. Claude Code reads `CLAUDE.md`, which points to `AGENTS.md`.

=== "Codex"

    ```bash
    codex
    ```
    Then type: `Start the course`. Codex reads `AGENTS.md` automatically.

=== "Cursor and others"

    Open the folder, open the agent chat, and type `Start the course`. Cursor and most other coding agents read `AGENTS.md`. If yours doesn't, start with: `Read AGENTS.md and follow it.`

=== "GitHub Copilot"

    Open the folder in VS Code, open Copilot Chat in agent mode, and type `Start the course`. Copilot reads `.github/copilot-instructions.md`, which points to `AGENTS.md`.

=== "Gemini CLI"

    ```bash
    gemini
    ```
    Then type: `Start the course`. Gemini CLI reads `GEMINI.md`, which points to `AGENTS.md`.

=== "A chat app"

    No coding agent? Use ChatGPT, Claude or Gemini in the browser with the [chat tutor prompt](ai-tutor.md#no-coding-agent-use-a-chat-app). You run the commands yourself and paste the output.

Your tutor asks a few questions about you, creates `PROGRESS.md`, and starts [Module 1](modules/01-discovery.md).

## Optional: preview this website locally

```bash
mkdocs serve
```

Then open <http://127.0.0.1:8000>.
