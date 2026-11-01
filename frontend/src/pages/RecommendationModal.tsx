import type { Recommendation } from '../types';

interface RecommendationModalProps {
  recommendation: Recommendation;
  onContinue: (targetConceptId: string, activityType: string) => void;
  onClose: () => void;
}

export function RecommendationModal({
  recommendation,
  onContinue,
  onClose,
}: RecommendationModalProps) {
  const { outcome, target_concept_title, target_concept_id, target_activity_type, explanation, confidence_score, evidence_summary, policy_version } = recommendation;

  const outcomeHeaders: Record<string, string> = {
    BRIDGE_BACK: 'Prerequisite Reinforcement Recommended',
    SCAFFOLD: 'Guided Practice & Scaffolding Recommended',
    STRETCH: 'Mastery Demonstrated — Stretch Progression',
    CONFIRM: 'Confirming Understanding with Further Evidence',
    TEACHER_REVIEW: 'Flagged for Human Teacher Review',
  };

  const getActionLabel = () => {
    switch (outcome) {
      case 'BRIDGE_BACK':
        return `Reinforce Prerequisite: ${target_concept_title} →`;
      case 'SCAFFOLD':
        return `Start Guided Practice: ${target_concept_title} →`;
      case 'STRETCH':
        return `Advance to Next Concept: ${target_concept_title} →`;
      case 'CONFIRM':
        return 'Take Clarifying Diagnostic Assessment →';
      case 'TEACHER_REVIEW':
        return 'Return to Curriculum Map (Teacher Notified)';
      default:
        return 'Continue Learning Trajectory →';
    }
  };

  return (
    <div style={{ maxWidth: '820px', margin: '0 auto' }}>
      <div
        className="editorial-card"
        style={{
          borderLeft: '4px solid var(--sutra-mocha)',
          padding: 'var(--space-8)',
          backgroundColor: 'var(--surface-white)',
        }}
        role="dialog"
        aria-modal="true"
        aria-labelledby="rec-title"
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
          <div>
            <span className="status-pill" style={{ backgroundColor: 'var(--surface-warm)', color: 'var(--sutra-espresso)', border: '1px solid var(--border-default)' }}>
              {outcome.replace('_', ' ')}
            </span>
            <h2 id="rec-title" className="serif-title" style={{ fontSize: '26px', color: 'var(--sutra-espresso)', marginTop: '6px' }}>
              {outcomeHeaders[outcome] || outcome}
            </h2>
          </div>
          <div
            style={{
              textAlign: 'right',
              backgroundColor: 'var(--surface-paper)',
              padding: 'var(--space-2) var(--space-4)',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-secondary)', letterSpacing: '0.04em' }}>
              Engine Confidence
            </span>
            <div className="tabular-nums" style={{ fontFamily: 'var(--font-display)', fontSize: '22px', fontWeight: 700, color: 'var(--sutra-espresso)' }}>
              {Math.round(confidence_score * 100)}%
            </div>
          </div>
        </div>

        <p style={{ marginTop: 'var(--space-4)', fontSize: '15px', lineHeight: 1.6, color: 'var(--text-primary)' }}>
          {explanation}
        </p>

        {/* Diagnostic Evidence Summary Breakdown */}
        {evidence_summary && (
          <div
            style={{
              marginTop: 'var(--space-5)',
              backgroundColor: 'var(--surface-warm)',
              borderRadius: 'var(--radius-md)',
              padding: 'var(--space-4) var(--space-5)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
              <span className="editorial-kicker">
                Diagnostic Evidence Summary
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                Policy v{policy_version || '1.0.0'}
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 'var(--space-3)' }}>
              <div className="metric-tile" style={{ backgroundColor: 'var(--surface-white)' }}>
                <div className="metric-num tabular-nums" style={{ fontSize: '20px' }}>
                  {evidence_summary.total_distinct ?? evidence_summary.distinct_questions_evaluated ?? '1'}
                </div>
                <div className="metric-label">Distinct Items</div>
              </div>

              {evidence_summary.unassisted_correct !== undefined && (
                <div className="metric-tile" style={{ backgroundColor: 'var(--surface-white)' }}>
                  <div className="metric-num tabular-nums" style={{ fontSize: '20px', color: 'var(--feedback-success)' }}>
                    {evidence_summary.unassisted_correct}
                  </div>
                  <div className="metric-label">Unassisted Solves</div>
                </div>
              )}

              {evidence_summary.assisted_correct !== undefined && (
                <div className="metric-tile" style={{ backgroundColor: 'var(--surface-white)' }}>
                  <div className="metric-num tabular-nums" style={{ fontSize: '20px', color: 'var(--sutra-mocha)' }}>
                    {evidence_summary.assisted_correct}
                  </div>
                  <div className="metric-label">Hint-Assisted</div>
                </div>
              )}

              {evidence_summary.unassisted_accuracy !== undefined && (
                <div className="metric-tile" style={{ backgroundColor: 'var(--surface-white)' }}>
                  <div className="metric-num tabular-nums" style={{ fontSize: '20px' }}>
                    {Math.min(100, Math.round(Number(evidence_summary.unassisted_accuracy) * 100))}%
                  </div>
                  <div className="metric-label">Accuracy</div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Modal Actions */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 'var(--space-3)', marginTop: 'var(--space-6)', flexWrap: 'wrap' }}>
          <button type="button" className="btn-secondary" onClick={onClose}>
            Back to Curriculum Map
          </button>
          <button
            type="button"
            className="btn-primary"
            onClick={() => onContinue(target_concept_id, target_activity_type)}
          >
            {getActionLabel()}
          </button>
        </div>
      </div>
    </div>
  );
}
