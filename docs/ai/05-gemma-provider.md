# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 05: GEMMA 4 E2B LIGHTWEIGHT LOCAL FALLBACK PROVIDER
**Version:** 1.0.0  
**Adapter Implementation:** `backend/app/ai/ollama_adapters.py` (`GemmaAdapter`)  
**Runtime:** Local Ollama (`http://127.0.0.1:11434`)  
**Model Identifier:** `gemma4:e2b` (Digest: `b37049369adf`, 7.2 GB)  

---

### 1. Model Role and Characteristics

Gemma 4 E2B serves as the **Secondary Lightweight Local Fallback (Tier 3)**. It is invoked when both Gemini (Cloud) and Qwen (Primary Local) fail, timeout, or suffer circuit tripping.

#### Distinctive Operational Traits:
1. **Direct Instruction Following:** Gemma 4 emits immediate, concise instructional text without requiring long thinking pre-computations.
2. **CPU Generation Speed:** Executes substantially faster on CPU architectures than large reasoning models (~9.5s to 12s on commodity CPU).
3. **Scaffolded Output:** Reliably adheres to prompt constraints such as "Explain in 10 words or less" or "Provide 2 sequential hints".

---

### 2. Live Verification Evidence

Execution output from `scripts/ai/verify_gemma.ps1`:
```powershell
======================================================================
SUTRA LEARN — GEMMA 4 E2B INFERENCE VERIFICATION
======================================================================
[PASS] Model: gemma4:e2b
[PASS] Generation Latency: 9553 ms
[PASS] Tokens Evaluated: 15
Output: Add 8 to both sides to isolate the variable term.
======================================================================
GEMMA 4 E2B VERIFICATION: SUCCESS (Exit Code 0)
```

---

### 3. Failover Trigger Conditions

- **Socket Unreachable:** If Ollama daemon is not running on `127.0.0.1:11434`, `is_available()` returns `False` immediately.
- **Model Not Found (404):** If the image is not pulled, trips circuit breaker to `OPEN`.
- **Inference Timeout:** Controlled by `GEMMA_TIMEOUT_SECONDS` (default: 20.0s). If breached, safely hands off request to Tier 4 (Curriculum Engine).

