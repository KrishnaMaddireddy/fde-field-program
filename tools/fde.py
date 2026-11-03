#!/usr/bin/env python3
"""
fde — helper for the FDE Field Program.

    python3 tools/fde.py doctor        check your setup (and build the client data if missing)
    python3 tools/fde.py status        see what's done and what's next
    python3 tools/fde.py check 01      auto-check a module's answers and deliverables

Standard library only.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES = {
    "01": ("01-discovery", "Discovery and decomposition"),
    "02": ("02-data", "Data integration"),
    "03": ("03-prototype", "Week-one prototype"),
    "04": ("04-rag", "RAG over documents"),
    "05": ("05-agents", "Agents and tool use"),
    "06": ("06-evals", "Evals and observability"),
    "07": ("07-deploy", "Production deployment"),
    "08": ("08-handover", "Handover and capstone"),
}

GREEN, RED, YELLOW, DIM, BOLD, END = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[1m", "\033[0m"
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    GREEN = RED = YELLOW = DIM = BOLD = END = ""


def ok(msg):
    print(f"  {GREEN}✔{END} {msg}")


def bad(msg):
    print(f"  {RED}✘{END} {msg}")


def warn(msg):
    print(f"  {YELLOW}!{END} {msg}")


# ---------------------------------------------------------------- doctor
def doctor():
    print(f"{BOLD}Checking your setup{END}")
    good = True
    if sys.version_info >= (3, 10):
        ok(f"Python {sys.version.split()[0]}")
    else:
        bad(f"Python {sys.version.split()[0]}: please use 3.10 or newer")
        good = False
    raw = os.path.join(ROOT, "ridgeway", "data", "raw")
    if os.path.isdir(os.path.join(raw, "erp")):
        ok("Ridgeway client data is present")
    else:
        warn("Ridgeway client data missing; generating it now (about 5 seconds)…")
        subprocess.run([sys.executable, os.path.join(ROOT, "ridgeway", "data", "generate.py")], check=True)
        ok("Ridgeway client data generated")
    if os.path.exists(os.path.join(ROOT, "real-data", "scms", "SCMS_Delivery_History_Dataset.csv")):
        ok("Real dataset (USAID SCMS) is present")
    else:
        bad("real-data/scms/SCMS_Delivery_History_Dataset.csv is missing; see real-data/scms/SOURCE.md")
        good = False
    for pkg, why in [("pandas", "recommended for labs"), ("duckdb", "needed from Module 2"),
                     ("mkdocs", "only to preview the website")]:
        if importlib.util.find_spec(pkg):
            ok(f"{pkg} installed")
        else:
            warn(f"{pkg} not installed ({why}): pip install -r requirements.txt")
    if os.path.exists(os.path.join(ROOT, "PROGRESS.md")):
        ok("PROGRESS.md found")
    else:
        warn("No PROGRESS.md yet. Your AI tutor creates it in your first session (or copy PROGRESS.template.md)")
    print()
    print(f"{GREEN}Ready to learn.{END} Open this folder in your AI agent and say: \"Start the course\"" if good
          else f"{RED}Fix the items above, then run doctor again.{END}")


# ---------------------------------------------------------------- status
def status():
    print(f"{BOLD}Your progress{END}")
    for num, (folder, title) in MODULES.items():
        path = os.path.join(ROOT, "modules", folder)
        sub = os.path.join(path, "submission")
        if not os.path.isdir(path) or os.path.exists(os.path.join(path, "LOCKED")):
            print(f"  {DIM}○ {num} {title} — coming soon{END}")
            continue
        files = [f for f in os.listdir(sub) if not f.startswith(".")] if os.path.isdir(sub) else []
        if "FEEDBACK.md" in files:
            print(f"  {GREEN}●{END} {num} {title} — graded (see submission/FEEDBACK.md)")
        elif files:
            print(f"  {YELLOW}◐{END} {num} {title} — in progress ({len(files)} file(s) in submission/)")
        else:
            print(f"  ○ {num} {title} — not started")


# ---------------------------------------------------------------- check
CHECKS_01 = {
    # key: (path, tolerance, kind). Hints live in solutions/01-discovery/check_hints.json.
    "shipped_within_1_business_day_pct": ("easy", 1.0, "pts"),
    "order_status_ticket_share_pct": ("easy", 1.0, "pts"),
    "orders_with_backorder_line_pct": ("easy", 1.0, "pts"),
    "scms_on_or_before_scheduled_pct": ("easy", 1.0, "pts"),
    "scms_delivered_exactly_on_scheduled_pct": ("easy", 1.0, "pts"),
    "delivered_on_time_pct": ("stretch", 2.0, "pts"),
    "boise_delivered_on_time_pct": ("stretch", 2.5, "pts"),
    "tier1_late_credit_usd_6mo": ("stretch", 0.25, "rel"),
}


def load_reference(module_folder):
    path = os.path.join(ROOT, "solutions", module_folder, "reference.py")
    spec = importlib.util.spec_from_file_location("reference", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.compute()


def check_01():
    folder = MODULES["01"][0]
    sub = os.path.join(ROOT, "modules", folder, "submission")
    print(f"{BOLD}Module 1 — auto-check{END}  {DIM}(numbers, then deliverables; your tutor grades the writing){END}\n")
    answers_path = os.path.join(sub, "answers.json")
    if not os.path.exists(answers_path):
        bad("submission/answers.json not found. Copy templates/answers.json there and fill it in.")
        return
    try:
        answers = json.load(open(answers_path))
    except json.JSONDecodeError as e:
        bad(f"answers.json isn't valid JSON: {e}")
        return
    if not isinstance(answers, dict):
        bad("answers.json should be one JSON object, like the template: {\"key\": number, ...}")
        return
    hints = json.load(open(os.path.join(ROOT, "solutions", folder, "check_hints.json")))
    counter = os.path.join(sub, ".checks")
    runs = int(open(counter).read() or 0) + 1 if os.path.exists(counter) else 1
    open(counter, "w").write(str(runs))
    expected = load_reference(folder)
    score = {"easy": [0, 0], "stretch": [0, 0]}
    for path in ("easy", "stretch"):
        print(f"{BOLD}{path.title()} path{END}")
        for key, (p, tol, kind) in CHECKS_01.items():
            if p != path:
                continue
            got = answers.get(key)
            if got in (None, ""):
                print(f"  {DIM}·{END} {key}: {DIM}not answered{END}")
                continue
            score[path][1] += 1
            try:
                got = float(str(got).replace(",", "").replace("%", "").replace("$", ""))
            except ValueError:
                bad(f"{key}: '{got}' isn't a number")
                continue
            exp = expected[key]
            diff = abs(got - exp) if kind == "pts" else abs(got - exp) / exp
            if diff <= tol:
                score[path][0] += 1
                ok(f"{key}: {got:g}")
            elif kind == "pts" and 0 < got <= 1 < exp:
                bad(f"{key}: {got:g} looks like a fraction. Write percentages as 0-100 (e.g. 42.5).")
            else:
                direction = "too high" if got > exp else "too low"
                bad(f"{key}: {got:g} is {direction}. Hint: {hints[key]}")
        print()
    print(f"{BOLD}Deliverables{END}")
    for name, need in [("sanity_checks", "your sanity-check code (.py, .sql or .ipynb)"),
                       ("discovery_notes.md", "notes from the kickoff call"),
                       ("scoping_doc.md", "the scoping doc"),
                       ("drill_1.md", "decomposition drill 1"), ("drill_2.md", "decomposition drill 2")]:
        found = [f for f in os.listdir(sub) if f.startswith(name)]
        (ok if found else bad)(f"{name}: {', '.join(found) if found else 'missing — ' + need}")
    doc = os.path.join(sub, "scoping_doc.md")
    if os.path.exists(doc):
        words = len(re.findall(r"\w+", open(doc).read()))
        (ok if words <= 1100 else warn)(f"scoping doc length: {words} words (aim for ≤ 1,100, about 2 pages)")
    print()
    e, s = score["easy"], score["stretch"]
    stretch = f"stretch {s[0]}/{s[1]} correct" if s[1] else "stretch not attempted"
    print(f"{BOLD}Numbers:{END} easy {e[0]}/{e[1]} correct, {stretch}.")
    if runs >= 6:
        print(f"{YELLOW}You've run the checker {runs} times.{END} If you're adjusting numbers to hit the target, stop and "
              "ask your tutor to talk through the definition instead. Guessing teaches nothing.")
    print("Next: ask your AI tutor to \"grade Module 1\" for rubric feedback on your writing.")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
    elif args[0] == "doctor":
        doctor()
    elif args[0] == "status":
        status()
    elif args[0] == "check" and len(args) > 1:
        num = args[1].zfill(2)
        if num == "01":
            check_01()
        else:
            print(f"Module {num}'s checker isn't released yet.")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
