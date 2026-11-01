# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 03: CONFIGURATION SPECIFICATION & RUNTIME ENVIRONMENT
**Version:** 1.0.0  
**Domain 3 (650 pts) & Domain 19 (400 pts):** Configuration & Deployment Operations  

---

### 1. Unified Configuration Architecture

Configuration in SUTRA LEARN is centrally validated using `AISettings` (`backend/app/ai/config.py`) powered by `pydantic-settings` v2.
It enforces type constraints, value ranges, mutually exclusive operational rules, and automatic secret redaction.

---

### 2. Parameter Matrix & Operational Rules

| Configuration Variable | Type | Allowed Values / Range | Default | Purpose & Failure Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `APP_ENV` | `Literal` | `development`, `testing`, `staging`, `production` | `development` | Enforces production security headers and cookie flags. When set to `testing`, enforces deterministic test execution. |
| `APP_DEBUG` | `bool` | `true`, `false` | `false` | Verbose logging control. Strictly forbidden in production. |
| `APP_TIMEZONE` | `str` | Valid IANA timezone | `Asia/Kolkata` | Standardizes timestamp generation across audits and student attempts. |
| `SUTRA_DB_PATH` | `str` | Valid filesystem path | `backend/sutra_learn.db` | Location of SQLite database file. Easily overridden for isolated test databases. |
| `SUTRA_SECRET_KEY` | `str` | Min 32 chars | (Dev default key) | HMAC-SHA256 secret key for signing JWT tokens. |
| `AI_MODE` | `Literal` | `auto`, `cloud`, `local`, `offline` | `auto` | Global routing policy. `offline` prohibits outbound HTTP requests. |
| `AI_PRIMARY_PROVIDER` | `str` | `gemini`, `qwen`, `gemma`, `fallback` | `gemini` | Top-priority provider candidate in `auto` mode. |
| `AI_OFFLINE_MODE` | `bool` | `true`, `false` | `false` | Hard constraint blocking all remote network egress. |
| `GEMINI_API_KEY` | `SecretStr` | Any string | `None` | Google Generative AI API credential. Redacted in diagnostic dumps and logs. |
| `GEMINI_MODEL` | `str` | Valid model tag | `gemini-3.8-flash` | Cloud model identifier. |
| `GEMINI_TIMEOUT_SECONDS` | `float` | `5.0` to `300.0` | `15.0` | Cloud request SLA budget. |
| `OLLAMA_BASE_URL` | `str` | Valid HTTP URL | `http://127.0.0.1:11434` | Ollama daemon endpoint. |
| `OLLAMA_QWEN_MODEL` | `str` | Valid Ollama model | `qwen3.5:4b` | Primary local reasoning model. |
| `OLLAMA_GEMMA_MODEL` | `str` | Valid Ollama model | `gemma4:e2b` | Lightweight local fallback model. |
| `QWEN_TIMEOUT_SECONDS` | `float` | `2.0` to `120.0` | `45.0` | CPU reasoning timeout budget. |
| `GEMMA_TIMEOUT_SECONDS` | `float` | `2.0` to `60.0` | `20.0` | Local direct response timeout budget. |
| `AI_CIRCUIT_FAILURE_THRESHOLD` | `int` | `1` to `10` | `3` | Consecutive failures before tripping to `OPEN`. |
| `AI_CIRCUIT_COOLDOWN_SECONDS`| `float` | `5.0` to `3600.0` | `60.0` | Duration circuit stays in `OPEN` before probing `HALF_OPEN`. |
| `AI_MAX_USER_INPUT_CHARS` | `int` | `100` to `32000` | `8000` | Maximum student question length to prevent DoS. |
| `AI_MAX_HISTORY_MESSAGES` | `int` | `1` to `30` | `8` | Maximum conversation history turns retained in context window. |

---

### 3. Safe Startup Diagnostics

The method `AISettings.safe_dump()` serializes settings for telemetry without exposing sensitive credentials:
```python
{
    "app_env": "development",
    "ai_mode": "auto",
    "ai_offline_mode": False,
    "gemini_api_key_configured": True,  # Secret value is masked
    "gemini_model": "gemini-3.8-flash",
    "ollama_base_url": "http://127.0.0.1:11434",
    "ollama_qwen_model": "qwen3.5:4b",
    "ollama_gemma_model": "gemma4:e2b"
}
```
All environment template examples are stored in `.env.example` using non-sensitive placeholders.

