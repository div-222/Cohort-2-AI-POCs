"""Gemini LLM client wrapper.

Returns both the generated text and token usage so the Cost Monitor agent can
price every call. JSON mode is supported for the Planner agent.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

from . import config

_client = None


class LLMError(RuntimeError):
    """Raised when a Gemini call fails (bad key, quota, network, safety)."""


def friendly_error(exc: Exception) -> str:
    """Turn a raw provider error into a short, user-actionable hint."""
    msg = str(exc)
    low = msg.lower()
    if "api key not valid" in low or "api_key_invalid" in low:
        return ("Gemini API key is invalid. Check GOOGLE_API_KEY in .env — it should "
                "be a Google AI Studio key (usually starts with 'AIza'). "
                "Get one at https://aistudio.google.com/app/apikey")
    if "quota" in low or "rate" in low or "429" in low:
        return "Gemini quota/rate limit hit. Wait a moment or check your billing."
    if "permission" in low or "403" in low:
        return "Gemini permission denied. Ensure the Generative Language API is enabled for this key."
    if "not found" in low or "404" in low:
        return f"Model not found. Check GEMINI_MODEL in .env. ({msg[:120]})"
    return msg[:200]


def _ensure_configured():
    global _configured
    global _client
    if _client is not None:
        return _client
    if not config.llm_available():
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    from google import genai

    _client = genai.Client(api_key=config.GOOGLE_API_KEY)
    return _client


@dataclass
class LLMResult:
    text: str
    input_tokens: int
    output_tokens: int
    model: str


def generate(
    prompt: str,
    system: Optional[str] = None,
    json_mode: bool = False,
    temperature: float = 0.2,
    model: Optional[str] = None,
) -> LLMResult:
    """Call Gemini and return text + token usage."""
    client = _ensure_configured()
    from google.genai import types

    model_name = model or config.GEMINI_MODEL
    cfg_kwargs = {"temperature": temperature}
    if system:
        cfg_kwargs["system_instruction"] = system
    if json_mode:
        cfg_kwargs["response_mime_type"] = "application/json"

    try:
        resp = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(**cfg_kwargs),
        )
    except Exception as exc:  # bad key, quota, network, etc.
        raise LLMError(friendly_error(exc)) from exc

    usage = getattr(resp, "usage_metadata", None)
    in_tok = getattr(usage, "prompt_token_count", 0) or 0
    out_tok = getattr(usage, "candidates_token_count", 0) or 0

    try:
        text = resp.text
    except Exception:
        # Safety blocks / empty candidates
        text = ""

    return LLMResult(text=text, input_tokens=in_tok, output_tokens=out_tok, model=model_name)


def parse_json(text: str) -> dict:
    """Best-effort JSON parse from a model response."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.split("\n", 1)[-1] if "\n" in text else text
    try:
        return json.loads(text)
    except Exception:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start : end + 1])
            except Exception:
                pass
    return {}
