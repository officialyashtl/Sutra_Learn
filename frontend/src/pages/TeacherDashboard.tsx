import { useState, useEffect, useCallback } from 'react';
import type { FormEvent } from 'react';
import type { Learner, CohortStudentSummary, TeacherOverrideRecord, Concept, StudentAttemptHistoryItem, ConceptAnalytics } from '../types';

interface TeacherDashboardProps {
  currentTeacher: Learner;
  concepts: Concept[];
  cohort?: CohortStudentSummary[];
  conceptAnalytics?: ConceptAnalytics[];
  apiBaseUrl: string;
  authToken?: string | null;
  onRefreshData?: () => void;
  onInspectLearner?: (learnerId: string) => void;
  onNavigateToLearners?: () => void;
  onNavigateToInsights?: () => void;
  onNavigateToInterventions?: () => void;
  onNavigateToAudit?: () => void;
}

export function TeacherDashboard({
  currentTeacher,
  concepts,
  cohort: propCohort,
  conceptAnalytics: propConceptAnalytics,
  apiBaseUrl,
  authToken,
  onRefreshData,
  onInspectLearner,
  onNavigateToLearners,
  onNavigateToInsights,
  onNavigateToInterventions,
  onNavigateToAudit,
}: TeacherDashboardProps) {
  const [fetchedCohort, setFetchedCohort] = useState<CohortStudentSummary[]>([]);
  const cohort = propCohort && propCohort.length > 0 ? propCohort : fetchedCohort;
  const [overrides, setOverrides] = useState<TeacherOverrideRecord[]>([]);
  const [fetchedAnalytics, setFetchedAnalytics] = useState<ConceptAnalytics[]>([]);
  const conceptAnalytics = propConceptAnalytics && propConceptAnalytics.length > 0 ? propConceptAnalytics : fetchedAnalytics;
  const [loading, setLoading] = useState<boolean>(!propCohort || propCohort.length === 0);
  const [error, setError] = useState<string | null>(null);

  // Intervention Modal State (Inline fallback)
  const [selectedStudent, setSelectedStudent] = useState<CohortStudentSummary | null>(null);
  const [targetConceptId, setTargetConceptId] = useState<string>(concepts[0]?.id || 'MATH-C01');
  const [overriddenOutcome, setOverriddenOutcome] = useState<string>('SCAFFOLD');
  const [reason, setReason] = useState<string>('');
  const [submittingOverride, setSubmittingOverride] = useState<boolean>(false);
  const [overrideFeedback, setOverrideFeedback] = useState<string | null>(null);

  // Student Detail Evidence Modal State
  const [inspectingStudent, setInspectingStudent] = useState<CohortStudentSummary | null>(null);
  const [studentAttempts, setStudentAttempts] = useState<StudentAttemptHistoryItem[]>([]);
  const [loadingAttempts, setLoadingAttempts] = useState<boolean>(false);

  const fetchDashboardData = useCallback(async () => {
    if (!authToken) {
      return;
    }
    try {
      setLoading(true);
      setError(null);

      const authHeader: Record<string, string> = { Authorization: `Bearer ${authToken}` };
      const cohortRes = await fetch(`${apiBaseUrl}/api/v1/teacher/cohort`, {
        headers: authHeader,
      });

      if (!cohortRes.ok) {
        if (cohortRes.status === 403 || cohortRes.status === 401) {
          throw new Error(`Unauthorized: User '${currentTeacher.name}' does not hold verified teacher privileges.`);
        }
        throw new Error('Failed to load cohort data from server.');
      }
      const cohortData = await cohortRes.json();
      setFetchedCohort(cohortData);

      const auditRes = await fetch(`${apiBaseUrl}/api/v1/teacher/overrides`, {
        headers: authHeader,
      });
      if (auditRes.ok) {
        const auditData = await auditRes.json();
        setOverrides(auditData);
      }

      const analyticsRes = await fetch(`${apiBaseUrl}/api/v1/teacher/analytics/concepts`, {
        headers: authHeader,
      });
      if (analyticsRes.ok) {
        const analyticsData = await analyticsRes.json();
        setFetchedAnalytics(analyticsData);
      }
    } catch (err: any) {
      setError(err.message || 'Error fetching educator workspace data.');
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, currentTeacher.name, authToken]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      void fetchDashboardData();
    }, 0);
    return () => clearTimeout(timeout);
  }, [fetchDashboardData]);

  const handleOpenOverride = (student: CohortStudentSummary) => {
    setSelectedStudent(student);
    setReason('');
    setOverrideFeedback(null);
  };

  const handleInspectStudent = async (student: CohortStudentSummary) => {
    if (onInspectLearner) {
      onInspectLearner(student.learner_id);
      return;
    }
    setInspectingStudent(student);
    setLoadingAttempts(true);
    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/learners/${student.learner_id}/attempts`, {
        headers: {
          ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        },
      });
      if (res.ok) {
        const data = await res.json();
        setStudentAttempts(data.attempts || []);
      }
    } catch (err) {
      console.warn('Failed to fetch student attempts:', err);
    } finally {
      setLoadingAttempts(false);
    }
  };

  const handleApplyOverride = async (e: FormEvent) => {
    e.preventDefault();
    if (!selectedStudent) return;
    if (reason.trim().length < 5) {
      setOverrideFeedback('A substantive pedagogical rationale (minimum 5 characters) is required.');
      return;
    }

    setSubmittingOverride(true);
    setOverrideFeedback(null);

    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/teacher/override`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        },
        body: JSON.stringify({
          learner_id: selectedStudent.learner_id,
          concept_id: targetConceptId,
          previous_outcome: selectedStudent.latest_outcome || 'CONFIRM',
          overridden_outcome: overriddenOutcome,
          reason: reason.trim(),
          teacher_id: currentTeacher.id,
        }),
      });

      if (!res.ok) {
        const errJson = await res.json();
        throw new Error(errJson.detail || 'Failed to submit override.');
      }

      setOverrideFeedback('Override successfully applied and logged to compliance audit.');
      setTimeout(() => {
        setSelectedStudent(null);
        void fetchDashboardData();
      }, 1000);
    } catch (err: any) {
      setOverrideFeedback(err.message || 'Error applying override.');
    } finally {
      setSubmittingOverride(false);
    }
  };

  if (loading) {
    return (
      <div className="editorial-card" style={{ textAlign: 'center', padding: 'var(--space-12)' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Synchronizing Educator Workspace & Cohort Diagnostics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="editorial-card" style={{ padding: 'var(--space-8)', borderColor: 'var(--feedback-error-border)', backgroundColor: 'var(--feedback-error-bg)' }}>
        <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--feedback-error)' }}>Access Restriction</h3>
        <p style={{ margin: 'var(--space-3) 0', color: 'var(--feedback-error)', fontSize: '14px' }}>{error}</p>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
          Please ensure your session has an authorized educator role and a valid cryptographic Bearer token.
        </p>
      </div>
    );
  }

  const activeLearnersCount = cohort.filter((s) => s.total_attempts > 0).length;
  const flaggedCount = cohort.filter((s) => !!s.needs_review).length;
  const totalCohortAttempts = cohort.reduce((acc, s) => acc + (s.total_attempts || 0), 0);

  return (
    <div>
      {/* Workspace Header Banner */}
      <section className="editorial-card" style={{ marginBottom: 'var(--space-6)' }} aria-label="Educator Overview Header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
          <div>
            <div className="editorial-kicker">EDUCATOR WORKSPACE &bull; CLASSROOM OVERVIEW</div>
            <h1 className="serif-display" style={{ fontSize: '30px', color: 'var(--sutra-espresso)', marginTop: '4px' }}>
              Class 8 Mathematics &bull; Cohort Diagnostics & Clinical Oversight
            </h1>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '6px' }}>
              Instructor: <strong>{currentTeacher.name}</strong> &bull; Verified Cryptographic Session &bull; Defensible Pedagogical Audit
            </p>
          </div>
          <button
            type="button"
            className="btn-secondary"
            onClick={() => {
              if (onRefreshData) onRefreshData();
              void fetchDashboardData();
            }}
          >
            ↻ Refresh Overview
          </button>
        </div>

        {/* Cohort Overview Metrics */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: 'var(--space-3)', marginTop: 'var(--space-6)' }}>
          <div className="metric-tile">
            <div className="metric-num">{cohort.length}</div>
            <div className="metric-label">Enrolled Learners</div>
          </div>
          <div className="metric-tile">
            <div className="metric-num" style={{ color: 'var(--sutra-espresso)' }}>{activeLearnersCount}</div>
            <div className="metric-label">Active Learners</div>
          </div>
          <div
            className="metric-tile"
            style={flaggedCount > 0 ? { backgroundColor: 'var(--feedback-warning-bg)', borderColor: 'var(--feedback-warning-border)' } : {}}
          >
            <div className="metric-num" style={{ color: flaggedCount > 0 ? 'var(--feedback-warning)' : 'var(--sutra-espresso)' }}>
              {flaggedCount}
            </div>
            <div className="metric-label" style={flaggedCount > 0 ? { color: 'var(--feedback-warning)' } : {}}>
              Flagged for Review
            </div>
          </div>
          <div className="metric-tile">
            <div className="metric-num">{totalCohortAttempts}</div>
            <div className="metric-label">Total Submissions</div>
          </div>
          <div className="metric-tile">
            <div className="metric-num">{overrides.length}</div>
            <div className="metric-label">Interventions Logged</div>
          </div>
        </div>
      </section>

      {/* Cohort Student Diagnostics Table */}
      <section className="editorial-card" style={{ marginBottom: 'var(--space-6)' }} aria-label="Student Cohort Diagnostics">
        <div className="card-header-line">
          <div>
            <div className="editorial-kicker">INDIVIDUAL STUDENT EVIDENCE</div>
            <h2 className="serif-title" style={{ fontSize: '22px', color: 'var(--sutra-espresso)' }}>
              Learner Trajectories & Attention Roster
            </h2>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Real-time diagnostic metrics from student problem submissions. Verified non-duplicating accuracy data.
            </p>
          </div>
          {onNavigateToLearners && (
            <button type="button" className="btn-ghost" onClick={onNavigateToLearners} style={{ fontSize: '13px' }}>
              View All Directory &rarr;
            </button>
          )}
        </div>

        {cohort.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: 'var(--space-6) 0' }}>
            No enrolled students found in database.
          </p>
        ) : (
          <div className="editorial-table-wrapper">
            <table className="editorial-table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Grade</th>
                  <th>Attempts</th>
                  <th>Accuracy</th>
                  <th>Adaptive Status</th>
                  <th>Review Signal</th>
                  <th>Intervention Actions</th>
                </tr>
              </thead>
              <tbody>
                {cohort.map((s) => {
                  const accuracy = s.total_attempts > 0 ? Math.round((s.total_correct / s.total_attempts) * 100) : 0;
                  const isFlagged = !!s.needs_review;

                  let pillStatus: 'mastered' | 'in_progress' | 'needs_reinforcement' | 'not_started' = 'not_started';
                  if (s.latest_outcome === 'STRETCH') pillStatus = 'mastered';
                  else if (s.latest_outcome === 'BRIDGE_BACK') pillStatus = 'needs_reinforcement';
                  else if (s.latest_outcome === 'SCAFFOLD' || s.latest_outcome === 'CONFIRM') pillStatus = 'in_progress';
                  else if (s.latest_outcome === 'TEACHER_REVIEW') pillStatus = 'needs_reinforcement';

                  return (
                    <tr key={s.learner_id}>
                      <td>
                        <strong>{s.name}</strong>
                        <div style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                          {s.learner_id}
                        </div>
                      </td>
                      <td>Class {s.grade}</td>
                      <td className="tabular-nums">{s.total_attempts}</td>
                      <td>
                        {s.total_attempts > 0 ? (
                          <span className="tabular-nums" style={{ fontWeight: 600 }}>
                            {accuracy}% ({s.total_correct}/{s.total_attempts})
                          </span>
                        ) : (
                          <span style={{ color: 'var(--text-muted)' }}>None</span>
                        )}
                      </td>
                      <td>
                        {s.latest_outcome ? (
                          <span className={`status-pill ${pillStatus}`}>
                            {s.latest_outcome.replace('_', ' ')}
                          </span>
                        ) : (
                          <span style={{ color: 'var(--text-muted)' }}>Pending</span>
                        )}
                      </td>
                      <td>
                        {isFlagged ? (
                          <span className="status-pill needs_reinforcement">⚠️ Needs Review</span>
                        ) : (
                          <span style={{ color: 'var(--feedback-success)', fontSize: '13px', fontWeight: 600 }}>✓ Normal</span>
                        )}
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '6px' }}>
                          <button
                            type="button"
                            className="btn-secondary"
                            style={{ fontSize: '12px', padding: '4px 10px', height: '32px' }}
                            onClick={() => void handleInspectStudent(s)}
                            title="Inspect complete student evidence dossier"
                          >
                            Inspect Dossier
                          </button>
                          <button
                            type="button"
                            className="btn-primary"
                            style={{ fontSize: '12px', padding: '4px 10px', height: '32px' }}
                            onClick={() => handleOpenOverride(s)}
                          >
                            Intervene
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Curriculum Concept Difficulty & Misconception Bottlenecks Preview */}
      <section className="editorial-card" style={{ marginBottom: 'var(--space-6)' }} aria-label="Curriculum Concept Analytics Preview">
        <div className="card-header-line">
          <div>
            <div className="editorial-kicker">CURRICULUM INTELLIGENCE</div>
            <h2 className="serif-title" style={{ fontSize: '22px', color: 'var(--sutra-espresso)' }}>
              Curriculum Friction & Bottleneck Highlights
            </h2>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Prerequisite bottlenecks and common misconceptions requiring group pedagogical reinforcement.
            </p>
          </div>
          {onNavigateToInsights && (
            <button type="button" className="btn-ghost" onClick={onNavigateToInsights} style={{ fontSize: '13px' }}>
              Full Analytics Matrix &rarr;
            </button>
          )}
        </div>

        {conceptAnalytics.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: 'var(--space-4) 0' }}>
            No student attempt data recorded for concepts yet.
          </p>
        ) : (
          <div className="editorial-table-wrapper">
            <table className="editorial-table">
              <thead>
                <tr>
                  <th>Concept</th>
                  <th>Attempts</th>
                  <th>Class Accuracy</th>
                  <th>Assisted Ratio</th>
                  <th>Observed Misconceptions</th>
                  <th>Health Signal</th>
                </tr>
              </thead>
              <tbody>
                {conceptAnalytics.slice(0, 4).map((ca) => {
                  const conceptObj = concepts.find((c) => c.id === ca.concept_id);
                  const title = conceptObj ? conceptObj.title : ca.concept_id;
                  const isChallenging = ca.accuracy_percentage < 60;
                  const isModerate = ca.accuracy_percentage >= 60 && ca.accuracy_percentage < 80;

                  return (
                    <tr key={ca.concept_id}>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--sutra-mocha)', fontWeight: 600 }}>
                            {ca.concept_id}
                          </span>
                          <strong>{title}</strong>
                        </div>
                      </td>
                      <td className="tabular-nums">{ca.total_attempts}</td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div
                            style={{
                              flex: '0 0 60px',
                              height: '8px',
                              background: 'var(--border-subtle)',
                              borderRadius: '4px',
                              overflow: 'hidden',
                            }}
                          >
                            <div
                              style={{
                                width: `${Math.min(100, Math.max(0, ca.accuracy_percentage))}%`,
                                height: '100%',
                                background: isChallenging
                                  ? 'var(--feedback-error)'
                                  : isModerate
                                  ? 'var(--feedback-warning)'
                                  : 'var(--feedback-success)',
                              }}
                            />
                          </div>
                          <span className="tabular-nums" style={{ fontWeight: 600 }}>{ca.accuracy_percentage}%</span>
                        </div>
                      </td>
                      <td style={{ fontSize: '13px' }}>
                        <span style={{ color: 'var(--feedback-success)' }}>{ca.unassisted_correct} clean</span>
                        {ca.total_assisted > 0 && (
                          <span style={{ color: 'var(--text-muted)', marginLeft: '6px' }}>
                            &bull; {ca.total_assisted} hinted
                          </span>
                        )}
                      </td>
                      <td>
                        {ca.top_misconceptions.length > 0 ? (
                          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                            {ca.top_misconceptions.map((tag, idx) => (
                              <span
                                key={idx}
                                style={{
                                  fontSize: '11px',
                                  padding: '2px 6px',
                                  borderRadius: '4px',
                                  background: 'var(--feedback-warning-bg)',
                                  color: 'var(--feedback-warning)',
                                  border: '1px solid var(--feedback-warning-border)',
                                }}
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <span style={{ color: 'var(--text-muted)', fontSize: '12px' }}>None detected</span>
                        )}
                      </td>
                      <td>
                        {isChallenging ? (
                          <span className="status-pill needs_reinforcement">⚠️ High Friction</span>
                        ) : isModerate ? (
                          <span className="status-pill in_progress">Developing</span>
                        ) : (
                          <span className="status-pill mastered">✓ Stable</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Compliance Override Audit Log Preview */}
      <section className="editorial-card" aria-label="Pedagogical Override Audit Log Preview">
        <div className="card-header-line">
          <div>
            <div className="editorial-kicker">COMPLIANCE & ACCOUNTABILITY</div>
            <h2 className="serif-title" style={{ fontSize: '22px', color: 'var(--sutra-espresso)' }}>
              Recent Pedagogical Interventions
            </h2>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Defensible audit record of educator overrides with mandatory clinical rationale.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            {onNavigateToInterventions && (
              <button type="button" className="btn-secondary" onClick={onNavigateToInterventions} style={{ fontSize: '12px', height: '32px' }}>
                + Log Intervention
              </button>
            )}
            {onNavigateToAudit && (
              <button type="button" className="btn-ghost" onClick={onNavigateToAudit} style={{ fontSize: '13px' }}>
                Complete Audit Ledger &rarr;
              </button>
            )}
          </div>
        </div>

        {overrides.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '14px', fontStyle: 'italic', padding: 'var(--space-4) 0' }}>
            No recorded educator overrides yet.
          </p>
        ) : (
          <div className="editorial-table-wrapper">
            <table className="editorial-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Student</th>
                  <th>Concept</th>
                  <th>Outcome Adjustment</th>
                  <th>Educator Rationale</th>
                  <th>Authorized Instructor</th>
                </tr>
              </thead>
              <tbody>
                {overrides.slice(0, 5).map((ov) => (
                  <tr key={ov.id}>
                    <td className="timestamp" style={{ fontSize: '12px', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
                      {new Date(ov.created_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                    </td>
                    <td><strong>{ov.learner_name || ov.learner_id}</strong></td>
                    <td>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--sutra-mocha)' }}>
                        {ov.concept_id}
                      </span>
                    </td>
                    <td>
                      <span style={{ textDecoration: 'line-through', color: 'var(--text-muted)' }}>
                        {ov.previous_outcome}
                      </span>
                      {' '}&rarr;{' '}
                      <strong>{ov.overridden_outcome}</strong>
                    </td>
                    <td style={{ maxWidth: '340px', fontSize: '13px', lineHeight: 1.4 }}>{ov.reason}</td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>{ov.teacher_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Student Evidence Inspection Modal (Fallback if not navigating to profile) */}
      {inspectingStudent && (
        <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="inspect-dialog-title">
          <div className="modal-content">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-4)' }}>
              <div>
                <h3 id="inspect-dialog-title" className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)' }}>
                  Evidence Inspector: {inspectingStudent.name}
                </h3>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                  Learner ID: {inspectingStudent.learner_id} &bull; Class {inspectingStudent.grade}
                </p>
              </div>
              <button
                type="button"
                className="btn-secondary"
                style={{ height: '32px', padding: '4px 12px' }}
                onClick={() => setInspectingStudent(null)}
              >
                ✕ Close
              </button>
            </div>

            {loadingAttempts ? (
              <p style={{ color: 'var(--text-secondary)', padding: 'var(--space-6) 0', textAlign: 'center' }}>
                Loading verified attempt chronology...
              </p>
            ) : studentAttempts.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', padding: 'var(--space-6) 0', fontStyle: 'italic', textAlign: 'center' }}>
                No attempts recorded yet for this learner.
              </p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                {studentAttempts.map((att) => (
                  <div
                    key={att.id}
                    style={{
                      padding: 'var(--space-3) var(--space-4)',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid var(--border-subtle)',
                      backgroundColor: att.is_correct ? 'var(--feedback-success-bg)' : 'var(--feedback-warning-bg)',
                      fontSize: '13px',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--sutra-mocha)' }}>
                        {att.concept_id} &bull; {att.question_id}
                      </span>
                      <span className="timestamp" style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                        {new Date(att.server_timestamp).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                      </span>
                    </div>
                    <div style={{ marginTop: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <strong>{att.is_correct ? '✓ Correct' : '✗ Incorrect'}</strong>
                      <span>(Selected: Option {att.selected_option_id})</span>
                      {att.hint_used && (
                        <span style={{ fontSize: '11px', color: 'var(--feedback-info)', fontWeight: 600 }}>
                          [💡 Hint Assisted]
                        </span>
                      )}
                    </div>
                    {att.misconception_tag && att.misconception_tag !== 'none' && (
                      <div style={{ marginTop: '4px', fontSize: '12px', color: 'var(--feedback-warning)', fontWeight: 600 }}>
                        Diagnosed Misconception: {att.misconception_tag}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Manual Override Intervention Modal */}
      {selectedStudent && (
        <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="override-dialog-title">
          <div className="modal-content" style={{ maxWidth: '540px' }}>
            <h3 id="override-dialog-title" className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginBottom: '4px' }}>
              Manual Pedagogical Intervention
            </h3>
            <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: 'var(--space-4)' }}>
              Intervening for student: <strong>{selectedStudent.name}</strong> ({selectedStudent.learner_id})
            </p>

            <form onSubmit={(e) => void handleApplyOverride(e)}>
              <div style={{ marginBottom: 'var(--space-3)' }}>
                <label className="form-label">Target Concept:</label>
                <select
                  value={targetConceptId}
                  onChange={(e) => setTargetConceptId(e.target.value)}
                  className="form-input"
                  style={{ height: '42px' }}
                >
                  {concepts.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.code}: {c.title}
                    </option>
                  ))}
                </select>
              </div>

              <div style={{ marginBottom: 'var(--space-3)' }}>
                <label className="form-label">Target Learning Path Outcome:</label>
                <select
                  value={overriddenOutcome}
                  onChange={(e) => setOverriddenOutcome(e.target.value)}
                  className="form-input"
                  style={{ height: '42px' }}
                >
                  <option value="SCAFFOLD">SCAFFOLD (Guided Practice & Hints)</option>
                  <option value="BRIDGE_BACK">BRIDGE_BACK (Reinforce Prerequisite)</option>
                  <option value="STRETCH">STRETCH (Advance to Challenge)</option>
                  <option value="CONFIRM">CONFIRM (Clarifying Diagnostic)</option>
                </select>
              </div>

              <div style={{ marginBottom: 'var(--space-4)' }}>
                <label className="form-label">
                  Required Pedagogical Rationale (Minimum 5 characters):
                </label>
                <textarea
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  placeholder="Provide clinical explanation for overriding automated engine (e.g. in-person formative check confirmed resolution of sign error)..."
                  rows={3}
                  required
                  className="form-input"
                  style={{ height: 'auto', padding: '10px', fontSize: '13px' }}
                />
              </div>

              {overrideFeedback && (
                <div
                  style={{
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    marginBottom: 'var(--space-4)',
                    fontSize: '13px',
                    backgroundColor: overrideFeedback.includes('successfully') ? 'var(--feedback-success-bg)' : 'var(--feedback-error-bg)',
                    color: overrideFeedback.includes('successfully') ? 'var(--feedback-success)' : 'var(--feedback-error)',
                    border: `1px solid ${overrideFeedback.includes('successfully') ? 'var(--feedback-success-border)' : 'var(--feedback-error-border)'}`,
                  }}
                >
                  {overrideFeedback}
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 'var(--space-2)' }}>
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setSelectedStudent(null)}
                  disabled={submittingOverride}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-primary"
                  disabled={submittingOverride || reason.trim().length < 5}
                >
                  {submittingOverride ? 'Saving Override...' : 'Confirm Override'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
