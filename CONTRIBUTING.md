# Contributing

Thanks for helping make FDE Field Program better. Fixes, new real-world twins, translations and whole new modules are all welcome.

## Good first contributions

- **Fix something confusing.** If a lesson, hint or checker message confused you, open an issue quoting it; that's a bug.
- **Add a real-world twin.** A public dataset with a clear license that mirrors a module's problem. Add it under `real-data/<name>/` with a `SOURCE.md`.
- **Translate** a module page or video captions.
- **Test with your AI agent.** Run Module 1 with a tool we haven't tried and report how the tutor behaved.

## How the course is built

| Piece | Where | Rule |
| --- | --- | --- |
| Lesson + lab page | `docs/modules/NN-*.md` | Plain language, short sections, one idea per section |
| Lab files | `modules/NN-*/` | Learners write only in `submission/` |
| Tutor guide | `tutor/modules/NN-*.md` | Objectives, check questions, hint ladders, rubric, answer-key notes |
| Personas | `tutor/personas/*.md` | Voice, beliefs, hidden facts with triggers |
| Reference solution | `solutions/NN-*/reference.py` | Standard library only; the checker imports `compute()` |
| Checker | `tools/fde.py` | Never prints expected values |
| Videos | `videos/NN-*/` | Rendered from code so anyone can edit and re-render |

## Style

- Write for someone with basic Python. Define every term the first time.
- Short sentences, concrete examples from Ridgeway, no hype.
- Ridgeway is fictional; never use real company names for its customers or vendors.
- Keep `ridgeway/data/generate.py` deterministic. If you change it, update the reference solutions and say so in your PR.

## Before you open a pull request

CI (`.github/workflows/ci.yml`) runs these on every pull request and publishes the website to GitHub Pages on every push to `main`. Run them locally first:

```bash
python3 ridgeway/data/generate.py
python3 tools/fde.py doctor
python3 solutions/01-discovery/reference.py
mkdocs build --strict
```

By contributing you agree your content is licensed under CC BY 4.0 and your code under MIT (see `LICENSE-CONTENT.md`). Please follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) code of conduct.
