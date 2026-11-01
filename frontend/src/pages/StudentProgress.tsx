import { useState, useEffect } from 'react';
import type { Concept, ConceptProgress, Learner, StudentAttemptHistoryItem, LearnerMetrics } from '../types';

interface StudentProgressProps {
  learner: Learner;
  concepts: Concept[];
  progressMap: Record<string, ConceptProgress>;
  apiBaseUrl: string;
  authToken?: string | null;
  onBackToHome: () => void;
  onPracticeConcept: (conceptId: string) => void;
}

export function StudentProgress({
  learner,
  concepts,
  progressMap,
  apiBaseUrl,
  authToken,
  onBackToHome,
  onPracticeConcept,
}: StudentProgressProps) {
  const [attempts, setAttempts] = useState<StudentAttemptHistoryItem[]>([]);
  const [canonicalMetrics, setCanonicalMetrics] = useState<LearnerMetrics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let isMounted = true;
    async function loadData() {
      try {
        setLoading(true);
        const headers: Record<string, string> = authToken ? { Authorization: `Bearer ${authToken}` } : {};

        // 1. Fetch attempts
        const res = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/attempts`, { headers });
        if (res.ok && isMounted) {
          const data = await res.json();
          setAttempts(data.attempts || []);
        }

        // 2. Fetch canonical metrics
        const mRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/metrics`, { headers });
        if (mRes.ok && isMounted) {
          const mData = await mRes.json();
          setCanonicalMetrics(mData);
        }
      } catch {
        // preserve clean state
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    void loadData();
    return () => {
      isMounted = false;
    };
  }, [apiBaseUrl, learner.id, authToken]);

  const progressList = Object.values(progressMap);
  const totalSubmissions = canonicalMetrics
    ? canonicalMetrics.attempts.total_attempts
    : attempts.length;

  const totalUnassisted = canonicalMetrics
    ? canonicalMetrics.attempts.correct_attempts
    : progressList.reduce((acc, p) => acc + (p.unassisted_correct || 0), 0);

  const totalAssisted = canonicalMetrics
    ? canonicalMetrics.attempts.hints_requested_total
    : progressList.reduce((acc, p) => acc + (p.assisted_correct || 0), 0);

  const masteredCount = canonicalMetrics
    ? canonicalMetrics.curriculum.mastered_concepts
    : progressList.filter((p) => p.status === 'mastered').length;

  const reviewCount = canonicalMetrics
    ? canonicalMetrics.curriculum.needs_review_concepts
    : progressList.filter((p) => p.status === 'needs_reinforcement').length;

  const verifiedAccuracy = canonicalMetrics
    ? canonicalMetrics.accuracy.overall_accuracy_pct
    : (totalSubmissions > 0 ? Math.min(100, Math.round((totalUnassisted / totalSubmissions) * 100)) : null);

  return (
    <div style={{ maxWidth: 'var(--dashboard-width)', margin: '0 auto' }}>
      {/* Top Header */}
      <div style={{ marginBottom: 'var(--space-8)' }}>
        <button
          type="button"
          className="btn-ghost"
          style={{ fontSize: '13px', marginBottom: 'var(--space-3)', paddingLeft: 0 }}
          onClick={onBackToHome}
        >
          &larr; Back to Learning Home
        </button>
        <div className="editorial-kicker">EVIDENCE DOSSIER</div>
        <h1 className="serif-display" style={{ fontSize: '36px', color: 'var(--sutra-espresso)', marginTop: '4px' }}>
          Personal Learning Evidence & Mastery
        </h1>
        <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: 'var(--space-2)', maxWidth: '680px', lineHeight: 1.6 }}>
          In SUTRA LEARN, <strong>accuracy is not mastery</strong>. Mastery requires consistent, unassisted correct problem solving across multiple distinct items.
        </p>
      </div>

      {/* Summary Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 'var(--space-4)', marginBottom: 'var(--space-8)' }}>
        <div className="metric-tile">
          <div className="metric-num tabular-nums">{masteredCount} / {concepts.length}</div>
          <div className="metric-label">Concepts Mastered</div>
        </div>
        <div className="metric-tile">
          <div className="metric-num tabular-nums" style={{ color: 'var(--sutra-mocha)' }}>
            {verifiedAccuracy !== null ? `${verifiedAccuracy}%` : '—'}
          </div>
          <div className="metric-label">Unassisted Accuracy</div>
        </div>
        <div className="metric-tile">
          <div className="metric-num tabular-nums">{totalSubmissions}</div>
          <div className="metric-label">Total Submissions</div>
        </div>
        <div className="metric-tile">
          <div className="metric-num tabular-nums">{totalAssisted}</div>
          <div className="metric-label">Hint-Assisted Solves</div>
        </div>
        <div className="metric-tile" style={reviewCount > 0 ? { backgroundColor: 'var(--feedback-warning-bg)' } : {}}>
          <div className="metric-num tabular-nums" style={reviewCount > 0 ? { color: 'var(--feedback-warning)' } : {}}>
            {reviewCount}
          </div>
          <div className="metric-label">Units Needing Review</div>
        </div>
      </div>

      {/* Concept by Concept Breakdown Table */}
      <section className="editorial-card" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="card-header-line">
          <div>
            <span className="editorial-kicker">MASTERY LEDGER</span>
            <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)' }}>
              Curriculum Unit Evidence
            </h3>
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
            Updated in real-time
          </span>
        </div>

        <div className="editorial-table-wrapper">
          <table className="editorial-table">
            <thead>
              <tr>
                <th>Concept</th>
                <th>Status</th>
                <th>Unassisted Correct</th>
                <th>Assisted Correct</th>
                <th>Total Attempts</th>
                <th>Mastery Requirement</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {concepts.map((concept) => {
                const prog = progressMap[concept.id];
                const unassisted = prog?.unassisted_correct || 0;
                const assisted = prog?.assisted_correct || 0;
                const attemptsCount = prog?.total_attempts || 0;
                const status = prog?.status || 'not_started';

                return (
                  <tr key={concept.id}>
                    <td>
                      <strong>{concept.title}</strong>
                      <div style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                        {concept.id}
                      </div>
                    </td>
                    <td>
                      <span className={`status-pill ${status}`}>
                        {status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="tabular-nums" style={{ color: 'var(--feedback-success)', fontWeight: 600 }}>
                      {unassisted}
                    </td>
                    <td className="tabular-nums" style={{ color: 'var(--sutra-mocha)' }}>
                      {assisted}
                    </td>
                    <td className="tabular-nums">
                      {attemptsCount}
                    </td>
                    <td style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                      {status === 'mastered'
                        ? '✓ Requirement satisfied'
                        : `Needs ≥ 85% clean solves (${unassisted}/2 required)`}
                    </td>
                    <td>
                      <button
                        type="button"
                        className="btn-secondary"
                        style={{ fontSize: '11px', height: '30px', padding: '0 10px' }}
                        onClick={() => onPracticeConcept(concept.id)}
                      >
                        Practice
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      {/* Full Chronological Attempt History */}
      <section className="editorial-card">
        <div className="card-header-line">
          <div>
            <span className="editorial-kicker">CHRONOLOGICAL AUDIT</span>
            <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)' }}>
              Complete Attempt History
            </h3>
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
            {attempts.length} recorded items
          </span>
        </div>

        {loading ? (
          <p style={{ textAlign: 'center', padding: 'var(--space-6)', color: 'var(--text-muted)' }}>
            Loading attempt verification log...
          </p>
        ) : attempts.length === 0 ? (
          <p style={{ fontStyle: 'italic', color: 'var(--text-muted)', padding: 'var(--space-4) 0' }}>
            No attempts recorded yet. Begin by practicing your first concept!
          </p>
        ) : (
          <div className="editorial-table-wrapper">
            <table className="editorial-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Concept</th>
                  <th>Item ID</th>
                  <th>Result</th>
                  <th>Assistance</th>
                  <th>Diagnosed Signal</th>
                </tr>
              </thead>
              <tbody>
                {attempts.map((att) => (
                  <tr key={att.id}>
                    <td className="timestamp" style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                      {new Date(att.server_timestamp).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                    </td>
                    <td><strong>{att.concept_id}</strong></td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>{att.question_id}</td>
                    <td>
                      <span style={{ color: att.is_correct ? 'var(--feedback-success)' : 'var(--feedback-warning)', fontWeight: 600 }}>
                        {att.is_correct ? '✓ Correct' : '✗ Incorrect'}
                      </span>
                    </td>
                    <td>
                      {att.hint_used ? (
                        <span style={{ fontSize: '12px', color: 'var(--sutra-mocha)', fontWeight: 600 }}>
                          💡 Hint Assisted
                        </span>
                      ) : (
                        <span style={{ fontSize: '12px', color: 'var(--feedback-success)' }}>
                          Clean unassisted
                        </span>
                      )}
                    </td>
                    <td style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                      {att.misconception_tag && att.misconception_tag !== 'none'
                        ? att.misconception_tag
                        : 'No misconception detected'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

