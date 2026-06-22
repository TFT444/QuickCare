# NHS Compliance — QuickCare

## GDPR (UK GDPR / Data Protection Act 2018)

### Lawful Basis
- **Consent** — explicit opt-in at registration for health data processing
- **Vital interests** — emergency triage guidance only

### Data Minimisation
- NHS number stored only when NHS Login OAuth is active (Phase 2+)
- Prescription text hashed (SHA-256) for audit; raw text not retained beyond session unless user opts in
- No biometric data stored

### Data Retention
| Data Type | Retention Period |
|---|---|
| Prescription explanations | 90 days (user-configurable) |
| Medication reminders | Until user deletion |
| Audit logs | 7 years (NHS requirement) |
| Voice audio | Session only — not persisted |

### Subject Rights
- Right of access: `GET /users/{id}/data` (Phase 2)
- Right to erasure: `DELETE /users/{id}` cascades all records
- Data portability: JSON export (Phase 2)

### Data Transfers
All data processed and stored within UK/EEA (Azure UK South). No third-country transfers without Standard Contractual Clauses.

---

## NHS DSPT (Data Security and Protection Toolkit)

| DSPT Standard | Status |
|---|---|
| Leadership accountability | Founder accountable — SIRO designated pre-launch |
| Training | All contributors complete NHS DSPT IG training |
| Data flows documented | In progress — DPIA drafted |
| Security assurance | Penetration test scheduled pre-pilot |
| Incident response | Policy drafted, playbook in progress |

---

## DCB0129 Clinical Safety

DCB0129 is the NHS clinical risk management standard for health IT systems.

All AI-generated outputs are classified as Decision Support, not Clinical Decision Making.

### Hazard Register (Draft)
| Hazard | Likelihood | Severity | Mitigation |
|---|---|---|---|
| AI provides incorrect drug interaction information | Low | High | BNF data validation layer (Phase 3), mandatory disclaimer |
| Patient misunderstands AI-generated explanation | Medium | Medium | Plain language, multiple languages |
| OCR misreads prescription | Medium | High | Raw OCR text shown to user for confirmation before explanation |
| System unavailable during urgent need | Low | High | Redirect to NHS 111 on all errors |

### Safety Guardrails (Implemented)
- `safety.py` blocks diagnostic claims and dose change recommendations
- Every output carries mandatory disclaimer in the patient's language
- All outputs SHA-256 hashed and audit-logged
- Clinical accuracy benchmark suite in `tests/clinical/`

---

## Audit Logging

Every AI output is logged with:
- Timestamp
- Language code
- SHA-256 hash of output text
- Route that triggered it

Logs are structured JSON, shipped to Azure Monitor in production.
