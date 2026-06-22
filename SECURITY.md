# Security Policy — QuickCare

## Supported Versions

| Version | Supported |
|---|---|
| `main` (latest) | ✅ |
| `dev` (pre-release) | ⚠️ Active development — may contain known issues |
| Older branches | ❌ |

---

## Reporting a Vulnerability

QuickCare handles health data for vulnerable populations. We take every security report seriously.

**Please do not open a public GitHub issue for security vulnerabilities.**

### How to Report

Use GitHub's private vulnerability reporting:

1. Go to the [Security tab](../../security/advisories/new) of this repository
2. Click **"Report a vulnerability"**
3. Provide as much detail as possible

Alternatively, email: **security@quickcare.nhs.uk** *(placeholder — update before public launch)*

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Affected component (e.g., `src/core/safety.py`, `/prescriptions/explain` endpoint)
- Potential impact (data exposure, clinical safety risk, auth bypass, etc.)
- Your suggested fix if you have one

---

## Response Timeline

| Stage | Target |
|---|---|
| Acknowledgement | Within 48 hours |
| Initial assessment | Within 5 business days |
| Fix deployed (critical) | Within 14 days |
| Fix deployed (high/medium) | Within 30 days |
| Public disclosure | After fix is live and verified |

---

## Security Architecture

### Application Layer

- **JWT authentication** on all API routes (except `/health`)
- **Rate limiting**: 30 requests/minute per IP (`src/api/middleware/rate_limit.py`)
- **Input validation**: Pydantic schemas enforce type safety on all endpoints
- **AI output guardrails**: `src/core/safety.py` blocks diagnostic claims and prescription changes before any response reaches the user
- **Audit logging**: Every AI output is SHA-256 hashed and logged with timestamp and language code

### Data Security

- No raw prescription text is stored beyond the active session without explicit user opt-in
- NHS numbers are only stored when NHS Login OAuth is active (Phase 2+)
- All logs are structured JSON — no PII in log lines
- Database: PostgreSQL with parameterised queries only (SQLAlchemy ORM — no raw SQL)
- Secrets via environment variables only — no hardcoded credentials anywhere in the codebase

### CI/CD Security

- **Bandit** static analysis runs on every push
- **TruffleHog** secret scanning runs on every push
- All merges to `main` require passing CI and an approved review from `@TFT444`

### Clinical Safety Controls

- AI outputs are validated against a blocklist of diagnostic claim patterns before delivery
- Mandatory multilingual disclaimer appended to every AI response
- No model output bypasses `safety.py`

---

## Scope

The following are **in scope** for vulnerability reports:

- Authentication and authorisation bypass
- Injection vulnerabilities (prompt injection, SQL injection, command injection)
- Data exposure (PII, NHS numbers, prescription data)
- Clinical safety bypass (AI output reaching users without disclaimer or safety check)
- Broken access control between users
- Insecure direct object references

The following are **out of scope**:

- Denial of service attacks
- Social engineering of team members
- Issues in third-party services (Anthropic API, Azure, NHS Login) — report those directly to the vendor

---

## Disclosure Policy

We follow **coordinated disclosure**. We ask that you give us reasonable time to fix a reported issue before making it public. We will credit researchers who report valid vulnerabilities (with their permission) in our release notes.
