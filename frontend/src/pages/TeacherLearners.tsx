import { useState } from 'react';
import type { CohortStudentSummary } from '../types';

interface TeacherLearnersProps {
  cohort: CohortStudentSummary[];
  onInspectLearner: (learnerId: string) => void;
  onInterveneLearner: (student: CohortStudentSummary) => void;
}

export function TeacherLearners({
  cohort,
  onInspectLearner,
  onInterveneLearner,
}: TeacherLearnersProps) {
  const [searchTerm, setSearchTerm] = useState('');

  const filtered = cohort.filter(
    (s) =>
      s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      s.learner_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: 'var(--space-6)' }}>
        <div className="editorial-kicker">COHORT DIRECTORY</div>
        <h1 className="serif-display" style={{ fontSize: '32px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
          Enrolled Learners & Academic Trajectories
        </h1>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '4px' }}>
          Class 8 Mathematics &bull; {cohort.length} Enrolled Students
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div style={{ marginBottom: 'var(--space-6)', maxWidth: '420px' }}>
        <input
          type="text"
          className="form-input"
          placeholder="Search by student name or identifier..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Cohort Table */}
      <div className="editorial-card">
        <div className="editorial-table-wrapper">
          <table className="editorial-table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Class</th>
                <th>Submissions</th>
                <th>Verified Accuracy</th>
                <th>Adaptive Outcome</th>
                <th>Attention Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((student) => {
                const totalAtt = student.total_attempts || 0;
                const totalCorr = student.total_correct || 0;
                const accuracy = totalAtt > 0 ? Math.min(100, Math.round((totalCorr / totalAtt) * 100)) : null;

                return (
                  <tr key={student.learner_id}>
                    <td>
                      <strong>{student.name}</strong>
                      <div style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                        {student.learner_id}
                      </div>
                    </td>
                    <td>Class {student.grade}</td>
                    <td className="tabular-nums">{totalAtt}</td>
                    <td>
                      {totalAtt > 0 ? (
                        <span className="tabular-nums" style={{ fontWeight: 600 }}>
                          {accuracy}% ({totalCorr}/{totalAtt})
                        </span>
                      ) : (
                        <span style={{ color: 'var(--text-muted)' }}>No attempts yet</span>
                      )}
                    </td>
                    <td>
                      {student.latest_outcome ? (
                        <span className="status-pill" style={{ backgroundColor: 'var(--surface-warm)', color: 'var(--sutra-espresso)', border: '1px solid var(--border-default)' }}>
                          {student.latest_outcome.replace('_', ' ')}
                        </span>
                      ) : (
                        <span style={{ color: 'var(--text-muted)' }}>Pending</span>
                      )}
                    </td>
                    <td>
                      {student.needs_review ? (
                        <span className="status-pill needs_reinforcement">⚠️ Needs Review</span>
                      ) : (
                        <span style={{ color: 'var(--feedback-success)', fontSize: '12px', fontWeight: 600 }}>✓ On Track</span>
                      )}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '6px' }}>
                        <button
                          type="button"
                          className="btn-secondary"
                          style={{ fontSize: '12px', height: '32px', padding: '0 10px' }}
                          onClick={() => onInspectLearner(student.learner_id)}
                        >
                          Dossier
                        </button>
                        <button
                          type="button"
                          className="btn-primary"
                          style={{ fontSize: '12px', height: '32px', padding: '0 10px' }}
                          onClick={() => onInterveneLearner(student)}
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
      </div>
    </div>
  );
}

