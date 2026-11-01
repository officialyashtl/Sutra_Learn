# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 04: QWEN 3.5 4B LOCAL REASONING PROVIDER
**Version:** 1.0.0  
**Adapter Implementation:** `backend/app/ai/ollama_adapters.py` (`QwenAdapter`)  
**Runtime:** Local Ollama (`http://127.0.0.1:11434`)  
**Model Identifier:** `qwen3.5:4b` (Digest: `d8b0f5e9760c`, 2.7 GB)  

---

### 1. Model Role and Characteristics

Qwen 3.5 4B acts as the **Primary Local Inference Model (Tier 2)** in the SUTRA LEARN multi-model cascade. When cloud connectivity is unavailable or the Gemini circuit breaker is open, the system routes requests to Qwen 3.5 4B.

#### Distinctive Operational Traits:
1. **Extended CoT (Thinking Stream):** Qwen 3.5 natively generates an internal reasoning trace `<think>...</think>` (or dedicated `thinking` field in Ollama v0.5+ API) before emitting its conversational answer.
2. **Pedagogical Alignment:** Formulates rigorous Socratic scaffolding for NCERT Class 8 algebra questions.
3. **Hardware Latency Profile:**
   - **Local CPU Execution:** Generation takes 20s to 35s when evaluating up to 150-250 reasoning tokens.
   - **GPU Acceleration (when enabled):** Sub-3s response.
4. **Adapter Content Extraction:** `QwenAdapter` inspects both `res.message.content` and `res.message.thinking`. If the content buffer is empty due to token budgets or thinking stream emission, it safely extracts the pedagogical essence without failing.

---

### 2. Live Verification Evidence

Execution output from `scripts/ai/verify_qwen.ps1`:
```powershell
======================================================================
SUTRA LEARN — QWEN 3.5 4B INFERENCE VERIFICATION
======================================================================
[PASS] Model: qwen3.5:4b
[PASS] Generation Latency: 29367 ms
[PASS] Tokens Evaluated: 150
Output: Thinking output generated: Thinking Process:

1.  **Analyze the Request:**
    *   Equation: $3x + 6 = 21$
    *   Task: State the first step to solve...
======================================================================
QWEN 3.5 4B VERIFICATION: SUCCESS (Exit Code 0)
```

---

### 3. Failover & Timeout Safeguards

To prevent student UI hangs during peak CPU load:
- The default timeout is configurable via `QWEN_TIMEOUT_SECONDS` (default: 45.0s).
- If inference exceeds this SLA, `QwenAdapter` raises an `OllamaException(ErrorCategory.TIMEOUT)`.
- The circuit breaker records the timeout failure and immediately cascades to **Tier 3 (Gemma 4 E2B)** or **Tier 4 (Curriculum Engine)**.

