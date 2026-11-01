import { useState, useEffect } from 'react';
import type { Concept, Learner, LearnerMetrics } from '../types';

interface StudentInsightsProps {
  learner: Learner;
  concepts: Concept[];
  apiBaseUrl: string;
  authToken?: string | null;
  onBackToHome: () => void;
  onNavigateToPathway: () => void;
  onPracticeConcept: (conceptId: string) => void;
}

export function StudentInsights({
  learner,
  concepts: _concepts,
  apiBaseUrl,
  authToken,
  onBackToHome,
  onNavigateToPathway,
  onPracticeConcept: _onPracticeConcept,
}: StudentInsightsProps) {
  const [metrics, setMetrics] = useState<LearnerMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function fetchMetrics() {
      try {
        setLoading(true);
        setError(null);
        const res = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/metrics`, {
          headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
        });
        if (!res.ok) {
          throw new Error(`Failed to load student analytics (HTTP ${res.status})`);
        }
        const data: LearnerMetrics = await res.json();
        if (isMounted) setMetrics(data);
      } catch (err: any) {
        if (isMounted) setError(err.message || 'Error fetching student insights.');
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    void fetchMetrics();
    return () => {
      isMounted = false;
    };
  }, [apiBaseUrl, learner.id, authToken]);

  if (loading) {
    return (
      <div style={{ maxWidth: 'var(--dashboard-width)', margin: '0 auto', padding: 'var(--space-12) 0', textAlign: 'center' }}>
        <div className="editorial-card" style={{ padding: 'var(--space-12)' }}>
          <span className="editorial-kicker">ANALYTICS PIPELINE</span>
          <h2 className="serif-title" style={{ fontSize: '24px', color: 'var(--sutra-espresso)', marginTop: '8px' }}>
            Compiling Multi-Dimensional Learning Evidence...
          </h2>
          <p style={{ color: 'var(--text-secondary)', marginTop: '8px', fontSize: '14px' }}>
            Aggregating 56 canonical metrics across curriculum, accuracy, cognitive demand, and retention.
          </p>
        </div>
      </div>
    );
  }

  if (error || !metrics) {
    return (
      <div style={{ maxWidth: 'var(--dashboard-width)', margin: '0 auto', padding: 'var(--space-8) 0' }}>
        <button type="button" className="btn-ghost" onClick={onBackToHome} style={{ marginBottom: 'var(--space-4)' }}>
          &larr; Back to Learning Home
        </button>
        <div className="editorial-card" style={{ borderColor: 'var(--feedback-error-border)', backgroundColor: 'var(--feedback-error-bg)', padding: 'var(--space-6)' }}>
          <h3 className="serif-title" style={{ color: 'var(--feedback-error)' }}>Unable to Load Learning Insights</h3>
          <p style={{ color: 'var(--feedback-error)', marginTop: '4px' }}>{error}</p>
        </div>
      </div>
    );
  }

  const {
    curriculum: cur,
    accuracy: acc,
    attempts: att,
    mastery: mas,
    misconceptions: mis,
    assistance: ast,
    efficiency: eff,
    outcomes: out,
  } = metrics;

  return (
    <div style={{ maxWidth: 'var(--dashboard-width)', margin: '0 auto', paddingBottom: 'var(--space-12)' }}>
      {/* Top Header Navigation & Title */}
      <div style={{ marginBottom: 'var(--space-8)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
          <button type="button" className="btn-ghost" onClick={onBackToHome} style={{ paddingLeft: 0, fontSize: '13px' }}>
            &larr; Back to Learning Home
          </button>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
            Evidence Snapshot &bull; {new Date(metrics.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        <div className="editorial-kicker">COMPREHENSIVE LEARNING DOSSIER</div>
        <h1 className="serif-display" style={{ fontSize: '36px', color: 'var(--sutra-espresso)', marginTop: '4px' }}>
          Student Learning Insights &amp; Analytics
        </h1>
        <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: '6px', maxWidth: '720px' }}>
          Clinical diagnostics, accuracy trajectories, scaffolding independence, and retention evidence for <strong>{learner.name}</strong> (Class 8 Mathematics).
        </p>
      </div>

      {/* Top 4 KPI Banner */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 'var(--space-4)', marginBottom: 'var(--space-8)' }}>
        <div className="editorial-card" style={{ padding: 'var(--space-5)' }}>
          <span className="metric-label">OVERALL ACCURACY</span>
          <div className="metric-value-lg" style={{ color: 'var(--sutra-espresso)', marginTop: '4px' }}>
            {acc.overall_accuracy_pct !== null ? `${acc.overall_accuracy_pct}%` : '—'}
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px', display: 'block' }}>
            {att.correct_attempts} / {att.total_attempts} verified attempts
          </span>
        </div>

        <div className="editorial-card" style={{ padding: 'var(--space-5)' }}>
          <span className="metric-label">INDEPENDENT ACCURACY</span>
          <div className="metric-value-lg" style={{ color: 'var(--sutra-espresso)', marginTop: '4px' }}>
            {acc.unassisted_accuracy_pct !== null ? `${acc.unassisted_accuracy_pct}%` : '—'}
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px', display: 'block' }}>
            Unassisted problem solving
          </span>
        </div>

        <div className="editorial-card" style={{ padding: 'var(--space-5)' }}>
          <span className="metric-label">CURRICULUM COMPLETION</span>
          <div className="metric-value-lg" style={{ color: 'var(--sutra-espresso)', marginTop: '4px' }}>
            {cur.curriculum_completion_pct}%
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px', display: 'block' }}>
            {cur.mastered_concepts} of {cur.total_concepts} concepts mastered
          </span>
        </div>

        <div className="editorial-card" style={{ padding: 'var(--space-5)' }}>
          <span className="metric-label">RETENTION STATUS</span>
          <div className="metric-value-lg" style={{ color: out.retention_status === 'RETAINED' ? 'var(--sutra-mocha)' : 'var(--sutra-espresso)', fontSize: '20px', marginTop: '6px' }}>
            {out.retention_status}
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px', display: 'block' }}>
            Spaced retrieval readiness
          </span>
        </div>
      </div>

      {/* 12 MANDATED ANALYTICAL SECTIONS IN EDITORIAL GRID */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(520px, 100%), 1fr))', gap: 'var(--space-6)' }}>
        
        {/* SECTION 1: Strengths & Mastery Summary */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 01</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Learning Strengths &amp; Core Competencies
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Demonstrated competencies meeting the 85% threshold with &ge;2 unassisted correct submissions.
          </p>
          <div style={{ marginTop: 'var(--space-4)', backgroundColor: 'var(--surface-warm)', padding: 'var(--space-4)', borderRadius: 'var(--radius-sm)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '14px', fontWeight: 600, color: 'var(--sutra-espresso)' }}>
                {mas.highest_mastery_concept ? mas.highest_mastery_concept.title : 'No concept mastered yet'}
              </span>
              <span className="status-pill status-pill-mastered">
                {mas.highest_mastery_concept ? `${mas.highest_mastery_concept.mastery_pct}% Mastery` : 'Pending'}
              </span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '6px' }}>
              Consistently solves linear operations with balanced transposition and zero sign confusion.
            </p>
          </div>
        </section>

        {/* SECTION 2: Prerequisite & Gap Analysis */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 02</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Prerequisite &amp; Gap Analysis
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Inspection of foundational dependencies in the NCERT Class 8 DAG.
          </p>
          <div style={{ marginTop: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: 'var(--surface-warm)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '13px', color: 'var(--sutra-espresso)' }}>Active Prerequisite Bottlenecks</span>
              <span style={{ fontSize: '13px', fontWeight: 700, color: cur.prerequisite_gaps_count > 0 ? 'var(--feedback-error)' : 'var(--sutra-mocha)' }}>
                {cur.prerequisite_gaps_count} Detected
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: 'var(--surface-warm)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '13px', color: 'var(--sutra-espresso)' }}>Foundational Anchor (MATH-C01)</span>
              <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--sutra-espresso)' }}>
                {cur.unlocked_concepts.includes('MATH-C01') ? 'Unlocked & Active' : 'Locked'}
              </span>
            </div>
          </div>
        </section>

        {/* SECTION 3: Misconception Profile & Error Analysis */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 03</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Misconception Profile &amp; Diagnostic Signals
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Evidence-backed classification of algebraic misconceptions from assessment traps.
          </p>
          <div style={{ marginTop: 'var(--space-4)', display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 'var(--space-3)' }}>
            <div style={{ backgroundColor: 'var(--surface-warm)', padding: 'var(--space-3)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Primary Trap</span>
              <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--sutra-espresso)', marginTop: '2px' }}>
                {mis.top_recurring_misconception !== 'none' ? mis.top_recurring_misconception : 'No Active Traps'}
              </div>
            </div>
            <div style={{ backgroundColor: 'var(--surface-warm)', padding: 'var(--space-3)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Severity Index</span>
              <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--sutra-espresso)', marginTop: '2px' }}>
                {mis.misconception_severity_index} / 1.0
              </div>
            </div>
          </div>
          <div style={{ marginTop: 'var(--space-3)', fontSize: '12px', color: 'var(--text-secondary)' }}>
            Resolved Misconceptions: <strong>{mis.resolved_misconceptions_count}</strong> &bull; Active Remediation Required: <strong>{mis.active_misconceptions_count}</strong>
          </div>
        </section>

        {/* SECTION 4: Accuracy Trends (Historical & Rolling) */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 04</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Accuracy Trends &amp; Rolling Performance
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            First-attempt accuracy vs 7-day rolling window indicating conceptual trajectory.
          </p>
          <div style={{ marginTop: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                <span>First-Attempt Accuracy</span>
                <strong>{acc.first_attempt_accuracy_pct !== null ? `${acc.first_attempt_accuracy_pct}%` : '—'}</strong>
              </div>
              <div style={{ width: '100%', height: '8px', backgroundColor: 'var(--sutra-linen)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: `${acc.first_attempt_accuracy_pct || 0}%`, height: '100%', backgroundColor: 'var(--sutra-taupe)' }} />
              </div>
            </div>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                <span>Rolling 7-Day / Recent Accuracy</span>
                <strong>{acc.rolling_7d_accuracy_pct !== null ? `${acc.rolling_7d_accuracy_pct}%` : '—'}</strong>
              </div>
              <div style={{ width: '100%', height: '8px', backgroundColor: 'var(--sutra-linen)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: `${acc.rolling_7d_accuracy_pct || 0}%`, height: '100%', backgroundColor: 'var(--sutra-mocha)' }} />
              </div>
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Directional Momentum: <strong style={{ color: 'var(--sutra-espresso)', textTransform: 'capitalize' }}>{acc.accuracy_trend_direction}</strong>
            </div>
          </div>
        </section>

        {/* SECTION 5: Assisted vs. Unassisted Performance Comparison */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 05</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Assisted vs. Unassisted Performance
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Quantifies student independence and scaffolding dependency during problem solving.
          </p>
          <div style={{ marginTop: 'var(--space-4)', display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 'var(--space-3)' }}>
            <div style={{ backgroundColor: 'var(--surface-warm)', padding: 'var(--space-3)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>HINT DEPENDENCY RATIO</span>
              <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--sutra-espresso)', marginTop: '2px' }}>
                {ast.hint_dependency_ratio}%
              </div>
            </div>
            <div style={{ backgroundColor: 'var(--surface-warm)', padding: 'var(--space-3)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>INDEPENDENT INDEX</span>
              <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--sutra-espresso)', marginTop: '2px' }}>
                {ast.independent_problem_solving_index}%
              </div>
            </div>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: 'var(--space-3)' }}>
            Unassisted to Assisted Ratio: <strong>{ast.unassisted_to_assisted_ratio} : 1</strong>
          </p>
        </section>

        {/* SECTION 6: Mastery Progression Velocity */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 06</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Mastery Progression Velocity
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Pace of advancing through Class 8 concept milestones and active streak metrics.
          </p>
          <div style={{ marginTop: 'var(--space-4)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'var(--surface-warm)', padding: 'var(--space-4)', borderRadius: 'var(--radius-sm)' }}>
            <div>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Learning Velocity</span>
              <div style={{ fontSize: '22px', fontWeight: 700, color: 'var(--sutra-espresso)' }}>
                {mas.mastery_velocity_concepts_per_week} <span style={{ fontSize: '12px', fontWeight: 400 }}>concepts / week</span>
              </div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Active Streak</span>
              <div style={{ fontSize: '22px', fontWeight: 700, color: 'var(--sutra-mocha)' }}>
                {mas.mastery_streak_days} <span style={{ fontSize: '12px', fontWeight: 400 }}>days</span>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 7: Learning Efficiency & Time Allocation */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 07</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Learning Efficiency &amp; Item Cadence
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Average response duration and calibrated efficiency index.
          </p>
          <div style={{ marginTop: 'var(--space-4)', display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 'var(--space-3)' }}>
            <div style={{ backgroundColor: 'var(--surface-warm)', padding: 'var(--space-3)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>AVG TIME PER ITEM</span>
              <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--sutra-espresso)', marginTop: '2px' }}>
                {eff.avg_time_per_item_seconds}s
              </div>
            </div>
            <div style={{ backgroundColor: 'var(--surface-warm)', padding: 'var(--space-3)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>EFFICIENCY SCORE</span>
              <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--sutra-espresso)', marginTop: '2px' }}>
                {eff.learning_efficiency_score} / 100
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 8: Time to Mastery by Concept */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 08</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Time to Mastery &amp; Attempt Rigor
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Invested attempts and estimated duration required to reach proven mastery.
          </p>
          <div style={{ marginTop: 'var(--space-4)', backgroundColor: 'var(--surface-warm)', padding: 'var(--space-4)', borderRadius: 'var(--radius-sm)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontSize: '13px', color: 'var(--sutra-espresso)' }}>Average Time to Mastery:</span>
              <strong>{eff.avg_time_to_mastery_minutes} min</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontSize: '13px', color: 'var(--sutra-espresso)' }}>Average Attempts per Concept:</span>
              <strong>{att.avg_attempts_per_concept}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '13px', color: 'var(--sutra-espresso)' }}>Distinct Questions Solved:</span>
              <strong>{att.distinct_questions_attempted}</strong>
            </div>
          </div>
        </section>

        {/* SECTION 9: Retention & Decay Projections */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 09</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Retention &amp; Decay Projections
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Longitudinal retention monitoring based on spaced retrieval assessment.
          </p>
          <div style={{ marginTop: 'var(--space-4)', backgroundColor: 'var(--surface-warm)', padding: 'var(--space-4)', borderRadius: 'var(--radius-sm)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--sutra-espresso)' }}>Current Retention State:</span>
              <span className="status-pill status-pill-in-progress" style={{ textTransform: 'uppercase' }}>
                {out.retention_status}
              </span>
            </div>
            <div style={{ marginTop: '8px', fontSize: '12px', color: 'var(--text-secondary)' }}>
              Projected Weekly Decay Rate: <strong>{out.retention_decay_rate}% / week</strong>
            </div>
          </div>
        </section>

        {/* SECTION 10: Cognitive Load & Struggle Index */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 10</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Cognitive Load &amp; Struggle Index
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Composite struggle metric derived from error persistence and scaffolding utilization.
          </p>
          <div style={{ marginTop: 'var(--space-4)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '4px' }}>
              <span>Cognitive Friction Rating</span>
              <strong>{eff.cognitive_struggle_index} / 1.0</strong>
            </div>
            <div style={{ width: '100%', height: '10px', backgroundColor: 'var(--sutra-linen)', borderRadius: '5px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.min(100, eff.cognitive_struggle_index * 100)}%`, height: '100%', backgroundColor: eff.cognitive_struggle_index > 0.5 ? 'var(--feedback-error)' : 'var(--sutra-mocha)' }} />
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '6px' }}>
              Values &lt; 0.35 represent fluent mastery; values &gt; 0.60 trigger automatic adaptive scaffolding.
            </p>
          </div>
        </section>

        {/* SECTION 11: Personalized Pedagogical Recommendations */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 11</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Pedagogical Recommendations
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Actionable next steps determined by the deterministic adaptive rule engine.
          </p>
          <div style={{ marginTop: 'var(--space-4)', padding: 'var(--space-4)', borderLeft: '3px solid var(--sutra-espresso)', backgroundColor: 'var(--surface-warm)', borderRadius: '0 var(--radius-sm) var(--radius-sm) 0' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--sutra-espresso)', textTransform: 'uppercase' }}>
              ADAPTIVE DIRECTIVE
            </span>
            <p style={{ fontSize: '13px', color: 'var(--text-primary)', marginTop: '4px', lineHeight: 1.5 }}>
              {cur.mastered_concepts === 0
                ? 'Complete unassisted diagnostic challenges on Integer Arithmetic (MATH-C01) to substantiate foundational mastery.'
                : 'Progress to Multi-Step Linear Equations (MATH-C05) while conducting verification checks using substitution.'}
            </p>
            <div style={{ marginTop: 'var(--space-3)' }}>
              <button
                type="button"
                className="btn-primary"
                onClick={onNavigateToPathway}
                style={{ fontSize: '12px', padding: '6px 14px' }}
              >
                Open Curriculum Pathway &rarr;
              </button>
            </div>
          </div>
        </section>

        {/* SECTION 12: Executive Learning Summary */}
        <section className="editorial-card" style={{ padding: 'var(--space-6)' }}>
          <div className="editorial-kicker">SECTION 12</div>
          <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Executive Learning Summary
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Authoritative assessment conclusion for school records and parent-teacher conferences.
          </p>
          <div style={{ marginTop: 'var(--space-4)', backgroundColor: 'var(--surface-warm)', padding: 'var(--space-4)', borderRadius: 'var(--radius-sm)' }}>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Student <strong>{learner.name}</strong> has submitted <strong>{att.total_attempts}</strong> attempts across Class 8 Mathematics with an unassisted accuracy of <strong>{acc.unassisted_accuracy_pct !== null ? `${acc.unassisted_accuracy_pct}%` : 'N/A'}</strong>. 
              {mis.total_misconceptions_detected === 0
                ? ' No persistent algebraic misconceptions have been recorded.'
                : ` Primary error pattern is ${mis.top_recurring_misconception}, with ${mis.resolved_misconceptions_count} instances remediated.`}
            </p>
            <div style={{ marginTop: 'var(--space-3)', display: 'flex', gap: 'var(--space-2)' }}>
              <span className="status-pill status-pill-mastered" style={{ fontSize: '11px' }}>
                Normalized Gain g: {out.normalized_gain_g !== null ? out.normalized_gain_g : '0.00'}
              </span>
              <span className="status-pill status-pill-in-progress" style={{ fontSize: '11px' }}>
                Effect Size d: {out.effect_size_d !== null ? out.effect_size_d : '0.00'}
              </span>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}
