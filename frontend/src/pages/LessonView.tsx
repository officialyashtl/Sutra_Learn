import { useState, useEffect } from 'react';
import type { Concept, Lesson } from '../types';

interface LessonViewProps {
  concept: Concept;
  onBack: () => void;
  onStartAssessment: (conceptId: string) => void;
  onOpenTutor?: (conceptId: string) => void;
  apiBaseUrl?: string;
}

export function LessonView({
  concept,
  onBack,
  onStartAssessment,
  onOpenTutor,
  apiBaseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
}: LessonViewProps) {
  const [fetchedLesson, setFetchedLesson] = useState<Lesson | undefined>();
  const activeLesson = concept.lesson || fetchedLesson;

  useEffect(() => {
    if (concept.lesson) {
      return;
    }
    let isMounted = true;
    async function loadLessonDetail() {
      try {
        const res = await fetch(`${apiBaseUrl}/api/v1/concepts/${concept.id}`);
        if (res.ok) {
          const detail = await res.json();
          if (isMounted && detail.lesson) {
            setFetchedLesson(detail.lesson);
          }
        }
      } catch (err) {
        console.warn('Failed to fetch lesson detail:', err);
      }
    }
    void loadLessonDetail();
    return () => {
      isMounted = false;
    };
  }, [concept.id, concept.lesson, apiBaseUrl]);

  return (
    <div style={{ maxWidth: 'var(--reading-width)', margin: '0 auto' }}>
      {/* Navigation Breadcrumb */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)' }}>
        <button
          type="button"
          className="btn-ghost"
          style={{ fontSize: '13px', paddingLeft: 0 }}
          onClick={onBack}
        >
          &larr; Return to Curriculum
        </button>
        <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>
          {concept.code} &bull; Class 8 Mathematics
        </span>
      </div>

      <article
        className="editorial-card"
        style={{
          padding: 'var(--space-8)',
          backgroundColor: 'var(--surface-white)',
        }}
        aria-labelledby="lesson-heading"
      >
        {/* Editorial Header */}
        <header className="card-header-line" style={{ display: 'block', paddingBottom: 'var(--space-5)' }}>
          <span className="editorial-kicker">MATHEMATICAL FOUNDATION &bull; LESSON</span>
          <h1 id="lesson-heading" className="serif-display" style={{ fontSize: '32px', color: 'var(--sutra-espresso)', marginTop: '4px' }}>
            {activeLesson?.title || concept.title}
          </h1>
          <div
            style={{
              marginTop: 'var(--space-4)',
              padding: 'var(--space-3) var(--space-4)',
              backgroundColor: 'var(--surface-warm)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-md)',
            }}
          >
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--sutra-mocha)', letterSpacing: '0.05em' }}>
              Core Pedagogical Objective:
            </span>
            <p style={{ fontSize: '14px', color: 'var(--text-primary)', marginTop: '2px', lineHeight: 1.5 }}>
              {activeLesson?.objective || concept.description}
            </p>
          </div>
        </header>

        {/* SECTION 1: KEY PRINCIPLES */}
        {activeLesson?.key_principles && activeLesson.key_principles.length > 0 && (
          <section style={{ marginBottom: 'var(--space-8)' }} aria-label="Key Principles">
            <h2 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginBottom: 'var(--space-3)' }}>
              1. Fundamental Mathematical Principles
            </h2>
            <div
              style={{
                backgroundColor: 'var(--surface-paper)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: 'var(--space-4) var(--space-5)',
              }}
            >
              <ul style={{ listStyleType: 'disc', paddingLeft: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {activeLesson.key_principles.map((principle, idx) => (
                  <li key={idx} style={{ fontSize: '14px', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                    {principle}
                  </li>
                ))}
              </ul>
            </div>
          </section>
        )}

        {/* SECTION 2: WORKED EXAMPLE & STEP-BY-STEP SOLUTION */}
        {activeLesson?.worked_steps && activeLesson.worked_steps.length > 0 && (
          <section style={{ marginBottom: 'var(--space-8)' }} aria-label="Step-by-step Worked Example">
            <h2 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginBottom: 'var(--space-2)' }}>
              2. Fully Worked Solution Walkthrough
            </h2>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: 'var(--space-4)', lineHeight: 1.5 }}>
              Notice how inverse operations and balance rules preserve equality on both sides of the relation:
            </p>

            <div>
              {activeLesson.worked_steps.map((step) => (
                <div key={step.step_number} className="worked-step-card">
                  <div className="step-num-kicker">
                    Step {step.step_number} &bull; {step.action}
                  </div>
                  <div className="math-display-block" style={{ fontSize: '20px', padding: 'var(--space-3)', margin: 'var(--space-3) 0' }}>
                    {step.expression}
                  </div>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                    <strong style={{ color: 'var(--text-primary)' }}>Mathematical Reasoning:</strong> {step.reasoning}
                  </p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* SECTION 3: COMMON MISCONCEPTIONS */}
        {activeLesson?.common_pitfalls && activeLesson.common_pitfalls.length > 0 && (
          <section className="pitfall-callout" aria-label="Common Pitfalls and Misconceptions">
            <h3 style={{ fontSize: '14px', fontWeight: 700, color: 'var(--feedback-warning)', marginBottom: '4px' }}>
              ⚠️ Common Misconceptions to Avoid
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: 'var(--space-3)' }}>
              Frequent cognitive friction points observed in algebra:
            </p>
            <ul style={{ listStyleType: 'disc', paddingLeft: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {activeLesson.common_pitfalls.map((pitfall, idx) => (
                <li key={idx} style={{ fontSize: '13px', color: 'var(--text-primary)', lineHeight: 1.5 }}>
                  {pitfall}
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* SECTION 4: KNOWLEDGE CHECK */}
        {activeLesson?.interactive_prompt && (
          <div
            style={{
              marginTop: 'var(--space-6)',
              padding: 'var(--space-4) var(--space-5)',
              border: '1px solid var(--border-default)',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--surface-warm)',
            }}
          >
            <span className="editorial-kicker">COMPREHENSION CHECK</span>
            <p style={{ fontSize: '14px', fontWeight: 600, color: 'var(--sutra-espresso)', marginTop: '4px' }}>
              {activeLesson.interactive_prompt}
            </p>
          </div>
        )}

        {/* Lesson Footer Actions */}
        <footer
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginTop: 'var(--space-8)',
            borderTop: '1px solid var(--border-subtle)',
            paddingTop: 'var(--space-5)',
            flexWrap: 'wrap',
            gap: 'var(--space-3)',
          }}
        >
          <button type="button" className="btn-secondary" onClick={onBack}>
            &larr; Back to Curriculum
          </button>
          <div style={{ display: 'flex', gap: '8px' }}>
            {onOpenTutor && (
              <button
                type="button"
                className="btn-secondary"
                onClick={() => onOpenTutor(concept.id)}
                style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
              >
                <span>✨</span>
                <span>Ask AI Tutor</span>
              </button>
            )}
            <button type="button" className="btn-primary" onClick={() => onStartAssessment(concept.id)}>
              Start Diagnostic Practice &rarr;
            </button>
          </div>
        </footer>
      </article>
    </div>
  );
}
