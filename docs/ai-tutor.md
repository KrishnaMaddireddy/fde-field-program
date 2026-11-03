# Learn with an AI tutor

Every module is designed to be learned **with an AI agent beside you**. The agent follows `AGENTS.md` in the course folder, which turns it into three people at once.

<div class="fde-grid" markdown>

<div class="fde-card" markdown>
<span class="fde-num">Teacher</span>
### Explains, then checks
<p>Teaches one idea at a time with Ridgeway examples, then asks you a quick question before moving on.</p>
</div>

<div class="fde-card" markdown>
<span class="fde-num">Client</span>
### Plays the characters
<p>Dana, Renee, Greg, Linda and Hector each have a personality, blind spots and secrets you only uncover by asking well.</p>
</div>

<div class="fde-card" markdown>
<span class="fde-num">Reviewer</span>
### Grades honestly
<p>Runs the auto-checker, scores your writing against the rubric, and tells you exactly what to fix.</p>
</div>

</div>

## Things you can say

| Say | What happens |
| --- | --- |
| `Start the course` | First session: intro, a few questions about you, setup check |
| `Teach me Module 1` | The lesson, in small pieces |
| `Explain that differently` | Same idea, new angle or example |
| `I'm stuck` | The next hint, one step at a time |
| `Start the kickoff call with Dana` | Role-play begins; the agent stays in character |
| `Pause` / `Resume` | Step out of / back into a role-play |
| `Check my answers` | Runs `python3 tools/fde.py check 01` and explains the result |
| `Grade Module 1` | Rubric score and written feedback in `submission/FEEDBACK.md` |
| `Give me a drill` | A timed decomposition case on a brand-new client |
| `Where was I?` | Summary from `PROGRESS.md` |

## Hints, not answers

Your tutor won't write your submission for you, even if you ask nicely. That's on purpose: the judgment is the skill. It climbs a **hint ladder** instead:

1. A question that points you the right way
2. The concept or file you need
3. The shape of the solution in pseudo-code
4. A few lines of code that unblock you

If you're stuck on Python itself, it teaches that directly. Reference solutions live in `solutions/` for after you submit.

## No coding agent? Use a chat app

Paste the prompt below into ChatGPT, Claude, Gemini or any chat assistant. Upload the module page and the files it asks for, or paste them in, when the tutor asks. You run the commands yourself and paste the output back.

```text
You are my tutor for "FDE Field Program", an open-source course on becoming a Forward
Deployed Engineer. I'll paste the course's AGENTS.md next; follow it as your instructions.
Then I'll paste files as you ask for them (module pages, tutor guides, personas), since you
can't read my folder. You can't run commands either: tell me what to run and I'll paste the
output. Start with the "First session" steps in AGENTS.md.
```

Then paste `AGENTS.md`. When you start a module, paste its page from `docs/modules/` and its tutor guide from `tutor/modules/`. Before a role-play, paste that character's file from `tutor/personas/`.

!!! warning "Keep the surprise"
    Persona files hold the characters' secrets, and tutor guides list the hints and data traps. Copy them without reading them (open, select all, copy, paste). Never paste anything from `solutions/`: your chat tutor doesn't need the answers, because `python3 tools/fde.py check 01` tells you which numbers are right.
