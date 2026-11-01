# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 02: CONFIGURATION & ENVIRONMENT SPECIFICATION
**Version:** 1.0.0  
**Module:** `backend/app/ai/config.py`  
**Configuration Paradigm:** Type-safe, validated via `pydantic-settings`  

---

### 1. Configuration Philosophy

All AI infrastructure parameters are centrally managed in `AISettings` (`backend/app/ai/config.py`). The configuration system enforces:
1. Strict typing and runtime validation through Pydantic v2.
2. Safe defaults enabling immediate offline/local fallback out-of-the-box.
3. Separation of secrets from runtime code.
4. Redaction of sensitive API credentials in logs and serialization dumps.

---

### 2. Comprehensive Parameter Reference

| Parameter Name | Type | Default | Allowed Range | Validation Rule | Purpose & Failure Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | `SecretStr` | `""` | Any non-whitespace string | Validates prefix or non-empty string | Remote cloud access key. If missing or invalid, provider trips circuit to OPEN and fails over to Ollama. |
| `GEMINI_MODEL` | `str` | `gemini-3.8-flash` | `gemini-3.8-flash`, `gemini-1.5-pro`, `gemini-1.5-flash` | Valid identifier string | Target Google Generative AI model identifier. On 404, trips circuit. |
| `GEMINI_ENDPOINT` | `str` | `https://generativelanguage.googleapis.com` | Valid URL | Starts with `http://` or `https://` | REST base URL for Gemini inference. |
| `GEMINI_TIMEOUT_SECONDS` | `float` | `15.0` | `1.0` - `60.0` | Positive float | HTTP timeout for Gemini API calls. On timeout, trips circuit. |
| `GEMINI_MAX_RETRIES` | `int` | `1` | `0` - `3` | Non-negative integer | Max retries before triggering circuit trip. |
| `OLLAMA_BASE_URL` | `str` | `http://127.0.0.1:11434` | Valid HTTP URL | Must be valid HTTP endpoint | Base URL of the Ollama inference server. |
| `OLLAMA_QWEN_MODEL` | `str` | `qwen3.5:4b` | Any valid Ollama model tag | Non-empty string | Model identifier for Primary Local Model (Tier 2). |
| `OLLAMA_GEMMA_MODEL` | `str` | `gemma4:e2b` | Any valid Ollama model tag | Non-empty string | Model identifier for Secondary Local Model (Tier 3). |
| `QWEN_TIMEOUT_SECONDS` | `float` | `45.0` | `2.0` - `120.0` | Positive float | Max generation latency allowed for Qwen 3.5 4B before failover. |
| `GEMMA_TIMEOUT_SECONDS` | `float` | `20.0` | `2.0` - `60.0` | Positive float | Max generation latency allowed for Gemma 4 E2B before failover. |
| `AI_MODE` | `str` | `auto` | `auto`, `cloud`, `local`, `offline` | Strict enum string | Global operational routing mode. `offline` bypasses remote calls completely. |
| `AI_OFFLINE_MODE` | `bool` | `False` | `True`, `False` | Boolean | Hard lock preventing any outgoing network requests. |
| `AI_CIRCUIT_FAILURE_THRESHOLD` | `int` | `3` | `1` - `10` | Positive integer | Consecutive failures before circuit transitions to OPEN. |
| `AI_CIRCUIT_COOLDOWN_SECONDS` | `float` | `60.0` | `5.0` - `3600.0` | Positive float | Duration circuit stays OPEN before probing HALF_OPEN. |
| `AI_MAX_USER_INPUT_CHARS` | `int` | `8000` | `100` - `32000` | Positive integer | Max characters in student/teacher prompt to prevent denial-of-service. |
| `AI_MAX_HISTORY_MESSAGES` | `int` | `8` | `1` - `30` | Positive integer | Number of conversational turns sent in context window. |

---

### 3. Safe Serialization & Diagnostic Exposure

The `AISettings.safe_dump()` method outputs all configuration properties with masked API credentials:
```python
{
    "gemini_api_key_configured": True,  # Secret is never dumped directly
    "gemini_model": "gemini-3.8-flash",
    "ollama_base_url": "http://127.0.0.1:11434",
    "ollama_qwen_model": "qwen3.5:4b",
    "ollama_gemma_model": "gemma4:e2b",
    "ai_mode": "auto",
    "ai_offline_mode": False
}
```
This guarantees operational visibility without credential leakage across logs, error diagnostics, and administrative APIs.

