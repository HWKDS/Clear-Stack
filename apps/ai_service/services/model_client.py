from dataclasses import dataclass
import json
from urllib import error, request

from apps.ai_service.core.config import settings


@dataclass(frozen=True)
class ModelOutput:
    provider: str
    model_name: str
    prompt: str
    text: str


def _post_json(url: str, payload: dict, headers: dict[str, str]) -> dict:
    body = json.dumps(payload).encode("utf-8")
    api_request = request.Request(
        url,
        data=body,
        headers=headers,
        method="POST",
    )

    with request.urlopen(api_request, timeout=settings.request_timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def generate_with_local_model(model_name: str, prompt: str) -> str:
    try:
        response_payload = _post_json(
            f"{settings.ollama_base_url}/api/generate",
            {"model": model_name, "prompt": prompt, "stream": False},
            {"Content-Type": "application/json"},
        )
    except error.URLError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {settings.ollama_base_url}. Start Ollama and pull {model_name}."
        ) from exc

    generated_text = response_payload.get("response")
    if not isinstance(generated_text, str):
        raise RuntimeError("Ollama response did not contain text.")

    return generated_text.strip()


def generate_with_cloud_model(model_name: str, prompt: str) -> str:
    if not settings.cloud_api_key:
        raise RuntimeError("CLOUD_API_KEY is missing. Set it in your environment before using cloud generation.")

    try:
        response_payload = _post_json(
            f"{settings.cloud_api_base_url}/chat/completions",
            {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "You are a concise AI assistant."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            },
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.cloud_api_key}",
            },
        )
    except error.URLError as exc:
        raise RuntimeError("Could not reach cloud model provider. Check CLOUD_API_BASE_URL and internet access.") from exc

    choices = response_payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("Cloud response did not include choices.")

    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        raise RuntimeError("Cloud response choice format is invalid.")

    message = first_choice.get("message")
    if not isinstance(message, dict):
        raise RuntimeError("Cloud response message format is invalid.")

    generated_text = message.get("content")
    if not isinstance(generated_text, str):
        raise RuntimeError("Cloud response did not contain text content.")

    return generated_text.strip()