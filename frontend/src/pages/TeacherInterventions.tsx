import { useState } from 'react';
import type { FormEvent } from 'react';
import type { CohortStudentSummary, Concept, Learner } from '../types';

interface TeacherInterventionsProps {
  cohort: CohortStudentSummary[];
  concepts: Concept[];
  currentTeacher: Learner;
  apiBaseUrl: string;
  authToken?: string | null;
  onInterventionSuccess: () => void;
}

export function TeacherInterventions({
  cohort,
  concepts,
  currentTeacher,
  apiBaseUrl,
  authToken,
  onInterventionSuccess,
}: TeacherInterventionsProps) {
  const [selectedStudentId, setSelectedStudentId] = useState<string>(cohort[0]?.learner_id || '');
  const [targetConceptId, setTargetConceptId] = useState<string>(concepts[0]?.id || 'MATH-C01');
  const [overriddenOutcome, setOverriddenOutcome] = useState<string>('SCAFFOLD');
  const [reason, setReason] = useState<string>('');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const selectedStudent = cohort.find((s) => s.learner_id === selectedStudentId);

  const handleApplyOverride = async (e: FormEvent) => {
    e.preventDefault();
    if (!selectedStudent) return;
    if (reason.trim().length < 5) {
      setFeedback({ type: 'error', message: 'A substantive pedagogical rationale (minimum 5 characters) is required.' });
      return;
    }

    setSubmitting(true);
    setFeedback(null);

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
        throw new Error(errJson.detail || 'Failed to submit clinical intervention.');
      }

      setFeedback({
        type: 'success',
        message: `Override successfully applied for ${selectedStudent.name}. Logged to immutable audit trail.`,
      });
      setReason('');
      onInterventionSuccess();
    } catch (err: any) {
      setFeedback({ type: 'error', message: err.message || 'Error applying override.' });
    } finally {
      setSubmitting(false);
    }
  };

  const flaggedStudents = cohort.filter((s) => s.needs_review);

  return (
    <div style={{ maxWidth: '960px' }}>
      {/* Header */}
      <div style={{ marginBottom: 'var(--space-6)' }}>
        <div className="editorial-kicker">CLINICAL OVERSIGHT WORKSPACE</div>
        <h1 className="serif-display" style={{ fontSize: '32px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
          Pedagogical Interventions & Overrides
        </h1>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '4px', lineHeight: 1.5 }}>
          Authorized faculty can adjust an automated adaptive recommendation when human observation or contextual evidence warrants a modified path.
          Every intervention requires a substantive rationale and is permanently logged.
        </p>
      </div>

      {/* Flagged Review Banner if any */}
      {flaggedStudents.length > 0 && (
        <div
          style={{
            marginBottom: 'var(--space-6)',
            padding: 'var(--space-4) var(--space-5)',
            backgroundColor: 'var(--feedback-warning-bg)',
            border: '1px solid var(--feedback-warning-border)',
            borderRadius: 'var(--radius-md)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <span style={{ fontSize: '14px' }}>⚠️</span>
            <strong style={{ fontSize: '13px', color: 'var(--feedback-warning)' }}>
              {flaggedStudents.length} Student(s) Flagged for Review
            </strong>
          </div>
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '6px' }}>
            {flaggedStudents.map((s) => (
              <button
                key={s.learner_id}
                type="button"
                className="btn-ghost"
                style={{
                  fontSize: '12px',
                  backgroundColor: 'var(--surface-white)',
                  border: '1px solid var(--feedback-warning-border)',
                  color: 'var(--sutra-espresso)',
                  padding: '3px 8px',
                }}
                onClick={() => setSelectedStudentId(s.learner_id)}
              >
                {s.name} ({s.learner_id}) &bull; {s.latest_outcome}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Intervention Form Card */}
      <div className="editorial-card" style={{ padding: 'var(--space-8)' }}>
        <form onSubmit={(e) => void handleApplyOverride(e)}>
          {/* 1. Target Student Selection */}
          <div style={{ marginBottom: 'var(--space-5)' }}>
            <label htmlFor="student-picker" className="form-label">
              Select Student to Intervene:
            </label>
            <select
              id="student-picker"
              className="form-input"
              value={selectedStudentId}
              onChange={(e) => setSelectedStudentId(e.target.value)}
            >
              {cohort.map((s) => (
                <option key={s.learner_id} value={s.learner_id}>
                  {s.name} ({s.learner_id}) — {s.latest_outcome || 'Pending'} {s.needs_review ? '⚠️ [Review Flag]' : ''}
                </option>
              ))}
            </select>
          </div>

          {/* Student Context Card */}
          {selectedStudent && (
            <div
              style={{
                marginBottom: 'var(--space-6)',
                padding: 'var(--space-4) var(--space-5)',
                backgroundColor: 'var(--surface-warm)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
                gap: 'var(--space-3)',
                fontSize: '13px',
              }}
            >
              <div>
                <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '11px', textTransform: 'uppercase' }}>
                  Current Engine Trajectory
                </span>
                <strong>{selectedStudent.latest_outcome || 'No outcome generated yet'}</strong>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '11px', textTransform: 'uppercase' }}>
                  Submissions & Accuracy
                </span>
                <span className="tabular-nums">
                  {selectedStudent.total_attempts > 0
                    ? `${selectedStudent.total_attempts} attempts &bull; ${Math.round((selectedStudent.total_correct / selectedStudent.total_attempts) * 100)}%`
                    : 'No attempts yet'}
                </span>
              </div>
            </div>
          )}

          {/* 2. Target Concept Unit */}
          <div style={{ marginBottom: 'var(--space-5)' }}>
            <label htmlFor="concept-picker" className="form-label">
              Target Curriculum Concept:
            </label>
            <select
              id="concept-picker"
              className="form-input"
              value={targetConceptId}
              onChange={(e) => setTargetConceptId(e.target.value)}
            >
              {concepts.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.id}: {c.title}
                </option>
              ))}
            </select>
          </div>

          {/* 3. New Overridden Outcome */}
          <div style={{ marginBottom: 'var(--space-5)' }}>
            <label htmlFor="outcome-picker" className="form-label">
              Adjusted Pedagogical Outcome:
            </label>
            <select
              id="outcome-picker"
              className="form-input"
              value={overriddenOutcome}
              onChange={(e) => setOverriddenOutcome(e.target.value)}
            >
              <option value="SCAFFOLD">SCAFFOLD — Provide guided steps and worked hints</option>
              <option value="BRIDGE_BACK">BRIDGE_BACK — Direct student to reinforce prerequisite gaps</option>
              <option value="STRETCH">STRETCH — Advance student to deeper or next concept challenge</option>
              <option value="CONFIRM">CONFIRM — Administer fresh diagnostic item for additional evidence</option>
            </select>
          </div>

          {/* 4. Mandatory Clinical Rationale */}
          <div style={{ marginBottom: 'var(--space-6)' }}>
            <label htmlFor="override-rationale" className="form-label">
              Substantive Pedagogical Rationale (Mandatory, &ge; 5 characters):
            </label>
            <textarea
              id="override-rationale"
              rows={3}
              className="form-input"
              style={{ height: 'auto', padding: 'var(--space-3)' }}
              placeholder="Detail the clinical or observational reasons for adjusting this student's trajectory..."
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              required
            />
            <span style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px', display: 'block' }}>
              Minimum 5 characters required for compliance audit logging.
            </span>
          </div>

          {feedback && (
            <div
              style={{
                padding: 'var(--space-3) var(--space-4)',
                marginBottom: 'var(--space-5)',
                borderRadius: 'var(--radius-sm)',
                backgroundColor: feedback.type === 'success' ? 'var(--feedback-success-bg)' : 'var(--feedback-error-bg)',
                border: `1px solid ${feedback.type === 'success' ? 'var(--feedback-success-border)' : 'var(--feedback-error-border)'}`,
                color: feedback.type === 'success' ? 'var(--feedback-success)' : 'var(--feedback-error)',
                fontSize: '13px',
              }}
            >
              {feedback.message}
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <button
              type="submit"
              className="btn-primary"
              style={{ backgroundColor: 'var(--sutra-espresso)', minWidth: '180px' }}
              disabled={submitting}
            >
              {submitting ? 'Applying & Logging...' : 'Record & Apply Intervention'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

