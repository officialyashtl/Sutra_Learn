import { useState, useEffect } from 'react';
import type { Concept, ConceptProgress, Learner, StudentAttemptHistoryItem, LearnerMetrics } from '../types';

interface StudentHomeProps {
  learner: Learner;
  concepts: Concept[];
  progressMap: Record<string, ConceptProgress>;
  apiBaseUrl: string;
  authToken?: string | null;
  onOpenLesson: (conceptId: string) => void;
  onOpenAssessment: (conceptId: string) => void;
  onViewPathway: () => void;
}

export function StudentHome({
  learner,
  concepts,
  progressMap,
  apiBaseUrl,
  authToken,
  onOpenLesson,
  onOpenAssessment,
  onViewPathway,
}: StudentHomeProps) {
  const [recentAttempts, setRecentAttempts] = useState<StudentAttemptHistoryItem[]>([]);
  const [canonicalMetrics, setCanonicalMetrics] = useState<LearnerMetrics | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function fetchData() {
      try {
        const headers: Record<string, string> = authToken ? { Authorization: `Bearer ${authToken}` } : {};
        
        // 1. Fetch recent attempts
        const res = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/attempts`, { headers });
        if (res.ok && isMounted) {
          const data = await res.json();
          setRecentAttempts((data.attempts || []).slice(0, 5));
        }

        // 2. Fetch canonical single-source-of-truth metrics
        const mRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/metrics`, { headers });
        if (mRes.ok && isMounted) {
          const mData = await mRes.json();
          setCanonicalMetrics(mData);
        }
      } catch {
        // preserve clean state
      }
    }
    void fetchData();
    return () => {
      isMounted = false;
    };
  }, [apiBaseUrl, learner.id, authToken]);

  // Determine current focus concept (first unlocked that is not mastered, or first concept)
  const currentConcept =
    concepts.find((c) => {
      const p = progressMap[c.id];
      return c.is_unlocked && (!p || p.status !== 'mastered');
    }) || concepts[0];

  const currentProg = currentConcept ? progressMap[currentConcept.id] : undefined;

  // Use canonical metrics if available, fallback to progressMap
  const progressList = Object.values(progressMap);
  const masteredCount = canonicalMetrics
    ? canonicalMetrics.curriculum.mastered_concepts
    : progressList.filter((p) => p.status === 'mastered').length;

  const inProgressCount = canonicalMetrics
    ? canonicalMetrics.curriculum.in_progress_concepts
    : progressList.filter((p) => p.status === 'in_progress').length;

  const overallAccuracy = canonicalMetrics
    ? canonicalMetrics.accuracy.overall_accuracy_pct
    : (progressList.reduce((acc, p) => acc + (p.total_attempts || 0), 0) > 0
        ? Math.round(
            (progressList.reduce((acc, p) => acc + (p.unassisted_correct || 0), 0) /
              progressList.reduce((acc, p) => acc + (p.total_attempts || 0), 0)) *
              100
          )
        : null);

  return (
    <div style={{ maxWidth: 'var(--dashboard-width)', margin: '0 auto' }}>
      {/* 1. PRIMARY INTRODUCTION (65% / 35% Editorial Grid) */}
      <section
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: 'var(--space-8)',
          alignItems: 'start',
          marginBottom: 'var(--space-8)',
          paddingBottom: 'var(--space-6)',
          borderBottom: '1px solid var(--border-subtle)',
        }}
        aria-label="Student Introduction"
      >
        {/* Left: 65% Editorial Greeting */}
        <div style={{ flex: '1.8' }}>
          <div className="editorial-kicker">CLASSROOM / MATHEMATICS / CLASS 8</div>
          <h1
            className="serif-display"
            style={{ fontSize: '38px', color: 'var(--sutra-espresso)', lineHeight: 1.15, marginTop: '4px' }}
          >
            Welcome, {learner.name.split(' ')[0]}.
          </h1>
          <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: 'var(--space-3)', lineHeight: 1.6, maxWidth: '620px' }}>
            You are building your foundation in <strong>Linear Equations and Prerequisite Concepts</strong>.
            Every problem is a signal to understand your thinking, not a test to assign a label.
          </p>
        </div>

        {/* Right: 35% Compact Real Progress Summary */}
        <div
          className="editorial-card"
          style={{
            backgroundColor: 'var(--surface-warm)',
            border: '1px solid var(--border-default)',
            padding: 'var(--space-5)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--sutra-mocha)' }}>
              Curriculum Progress
            </span>
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)' }}>
              {masteredCount} of {concepts.length} Mastered
            </span>
          </div>

          {/* Progress bar */}
          <div style={{ width: '100%', height: '6px', backgroundColor: 'var(--surface-linen)', borderRadius: '3px', overflow: 'hidden', marginBottom: 'var(--space-4)' }}>
            <div
              style={{
                width: `${concepts.length > 0 ? (masteredCount / concepts.length) * 100 : 0}%`,
                height: '100%',
                backgroundColor: 'var(--sutra-mocha)',
              }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-3)', fontSize: '12px' }}>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block' }}>Verified Accuracy</span>
              <strong className="tabular-nums" style={{ fontSize: '16px', color: 'var(--sutra-espresso)' }}>
                {overallAccuracy !== null ? `${overallAccuracy}%` : 'No attempts yet'}
              </strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)', display: 'block' }}>Active Units</span>
              <strong style={{ fontSize: '16px', color: 'var(--sutra-espresso)' }}>
                {inProgressCount} in study
              </strong>
            </div>
          </div>
        </div>
      </section>

      {/* 2. PRIMARY LEARNING FEATURE (Visually Dominant Next Action) */}
      {currentConcept && (
        <section
          className="editorial-card"
          style={{
            marginBottom: 'var(--space-8)',
            borderLeft: '4px solid var(--sutra-mocha)',
            padding: 'var(--space-6) var(--space-8)',
            backgroundColor: 'var(--surface-white)',
          }}
          aria-label="Recommended Next Learning Step"
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
            <div style={{ maxWidth: '720px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                <span className="editorial-kicker" style={{ margin: 0 }}>
                  CURRENT FOCUS &bull; {currentConcept.id}
                </span>
                <span className={`status-pill ${currentProg?.status || 'not_started'}`}>
                  {currentProg?.status ? currentProg.status.replace('_', ' ') : 'Ready to begin'}
                </span>
              </div>
              <h2 className="serif-title" style={{ fontSize: '26px', color: 'var(--sutra-espresso)', marginBottom: '8px' }}>
                {currentConcept.title}
              </h2>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                {currentConcept.description}
              </p>
              {currentProg?.last_recommended_outcome && (
                <div style={{ marginTop: 'var(--space-3)', fontSize: '13px', color: 'var(--sutra-mocha)', fontStyle: 'italic' }}>
                  Adaptive engine recommendation: <strong>{currentProg.last_recommended_outcome}</strong>
                </div>
              )}
            </div>

            {/* Dominant Actions */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)', minWidth: '180px' }}>
              <button
                type="button"
                className="btn-primary"
                style={{ width: '100%', height: '46px', fontSize: '14px' }}
                onClick={() => onOpenAssessment(currentConcept.id)}
              >
                Practice Concept &rarr;
              </button>
              <button
                type="button"
                className="btn-secondary"
                style={{ width: '100%' }}
                onClick={() => onOpenLesson(currentConcept.id)}
              >
                Study Lesson
              </button>
            </div>
          </div>
        </section>
      )}

      {/* 3. CONCEPT PROGRESSION SEQUENCE (Connected Editorial Layout) */}
      <section style={{ marginBottom: 'var(--space-8)' }} aria-label="Class 8 Learning Sequence">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 'var(--space-4)' }}>
          <div>
            <span className="editorial-kicker">CURRICULUM ARCHITECTURE</span>
            <h3 className="serif-title" style={{ fontSize: '22px', color: 'var(--sutra-espresso)' }}>
              Prerequisite & Equation Progression
            </h3>
          </div>
          <button
            type="button"
            className="btn-ghost"
            style={{ color: 'var(--sutra-mocha)', fontWeight: 600, fontSize: '13px' }}
            onClick={onViewPathway}
          >
            Explore Interactive Pathway Map &rarr;
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 'var(--space-4)' }}>
          {concepts.map((concept, index) => {
            const prog = progressMap[concept.id];
            const isUnlocked = concept.is_unlocked ?? true;
            const status = prog?.status || (isUnlocked ? 'not_started' : 'locked');

            return (
              <div
                key={concept.id}
                className="editorial-card"
                style={{
                  opacity: isUnlocked ? 1 : 0.75,
                  backgroundColor: isUnlocked ? 'var(--surface-white)' : 'var(--surface-warm)',
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-2)' }}>
                  <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                    {index + 1}. {concept.id}
                  </span>
                  <span className={`status-pill ${status}`}>
                    {status.replace('_', ' ')}
                  </span>
                </div>

                <h4 className="serif-title" style={{ fontSize: '17px', color: 'var(--sutra-espresso)', marginBottom: '6px' }}>
                  {concept.title}
                </h4>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.5, flex: 1, marginBottom: 'var(--space-4)' }}>
                  {concept.description}
                </p>

                {/* Prerequisites notice if locked */}
                {!isUnlocked && concept.missing_prerequisites && concept.missing_prerequisites.length > 0 && (
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: 'var(--space-3)' }}>
                    Requires: {concept.missing_prerequisites.join(', ')}
                  </div>
                )}

                <div style={{ display: 'flex', gap: 'var(--space-2)', marginTop: 'auto', paddingTop: 'var(--space-3)', borderTop: '1px solid var(--border-subtle)' }}>
                  <button
                    type="button"
                    className="btn-secondary"
                    style={{ flex: 1, fontSize: '12px', height: '36px' }}
                    onClick={() => onOpenLesson(concept.id)}
                  >
                    Lesson
                  </button>
                  <button
                    type="button"
                    className="btn-primary"
                    style={{ flex: 1, fontSize: '12px', height: '36px' }}
                    onClick={() => onOpenAssessment(concept.id)}
                    disabled={!isUnlocked}
                  >
                    {isUnlocked ? 'Practice' : 'Locked'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* 4. RECENT ACTIVITY & EVIDENCE CHRONOLOGY */}
      {recentAttempts.length > 0 && (
        <section className="editorial-card" aria-label="Recent Evidence Submissions">
          <div className="card-header-line">
            <div>
              <span className="editorial-kicker">EVIDENCE LOG</span>
              <h3 className="serif-title" style={{ fontSize: '18px', color: 'var(--sutra-espresso)' }}>
                Recent Practice Submissions
              </h3>
            </div>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Verified server timestamps
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
            {recentAttempts.map((att) => (
              <div
                key={att.id}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: 'var(--space-3) var(--space-4)',
                  backgroundColor: att.is_correct ? 'var(--feedback-success-bg)' : 'var(--feedback-warning-bg)',
                  border: `1px solid ${att.is_correct ? 'var(--feedback-success-border)' : 'var(--feedback-warning-border)'}`,
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '13px',
                }}
              >
                <div>
                  <strong style={{ color: att.is_correct ? 'var(--feedback-success)' : 'var(--feedback-warning)' }}>
                    {att.is_correct ? '✓ Correct' : '✗ Incorrect'}
                  </strong>
                  <span style={{ marginLeft: '8px', color: 'var(--text-primary)' }}>
                    {att.concept_id} &bull; Item {att.question_id}
                  </span>
                  {att.hint_used && (
                    <span style={{ marginLeft: '6px', fontSize: '11px', color: 'var(--sutra-mocha)', fontWeight: 600 }}>
                      [💡 Hint Assisted]
                    </span>
                  )}
                  {att.misconception_tag && att.misconception_tag !== 'none' && (
                    <span style={{ marginLeft: '6px', fontSize: '11px', color: 'var(--feedback-warning)' }}>
                      ({att.misconception_tag})
                    </span>
                  )}
                </div>
                <span className="timestamp" style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                  {new Date(att.server_timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
