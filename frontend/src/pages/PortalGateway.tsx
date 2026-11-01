import type { Learner } from '../types';

interface PortalGatewayProps {
  onSelectPortal: (portal: 'student' | 'teacher') => void;
  onQuickLogin: (learner: Learner) => void;
  learners: Learner[];
}

export function PortalGateway({ onSelectPortal, onQuickLogin, learners }: PortalGatewayProps) {
  const studentDemo = learners.find((l) => l.role === 'student') || {
    id: 'student-01',
    name: 'Aarav Sharma',
    grade: 8,
    role: 'student' as const,
  };

  const teacherDemo = learners.find((l) => l.role === 'teacher') || {
    id: 'teacher-01',
    name: 'Ms. Ananya Roy',
    grade: 8,
    role: 'teacher' as const,
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: 'var(--surface-paper)', display: 'flex', flexDirection: 'column' }}>
      {/* Top Header Wordmark */}
      <header
        style={{
          padding: 'var(--space-6) var(--space-8)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          borderBottom: '1px solid var(--border-subtle)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
          <div className="brand-symbol-mark">S</div>
          <div>
            <span className="brand-wordmark" style={{ fontSize: '20px' }}>SUTRA LEARN</span>
            <span className="brand-subline" style={{ display: 'block', fontSize: '10px', marginTop: '-2px' }}>
              LEARNING, THOUGHTFULLY CONNECTED
            </span>
          </div>
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          Class 8 Mathematics &bull; Directed Concept Architecture
        </div>
      </header>

      {/* Main Hero & Split Portal Composition */}
      <main style={{ flex: 1, maxWidth: '1240px', width: '100%', margin: '0 auto', padding: 'var(--space-8) var(--space-4)' }}>
        {/* Editorial Headline & Geometry Motif */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(280px, 100%), 1fr))', gap: 'var(--space-8)', alignItems: 'center', marginBottom: 'var(--space-12)' }}>
          <div>
            <div className="editorial-kicker">ADAPTIVE LEARNING ARCHITECTURE</div>
            <h1 className="serif-display" style={{ fontSize: 'clamp(28px, 4vw, 42px)', color: 'var(--sutra-espresso)', lineHeight: 1.15, marginTop: 'var(--space-2)' }}>
              Knowledge is connected. <br />Learning is a continuous journey.
            </h1>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: 'var(--space-4)', lineHeight: 1.6, maxWidth: '540px' }}>
              SUTRA LEARN distinguishes between developing intuition, prerequisite bottlenecks, and demonstrated mastery.
              Every assessment yields defensible insight.
            </p>
          </div>

          {/* Abstract Connected Knowledge Motif (Original SVG Geometry) */}
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <svg width="280" height="180" viewBox="0 0 280 180" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style={{ maxWidth: '100%', height: 'auto' }}>
              {/* Directed Connections */}
              <path d="M 40 90 C 80 50, 110 50, 140 90" stroke="#BEB5A9" strokeWidth="1.5" strokeDasharray="3 3" />
              <path d="M 40 90 C 80 130, 110 130, 140 90" stroke="#BEB5A9" strokeWidth="1.5" />
              <path d="M 140 90 C 180 50, 200 50, 240 90" stroke="#BEB5A9" strokeWidth="1.5" />
              <path d="M 140 90 C 180 130, 200 130, 240 90" stroke="#BEB5A9" strokeWidth="1.5" strokeDasharray="3 3" />

              {/* Node 1: Prerequisite */}
              <circle cx="40" cy="90" r="18" fill="#F2ECE3" stroke="#A78D78" strokeWidth="2" />
              <text x="40" y="94" textAnchor="middle" fill="#291C0E" fontSize="10" fontFamily="sans-serif" fontWeight="700">C01</text>

              {/* Node 2: Balance Principle */}
              <circle cx="140" cy="50" r="16" fill="#F8F5EF" stroke="#BEB5A9" strokeWidth="1.5" />
              <text x="140" y="54" textAnchor="middle" fill="#65584E" fontSize="9" fontFamily="sans-serif">C02</text>

              {/* Node 3: Core Equations */}
              <circle cx="140" cy="90" r="22" fill="#6E473B" stroke="#291C0E" strokeWidth="2" />
              <text x="140" y="94" textAnchor="middle" fill="#F8F5EF" fontSize="11" fontFamily="sans-serif" fontWeight="700">C05</text>

              {/* Node 4: Inverse Ops */}
              <circle cx="140" cy="130" r="16" fill="#F8F5EF" stroke="#BEB5A9" strokeWidth="1.5" />
              <text x="140" y="134" textAnchor="middle" fill="#65584E" fontSize="9" fontFamily="sans-serif">C03</text>

              {/* Node 5: Verification */}
              <circle cx="240" cy="90" r="18" fill="#291C0E" stroke="#291C0E" strokeWidth="2" />
              <text x="240" y="94" textAnchor="middle" fill="#E1D4C2" fontSize="10" fontFamily="sans-serif" fontWeight="700">C06</text>
            </svg>
          </div>
        </div>

        {/* Two Differentiated Portal Destinations */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(280px, 100%), 1fr))', gap: 'var(--space-6)' }}>
          {/* STUDENT PORTAL CARD */}
          <div
            className="editorial-card"
            style={{
              borderTop: '4px solid var(--sutra-mocha)',
              display: 'flex',
              flexDirection: 'column',
              backgroundColor: 'var(--surface-white)',
            }}
          >
            <div className="card-header-line">
              <span className="editorial-kicker">LEARNER ENVIRONMENT</span>
              <span style={{ fontSize: '18px' }}>🎒</span>
            </div>

            <h2 className="serif-title" style={{ fontSize: '26px', color: 'var(--sutra-espresso)', marginBottom: 'var(--space-1)' }}>
              SUTRA / STUDENT
            </h2>
            <p style={{ fontStyle: 'italic', fontSize: '14px', color: 'var(--text-secondary)', marginBottom: 'var(--space-5)' }}>
              &ldquo;Understand more. Discover your potential. Learn your way.&rdquo;
            </p>

            <ul style={{ listStyle: 'none', margin: '0 0 var(--space-6) 0', padding: 0, fontSize: '13px', color: 'var(--text-primary)', lineHeight: 1.8 }}>
              <li>✓ Class 8 Linear Equations DAG curriculum</li>
              <li>✓ Step-by-step worked textbook lessons with exact math</li>
              <li>✓ Distraction-free diagnostic assessments</li>
              <li>✓ Real-time misconception error diagnosis</li>
              <li>✓ Offline attempt persistence & idempotent sync</li>
            </ul>

            <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              <button
                type="button"
                className="btn-primary"
                style={{ width: '100%' }}
                onClick={() => onSelectPortal('student')}
              >
                Enter Student Portal &rarr;
              </button>
              <button
                type="button"
                className="btn-secondary"
                style={{ width: '100%', fontSize: '12px' }}
                onClick={() => onQuickLogin(studentDemo)}
              >
                Fast-Track Student Demo ({studentDemo.name})
              </button>
            </div>
          </div>

          {/* EDUCATOR WORKSPACE CARD */}
          <div
            className="editorial-card"
            style={{
              borderTop: '4px solid var(--sutra-espresso)',
              display: 'flex',
              flexDirection: 'column',
              backgroundColor: 'var(--surface-white)',
            }}
          >
            <div className="card-header-line">
              <span className="editorial-kicker" style={{ color: 'var(--sutra-espresso)' }}>FACULTY COMMAND CENTER</span>
              <span style={{ fontSize: '18px' }}>📋</span>
            </div>

            <h2 className="serif-title" style={{ fontSize: '26px', color: 'var(--sutra-espresso)', marginBottom: 'var(--space-1)' }}>
              SUTRA / EDUCATOR
            </h2>
            <p style={{ fontStyle: 'italic', fontSize: '14px', color: 'var(--text-secondary)', marginBottom: 'var(--space-5)' }}>
              &ldquo;See beyond scores. Understand learning. Make better decisions.&rdquo;
            </p>

            <ul style={{ listStyle: 'none', margin: '0 0 var(--space-6) 0', padding: 0, fontSize: '13px', color: 'var(--text-primary)', lineHeight: 1.8 }}>
              <li>✓ Real-time cohort mastery analytics (verified math)</li>
              <li>✓ Deep student evidence chronology inspector</li>
              <li>✓ Prerequisite bottleneck & misconception audit</li>
              <li>✓ Audited clinical pedagogical overrides</li>
              <li>✓ Server-enforced cryptographic authorization</li>
            </ul>

            <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              <button
                type="button"
                className="btn-primary"
                style={{ width: '100%', backgroundColor: 'var(--sutra-espresso)' }}
                onClick={() => onSelectPortal('teacher')}
              >
                Enter Educator Workspace &rarr;
              </button>
              <button
                type="button"
                className="btn-secondary"
                style={{ width: '100%', fontSize: '12px' }}
                onClick={() => onQuickLogin(teacherDemo)}
              >
                Fast-Track Educator Demo ({teacherDemo.name})
              </button>
            </div>
          </div>
        </div>
      </main>

      {/* Bottom Architectural Colophon */}
      <footer
        style={{
          borderTop: '1px solid var(--border-subtle)',
          padding: 'var(--space-4) var(--space-8)',
          textAlign: 'center',
          fontSize: '12px',
          color: 'var(--text-muted)',
        }}
      >
        SUTRA LEARN &bull; Student Understanding, Targeted Reinforcement & Adaptation &bull; Earthbound Editorial Edition
      </footer>
    </div>
  );
}
