# Contributing to QuickCare

Thank you for your interest in contributing. QuickCare handles health data for vulnerable populations — contributions are held to a high standard of quality, security, and clinical safety.

---

## Branch Model

```
main  ← stable, production-ready — NO direct pushes
  └── dev  ← all active development lives here
        └── feature/your-feature  ← branch off dev, PR back into dev
```

| Branch | Purpose | Who can push |
|---|---|---|
| `main` | Production-ready, reviewed code | PRs from `dev` only, approved by `@TFT444` |
| `dev` | Active development | Contributors via feature branches |
| `feature/*` | Individual features or fixes | You |

**Never push directly to `main`.** All changes must go through `dev` and pass review before being merged to `main`.

---

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/TFT444/QuickCare.git
cd QuickCare

# 2. Create your feature branch from dev
git checkout dev
git checkout -b feature/your-feature-name

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment
cp .env.example .env
# Fill in your API keys

# 5. Run tests before committing
pytest tests/ -v --tb=short
```

---

## Development Rules

### Code Quality
- All code must pass `bandit -r src/ -ll` with no high-severity findings
- All endpoints must have Pydantic input validation
- No raw SQL — SQLAlchemy ORM only
- No secrets or API keys in code or comments

### Clinical Safety (mandatory)
- Every AI output **must** pass through `src/core/safety.py` before being returned to the user
- No code may bypass the safety guardrail
- No code may make diagnostic claims or suggest changing prescribed dosages
- All new AI prompts must be reviewed for clinical safety implications

### Testing
- New features require unit tests in `tests/unit/`
- New API endpoints require integration tests in `tests/integration/`
- Changes to AI output logic require updates to `tests/clinical/test_accuracy.py`

---

## Pull Request Process

1. Branch off `dev`, not `main`
2. Ensure all tests pass: `pytest tests/ -v --tb=short`
3. Ensure no secrets: `trufflehog filesystem .`
4. Ensure no high-severity issues: `bandit -r src/ -ll`
5. Fill in the PR template fully
6. Request review from `@TFT444`
7. PR is merged only after approval + CI green

---

## Commit Message Format

```
type: short description (max 72 chars)

Optional longer body explaining WHY, not WHAT.
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `ci`, `security`

Examples:
```
feat: add Bengali TTS voice mapping in Azure voice layer
fix: prevent safety.py bypass when language is unsupported
security: add rate limiting to voice/transcribe endpoint
```

---

## Security Vulnerabilities

Do **not** open a public issue for security vulnerabilities. See [SECURITY.md](./SECURITY.md) for the responsible disclosure process.

---

## Authors

- **Tanvir Farhad** — Founder & Lead Engineer (`@TFT444`)
- **Emon** — Co-Author & Contributor
