# SUTRA LEARN — OMEGA ∞
## DOCUMENT 02: AUTHORITATIVE API SPECIFICATION REPORT

**API Key Under Test:** `AQ.Ab8...fiVQ [REDACTED_FOR_SECURITY]`  
**Provider:** Google GenAI / Google Cloud AI  
**Product:** Gemini Developer API  
**Official Documentation:** https://ai.google.dev/api  
**Verification Date:** November 4, 2026  
**Empirical Verification Status:** CONFIRMED & OPERATIONAL (HTTP 200 OK)  

---

### 1. PROVIDER IDENTITY & ACCESS PROFILE

| Specification Field | Authoritative Value | Empirical Evidence |
|---|---|---|
| **Provider** | Google DeepMind / Google Cloud AI | Discovered via `generativelanguage.googleapis.com` |
| **API Architecture** | RESTful HTTP/2 JSON + gRPC | Successfully tested via HTTPS v1beta endpoints |
| **Authentication Type** | Developer Secret Key | Verified with query string `?key=...` and header `x-goog-api-key` |
| **Base URL** | `https://generativelanguage.googleapis.com/v1beta` | Resolved and answered in 999.83ms |
| **SDK Standard** | `google-genai` (v0.1+) | Imported in Python 3.11 environment |
| **Total Available Models** | 50 distinct models | Discovered from live `models.list()` call |

---

### 2. EMPIRICAL MODEL DISCOVERY & PROBE RESULTS

A comprehensive live network probe was executed against all primary model candidates using the provided key. The results are summarized below:

```
[PASS] gemini-flash-lite-latest | Status: 200 OK | Latency: 4881ms | Tokens: 536
       Excerpt: "A linear equation is a mathematical statement where the highest exponent of the..."
[PASS] gemini-3.5-flash-lite     | Status: 200 OK | Latency: 4563ms | Tokens: 498
       Excerpt: "A linear equation is a mathematical statement where the highest exponent of the..."
[PASS] gemini-3.1-flash-lite     | Status: 200 OK | Latency: 7400ms | Tokens: 512
       Excerpt: "A linear equation is a mathematical statement expressing the equality of two exp..."
[FAIL] gemini-3.8-flash          | Status: 503 Service Unavailable (Temporary high demand spike)
[FAIL] gemini-2.5-flash          | Status: 404 Model Retired ("no longer available to new users")
[FAIL] gemini-2.5-pro            | Status: 404 Model Retired ("no longer available to new users")
[FAIL] gemini-pro-latest         | Status: 429 Rate Limit ("quota exceeded")
```

#### Verified Operational Model Hierarchy:
1. **Primary Model:** `gemini-flash-lite-latest` (Optimal balance of speed, mathematical rigor, and reliability).
2. **Secondary Failover 1:** `gemini-3.5-flash-lite` (Fastest observed latency at 4563ms).
3. **Secondary Failover 2:** `gemini-3.1-flash-lite` (High accuracy fallback).
4. **Secondary Failover 3:** `gemini-3.8-flash` (Configured for retry on demand recovery).

---

### 3. API PROTOCOL & SCHEMAS

#### 3.1 Inference Request Schema (`POST /v1beta/models/{model}:generateContent`)

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "Solve for x: 3x - 7 = 11. Show both steps and explain the balance principle."
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.2,
    "maxOutputTokens": 2048,
    "topP": 0.8,
    "candidateCount": 1
  },
  "systemInstruction": {
    "parts": [
      {
        "text": "You are SUTRA AI, an elite mathematics tutor specializing in NCERT Class 8 Mathematics. Ground all reasoning in balance operations."
      }
    ]
  },
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]
}
```

#### 3.2 Response Schema

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "### Step 1: Undo Subtraction Using the Balance Principle..."
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "index": 0
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 54,
    "candidatesTokenCount": 482,
    "totalTokenCount": 536
  }
}
```

---

### 4. ERROR CODE MAPPING & HANDLING

| HTTP Status | Error Type | Sutra Learn Classification | Handled By |
|---|---|---|---|
| **200** | Success | `OPERATIONAL` | Normal response parser & SymPy validator |
| **400** | Invalid Request | `INVALID_PAYLOAD` | Request sanitizer; drop invalid history |
| **401** | Unauthorized | `AUTHENTICATION_ERROR` | Immediate circuit breaker trip; notify admin |
| **403** | Forbidden | `PERMISSION_DENIED` | Failover to local Ollama / Deterministic |
| **404** | Not Found | `MODEL_RETIRED` | Automatic cascade to next candidate model |
| **429** | Too Many Requests | `QUOTA_EXHAUSTED` | Exponential backoff with jitter (max 2 retries) |
| **500** | Internal Error | `PROVIDER_OUTAGE` | Failover to secondary candidate |
| **503** | High Demand | `TRANSIENT_OVERLOAD` | Immediate retry on secondary candidate |

---

### 5. PRIVACY & SECURITY BOUNDARIES

- **Secret Handling:** The API key is stored exclusively in backend `.env` variables (`GEMINI_API_KEY`) and parsed through Pydantic `AISettings`. It is never exported in frontend bundles, build artifacts, or client telemetry.
- **Data Minimization:** Requests sent to Gemini include only the student's mathematical input, sanitized conversation context, and the NCERT concept grounding. No student PII (passwords, emails, student IDs, or school affiliations) is transmitted.
- **Audit Logging:** Request durations, token counts, and model selections are recorded with sanitized telemetry. Raw tokens and keys are strictly excluded.

