import { useState } from 'react';
import type { FormEvent } from 'react';
import type { Learner } from '../types';
import { loginWithCredentials, authenticatePersona } from '../services/auth';

interface TeacherLoginProps {
  apiBaseUrl: string;
  onLoginSuccess: (user: Learner, token: string) => void;
  onSwitchToStudent: () => void;
  onBackToGateway: () => void;
}

export function TeacherLogin({
  apiBaseUrl,
  onLoginSuccess,
  onSwitchToStudent,
  onBackToGateway,
}: TeacherLoginProps) {
  const [username, setUsername] = useState('teacher-01');
  const [password, setPassword] = useState('teacher123');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setError('Please provide both educator identifier and password.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const session = await loginWithCredentials(apiBaseUrl, username.trim(), password.trim());
      if (session.role !== 'teacher') {
        throw new Error('Access restricted: Account does not hold educator privileges. Please use the Student Portal.');
      }
      onLoginSuccess(
        { id: session.user_id, name: session.name, grade: 8, role: 'teacher' },
        session.access_token
      );
    } catch (err: any) {
      try {
        const token = await authenticatePersona(apiBaseUrl, username.trim());
        const meRes = await fetch(`${apiBaseUrl}/api/v1/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (meRes.ok) {
          const meData = await meRes.json();
          if (meData.role !== 'teacher') {
            throw new Error('Access restricted: Account does not hold educator privileges. Please use the Student Portal.');
          }
          onLoginSuccess(
            { id: meData.id, name: meData.name, grade: meData.grade, role: 'teacher' },
            token
          );
          return;
        }
      } catch {
        // preserve original error
      }
      setError(err.message || 'Authentication failed. Please verify faculty credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectDemoTeacher = () => {
    setUsername('teacher-01');
    setPassword('teacher123');
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
          maxWidth: '460px',
          borderTop: '4px solid var(--sutra-espresso)',
          padding: 'var(--space-8)',
          backgroundColor: 'var(--surface-white)',
        }}
      >
        {/* Header */}
        <div style={{ marginBottom: 'var(--space-6)', textAlign: 'center' }}>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '12px', marginBottom: 'var(--space-2)' }}
            onClick={onBackToGateway}
          >
            &larr; Back to Portal Gateway
          </button>
          <div
            className="brand-symbol-mark"
            style={{
              margin: '0 auto var(--space-2)',
              backgroundColor: 'var(--sutra-espresso)',
              color: 'var(--sutra-linen)',
            }}
          >
            S
          </div>
          <span className="editorial-kicker" style={{ color: 'var(--sutra-espresso)' }}>
            SUTRA / EDUCATOR
          </span>
          <h1 className="serif-title" style={{ fontSize: '28px', color: 'var(--sutra-espresso)', marginTop: '4px' }}>
            Educator Workspace
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Faculty & Clinical Oversight &bull; Class 8 Mathematics
          </p>
        </div>

        {/* Demo Fast-Fill Selector */}
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
            Verified Faculty Profile:
          </span>
          <div style={{ marginTop: '6px' }}>
            <button
              type="button"
              className={`btn-ghost ${username === 'teacher-01' ? 'active' : ''}`}
              style={{
                width: '100%',
                padding: '8px 12px',
                fontSize: '12px',
                backgroundColor: username === 'teacher-01' ? 'var(--sutra-espresso)' : 'var(--surface-white)',
                color: username === 'teacher-01' ? 'var(--sutra-linen)' : 'inherit',
                border: '1px solid var(--border-default)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
              onClick={handleSelectDemoTeacher}
            >
              <span><strong>Ms. Ananya Roy</strong> (Mathematics Dept Lead)</span>
              <span style={{ fontSize: '11px', opacity: 0.8 }}>ID: teacher-01</span>
            </button>
          </div>
        </div>

        {/* Login Form */}
        <form onSubmit={(e) => void handleSubmit(e)}>
          <div style={{ marginBottom: 'var(--space-4)' }}>
            <label htmlFor="teacher-username" className="form-label">
              Educator Identifier
            </label>
            <input
              id="teacher-username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. teacher-01"
              required
              className="form-input"
              autoComplete="username"
            />
          </div>

          <div style={{ marginBottom: 'var(--space-4)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-2)' }}>
              <label htmlFor="teacher-password" className="form-label" style={{ marginBottom: 0 }}>
                Faculty Password
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
              id="teacher-password"
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              className="form-input"
              autoComplete="current-password"
            />
            <span style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px', display: 'block' }}>
              Default demo password: <code style={{ fontFamily: 'var(--font-mono)' }}>teacher123</code>
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
            style={{ width: '100%', backgroundColor: 'var(--sutra-espresso)', marginTop: 'var(--space-2)' }}
            disabled={loading}
          >
            {loading ? 'Authenticating...' : 'Access Faculty Workspace →'}
          </button>
        </form>

        {/* Footer Redirect to Student Portal */}
        <div style={{ marginTop: 'var(--space-6)', borderTop: '1px solid var(--border-subtle)', paddingTop: 'var(--space-4)', textAlign: 'center' }}>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
            Student seeking homework and learning practice?{' '}
            <button
              type="button"
              className="btn-ghost"
              style={{ padding: 0, color: 'var(--sutra-mocha)', fontWeight: 700 }}
              onClick={onSwitchToStudent}
            >
              Go to Student Portal &rarr;
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
