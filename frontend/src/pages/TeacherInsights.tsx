import type { Concept, ConceptAnalytics } from '../types';

interface TeacherInsightsProps {
  concepts: Concept[];
  analytics: ConceptAnalytics[];
  onRefresh: () => void;
}

export function TeacherInsights({
  concepts,
  analytics,
  onRefresh,
}: TeacherInsightsProps) {
  return (
    <div>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 'var(--space-4)', marginBottom: 'var(--space-6)' }}>
        <div>
          <div className="editorial-kicker">CURRICULUM INTELLIGENCE & BOTTLENECK ANALYSIS</div>
          <h1 className="serif-display" style={{ fontSize: '32px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
            Concept Difficulty & Misconceptions
          </h1>
          <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '4px', maxWidth: '640px' }}>
            Aggregated diagnostic evidence across all Class 8 submissions. Highlights prerequisite bottlenecks and systemic misconception patterns requiring group instruction.
          </p>
        </div>
        <button type="button" className="btn-secondary" onClick={onRefresh}>
          ↻ Refresh Analytics
        </button>
      </div>

      {/* Analytics Matrix Table */}
      <div className="editorial-card">
        {analytics.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: 'var(--space-6) 0', textAlign: 'center' }}>
            No student attempt data recorded yet across the curriculum.
          </p>
        ) : (
          <div className="editorial-table-wrapper">
            <table className="editorial-table">
              <thead>
                <tr>
                  <th>Concept Unit</th>
                  <th>Total Attempts</th>
                  <th>Class Accuracy</th>
                  <th>Clean vs Hinted</th>
                  <th>Top Observed Misconceptions</th>
                  <th>Friction State</th>
                </tr>
              </thead>
              <tbody>
                {analytics.map((ca) => {
                  const conceptObj = concepts.find((c) => c.id === ca.concept_id);
                  const title = conceptObj ? conceptObj.title : ca.concept_id;
                  const isChallenging = ca.accuracy_percentage < 60;
                  const isModerate = ca.accuracy_percentage >= 60 && ca.accuracy_percentage < 80;

                  return (
                    <tr key={ca.concept_id}>
                      <td>
                        <strong>{title}</strong>
                        <div style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                          {ca.concept_id}
                        </div>
                      </td>
                      <td className="tabular-nums">{ca.total_attempts}</td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div
                            style={{
                              flex: '0 0 60px',
                              height: '6px',
                              backgroundColor: 'var(--surface-warm)',
                              borderRadius: '3px',
                              overflow: 'hidden',
                            }}
                          >
                            <div
                              style={{
                                width: `${Math.min(100, Math.max(0, ca.accuracy_percentage))}%`,
                                height: '100%',
                                backgroundColor: isChallenging
                                  ? 'var(--feedback-error)'
                                  : isModerate
                                  ? 'var(--sutra-mocha)'
                                  : 'var(--feedback-success)',
                              }}
                            />
                          </div>
                          <span className="tabular-nums" style={{ fontWeight: 600 }}>
                            {ca.accuracy_percentage}%
                          </span>
                        </div>
                      </td>
                      <td style={{ fontSize: '12px' }}>
                        <span style={{ color: 'var(--feedback-success)', fontWeight: 600 }}>{ca.unassisted_correct} clean</span>
                        {ca.total_assisted > 0 && (
                          <span style={{ color: 'var(--sutra-mocha)', marginLeft: '6px' }}>
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
                                  backgroundColor: 'var(--feedback-warning-bg)',
                                  color: 'var(--feedback-warning)',
                                  border: '1px solid var(--feedback-warning-border)',
                                }}
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <span style={{ color: 'var(--text-muted)', fontSize: '12px' }}>None recorded</span>
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
      </div>
    </div>
  );
}

