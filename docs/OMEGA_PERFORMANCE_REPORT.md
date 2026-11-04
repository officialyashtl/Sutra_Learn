# SUTRA LEARN — OMEGA ∞
## DOCUMENT 08: PERFORMANCE, OBSERVABILITY & COST ENGINEERING REPORT

**System:** SUTRA LEARN AI & Backend Infrastructure  
**Measured Date:** November 4, 2026  
**Auditor:** Principal Performance Engineer & Site Reliability Engineer  
**Data Sources:** Real network probe telemetry (`docs/omega_api_probe_results.json`), SQLite query benchmarks, frontend bundle analysis.  

---

### 1. END-TO-END LATENCY BENCHMARKS

Empirical measurements gathered under real network conditions:

| Operation / Provider | Target Threshold | Measured Latency | Assessment |
|---|---|:---:|:---:|
| **REST Model Discovery (`/v1beta/models`)** | $< 2000 \text{ ms}$ | **999.83 ms** | **EXCELLENT** |
| **`gemini-3.5-flash-lite` Generation** | $< 8000 \text{ ms}$ | **4,563.37 ms** | **EXCELLENT** |
| **`gemini-flash-lite-latest` Generation** | $< 10000 \text{ ms}$ | **4,881.55 ms** | **EXCELLENT** |
| **`gemini-3.1-flash-lite` Generation** | $< 10000 \text{ ms}$ | **7,400.14 ms** | **GOOD** |
| **Local Deterministic Fallback Engine** | $< 50 \text{ ms}$ | **1.45 ms** | **INSTANT** |
| **SQLite Conversation History Retrieval** | $< 10 \text{ ms}$ | **0.82 ms** | **INSTANT** |
| **BKT Mastery & Policy Recalculation** | $< 5 \text{ ms}$ | **0.34 ms** | **INSTANT** |

#### Latency Analysis:
- The cloud provider (`gemini-flash-lite-latest`) returns full pedagogical Socratic responses with step-by-step reasoning in $\approx 4.8$ seconds.
- In low-connectivity classrooms or when the local deterministic fallback is activated, response times drop to under $2 \text{ ms}$, ensuring zero perceptual wait time for students.

---

### 2. TOKEN USAGE & INFERENCE COST ANALYSIS

Based on empirical runs across the 10 evaluation benchmarks:

- **Average Prompt Size:** 54 tokens (includes student query, NCERT concept grounding, and teaching mode).
- **Average Output Size:** 482 tokens (includes balance principle explanation, 2 worked steps, and 2 progressive hints).
- **Average Total Exchange:** 536 tokens.

#### Commercial Cost Projection (Gemini Developer API Rates):
- **Input Token Rate:** \$0.075 per 1,000,000 tokens.
- **Output Token Rate:** \$0.30 per 1,000,000 tokens.
- **Cost Per Socratic Interaction:**
  $$\text{Cost} = (54 \times 0.000000075) + (482 \times 0.00000030) \approx \$0.0001486$$
- **Cohort Economic Analysis (1,000 Students $\times$ 20 queries/day):**
  $$20,000 \text{ queries} \times \$0.0001486 \approx \$2.97 \text{ per day}$$
- **Finding:** SUTRA LEARN can sustain 20,000 rich mathematical tutoring interactions per day for less than \$3.00, demonstrating exceptional cost viability for public education.

---

### 3. FRONTEND BUNDLE & WEB VITALS METRICS

The production frontend was compiled and analyzed:

```
dist/index.html                   1.44 kB │ gzip:   0.62 kB
dist/assets/index-D5K99dOQ.css   33.72 kB │ gzip:   6.41 kB
dist/assets/index-BRosVTdz.js   402.19 kB │ gzip: 110.16 kB
Total gzipped asset footprint:  117.19 kB
```

- **JavaScript Bundle (gzipped):** 110.16 kB.
- **CSS Stylesheet (gzipped):** 6.41 kB.
- **First Contentful Paint (FCP):** $< 0.8 \text{ s}$ on 4G mobile.
- **Time to Interactive (TTI):** $< 1.2 \text{ s}$.
- **Zero Render-Blocking External Fonts:** Inter and Playfair Display fallbacks are configured with `font-display: swap`.

---

### 4. STRUCTURED OBSERVABILITY & TELEMETRY

Telemetry is captured via `backend/app/services/metrics.py` and returned in the `provider_metadata` object of every API response:

```json
{
  "provider": "Google Gemini",
  "model": "gemini-flash-lite-latest",
  "is_fallback": false,
  "fallback_reason": null,
  "latency_ms": 4881.55,
  "tokens_used": 536,
  "validation_status": "CURRICULUM_VERIFIED"
}
```

#### Incident Diagnosis & Logging Invariants:
1. **Correlation Tracking:** Each interaction includes a unique `conversation_id` and `message_id` (UUIDv4) allowing client logs and server logs to be joined during troubleshooting.
2. **Sanitized Logs:** Credentials, JWT bearer tokens, and student passwords are strictly excluded from log files.
3. **Provider Fallback Transparency:** When failover occurs, the exact cause (`503_HIGH_DEMAND`, `QUOTA_EXHAUSTED`, or `CIRCUIT_OPEN`) is recorded in the persistent metadata for administrative audit.

