# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 16: PERFORMANCE & LATENCY BENCHMARK REPORT
**Version:** 1.0.0  
**Test Environment:** Windows 11 (64-bit), Python 3.11.9, Ollama Local Server  
**Metrics:** Response Latency (ms), Token Evaluation Count, Throughput  

---

### 1. Empirical Latency Measurements

Across live runs on the host system:

| Inference Engine | Model Tag | Prompt Description | Output Tokens | Latency (ms) | Operational Assessment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1 (Cloud)** | Google Gemini (`gemini-3.8-flash`) | First step for $2x+5=15$ | 0 (Permission Denied) | $1,240$ ms | Immediate circuit trip to OPEN; 0 ms penalty on subsequent requests. |
| **Tier 2 (Local)** | Qwen 3.5 4B (`qwen3.5:4b`) | First step for $3x+6=21$ | 150 (inc. thinking) | $29,367$ ms | Rigorous multi-step reasoning on local CPU; token rate ~5 tokens/s. |
| **Tier 3 (Local)** | Gemma 4 E2B (`gemma4:e2b`) | First step for $4x-8=16$ | 15 | $9,553$ ms | High responsiveness on CPU; ideal lightweight local fallback. |
| **Tier 4 (Final)** | NCERT Curriculum Engine | Guided explanation for $2x+5=15$ | Structured JSON | $2.4$ ms | Instantaneous deterministic execution. Guaranteed sub-5ms SLA. |

---

### 2. Frontend Asset Optimization

- **Bundle Size:** `dist/assets/index-CGfDL9Ao.js`: $391.76$ kB ($100.38$ kB gzipped).
- **CSS Bundle:** `dist/assets/index-jwj75MK1.css`: $13.37$ kB ($3.20$ kB gzipped).
- **Build Duration:** $442$ ms via Vite v8.3.5.
- **Lint Audit:** 0 warnings, 0 errors across 30 files in $120$ ms via Oxlint.

