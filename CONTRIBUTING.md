# Contributing to QuickCare

All work — no matter how small — follows the same process:  
**Open an issue → Branch from dev → Open a PR → Get reviewed → Merge**

No exceptions. No direct pushes. No skipping steps.

---

## Workflow (Mandatory)

```
1. Open a GitHub Issue
       ↓
2. Create a branch off dev
   naming: feature/42-short-description
           fix/17-bug-name
           security/9-vuln-name
       ↓
3. Do the work, commit locally
       ↓
4. Push branch → open Pull Request into dev
       ↓
5. PR reviewed and approved by @TFT444
       ↓
6. Merge into dev (squash merge preferred)
       ↓
7. When dev is stable → PR from dev into main
       ↓
8. Approved by @TFT444 → merge into main
```

### Branch Rules

| Branch | Direct push | PR required | Approvals needed |
|--------|-------------|-------------|------------------|
| `main` | ❌ Blocked  | ✅ Yes      | ✅ 1 — @TFT444 only |
| `dev`  | ❌ Blocked  | ✅ Yes      | ✅ 1 — @TFT444 only |
| `feature/*` | ✅ Yes | —          | —                |
| `fix/*`     | ✅ Yes | —          | —                |
| `security/*`| ✅ Yes | —          | —                |

> **@TFT444 must approve every PR into both `dev` and `main`. No exceptions.**

---

## Step 1 — Open an Issue First

Every piece of work starts with a GitHub Issue.

- Use the **Bug Report** template for bugs
- Use the **Feature Request** template for new features
- For security vulnerabilities — see [SECURITY.md](./SECURITY.md), do **not** open a public issue

The issue number becomes part of your branch name and PR title.

---

## Step 2 — Create Your Branch

```bash
# Always branch from dev — never from main
git checkout dev
git pull origin dev
git checkout -b feature/42-prescription-language-fallback
```

Branch naming:
```
feature/<issue-number>-short-description
fix/<issue-number>-short-description
security/<issue-number>-short-description
docs/<issue-number>-short-description
test/<issue-number>-short-description
```

---

## Step 3 — Do the Work

```bash
# Run tests before every commit
pytest tests/ -v --tb=short

# Security check
bandit -r src/ -ll

# No secrets
grep -r "API_KEY\|SECRET\|PASSWORD" src/ --include="*.py"
```

### Clinical Safety Rules (mandatory for any AI-touching code)
- All AI output **must** pass through `src/core/safety.py`
- No diagnostic claims
- No dose change suggestions
- Safety disclaimer must be appended to every AI response

---

## Step 4 — Commit Messages

```
type(scope): short description  ← max 72 chars

Why this change was needed (optional body).
Closes #42
```

Types: `feat` · `fix` · `docs` · `test` · `refactor` · `ci` · `security`

Examples:
```
feat(i18n): add Gujarati TTS voice mapping
Closes #42

fix(safety): prevent bypass when language code is unsupported
Closes #17

security(auth): enforce token expiry on all middleware routes
Closes #9
```

---

## Step 5 — Open a Pull Request

```bash
git push origin feature/42-prescription-language-fallback
```

Then open a PR on GitHub:
- **Target branch: `dev`** (never `main` directly)
- Fill in the PR template fully — do not skip sections
- Reference the issue: `Closes #42`
- Assign `@TFT444` as reviewer

The PR will not be merged until:
- ✅ All CI checks pass (tests, Bandit, TruffleHog, clinical safety suite)
- ✅ Approved by `@TFT444`

---

## Step 6 — dev → main Promotion

When `dev` is stable and tested:

1. Open a PR from `dev` into `main`
2. Title: `release: promote dev to main — vX.Y`
3. Describe what's included
4. Assign `@TFT444` for review
5. Merge only after approval + CI green

---

## Authors

- **Tanvir Farhad** — Founder & Lead Engineer, sole approver (`@TFT444`)
- **Emon** — Co-Author & Contributor
