# SUTRA LEARN — KNOWN LIMITATIONS & ARCHITECTURAL DISCLOSURES
**Version:** 1.0.0 (Production Release)  
**Standard:** Full Transparency & Engineering Integrity  

---

## 1. Hosting & Persistence Disclosures

### 1.1 Render Free-Tier Ephemeral Storage
- **Context:** The production backend is currently deployed on Render's free tier without a paid persistent disk attachment.
- **Behavior:** The SQLite database file (`backend/sutra_learn.db`) resides on the container root filesystem. While data persists across standard requests and client sessions, the filesystem is recreated during service redeployments, container upgrades, or spin-down recreations.
- **Mitigation & Future Work:** For commercial high-availability deployments, attaching a Render Persistent Disk (`/var/data`) or adopting a cloud-hosted relational store (such as Supabase, Turso SQLite, or PostgreSQL) provides durable, multi-region persistence without altering application logic.

### 1.2 Free-Tier Cold Starts
- **Context:** Render's free tier spins down idle containers after 15 minutes of inactivity.
- **Behavior:** The initial request following an idle period may take 40–50 seconds to complete while the container boots and initializes SQLite. Once warmed, standard API latency drops to $< 250\text{ms}$.
- **Mitigation:** A health-check ping job (or upgrading to Render Starter tier) maintains warm instances 24/7.

---

## 2. Artificial Intelligence & Third-Party Dependencies

### 2.1 Google Gemini API Demand Spikes
- **Context:** Google's Gemini public API (`gemini-flash-lite-latest` / `gemini-3.1-flash-lite`) occasionally experiences transient `503 UNAVAILABLE` responses during global traffic surges.
- **Mitigation:** SUTRA LEARN implements a 3-tier safety net:
  1. Exponential backoff and jittered retries within `gemini_adapter.py`.
  2. Automatic cascade across model candidates (`gemini-3.1-flash-lite`, `gemini-flash-lite-latest`, `gemini-2.5-flash`).
  3. Sub-2ms deterministic NCERT Curriculum Engine fallback that generates pedagogy-grounded feedback without crashing or interrupting the student's learning session.

### 2.2 Offline Model Availability in Cloud Environments
- **Context:** SUTRA LEARN contains architecture for local Ollama-based inference (Qwen 3.5 4B & Gemma 4 E2B).
- **Behavior:** These local models are intended for local edge environments (laptops, on-premise school servers) with local GPUs or CPU memory. They are intentionally disabled in the cloud Render container in favor of the Google Gemini API to prevent memory exhaustion on 512MB RAM containers.

---

## 3. Curriculum & Pedagogical Scope

### 3.1 Subject & Grade Focus
- **Context:** SUTRA LEARN is purpose-built and calibrated specifically for **NCERT Class 8 Mathematics**, comprising 30 comprehensive concepts spanning Integer Arithmetic, Linear Equations, Quadrilaterals, Mensuration, and Exponents.
- **Extensibility:** The DAG-based curriculum registry is schema-driven and designed to ingest Class 9 and Class 10 mathematics graphs by adding concept and question definitions to `backend/app/content/`.
