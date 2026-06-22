# QuickCare — Architecture

## Overview

QuickCare is a FastAPI backend with a multilingual AI layer. Designed for NHS deployment readiness, GDPR compliance, and clinical safety from the ground up.

## Layers

### API Layer (`src/api/`)
FastAPI REST API. Routes: `/prescriptions`, `/reminders`, `/appointments`, `/voice`. CORS enabled for PWA frontend. JWT middleware on all routes except `/health`.

### Core AI Engine (`src/core/`)
Wraps the Anthropic Claude API (claude-sonnet-4-6). Every prompt enforces:
- No diagnostic claims
- No dosage recommendations beyond the original prescription
- Mandatory safety disclaimer appended to every output
- SHA-256 audit hash logged per response

### Voice Layer (`src/voice/`)
- STT: OpenAI Whisper — auto language detection from audio
- TTS: Azure Cognitive Services — 10 NHS community languages
- Language detection: `langdetect` with NHS language fallback

### Prescription Processing (`src/prescriptions/`)
1. OCR via pytesseract (image → text)
2. AI explanation via Claude (text → plain language in patient's language)
3. Safety validation via `safety.py`
4. Structured response with medications, warnings, disclaimer

### Reminders (`src/reminders/`)
Redis-backed reminder store. Push notification stub (FCM/Azure Notification Hubs in Phase 2).

### Appointments (`src/appointments/`)
NHS Login OAuth 2.0 stub. GP Connect FHIR R4 stub. Full integration planned Phase 2–3.

### i18n (`src/i18n/`)
JSON translation files per language. Cultural context layer for mental health and family involvement preferences.

## Data Flow

```
User (voice/image/text)
  → API route
  → parser.py (OCR if image)
  → lang_detect.py (auto language)
  → ai_engine.py (Claude API)
  → safety.py (guardrails + disclaimer)
  → structured JSON response
```

## Full System Flowchart

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER (PWA)                              │
│              Voice  │  Photo  │  Text  │  Tap                   │
└──────┬──────────────┴────┬────┴────────┴──┬──────────────────── ┘
       │                   │                │
       ▼                   ▼                ▼
┌──────────────┐  ┌────────────────┐  ┌──────────────────────┐
│  /voice/     │  │ /prescriptions/│  │  /appointments/      │
│  transcribe  │  │ explain        │  │  slots  │  book      │
│  /voice/speak│  │                │  │                      │
└──────┬───────┘  └───────┬────────┘  └──────────┬───────────┘
       │                  │                       │
       ▼                  ▼                       ▼
┌──────────────┐  ┌────────────────┐  ┌──────────────────────┐
│  voice/      │  │ prescriptions/ │  │  appointments/       │
│  stt.py      │  │ parser.py      │  │  gp_connect.py       │
│  (Whisper)   │  │ (pytesseract)  │  │  (FHIR stub)         │
│  tts.py      │  │                │  │                      │
│  (Azure TTS) │  └───────┬────────┘  └──────────────────────┘
│  lang_detect │          │
└──────┬───────┘          ▼
       │         ┌────────────────┐
       │         │ prescriptions/ │
       │         │ explainer.py   │
       │         │ validator.py   │
       │         └───────┬────────┘
       │                 │
       └────────┬─────────┘
                │
                ▼
       ┌────────────────────┐
       │   core/            │
       │   ai_engine.py     │◄── Anthropic Claude API
       │   drug_checker.py  │
       │   triage.py        │
       └────────┬───────────┘
                │
                ▼
       ┌────────────────────┐
       │   core/safety.py   │  ← blocks diagnostic claims
       │                    │  ← appends disclaimer (translated)
       │                    │  ← SHA-256 audit log
       └────────┬───────────┘
                │
                ▼
       ┌────────────────────┐
       │   i18n/            │
       │   translator.py    │  ← JSON translations (10 languages)
       │   cultural_context │  ← cultural adaptation layer
       └────────┬───────────┘
                │
                ▼
       ┌────────────────────┐
       │  JSON Response     │
       │  to PWA / Voice    │
       └────────────────────┘

Supporting services (always running):
  ┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
  │  PostgreSQL  │    │  Redis          │    │  Audit Logger    │
  │  (users,     │    │  (reminders,    │    │  (Azure Monitor) │
  │  prescripts) │    │  sessions)      │    │                  │
  └──────────────┘    └─────────────────┘    └──────────────────┘
```

### Prescription Explanation — Step by Step

```
  Patient photographs prescription
           │
           ▼
  POST /prescriptions/explain (multipart image)
           │
           ▼
  parser.py → pytesseract OCR → raw text
           │
           ▼
  lang_detect.py → auto-detect language (no manual selection)
           │
           ▼
  validator.py → length/sanity check
           │
           ▼
  ai_engine.explain_prescription(text, language)
    └── Claude API prompt:
        "Explain in plain language. No diagnoses.
         No dose changes. Respond in {language}."
           │
           ▼
  safety.py → scan for diagnostic claims → block if found
           │
           ▼
  safety.py → append disclaimer in patient's language
           │
           ▼
  {
    original_text: "...",
    explanation:   "... [in Urdu/Bengali/etc] ...",
    language:      "ur",
    medications:   ["Amoxicillin"],
    warnings:      [],
    disclaimer:    "یہ معلومات صرف رہنمائی کے لیے ہے..."
  }
```

## Security

- JWT authentication on all routes (except `/health`)
- Rate limiting: 30 requests/minute per IP
- All AI outputs audit-logged with SHA-256 hash
- GDPR consent captured at user creation
- No PII stored without encryption (Phase 2)
