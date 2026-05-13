# ClearStack AI Service Backend

Production-ready backend MVP for notification ingestion, prioritization, digest generation, and privacy-first AI text generation.

## Backend capabilities

- Privacy-first model routing with PII redaction
- Local generation via Ollama
- Cloud generation fallback via OpenAI-compatible API
- Notification ingestion and priority scoring
- Daily digest generation from ingested notifications
- Integration listing and stub connect flow
- Consistent API response shape: `{ data, error, message }`
- Optional API key guard using `x-api-key`

## Project structure

```text
apps/ai_service/
	core/
		config.py
		response.py
		security.py
	models/
		notification.py
		digest.py
	repositories/
		notification_repository.py
	routers/
		generation.py
		notifications.py
		digest.py
		integrations.py
	services/
		model_router.py
		model_client.py
		pii_redaction.py
		notification_service.py
		digest_service.py
	main.py
	tests/
```

## Environment variables

Create `.env` in project root:

```env
APP_NAME=ClearStack AI Service
MODEL_PROVIDER=local
LOCAL_MODEL_NAME=llama3.1
CLOUD_MODEL_NAME=gpt-4o-mini
CLOUD_API_BASE_URL=https://api.openai.com/v1
CLOUD_API_KEY=
ALLOW_CLOUD_FOR_SENSITIVE_DATA=false
REDACT_SENSITIVE_TEXT=true
OLLAMA_BASE_URL=http://127.0.0.1:11434
REQUEST_TIMEOUT_SECONDS=60
SERVICE_API_KEY=
```

Notes:

- Keep `ALLOW_CLOUD_FOR_SENSITIVE_DATA=false` for strict privacy.
- Set `SERVICE_API_KEY` in non-local environments to protect endpoints.

## Setup and run

1. Create and activate venv (Windows PowerShell):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Pull local model:

```powershell
ollama pull llama3.1
```

4. Run API:

```powershell
python -m uvicorn apps.ai_service.main:app --reload --port 8000
```

## API endpoints

- `GET /health`
- `POST /route`
- `POST /generate`
- `POST /notifications/ingest`
- `GET /notifications`
- `GET /notifications/{notification_id}`
- `POST /digest/daily`
- `GET /integrations`
- `POST /integrations/{provider}/connect`

## Quick test commands

Generate text:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/generate -ContentType "application/json" -Body '{"prompt":"Summarize meeting notes in one line","sensitive_data":false}'
```

Ingest notification:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/notifications/ingest -ContentType "application/json" -Body '{"source":"gmail","title":"Urgent deadline","body":"Submit report by 5 PM","sensitive_data":false,"metadata":{}}'
```

Create digest:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/digest/daily -ContentType "application/json" -Body '{"limit":20}'
```

## Run tests

```powershell
$env:PYTHONPATH=(Get-Location).Path; .\.venv\Scripts\python.exe -m pytest .\apps\ai_service\tests -q
```
