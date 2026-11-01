import { useState, useEffect } from 'react';

interface AuditEvent {
  id: string;
  event_category: string;
  actor_id: string;
  actor_role: string;
  learner_id?: string;
  learner_name?: string;
  concept_id?: string;
  previous_state?: string;
  new_state?: string;
  rationale?: string;
  outcome: string;
  details?: string;
  created_at: string;
}

interface TeacherAuditProps {
  apiBaseUrl: string;
  authToken?: string | null;
}

type CategoryTab = 'ALL' | 'PEDAGOGICAL_INTERVENTIONS' | 'REJECTED_SECURITY_EVENTS' | 'SUCCESSFUL_AUTHORIZED_ACTIONS' | 'SYSTEM_EVENTS';

export function TeacherAudit({ apiBaseUrl, authToken }: TeacherAuditProps) {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [activeTab, setActiveTab] = useState<CategoryTab>('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    async function fetchAuditEvents() {
      try {
        setLoading(true);
        const query = activeTab === 'ALL' ? '' : `?category=${activeTab}`;
        const res = await fetch(`${apiBaseUrl}/api/v1/teacher/audit${query}`, {
          headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
        });
        if (res.ok && isMounted) {
          const data = await res.json();
          setEvents(data || []);
        }
      } catch (err) {
        console.warn('Error fetching audit trail:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    void fetchAuditEvents();
    return () => {
      isMounted = false;
    };
  }, [activeTab, apiBaseUrl, authToken]);

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: 'var(--space-6)' }}>
        <div className="editorial-kicker">GOVERNANCE & COMPLIANCE LEDGER</div>
        <h1 className="serif-display" style={{ fontSize: '32px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
          Immutable System & Pedagogical Audit Trail
        </h1>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '4px', maxWidth: '680px' }}>
          Defensible record of all pedagogical interventions, authorization events, and platform events.
          Entries are permanently logged with verified server timestamps.
        </p>
      </div>

      {/* Category Tabs */}
      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: 'var(--space-6)' }}>
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'ALL' ? 'active' : ''}`}
          onClick={() => setActiveTab('ALL')}
        >
          All Events ({events.length})
        </button>
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'PEDAGOGICAL_INTERVENTIONS' ? 'active' : ''}`}
          onClick={() => setActiveTab('PEDAGOGICAL_INTERVENTIONS')}
        >
          Pedagogical Interventions
        </button>
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'REJECTED_SECURITY_EVENTS' ? 'active' : ''}`}
          onClick={() => setActiveTab('REJECTED_SECURITY_EVENTS')}
        >
          Security & Access Events
        </button>
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'SUCCESSFUL_AUTHORIZED_ACTIONS' ? 'active' : ''}`}
          onClick={() => setActiveTab('SUCCESSFUL_AUTHORIZED_ACTIONS')}
        >
          Authorized Actions
        </button>
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'SYSTEM_EVENTS' ? 'active' : ''}`}
          onClick={() => setActiveTab('SYSTEM_EVENTS')}
        >
          System & Migrations
        </button>
      </div>

      {/* Table */}
      <div className="editorial-card">
        {loading ? (
          <p style={{ textAlign: 'center', padding: 'var(--space-8)', color: 'var(--text-muted)' }}>
            Retrieving verified audit records...
          </p>
        ) : events.length === 0 ? (
          <p style={{ fontStyle: 'italic', color: 'var(--text-muted)', padding: 'var(--space-6) 0', textAlign: 'center' }}>
            No audit records matching category: {activeTab.replace('_', ' ')}
          </p>
        ) : (
          <div className="editorial-table-wrapper">
            <table className="editorial-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Category</th>
                  <th>Actor</th>
                  <th>Subject Learner</th>
                  <th>Concept</th>
                  <th>State Transition</th>
                  <th>Mandatory Rationale</th>
                  <th>Outcome</th>
                </tr>
              </thead>
              <tbody>
                {events.map((ev) => (
                  <tr key={ev.id}>
                    <td className="timestamp" style={{ fontSize: '12px', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
                      {new Date(ev.created_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                    </td>
                    <td>
                      <span className="status-pill" style={{ fontSize: '10px', backgroundColor: 'var(--surface-warm)', color: 'var(--sutra-espresso)', border: '1px solid var(--border-default)' }}>
                        {ev.event_category.replace(/_/g, ' ')}
                      </span>
                    </td>
                    <td>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>{ev.actor_id}</span>
                      <span style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block' }}>({ev.actor_role})</span>
                    </td>
                    <td>
                      {ev.learner_name || ev.learner_id ? (
                        <>
                          <strong>{ev.learner_name || ev.learner_id}</strong>
                          <span style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', fontFamily: 'var(--font-mono)' }}>
                            {ev.learner_id}
                          </span>
                        </>
                      ) : (
                        <span style={{ color: 'var(--text-muted)' }}>—</span>
                      )}
                    </td>
                    <td>
                      {ev.concept_id ? (
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>{ev.concept_id}</span>
                      ) : (
                        <span style={{ color: 'var(--text-muted)' }}>—</span>
                      )}
                    </td>
                    <td>
                      {ev.previous_state || ev.new_state ? (
                        <span style={{ fontSize: '12px' }}>
                          <span style={{ textDecoration: 'line-through', color: 'var(--text-muted)' }}>{ev.previous_state}</span>
                          {' '}&rarr;{' '}
                          <strong>{ev.new_state}</strong>
                        </span>
                      ) : (
                        <span style={{ color: 'var(--text-muted)' }}>—</span>
                      )}
                    </td>
                    <td style={{ maxWidth: '280px', fontSize: '12px', lineHeight: 1.4 }}>
                      {ev.rationale || ev.details || '—'}
                    </td>
                    <td>
                      <span style={{ fontWeight: 600, color: ev.outcome === 'REJECTED' ? 'var(--feedback-error)' : 'var(--feedback-success)' }}>
                        {ev.outcome}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

