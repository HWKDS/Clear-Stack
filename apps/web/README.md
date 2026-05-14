Quick web frontend scaffold (Vite + React)

Setup

1. Install dependencies from the `apps/web` folder:

```bash
cd apps/web
npm install
```

2. Create a `.env` file with Vite variables (see `../.env.example`):

```
VITE_OLLAMA_URL=http://localhost:11434
VITE_OLLAMA_MODEL=your-model-name
```

3. Start dev server:

```bash
npm run dev
```

Notes

- The frontend reads `VITE_...` variables at build time. For local testing set `VITE_OLLAMA_URL` to your Ollama API host (usually `http://localhost:11434`).
- Do not call Ollama directly from production client code — proxy calls through your backend.

Example: call backend proxy

```js
// from the web app, call your FastAPI proxy which forwards to Ollama
fetch("/api/ollama/generate", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": "your-service-api-key",
  },
  body: JSON.stringify({ prompt: "Summarize this text." }),
})
  .then((r) => r.json())
  .then(console.log);
```
