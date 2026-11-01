import type { Learner } from '../types';

interface StudentHeaderProps {
  learner: Learner;
  activeTab: 'home' | 'pathway' | 'progress' | 'insights' | 'tutor';
  onSelectTab: (tab: 'home' | 'pathway' | 'progress' | 'insights' | 'tutor') => void;
  onSignOut: () => void;
}

export function StudentHeader({
  learner,
  activeTab,
  onSelectTab,
  onSignOut,
}: StudentHeaderProps) {
  return (
    <header className="student-header" role="banner">
      {/* Brand Identification */}
      <div
        className="student-brand"
        onClick={() => onSelectTab('home')}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            onSelectTab('home');
          }
        }}
        title="SUTRA LEARN — Student Space"
      >
        <div className="brand-symbol-mark" aria-hidden="true">
          S
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline' }}>
          <span className="brand-wordmark">SUTRA</span>
          <span className="brand-subline">STUDENT</span>
        </div>
      </div>

      {/* Main Student Navigation */}
      <nav className="student-nav-tabs" aria-label="Student Main Navigation">
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => onSelectTab('home')}
          aria-current={activeTab === 'home' ? 'page' : undefined}
        >
          Home
        </button>
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'pathway' ? 'active' : ''}`}
          onClick={() => onSelectTab('pathway')}
          aria-current={activeTab === 'pathway' ? 'page' : undefined}
        >
          My Learning
        </button>
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'progress' ? 'active' : ''}`}
          onClick={() => onSelectTab('progress')}
          aria-current={activeTab === 'progress' ? 'page' : undefined}
        >
          Progress
        </button>
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'insights' ? 'active' : ''}`}
          onClick={() => onSelectTab('insights')}
          aria-current={activeTab === 'insights' ? 'page' : undefined}
        >
          Insights
        </button>
        <button
          type="button"
          className={`student-nav-tab ${activeTab === 'tutor' ? 'active' : ''}`}
          onClick={() => onSelectTab('tutor')}
          aria-current={activeTab === 'tutor' ? 'page' : undefined}
          style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
        >
          <span style={{ fontSize: '13px' }}>✨</span>
          <span>AI Tutor</span>
        </button>
      </nav>

      {/* Authenticated Profile & Sign Out (No role switching permitted) */}
      <div className="student-profile-area">
        <div className="student-profile-pill">
          <span style={{ color: 'var(--sutra-mocha)' }}>●</span>
          <span>{learner.name}</span>
          <span style={{ color: 'var(--text-muted)', fontSize: '11px' }}>Class {learner.grade}</span>
        </div>
        <button
          type="button"
          className="btn-ghost"
          style={{ fontSize: '12px', padding: '4px 10px', height: '32px' }}
          onClick={onSignOut}
          title="Sign out of student portal"
        >
          Sign Out
        </button>
      </div>
    </header>
  );
}

