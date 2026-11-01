# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 06: GEMMA 4 E2B LIGHTWEIGHT LOCAL FALLBACK PROVIDER
**Version:** 1.0.0  
**Domain 6 (650 pts):** AI Provider Infrastructure (Tier 3 Local Fallback)  

---

### 1. Model Profile & Operational Purpose

- **Model Tag:** `gemma4:e2b`
- **Host Endpoint:** `http://127.0.0.1:11434` (Ollama local inference runtime)
- **Model Digest:** `b37049369adf` (7.2 GB)
- **Adapter Module:** `backend/app/ai/ollama_adapters.py` (`GemmaAdapter`)

Gemma 4 E2B acts as the **Secondary Local Direct Fallback (Tier 3)**. When cloud inference is restricted and Tier 2 (Qwen) encounters latency or timeout pressure, Gemma 4 E2B steps in to provide concise, direct pedagogical scaffolding without heavy reasoning pre-computation overhead.

---

### 2. Live Performance & Prompt Evaluation

In the automated master acceptance suite (`scripts/ai/verify_ai_all.ps1`), Stage 05 executed a live prompt:
- **Prompt:** *"State the first step to solve 4x - 8 = 16 in 10 words or less."*
- **Generated Output:** *"Add 8 to both sides to isolate the variable term."*
- **Measured Latency:** $14,032$ ms on local CPU.
- **Tokens Evaluated:** 15 tokens.
- **Pedagogical Evaluation:** Exact mathematical precision conforming to NCERT inverse operation rules.

---

### 3. Failover & Health Detection

`GemmaAdapter` incorporates non-invasive TCP socket polling:
1. `is_available()` performs a non-blocking TCP socket check against `127.0.0.1:11434` and verifies the model tag in the local Ollama catalog.
2. If the model is pulled and the daemon is responsive, it reports `AVAILABLE`.
3. If inference breaches `GEMMA_TIMEOUT_SECONDS` (default: 20.0s), the orchestrator triggers immediate fallback to **Tier 4 (NCERT Curriculum Engine)**.

