import { useState, useEffect } from 'react';
import type { CohortStudentSummary, Concept, StudentAttemptHistoryItem, TeacherOverrideRecord, ConceptProgress } from '../types';

interface TeacherLearnerProfileProps {
  learnerId: string;
  concepts: Concept[];
  apiBaseUrl: string;
  authToken?: string | null;
  onBack: () => void;
  onIntervene: (student: CohortStudentSummary) => void;
}

export function TeacherLearnerProfile({
  learnerId,
  concepts,
  apiBaseUrl,
  authToken,
  onBack,
  onIntervene,
}: TeacherLearnerProfileProps) {
  const [student, setStudent] = useState<CohortStudentSummary | null>(null);
  const [attempts, setAttempts] = useState<StudentAttemptHistoryItem[]>([]);
  const [progressMap, setProgressMap] = useState<Record<string, ConceptProgress>>({});
  const [overrides, setOverrides] = useState<TeacherOverrideRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    async function loadStudentData() {
      try {
        setLoading(true);
        const authHeader: Record<string, string> = authToken ? { Authorization: `Bearer ${authToken}` } : {};

        // 1. Fetch cohort to find student summary
        const cohortRes = await fetch(`${apiBaseUrl}/api/v1/teacher/cohort`, { headers: authHeader });
        if (cohortRes.ok) {
          const cohortData: CohortStudentSummary[] = await cohortRes.json();
          const found = cohortData.find((s) => s.learner_id === learnerId);
          if (found && isMounted) setStudent(found);
        }

        // 2. Fetch attempts
        const attRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learnerId}/attempts`, { headers: authHeader });
        if (attRes.ok) {
          const attData = await attRes.json();
          if (isMounted) setAttempts(attData.attempts || []);
        }

        // 3. Fetch progress
        const progRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learnerId}/progress`, { headers: authHeader });
        if (progRes.ok) {
          const progData = await progRes.json();
          const map: Record<string, ConceptProgress> = {};
          (progData.progress || []).forEach((p: ConceptProgress) => {
            map[p.concept_id] = p;
          });
          if (isMounted) setProgressMap(map);
        }

        // 4. Fetch overrides for this learner
        const ovRes = await fetch(`${apiBaseUrl}/api/v1/teacher/overrides`, { headers: authHeader });
        if (ovRes.ok) {
          const ovData: TeacherOverrideRecord[] = await ovRes.json();
          if (isMounted) setOverrides(ovData.filter((o) => o.learner_id === learnerId));
        }
      } catch (err) {
        console.warn('Error loading student profile dossier:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    void loadStudentData();
    return () => {
      isMounted = false;
    };
  }, [learnerId, apiBaseUrl, authToken]);

  if (loading) {
    return (
      <div className="editorial-card" style={{ textAlign: 'center', padding: 'var(--space-12)' }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading comprehensive student evidence dossier...</p>
      </div>
    );
  }

  if (!student) {
    return (
      <div className="editorial-card" style={{ padding: 'var(--space-8)' }}>
        <h3 style={{ color: 'var(--feedback-error)' }}>Learner Record Not Found</h3>
        <p style={{ color: 'var(--text-secondary)', margin: 'var(--space-3) 0' }}>
          No student dossier located for identifier: <code>{learnerId}</code>
        </p>
        <button type="button" className="btn-secondary" onClick={onBack}>
          &larr; Return to Roster
        </button>
      </div>
    );
  }

  // Calculate clean verified accuracy
  const totalAtt = attempts.length;
  const correctAtt = attempts.filter((a) => a.is_correct).length;
  const unassistedAtt = attempts.filter((a) => a.is_correct && !a.hint_used).length;
  const assistedAtt = attempts.filter((a) => a.hint_used).length;
  const accuracy = totalAtt > 0 ? Math.min(100, Math.round((correctAtt / totalAtt) * 100)) : null;

  // Extract observed misconceptions
  const misconceptions = attempts.filter((a) => a.misconception_tag && a.misconception_tag !== 'none');

  return (
    <div>
      {/* Top Breadcrumb & Action */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)' }}>
        <button type="button" className="btn-ghost" style={{ fontSize: '13px', paddingLeft: 0 }} onClick={onBack}>
          &larr; Back to Cohort Directory
        </button>
        <button
          type="button"
          className="btn-primary"
          style={{ backgroundColor: 'var(--sutra-mocha)' }}
          onClick={() => onIntervene(student)}
        >
          ⚖️ Apply Pedagogical Intervention
        </button>
      </div>

      {/* Header Profile Banner */}
      <div className="editorial-card" style={{ marginBottom: 'var(--space-6)', borderTop: '4px solid var(--sutra-espresso)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
          <div>
            <span className="editorial-kicker">INDIVIDUAL STUDENT DOSSIER</span>
            <h1 className="serif-display" style={{ fontSize: '32px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
              {student.name}
            </h1>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px' }}>
              Identifier: <code style={{ fontFamily: 'var(--font-mono)' }}>{student.learner_id}</code> &bull; Grade {student.grade} Mathematics
            </p>
          </div>

          <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
            <div style={{ textAlign: 'center', backgroundColor: 'var(--surface-warm)', padding: 'var(--space-2) var(--space-4)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Adaptive State</span>
              <div style={{ fontWeight: 700, color: 'var(--sutra-espresso)', marginTop: '2px' }}>
                {student.latest_outcome ? student.latest_outcome.replace('_', ' ') : 'Pending'}
              </div>
            </div>
            {student.needs_review ? (
              <div style={{ textAlign: 'center', backgroundColor: 'var(--feedback-warning-bg)', border: '1px solid var(--feedback-warning-border)', padding: 'var(--space-2) var(--space-4)', borderRadius: 'var(--radius-sm)' }}>
                <span style={{ fontSize: '11px', color: 'var(--feedback-warning)', textTransform: 'uppercase', fontWeight: 700 }}>Review Flag</span>
                <div style={{ fontWeight: 700, color: 'var(--feedback-warning)', marginTop: '2px' }}>
                  ⚠️ Attention Required
                </div>
              </div>
            ) : null}
          </div>
        </div>

        {/* Real Summary Metrics */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 'var(--space-3)', marginTop: 'var(--space-6)' }}>
          <div className="metric-tile" style={{ backgroundColor: 'var(--surface-paper)' }}>
            <div className="metric-num tabular-nums">{totalAtt}</div>
            <div className="metric-label">Total Submissions</div>
          </div>
          <div className="metric-tile" style={{ backgroundColor: 'var(--surface-paper)' }}>
            <div className="metric-num tabular-nums" style={{ color: 'var(--sutra-mocha)' }}>
              {accuracy !== null ? `${accuracy}%` : 'No attempts yet'}
            </div>
            <div className="metric-label">Verified Accuracy</div>
          </div>
          <div className="metric-tile" style={{ backgroundColor: 'var(--surface-paper)' }}>
            <div className="metric-num tabular-nums" style={{ color: 'var(--feedback-success)' }}>{unassistedAtt}</div>
            <div className="metric-label">Clean Solves</div>
          </div>
          <div className="metric-tile" style={{ backgroundColor: 'var(--surface-paper)' }}>
            <div className="metric-num tabular-nums">{assistedAtt}</div>
            <div className="metric-label">Hint Assisted</div>
          </div>
          <div className="metric-tile" style={{ backgroundColor: 'var(--surface-paper)' }}>
            <div className="metric-num tabular-nums">{overrides.length}</div>
            <div className="metric-label">Past Overrides</div>
          </div>
        </div>
      </div>

      {/* Concept Progression Matrix */}
      <section className="editorial-card" style={{ marginBottom: 'var(--space-6)' }}>
        <div className="card-header-line">
          <div>
            <span className="editorial-kicker">CURRICULUM TRAJECTORY</span>
            <h3 className="serif-title" style={{ fontSize: '18px', color: 'var(--sutra-espresso)' }}>
              Concept Mastery Matrix
            </h3>
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Class 8 Progression</span>
        </div>

        <div className="editorial-table-wrapper">
          <table className="editorial-table">
            <thead>
              <tr>
                <th>Concept</th>
                <th>Status</th>
                <th>Clean Solves</th>
                <th>Hinted Solves</th>
                <th>Total Attempts</th>
                <th>Last Engine Recommendation</th>
              </tr>
            </thead>
            <tbody>
              {concepts.map((concept) => {
                const prog = progressMap[concept.id];
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
                      {prog?.unassisted_correct || 0}
                    </td>
                    <td className="tabular-nums" style={{ color: 'var(--sutra-mocha)' }}>
                      {prog?.assisted_correct || 0}
                    </td>
                    <td className="tabular-nums">
                      {prog?.total_attempts || 0}
                    </td>
                    <td style={{ fontSize: '12px' }}>
                      {prog?.last_recommended_outcome ? (
                        <span style={{ fontWeight: 600 }}>{prog.last_recommended_outcome}</span>
                      ) : (
                        <span style={{ color: 'var(--text-muted)' }}>—</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      {/* Misconception Signals & Friction Points */}
      {misconceptions.length > 0 && (
        <section className="editorial-card" style={{ marginBottom: 'var(--space-6)' }}>
          <div className="card-header-line">
            <div>
              <span className="editorial-kicker">DIAGNOSTIC EVIDENCE</span>
              <h3 className="serif-title" style={{ fontSize: '18px', color: 'var(--sutra-espresso)' }}>
                Observed Misconception Patterns
              </h3>
            </div>
            <span style={{ fontSize: '12px', color: 'var(--feedback-warning)', fontWeight: 600 }}>
              {misconceptions.length} recorded signals
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
            {misconceptions.map((m) => (
              <div
                key={m.id}
                style={{
                  padding: 'var(--space-3) var(--space-4)',
                  backgroundColor: 'var(--feedback-warning-bg)',
                  border: '1px solid var(--feedback-warning-border)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '13px',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 700, color: 'var(--feedback-warning)' }}>
                    Tag: {m.misconception_tag}
                  </span>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                    {new Date(m.server_timestamp).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                  </span>
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  Item: {m.concept_id} &bull; {m.question_id} (Selected option {m.selected_option_id})
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Chronological Attempt History */}
      <section className="editorial-card" style={{ marginBottom: 'var(--space-6)' }}>
        <div className="card-header-line">
          <div>
            <span className="editorial-kicker">ATTEMPT LOG</span>
            <h3 className="serif-title" style={{ fontSize: '18px', color: 'var(--sutra-espresso)' }}>
              Complete Attempt Chronology
            </h3>
          </div>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{attempts.length} attempts</span>
        </div>

        {attempts.length === 0 ? (
          <p style={{ fontStyle: 'italic', color: 'var(--text-muted)', padding: 'var(--space-4) 0' }}>
            No attempts submitted yet by this learner.
          </p>
        ) : (
          <div className="editorial-table-wrapper">
            <table className="editorial-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Concept</th>
                  <th>Question ID</th>
                  <th>Outcome</th>
                  <th>Assistance</th>
                  <th>Selected Option</th>
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
                    <td style={{ fontFamily: 'var(--font-mono)' }}>Option {att.selected_option_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Teacher Interventions for this Student */}
      {overrides.length > 0 && (
        <section className="editorial-card">
          <div className="card-header-line">
            <div>
              <span className="editorial-kicker">CLINICAL AUDIT</span>
              <h3 className="serif-title" style={{ fontSize: '18px', color: 'var(--sutra-espresso)' }}>
                Past Educator Interventions
              </h3>
            </div>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{overrides.length} logged</span>
          </div>

          <div className="editorial-table-wrapper">
            <table className="editorial-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Concept</th>
                  <th>Transition</th>
                  <th>Pedagogical Rationale</th>
                  <th>Instructor</th>
                </tr>
              </thead>
              <tbody>
                {overrides.map((ov) => (
                  <tr key={ov.id}>
                    <td className="timestamp" style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                      {new Date(ov.created_at).toLocaleDateString()}
                    </td>
                    <td><strong>{ov.concept_id}</strong></td>
                    <td>
                      <span style={{ textDecoration: 'line-through', color: 'var(--text-muted)' }}>{ov.previous_outcome}</span>
                      {' '}&rarr;{' '}
                      <strong>{ov.overridden_outcome}</strong>
                    </td>
                    <td style={{ maxWidth: '320px', fontSize: '13px' }}>{ov.reason}</td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>{ov.teacher_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </div>
  );
}
