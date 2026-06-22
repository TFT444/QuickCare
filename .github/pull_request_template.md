## Linked Issue

Closes #<!-- issue number — required, do not skip -->

> ⚠️ Every PR must reference an issue. PRs without a linked issue will not be reviewed.

---

## What does this PR do?
<!-- Clear description of the change and why it was needed -->

## Type of Change
- [ ] `feat` — New feature
- [ ] `fix` — Bug fix
- [ ] `security` — Security fix
- [ ] `docs` — Documentation
- [ ] `test` — Tests only
- [ ] `refactor` — Refactor, no behaviour change
- [ ] `ci` — CI / workflow change

## Target Branch
- [ ] This PR targets `dev` ← **always, unless this is a dev→main release PR**

---

## Pre-merge Checklist

### Code
- [ ] I branched off `dev`, not `main`
- [ ] `pytest tests/ -v --tb=short` passes locally
- [ ] New tests added for new functionality
- [ ] No hardcoded secrets, API keys, or credentials

### Clinical Safety *(skip if no AI output code was touched)*
- [ ] All AI output still passes through `src/core/safety.py`
- [ ] No diagnostic claims introduced
- [ ] No dose change recommendations introduced
- [ ] Safety disclaimer still appended to all responses
- [ ] `tests/clinical/test_accuracy.py` passes

### Security
- [ ] `bandit -r src/ -ll` passes — no new HIGH findings
- [ ] Input validation present on any new endpoints
- [ ] No raw SQL introduced

---

## Screenshots / Evidence *(if applicable)*

---

## Reviewer
@TFT444 — please review and approve before merging.
