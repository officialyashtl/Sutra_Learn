import { useState } from 'react';
import type { FormEvent } from 'react';
import type { Learner } from '../types';
import { DeveloperSignature } from '../components/DeveloperSignature';
import { loginWithCredentials } from '../services/auth';

interface UnifiedLoginProps {
  apiBaseUrl: string;
  onLoginSuccess: (user: Learner, token: string, redirectTo: string) => void;
}

export function UnifiedLogin({ apiBaseUrl, onLoginSuccess }: UnifiedLoginProps) {
  const [identifier, setIdentifier] = useState('student-01');
  const [password, setPassword] = useState('sutra123');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const cleanId = identifier.trim();
    const cleanPw = password.trim();

    if (!cleanId || !cleanPw) {
      setError('Please provide both your institutional identifier and password.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const session = await loginWithCredentials(apiBaseUrl, cleanId, cleanPw);
      const role = session.role as 'student' | 'teacher';
      const learnerObj: Learner = {
        id: session.user_id,
        name: session.name,
        grade: 8,
        role,
      };
      const dest = session.redirect_to || (role === 'teacher' ? '/teacher/dashboard' : '/student/home');
      onLoginSuccess(learnerObj, session.access_token, dest);
    } catch (err: any) {
      setError(err.message || 'Invalid credentials. Please verify your ID and password.');
    } finally {
      setLoading(false);
    }
  };

  const setDemoAccount = (demoId: string, demoPw: string) => {
    setIdentifier(demoId);
    setPassword(demoPw);
    setError(null);
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
          NCERT Class 8 Mathematics &bull; Adaptive Learning Architecture
        </div>
      </header>

      {/* Main Content Area */}
      <main style={{ flex: 1, maxWidth: '1200px', width: '100%', margin: '0 auto', padding: 'var(--space-10) var(--space-6)', display: 'flex', alignItems: 'center' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(340px, 100%), 1fr))', gap: 'var(--space-12)', alignItems: 'center', width: '100%' }}>
          
          {/* Left Column: Platform Mission & Geometry Motif */}
          <div>
            <div className="editorial-kicker">ADAPTIVE LEARNING ARCHITECTURE</div>
            <h1 className="serif-display" style={{ fontSize: 'clamp(32px, 4.5vw, 48px)', color: 'var(--sutra-espresso)', lineHeight: 1.15, marginTop: 'var(--space-3)' }}>
              Learning, <br />thoughtfully connected.
            </h1>
            <p style={{ fontSize: '18px', color: 'var(--sutra-mocha)', fontWeight: 500, marginTop: 'var(--space-3)', lineHeight: 1.4 }}>
              Understand more. Discover your potential. Learn your way.
            </p>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: 'var(--space-4)', lineHeight: 1.6, maxWidth: '520px' }}>
              SUTRA LEARN is an evidence-driven learning ecosystem for Class 8 Mathematics. 
              Students receive targeted adaptive scaffolding and Socratic AI guidance, while educators 
              inspect cohort analytics, diagnose misconceptions, and lead human-in-the-loop interventions.
            </p>

            {/* Geometry Motif */}
            <div style={{ marginTop: 'var(--space-8)', display: 'flex', alignItems: 'center', gap: 'var(--space-6)' }}>
              <svg width="240" height="110" viewBox="0 0 240 110" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M 30 55 C 70 20, 90 20, 120 55" stroke="#BEB5A9" strokeWidth="1.5" strokeDasharray="3 3" />
                <path d="M 30 55 C 70 90, 90 90, 120 55" stroke="#BEB5A9" strokeWidth="1.5" />
                <path d="M 120 55 C 150 20, 170 20, 210 55" stroke="#BEB5A9" strokeWidth="1.5" />
                <path d="M 120 55 C 150 90, 170 90, 210 55" stroke="#BEB5A9" strokeWidth="1.5" strokeDasharray="3 3" />
                <circle cx="30" cy="55" r="14" fill="#F2ECE3" stroke="#A78D78" strokeWidth="1.5" />
                <text x="30" y="58" textAnchor="middle" fill="#291C0E" fontSize="9" fontWeight="700">C01</text>
                <circle cx="120" cy="55" r="18" fill="#6E473B" stroke="#291C0E" strokeWidth="2" />
                <text x="120" y="59" textAnchor="middle" fill="#F8F5EF" fontSize="10" fontWeight="700">C05</text>
                <circle cx="210" cy="55" r="14" fill="#291C0E" stroke="#291C0E" strokeWidth="1.5" />
                <text x="210" y="58" textAnchor="middle" fill="#E1D4C2" fontSize="9" fontWeight="700">C06</text>
              </svg>
              <div style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: 1.5 }}>
                <strong>Deterministic Graph</strong><br />
                Prerequisite Mastery &bull; Bayesian Evidentiary Policy
              </div>
            </div>

            {/* Core Pillars */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 'var(--space-4)', marginTop: 'var(--space-8)' }}>
              <div style={{ borderLeft: '2px solid var(--sutra-taupe)', paddingLeft: 'var(--space-3)' }}>
                <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--sutra-espresso)', display: 'block' }}>PREREQUISITE BRIDGING</span>
                <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Automated gap resolution to root concepts</span>
              </div>
              <div style={{ borderLeft: '2px solid var(--sutra-taupe)', paddingLeft: 'var(--space-3)' }}>
                <span style={{ fontSize: '11px', fontWeight: 700, color: 'var(--sutra-espresso)', display: 'block' }}>EDUCATOR DOSSIER</span>
                <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Clinical analytics with human-in-the-loop control</span>
              </div>
            </div>
          </div>

          {/* Right Column: Unified Authentication Form */}
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <div className="editorial-card" style={{ maxWidth: '440px', width: '100%', padding: 'var(--space-8)' }}>
              <div style={{ marginBottom: 'var(--space-6)' }}>
                <span className="editorial-kicker">UNIFIED SECURE ACCESS</span>
                <h2 className="serif-title" style={{ fontSize: '26px', color: 'var(--sutra-espresso)', marginTop: '4px' }}>
                  Sign in to SUTRA
                </h2>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                  Enter your credentials. SUTRA will resolve your authorized learning or teaching workspace automatically.
                </p>
              </div>

              {error && (
                <div
                  role="alert"
                  style={{
                    backgroundColor: 'var(--feedback-error-bg)',
                    border: '1px solid var(--feedback-error-border)',
                    padding: 'var(--space-3) var(--space-4)',
                    borderRadius: 'var(--radius-sm)',
                    marginBottom: 'var(--space-5)',
                    fontSize: '13px',
                    color: 'var(--feedback-error)',
                  }}
                >
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: 'var(--space-4)' }}>
                  <label
                    htmlFor="unified-identifier"
                    style={{
                      display: 'block',
                      fontSize: '12px',
                      fontWeight: 600,
                      color: 'var(--sutra-espresso)',
                      marginBottom: 'var(--space-1)',
                      letterSpacing: '0.03em',
                      textTransform: 'uppercase',
                    }}
                  >
                    Institutional ID or Username
                  </label>
                  <input
                    id="unified-identifier"
                    type="text"
                    value={identifier}
                    onChange={(e) => setIdentifier(e.target.value)}
                    placeholder="e.g. student-01 or teacher-01"
                    required
                    style={{
                      width: '100%',
                      padding: '10px 12px',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid var(--border-default)',
                      backgroundColor: 'var(--surface-white)',
                      fontSize: '14px',
                      color: 'var(--sutra-espresso)',
                      outline: 'none',
                    }}
                  />
                </div>

                <div style={{ marginBottom: 'var(--space-6)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-1)' }}>
                    <label
                      htmlFor="unified-password"
                      style={{
                        fontSize: '12px',
                        fontWeight: 600,
                        color: 'var(--sutra-espresso)',
                        letterSpacing: '0.03em',
                        textTransform: 'uppercase',
                      }}
                    >
                      Password
                    </label>
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      style={{
                        background: 'none',
                        border: 'none',
                        fontSize: '11px',
                        color: 'var(--sutra-mocha)',
                        cursor: 'pointer',
                        padding: 0,
                      }}
                    >
                      {showPassword ? 'Hide' : 'Show'}
                    </button>
                  </div>
                  <input
                    id="unified-password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter account password"
                    required
                    style={{
                      width: '100%',
                      padding: '10px 12px',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid var(--border-default)',
                      backgroundColor: 'var(--surface-white)',
                      fontSize: '14px',
                      color: 'var(--sutra-espresso)',
                      outline: 'none',
                    }}
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary"
                  style={{
                    width: '100%',
                    padding: '12px',
                    fontSize: '14px',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    gap: 'var(--space-2)',
                  }}
                >
                  {loading ? 'Authenticating...' : 'Continue to SUTRA \u2192'}
                </button>
              </form>

              {/* Demo Account Quick-Selection Pills */}
              <div style={{ marginTop: 'var(--space-6)', paddingTop: 'var(--space-5)', borderTop: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', display: 'block', marginBottom: 'var(--space-2)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Demo Accounts for Evaluator Inspection
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
                  <button
                    type="button"
                    onClick={() => setDemoAccount('student-01', 'sutra123')}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '8px 12px',
                      backgroundColor: identifier === 'student-01' ? 'var(--sutra-linen)' : 'var(--surface-warm)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: 'var(--radius-sm)',
                      cursor: 'pointer',
                      textAlign: 'left',
                    }}
                  >
                    <div>
                      <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--sutra-espresso)', display: 'block' }}>Aarav Sharma (Student)</span>
                      <span style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>ID: student-01 &bull; Class 8 Mathematics</span>
                    </div>
                    <span style={{ fontSize: '11px', color: 'var(--sutra-mocha)', fontWeight: 500 }}>Select &rarr;</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setDemoAccount('teacher-01', 'teacher123')}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '8px 12px',
                      backgroundColor: identifier === 'teacher-01' ? 'var(--sutra-linen)' : 'var(--surface-warm)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: 'var(--radius-sm)',
                      cursor: 'pointer',
                      textAlign: 'left',
                    }}
                  >
                    <div>
                      <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--sutra-espresso)', display: 'block' }}>Ms. Ananya Roy (Educator)</span>
                      <span style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>ID: teacher-01 &bull; Class 8 Cohort Lead</span>
                    </div>
                    <span style={{ fontSize: '11px', color: 'var(--sutra-mocha)', fontWeight: 500 }}>Select &rarr;</span>
                  </button>
                </div>
              </div>

              {/* Security Footnote */}
              <div style={{ marginTop: 'var(--space-5)', textAlign: 'center' }}>
                <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>
                  HMAC-SHA256 Token Session &bull; Server-Side Role Enforcement &bull; Zero Persona Spoofing
                </span>
              </div>
            </div>
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer
        style={{
          padding: 'var(--space-4) var(--space-8)',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 'var(--space-2)',
          fontSize: '11px',
          color: 'var(--text-muted)',
        }}
      >
        <div>&copy; 2026 SUTRA LEARN. All rights reserved. Directed Concept Architecture.</div>
        <DeveloperSignature />
      </footer>
    </div>
  );
}
