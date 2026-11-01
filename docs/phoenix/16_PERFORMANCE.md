# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 16: PERFORMANCE BENCHMARKING & RESOURCE UTILIZATION
**Version:** 1.0.0  
**Domain 18 (400 pts):** Performance & Resource Optimization  

---

### 1. Empirical Latency Measurements

Across live runs on Windows 11 host environment:

| Component / Subsystem | Operation Tested | Evaluated Tokens / Size | Measured Latency | Throughput / SLA |
| :--- | :--- | :--- | :--- | :--- |
| **Cloud (Gemini)** | Health probe & model discovery | 46 models listed | $2,797$ ms | SLA $< 3,000$ ms |
| **Local Reasoning (Qwen 3.5 4B)** | Multi-step algebraic reasoning | 150 tokens (inc. thinking) | $29,821$ ms | ~5 tokens/sec on local CPU |
| **Local Direct (Gemma 4 E2B)** | Concise step-by-step guidance | 15 tokens | $14,032$ ms | ~1.1 tokens/sec on local CPU |
| **Deterministic Fallback Engine** | NCERT curriculum retrieval & hints | Full lesson grounding | $1.08$ ms | Instantaneous (sub-5ms SLA) |
| **Mathematical Validator** | Algebraic root step evaluation | 3-step equation chain | $0.25$ ms | Instantaneous |
| **Database Queries (WAL Mode)** | Cohort analytics retrieval | 4 students, 6 concepts | $1.4$ ms | High concurrency support |
| **Frontend Static Linter** | Oxlint AST scan | 30 files / 116 rules | $1,194$ ms | 0 warnings, 0 errors |
| **Frontend Production Build** | TypeScript compilation & Vite bundle | 36 modules, 391 kB JS | $2,731$ ms | Clean asset chunking |

---

### 2. Frontend Bundle Footprint

- **Main JS Bundle:** `dist/assets/index-CGfDL9Ao.js`: $391.76$ kB ($100.38$ kB gzipped).
- **Styles Bundle:** `dist/assets/index-jwj75MK1.css`: $13.37$ kB ($3.20$ kB gzipped).
- **HTML Shell:** `dist/index.html`: $0.99$ kB.
- **Tree-Shaking:** Unused vendor modules eliminated via ES module tree-shaking.

