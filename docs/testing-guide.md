# SUTRA LEARN — Testing & Quality Assurance Guide

## 1. Quality Assurance Philosophy

In SUTRA LEARN, software reliability is verified through reproducible, automated suites covering every layer of the architecture:
1. **Mathematical & Algorithmic Correctness**: BKT calculation, DAG dependency validation, streak boosts, and prerequisite unlock sequences.
2. **REST API Contract Verification**: Request/response schemas, status codes, bearer token authentication, and RBAC boundaries.
3. **Hermetic End-to-End Verification**: Complete learner and educator lifecycles executed against an isolated test server and ephemeral database.
4. **Visual & Cross-Device Responsiveness**: Chrome headless screenshot capture across Desktop (1440px), Tablet (1024px), and Mobile (390px).
5. **Code Style & Type Safety**: Strict TypeScript compilation (`tsc -b`) and zero-warning linter audits (`oxlint`).

---

## 2. Running Automated Test Suites

### 2.1 Backend Pytest Suite (35 Tests)
The backend test suite validates database CRUD, BKT scoring algorithms, NCERT curriculum content, security boundaries, and AI endpoints.

```bash
# Run all backend tests
pytest backend/tests -v

# Run specific test modules
pytest backend/tests/test_api.py -v          # API contracts, auth, and student/teacher routes
pytest backend/tests/test_engine.py -v       # BKT algorithms and Bayesian probability updates
pytest backend/tests/test_content.py -v      # NCERT Class 8 curriculum DAG integrity
pytest backend/tests/test_scenarios.py -v    # Multi-step pedagogical journey simulations
pytest backend/tests/test_ai.py -v           # AI Tutor, Educator Assistant, and prompt grounding
```

**Verified Test Result**:
```
============================== 35 passed in 1.76s ==============================
```

---

### 2.2 Hermetic E2E Verification Script (`verify_e2e.py`)
The automated E2E script executes a 14-stage integration run covering both student and educator domains against an ephemeral uvicorn instance on port 8005 with an isolated database.

```bash
python scripts/verify_e2e.py
```

**The 14 Verification Stages**:
1. `Stage 01`: Backend Health & SQLite WAL Mode
2. `Stage 02`: Database Readiness & Seed Integrity
3. `Stage 03`: Student Authentication & Token Issuance
4. `Stage 04`: Student Curriculum Access
5. `Stage 05`: Assessment Submission & Idempotent Retry Guarantee
6. `Stage 06`: BKT Mastery Probability Progression
7. `Stage 07`: Adaptive Recommendation Engine
8. `Stage 08`: Teacher Authentication & RBAC Verification
9. `Stage 09`: Teacher Cohort Analytics
10. `Stage 10`: Pedagogical Override with Mandatory Clinical Rationale
11. `Stage 11`: Audit Trail Verification with Cryptographic Hash Check
12. `Stage 12`: Student Privacy Boundary Enforcement (Cross-Student Access Blocked)
13. `Stage 13`: Teacher Role Enforcement (Student Blocked from Teacher Endpoints)
14. `Stage 14`: Unauthenticated Access Guard (401 on Missing Bearer Token)

**Verified E2E Result**:
```
======================================================================
E2E VERIFICATION RESULT: 14/14 STAGES PASSED (100%)
EXIT CODE: 0
======================================================================
```

---

### 2.3 Frontend Linting & Type Compilation

```bash
# High-speed static analysis (Oxlint)
npm --prefix frontend run lint

# Expected Output: Found 0 warnings and 0 errors.

# TypeScript strict type checking & production Vite build
npm --prefix frontend run build

# Expected Output:
# ✓ 37 modules transformed.
# dist/assets/index-*.css   13.37 kB │ gzip:  3.20 kB
# dist/assets/index-*.js   372.64 kB │ gzip: 96.68 kB
# ✓ built in ~200ms
```

---

### 2.4 Browser Visual Screenshot Capture across Viewports

```bash
python scripts/capture_screenshots.py
```
This script launches an ephemeral backend and frontend preview, capturing 48 visual artifacts into `screenshots/`:
- **16 distinct application screens** (Gateways, Logins, Pathways, Lessons, Assessments, Dashboards, Insights, Interventions, Audit, AI Tutor, and AI Educator Intelligence).
- **3 responsive viewports**: Desktop ($1440 \times 960$), Tablet ($1024 \times 768$), and Mobile ($390 \times 844$).

**Verified Result**: `CAPTURED 48/48 SCREENSHOTS TO screenshots/` (100% success).

