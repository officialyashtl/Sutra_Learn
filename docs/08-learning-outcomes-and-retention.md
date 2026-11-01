# SUTRA LEARN — Learning Outcomes & Longitudinal Retention
**Document ID:** `docs/08-learning-outcomes-and-retention.md`  
**Execution Standard:** Educational Technology Architect + Adaptive Learning Systems Engineer  
**Timestamp:** 2026-11-01T17:27:00+05:30  
**Status:** IMPLEMENTED & VERIFIED  

---

## 1. Multi-Stage Learning Assessment Architecture

Educational progress is measured across four discrete stages rather than a single point-in-time score:

1. **Stage I: Baseline Diagnostic Assessment**
   - Unassisted first attempts on diagnostic question bank.
   - Evaluates initial student proficiency prior to targeted instruction.
   - Preserved as `outcomes.baseline_score_pct`.

2. **Stage II: Formative Adaptive Instruction**
   - Socratic guidance, progressive hints, and step-by-step scaffolding.
   - Distinguishes assisted attempts (`hint_used=1`) from unassisted problem solving.

3. **Stage III: Post-Learning Verification**
   - Minimum 2 distinct unassisted items meeting $\ge 85\%$ accuracy threshold.
   - Required for transitioning concept state to `mastered`.

4. **Stage IV: Longitudinal Delayed Retention**
   - Spaced retrieval probes scheduled $\ge 7$ calendar days after mastery acquisition.
   - Defends against transient cramming vs. durable algebraic intuition.

---

## 2. Discrete Retention States

The platform categorizes each concept and learner into one of six mutually exclusive retention states:

| Retention State | Formal Definition & Trigger Criteria |
|---|---|
| **NOT SCHEDULED** | Concept is unattempted or currently locked behind prerequisites. |
| **PENDING** | Mastery recently achieved; delayed retention window ($T \ge 7\text{ days}$) has not elapsed. |
| **REASSESSED** | Spaced retrieval assessment completed; evaluation in progress. |
| **RETAINED** | Verified durable mastery: accuracy $\ge 85\%$ on delayed reassessment with $\ge 2$ unassisted items. |
| **NEEDS REINFORCEMENT** | Retention decay observed: accuracy dropped below $70\%$ on reassessment. Automatically routes to `SCAFFOLD` or `BRIDGE_BACK`. |
| **INSUFFICIENT EVIDENCE** | Incomplete attempt history; fewer than 2 graded submissions available. |

---

## 3. Mathematical Outcome Formulations

### Absolute Learning Gain ($\Delta G$)
$$\Delta G = \text{Score}_{\text{post}} - \text{Score}_{\text{pre}}$$

### Hake's Normalized Learning Gain ($g$)
Evaluates learning effectiveness relative to available headroom:
$$g = \frac{\text{Score}_{\text{post}} - \text{Score}_{\text{pre}}}{100 - \text{Score}_{\text{pre}}}$$
- **High Gain:** $g \ge 0.70$
- **Medium Gain:** $0.30 \le g < 0.70$
- **Low Gain:** $g < 0.30$

### Cohen's Standardized Effect Size ($d$)
$$d = \frac{\Delta G}{\sigma_{\text{pooled}}}$$
Where $\sigma_{\text{pooled}} \approx 15\%$ represents the population standard deviation across NCERT Class 8 cohorts.

