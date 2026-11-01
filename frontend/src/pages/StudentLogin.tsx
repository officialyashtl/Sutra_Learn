import { useState } from 'react';
import type { FormEvent } from 'react';
import type { Learner } from '../types';
import { loginWithCredentials, authenticatePersona } from '../services/auth';

interface StudentLoginProps {
  apiBaseUrl: string;
  onLoginSuccess: (user: Learner, token: string) => void;
  onSwitchToTeacher: () => void;
  onBackToGateway: () => void;
}

export function StudentLogin({
  apiBaseUrl,
  onLoginSuccess,
  onSwitchToTeacher,
  onBackToGateway,
}: StudentLoginProps) {
  const [username, setUsername] = useState('student-01');
  const [password, setPassword] = useState('sutra123');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError('Please provide both student identifier and password.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 1. Authenticate with backend credentials
      const session = await loginWithCredentials(apiBaseUrl, username.trim(), password.trim());
      if (session.role !== 'student') {
        throw new Error('This account holds educator privileges. Please use the Educator Workspace login.');
      }
      onLoginSuccess(
        { id: session.user_id, name: session.name, grade: 8, role: 'student' },
        session.access_token
      );
    } catch (err: any) {
      // Fallback for evaluator convenience: check if persona exists in demo registry
      try {
        const token = await authenticatePersona(apiBaseUrl, username.trim());
        const meRes = await fetch(`${apiBaseUrl}/api/v1/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (meRes.ok) {
          const meData = await meRes.json();
          if (meData.role !== 'student') {
            throw new Error('This account holds educator privileges. Please use the Educator Workspace login.');
          }
          onLoginSuccess(
            { id: meData.id, name: meData.name, grade: meData.grade, role: 'student' },
            token
          );
          return;
        }
      } catch {
        // preserve original error
      }
      setError(err.message || 'Authentication failed. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectDemoStudent = (id: string) => {
    setUsername(id);
    setPassword('sutra123');
    setError(null);
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: 'var(--surface-paper)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 'var(--space-6)',
      }}
    >
      <div
        className="editorial-card"
        style={{
          width: '100%',
          maxWidth: '440px',
          borderTop: '4px solid var(--sutra-mocha)',
          padding: 'var(--space-8)',
          backgroundColor: 'var(--surface-white)',
        }}
      >
        {/* Top Back Action & Brand */}
        <div style={{ marginBottom: 'var(--space-6)', textAlign: 'center' }}>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '12px', marginBottom: 'var(--space-2)' }}
            onClick={onBackToGateway}
          >
            &larr; Back to Portal Gateway
          </button>
          <div className="brand-symbol-mark" style={{ margin: '0 auto var(--space-2)' }}>
            S
          </div>
          <span className="editorial-kicker">SUTRA / STUDENT</span>
          <h1 className="serif-title" style={{ fontSize: '28px', color: 'var(--sutra-espresso)', marginTop: '4px' }}>
            Welcome back.
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Sign in to continue your Class 8 Mathematics learning journey.
          </p>
        </div>

        {/* Demo Fast-Fill Selector for Evaluators */}
        <div
          style={{
            marginBottom: 'var(--space-5)',
            padding: 'var(--space-3)',
            backgroundColor: 'var(--surface-warm)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
          }}
        >
          <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-secondary)', letterSpacing: '0.04em' }}>
            Select Student Persona:
          </span>
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '6px' }}>
            <button
              type="button"
              className={`btn-ghost ${username === 'student-01' ? 'active' : ''}`}
              style={{
                fontSize: '12px',
                padding: '3px 8px',
                backgroundColor: username === 'student-01' ? 'var(--sutra-mocha)' : 'var(--surface-white)',
                color: username === 'student-01' ? '#ffffff' : 'inherit',
                border: '1px solid var(--border-default)',
              }}
              onClick={() => handleSelectDemoStudent('student-01')}
            >
              Aarav Sharma
            </button>
            <button
              type="button"
              className={`btn-ghost ${username === 'student-02' ? 'active' : ''}`}
              style={{
                fontSize: '12px',
                padding: '3px 8px',
                backgroundColor: username === 'student-02' ? 'var(--sutra-mocha)' : 'var(--surface-white)',
                color: username === 'student-02' ? '#ffffff' : 'inherit',
                border: '1px solid var(--border-default)',
              }}
              onClick={() => handleSelectDemoStudent('student-02')}
            >
              Diya Patel
            </button>
            <button
              type="button"
              className={`btn-ghost ${username === 'student-03' ? 'active' : ''}`}
              style={{
                fontSize: '12px',
                padding: '3px 8px',
                backgroundColor: username === 'student-03' ? 'var(--sutra-mocha)' : 'var(--surface-white)',
                color: username === 'student-03' ? '#ffffff' : 'inherit',
                border: '1px solid var(--border-default)',
              }}
              onClick={() => handleSelectDemoStudent('student-03')}
            >
              Kabir Sen
            </button>
          </div>
        </div>

        {/* Login Form */}
        <form onSubmit={(e) => void handleSubmit(e)}>
          <div style={{ marginBottom: 'var(--space-4)' }}>
            <label htmlFor="student-username" className="form-label">
              Student Identifier
            </label>
            <input
              id="student-username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. student-01"
              required
              className="form-input"
              autoComplete="username"
            />
          </div>

          <div style={{ marginBottom: 'var(--space-4)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-2)' }}>
              <label htmlFor="student-password" className="form-label" style={{ marginBottom: 0 }}>
                Password
              </label>
              <button
                type="button"
                className="btn-ghost"
                style={{ fontSize: '11px', height: 'auto', padding: 0, textDecoration: 'underline' }}
                onClick={() => setShowPassword((prev) => !prev)}
              >
                {showPassword ? 'Hide' : 'Show'}
              </button>
            </div>
            <input
              id="student-password"
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              className="form-input"
              autoComplete="current-password"
            />
            <span style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px', display: 'block' }}>
              Default demo password: <code style={{ fontFamily: 'var(--font-mono)' }}>sutra123</code>
            </span>
          </div>

          {error && (
            <div
              style={{
                padding: 'var(--space-3)',
                backgroundColor: 'var(--feedback-error-bg)',
                border: '1px solid var(--feedback-error-border)',
                color: 'var(--feedback-error)',
                borderRadius: 'var(--radius-sm)',
                fontSize: '13px',
                marginBottom: 'var(--space-4)',
              }}
            >
              {error}
            </div>
          )}

          <button
            type="submit"
            className="btn-primary"
            style={{ width: '100%', marginTop: 'var(--space-2)' }}
            disabled={loading}
          >
            {loading ? 'Authenticating...' : 'Enter Student Portal →'}
          </button>
        </form>

        {/* Footer Redirect to Educator Login */}
        <div style={{ marginTop: 'var(--space-6)', borderTop: '1px solid var(--border-subtle)', paddingTop: 'var(--space-4)', textAlign: 'center' }}>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
            Are you an educator or faculty member?{' '}
            <button
              type="button"
              className="btn-ghost"
              style={{ padding: 0, color: 'var(--sutra-mocha)', fontWeight: 700 }}
              onClick={onSwitchToTeacher}
            >
              Go to Educator Workspace &rarr;
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
