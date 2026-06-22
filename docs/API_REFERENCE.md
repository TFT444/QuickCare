# QuickCare API Reference

Base URL: `https://api.quickcare.nhs.uk/v1` (production) | `http://localhost:8000` (development)

## Authentication

All endpoints (except `/health`) require a Bearer JWT token:
```
Authorization: Bearer <token>
```

---

## Health

### GET /health
Returns service status.

**Response:**
```json
{"status": "ok", "service": "QuickCare API"}
```

---

## Prescriptions

### POST /prescriptions/explain

Accepts a prescription image or raw text and returns a plain-language explanation in the patient's detected language.

**Request:** `multipart/form-data`
| Field | Type | Required |
|---|---|---|
| image | file | One of image/text required |
| text | string | One of image/text required |
| language | string | Optional — auto-detected if omitted |

**Response:**
```json
{
  "original_text": "Amoxicillin 500mg...",
  "explanation": "This antibiotic treats bacterial infections...",
  "language": "en",
  "medications": ["Amoxicillin"],
  "warnings": [],
  "disclaimer": "This information is for guidance only..."
}
```

---

## Reminders

### POST /reminders/
Create a medication reminder.

### GET /reminders/{id}
Get a specific reminder.

### GET /reminders/user/{user_id}
List all reminders for a user.

### DELETE /reminders/{id}
Delete a reminder.

---

## Appointments

### GET /appointments/slots/{gp_practice_id}
Get available appointment slots for a GP practice.

### POST /appointments/book
Book an appointment slot.

### GET /appointments/user/{user_id}
Get all appointments for a user.

---

## Voice

### POST /voice/transcribe
Transcribe audio to text. Auto-detects language.

**Request:** `multipart/form-data` — `audio` file field

**Response:**
```json
{"transcript": "I have a headache", "language": "en"}
```

### POST /voice/speak
Convert text to speech in the specified language.

**Request:** `form-data` — `text` and `language` fields

**Response:**
```json
{"audio_url": "/static/audio/abc123.mp3", "language": "ur"}
```
