# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 05: QWEN 3.5 4B LOCAL REASONING INFERENCE PROVIDER
**Version:** 1.0.0  
**Domain 6 (650 pts):** AI Provider Infrastructure (Tier 2 Local Primary)  

---

### 1. Provider Specification

- **Model Tag:** `qwen3.5:4b`
- **Host Endpoint:** `http://127.0.0.1:11434` (Ollama local inference runtime)
- **Model Digest:** `d8b0f5e9760c` (2.7 GB)
- **Adapter Module:** `backend/app/ai/ollama_adapters.py` (`QwenAdapter`)

---

### 2. Operational Reasoning & CoT Stream Isolation

Qwen 3.5 4B is an advanced reasoning model that produces structured chain-of-thought traces wrapped in `<think>...</think>` tags (or in the `thinking` field of the Ollama v0.5+ API response) prior to generating final conversational answers.

#### Critical Security & Educational Safeguards:
1. **Never Expose Internal CoT:** The adapter strips raw `<think>` content from the student-facing response so that students receive structured pedagogical guidance rather than raw internal model musings.
2. **Fallback Content Extraction:** If the generation budget is consumed during deep reasoning and `content` is empty while `thinking` is populated, the adapter extracts the core pedagogical deductions cleanly.
3. **Bounded CPU Timeout:** When running on local CPU without dedicated GPU acceleration, Qwen 3.5 reasoning requires ~25s to 35s. The orchestrator enforces a configurable `QWEN_TIMEOUT_SECONDS` (default: 45.0s) to prevent thread exhaustion.

---

### 3. Empirical Verification Evidence

From execution of Stage 04 in `scripts/ai/verify_ai_all.ps1`:
```powershell
[PASS] Model: qwen3.5:4b
[PASS] Generation Latency: 29821 ms
[PASS] Tokens Evaluated: 150
Output: Thinking output generated: Thinking Process:
1. Analyze the Request: Equation: 3x + 6 = 21...
QWEN 3.5 4B VERIFICATION: SUCCESS (Exit Code 0)
```

