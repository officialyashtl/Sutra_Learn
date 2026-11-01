import { useState } from 'react';
import type { Concept, ConceptProgress } from '../types';

interface StudentPathwayProps {
  concepts: Concept[];
  progressMap: Record<string, ConceptProgress>;
  onOpenLesson: (conceptId: string) => void;
  onOpenAssessment: (conceptId: string) => void;
  onBackToHome: () => void;
}

interface ChapterGroup {
  number: number;
  title: string;
  conceptIds: string[];
}

const NCERT_CLASS_8_CHAPTERS: ChapterGroup[] = [
  { number: 1, title: 'Rational Numbers', conceptIds: ['MATH-C07', 'MATH-C08'] },
  { number: 2, title: 'Linear Equations in One Variable', conceptIds: ['MATH-C01', 'MATH-C02', 'MATH-C03', 'MATH-C04', 'MATH-C05', 'MATH-C06'] },
  { number: 3, title: 'Understanding Quadrilaterals', conceptIds: ['MATH-C09', 'MATH-C10'] },
  { number: 4, title: 'Data Handling', conceptIds: ['MATH-C11', 'MATH-C12'] },
  { number: 5, title: 'Squares and Square Roots', conceptIds: ['MATH-C13', 'MATH-C14'] },
  { number: 6, title: 'Cubes and Cube Roots', conceptIds: ['MATH-C15', 'MATH-C16'] },
  { number: 7, title: 'Comparing Quantities', conceptIds: ['MATH-C17', 'MATH-C18'] },
  { number: 8, title: 'Algebraic Expressions and Identities', conceptIds: ['MATH-C19', 'MATH-C20'] },
  { number: 9, title: 'Mensuration', conceptIds: ['MATH-C21', 'MATH-C22'] },
  { number: 10, title: 'Exponents and Powers', conceptIds: ['MATH-C23', 'MATH-C24'] },
  { number: 11, title: 'Direct and Inverse Proportions', conceptIds: ['MATH-C25', 'MATH-C26'] },
  { number: 12, title: 'Factorisation', conceptIds: ['MATH-C27', 'MATH-C28'] },
  { number: 13, title: 'Introduction to Graphs', conceptIds: ['MATH-C29', 'MATH-C30'] },
];

export function StudentPathway({
  concepts,
  progressMap,
  onOpenLesson,
  onOpenAssessment,
  onBackToHome,
}: StudentPathwayProps) {
  const [activeTab, setActiveTab] = useState<'chapters' | 'dag'>('chapters');

  // Index concepts by ID for fast lookup
  const conceptLookup = new Map<string, Concept>();
  for (const c of concepts) {
    conceptLookup.set(c.id, c);
  }

  // Linear Equations Track (C01 through C06)
  const linearTrack = ['MATH-C01', 'MATH-C02', 'MATH-C03', 'MATH-C04', 'MATH-C05', 'MATH-C06']
    .map((id) => conceptLookup.get(id))
    .filter((c): c is Concept => !!c);

  return (
    <div style={{ maxWidth: 'var(--dashboard-width)', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: 'var(--space-6)' }}>
        <button
          type="button"
          className="btn-ghost"
          style={{ fontSize: '13px', marginBottom: 'var(--space-3)', paddingLeft: 0 }}
          onClick={onBackToHome}
        >
          &larr; Back to Learning Home
        </button>
        <div className="editorial-kicker">NCERT CLASS 8 MATHEMATICS &bull; FULL CURRICULUM ARCHITECTURE</div>
        <h1 className="serif-display" style={{ fontSize: '36px', color: 'var(--sutra-espresso)', marginTop: '4px' }}>
          Interactive Learning Pathway
        </h1>
        <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: 'var(--space-2)', maxWidth: '720px', lineHeight: 1.6 }}>
          Explore all 13 chapters and 30 curriculum concepts. SUTRA LEARN tracks prerequisites and evidence-grounded mastery
          so you build confident mathematical intuition without gaps.
        </p>

        {/* View Switcher Tabs */}
        <div style={{ display: 'flex', gap: 'var(--space-3)', marginTop: 'var(--space-6)' }}>
          <button
            type="button"
            className={activeTab === 'chapters' ? 'btn-primary' : 'btn-secondary'}
            style={{ fontSize: '13px', padding: '8px 18px' }}
            onClick={() => setActiveTab('chapters')}
          >
            All 13 Chapters ({concepts.length} Concepts)
          </button>
          <button
            type="button"
            className={activeTab === 'dag' ? 'btn-primary' : 'btn-secondary'}
            style={{ fontSize: '13px', padding: '8px 18px' }}
            onClick={() => setActiveTab('dag')}
          >
            Linear Equations Prerequisite DAG (Tiers 1–4)
          </button>
        </div>
      </div>

      {/* VIEW A: Complete Chapter-by-Chapter Curriculum */}
      {activeTab === 'chapters' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-8)' }}>
          {NCERT_CLASS_8_CHAPTERS.map((ch) => {
            const chConcepts = ch.conceptIds
              .map((id) => conceptLookup.get(id))
              .filter((c): c is Concept => !!c);

            if (chConcepts.length === 0) return null;

            return (
              <section
                key={ch.number}
                className="editorial-card"
                style={{
                  backgroundColor: 'var(--surface-white)',
                  padding: 'var(--space-6)',
                  borderTop: '3px solid var(--sutra-mocha)',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 'var(--space-4)', flexWrap: 'wrap', gap: '8px' }}>
                  <div>
                    <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--sutra-mocha)' }}>
                      Chapter {ch.number}
                    </span>
                    <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', margin: '2px 0 0 0' }}>
                      {ch.title}
                    </h3>
                  </div>
                  <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                    {chConcepts.length} Concept{chConcepts.length > 1 ? 's' : ''}
                  </span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 'var(--space-4)' }}>
                  {chConcepts.map((c) => renderPathwayCard(c, progressMap, onOpenLesson, onOpenAssessment))}
                </div>
              </section>
            );
          })}
        </div>
      )}

      {/* VIEW B: Prerequisite Dependency DAG Flow */}
      {activeTab === 'dag' && (
        <div
          className="editorial-card"
          style={{
            marginBottom: 'var(--space-8)',
            backgroundColor: 'var(--surface-white)',
            padding: 'var(--space-8)',
          }}
        >
          <div style={{ textAlign: 'center', marginBottom: 'var(--space-6)' }}>
            <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--sutra-mocha)' }}>
              Chapter 2 Prerequisite Dependency Directed Acyclic Graph
            </span>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>
              Arrows depict pedagogical prerequisites. Green indicates demonstrated mastery; warm stone indicates unlocked for study.
            </p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
            {/* Tier 1: Root Prerequisite */}
            <div style={{ textAlign: 'center' }}>
              <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Tier 1 &bull; Foundational Arithmetic (Prerequisite Root)
              </span>
              <div style={{ display: 'flex', justifyContent: 'center', marginTop: 'var(--space-3)' }}>
                {linearTrack.slice(0, 1).map((c) => renderPathwayCard(c, progressMap, onOpenLesson, onOpenAssessment))}
              </div>
            </div>

            {/* Dependency Arrow */}
            <div style={{ textAlign: 'center', color: 'var(--sutra-stone)', fontSize: '20px', lineHeight: 1 }}>
              &darr; &darr; &darr;
            </div>

            {/* Tier 2: Intermediate Algebraic Principles (C02, C03, C04) */}
            <div>
              <div style={{ textAlign: 'center', marginBottom: 'var(--space-3)' }}>
                <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Tier 2 &bull; Equality, Balance & Transformations (Parallel Skills)
                </span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 'var(--space-4)' }}>
                {linearTrack.slice(1, 4).map((c) => renderPathwayCard(c, progressMap, onOpenLesson, onOpenAssessment))}
              </div>
            </div>

            {/* Dependency Convergence Arrow */}
            <div style={{ textAlign: 'center', color: 'var(--sutra-stone)', fontSize: '20px', lineHeight: 1 }}>
              &darr;
            </div>

            {/* Tier 3: Core Synthesis (C05) */}
            <div style={{ textAlign: 'center' }}>
              <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Tier 3 &bull; Target Synthesis: Linear Equations
              </span>
              <div style={{ display: 'flex', justifyContent: 'center', marginTop: 'var(--space-3)' }}>
                {linearTrack.slice(4, 5).map((c) => renderPathwayCard(c, progressMap, onOpenLesson, onOpenAssessment))}
              </div>
            </div>

            {/* Dependency Arrow */}
            <div style={{ textAlign: 'center', color: 'var(--sutra-stone)', fontSize: '20px', lineHeight: 1 }}>
              &darr;
            </div>

            {/* Tier 4: Verification & Metacognition (C06) */}
            <div style={{ textAlign: 'center' }}>
              <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Tier 4 &bull; Verification by Substitution & Proof
              </span>
              <div style={{ display: 'flex', justifyContent: 'center', marginTop: 'var(--space-3)' }}>
                {linearTrack.slice(5, 6).map((c) => renderPathwayCard(c, progressMap, onOpenLesson, onOpenAssessment))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function renderPathwayCard(
  c: Concept,
  progressMap: Record<string, ConceptProgress>,
  onOpenLesson: (id: string) => void,
  onOpenAssessment: (id: string) => void
) {
  const p = progressMap[c.id];
  const isUnlocked = c.is_unlocked ?? true;
  const status = p?.status || (isUnlocked ? 'not_started' : 'locked');
  const isMastered = status === 'mastered';

  return (
    <div
      key={c.id}
      style={{
        width: '100%',
        backgroundColor: isMastered ? 'var(--feedback-success-bg)' : isUnlocked ? 'var(--surface-paper)' : 'var(--surface-warm)',
        border: `1px solid ${isMastered ? 'var(--feedback-success-border)' : 'var(--border-default)'}`,
        borderTop: `3px solid ${isMastered ? 'var(--feedback-success)' : isUnlocked ? 'var(--sutra-mocha)' : 'var(--sutra-stone)'}`,
        borderRadius: 'var(--radius-md)',
        padding: 'var(--space-4) var(--space-5)',
        textAlign: 'left',
        opacity: isUnlocked ? 1 : 0.7,
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--text-muted)' }}>
          {c.id} &bull; {c.code}
        </span>
        <span className={`status-pill ${status}`}>
          {status.replace('_', ' ')}
        </span>
      </div>

      <h4 className="serif-title" style={{ fontSize: '16px', color: 'var(--sutra-espresso)', marginBottom: '4px' }}>
        {c.title}
      </h4>
      <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: 'var(--space-3)' }}>
        {c.description}
      </p>

      {c.prerequisites && c.prerequisites.length > 0 && (
        <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: 'var(--space-3)' }}>
          Prerequisites: <strong style={{ color: 'var(--sutra-mocha)' }}>{c.prerequisites.join(', ')}</strong>
        </div>
      )}

      {/* Actions */}
      <div style={{ display: 'flex', gap: '6px' }}>
        <button
          type="button"
          className="btn-secondary"
          style={{ flex: 1, fontSize: '11px', height: '32px' }}
          onClick={() => onOpenLesson(c.id)}
        >
          Lesson
        </button>
        <button
          type="button"
          className="btn-primary"
          style={{
            flex: 1,
            fontSize: '11px',
            height: '32px',
            backgroundColor: isUnlocked ? 'var(--action-primary)' : 'var(--sutra-stone)',
          }}
          onClick={() => onOpenAssessment(c.id)}
          disabled={!isUnlocked}
        >
          {isUnlocked ? 'Practice' : 'Locked'}
        </button>
      </div>
    </div>
  );
}
