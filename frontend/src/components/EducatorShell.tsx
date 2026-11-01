import type { ReactNode } from 'react';
import type { Learner } from '../types';
import { DeveloperSignature } from './DeveloperSignature';

export type EducatorTab = 'overview' | 'learners' | 'insights' | 'interventions' | 'assistant' | 'audit';

interface EducatorShellProps {
  currentTeacher: Learner;
  activeTab: EducatorTab;
  onSelectTab: (tab: EducatorTab) => void;
  onSignOut: () => void;
  children: ReactNode;
}

export function EducatorShell({
  currentTeacher,
  activeTab,
  onSelectTab,
  onSignOut,
  children,
}: EducatorShellProps) {
  return (
    <div className="educator-shell">
      {/* Left Navigation Rail (Desktop) */}
      <aside className="educator-sidebar" role="navigation" aria-label="Educator Navigation Rail">
        <div className="educator-sidebar-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div
              className="brand-symbol-mark"
              style={{
                backgroundColor: 'var(--sutra-mocha)',
                color: 'var(--surface-paper)',
                width: '32px',
                height: '32px',
                fontSize: '16px',
              }}
              aria-hidden="true"
            >
              S
            </div>
            <div>
              <div className="educator-brand-title">SUTRA</div>
              <div className="educator-brand-dept">EDUCATOR WORKSPACE</div>
            </div>
          </div>
        </div>

        {/* Navigation links */}
        <ul className="educator-nav-list">
          <li>
            <button
              type="button"
              className={`educator-nav-item ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => onSelectTab('overview')}
              style={{ width: '100%', border: 'none', textAlign: 'left' }}
            >
              <span>📊</span>
              <span>Overview</span>
            </button>
          </li>
          <li>
            <button
              type="button"
              className={`educator-nav-item ${activeTab === 'learners' ? 'active' : ''}`}
              onClick={() => onSelectTab('learners')}
              style={{ width: '100%', border: 'none', textAlign: 'left' }}
            >
              <span>👥</span>
              <span>Learners</span>
            </button>
          </li>
          <li>
            <button
              type="button"
              className={`educator-nav-item ${activeTab === 'insights' ? 'active' : ''}`}
              onClick={() => onSelectTab('insights')}
              style={{ width: '100%', border: 'none', textAlign: 'left' }}
            >
              <span>🧭</span>
              <span>Insights & Bottlenecks</span>
            </button>
          </li>
          <li>
            <button
              type="button"
              className={`educator-nav-item ${activeTab === 'interventions' ? 'active' : ''}`}
              onClick={() => onSelectTab('interventions')}
              style={{ width: '100%', border: 'none', textAlign: 'left' }}
            >
              <span>⚖️</span>
              <span>Interventions</span>
            </button>
          </li>
          <li>
            <button
              type="button"
              className={`educator-nav-item ${activeTab === 'assistant' ? 'active' : ''}`}
              onClick={() => onSelectTab('assistant')}
              style={{ width: '100%', border: 'none', textAlign: 'left' }}
            >
              <span>✨</span>
              <span>AI Assistant</span>
            </button>
          </li>
          <li>
            <button
              type="button"
              className={`educator-nav-item ${activeTab === 'audit' ? 'active' : ''}`}
              onClick={() => onSelectTab('audit')}
              style={{ width: '100%', border: 'none', textAlign: 'left' }}
            >
              <span>📜</span>
              <span>Audit Trail</span>
            </button>
          </li>
        </ul>

        {/* Authenticated Educator Profile (No role switching permitted) */}
        <div className="educator-sidebar-footer">
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--surface-paper)' }}>
              {currentTeacher.name}
            </span>
            <span style={{ fontSize: '11px', color: 'var(--sutra-taupe)' }}>
              Dept Lead &bull; {currentTeacher.id}
            </span>
          </div>
          <button
            type="button"
            className="btn-ghost"
            style={{
              color: 'var(--sutra-linen)',
              fontSize: '12px',
              padding: '4px 8px',
              border: '1px solid rgba(225, 212, 194, 0.2)',
            }}
            onClick={onSignOut}
            title="Sign out of educator console"
          >
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Workspace Area */}
      <main className="educator-main-area" role="main" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <div style={{ flex: 1 }}>{children}</div>
        <footer
          style={{
            borderTop: '1px solid var(--border-subtle)',
            padding: 'var(--space-4) var(--space-6)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: 'var(--space-2)',
            marginTop: 'var(--space-8)',
            fontSize: '11px',
            color: 'var(--text-muted)',
          }}
        >
          <span>SUTRA LEARN &bull; Educator Intelligence Console</span>
          <DeveloperSignature />
        </footer>
      </main>
    </div>
  );
}

