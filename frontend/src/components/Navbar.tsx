import { useState, useEffect, useCallback } from 'react';
import type { Learner } from '../types';
import { getPendingAttempts } from '../offline/db';
import { syncPendingAttempts } from '../offline/sync';

interface NavbarProps {
  currentLearner: Learner;
  allLearners: Learner[];
  onSelectLearner: (learner: Learner) => void;
  activeView: 'student' | 'teacher';
  onSelectView: (view: 'student' | 'teacher') => void;
  apiBaseUrl: string;
  authToken?: string | null;
  onHomeClick?: () => void;
  onNavigatePortalGateway?: () => void;
}

export function Navbar({
  currentLearner,
  allLearners,
  onSelectLearner,
  activeView,
  onSelectView,
  apiBaseUrl,
  authToken,
  onHomeClick,
  onNavigatePortalGateway,
}: NavbarProps) {
  const [isOnline, setIsOnline] = useState<boolean>(navigator.onLine);
  const [pendingCount, setPendingCount] = useState<number>(0);
  const [syncing, setSyncing] = useState<boolean>(false);

  const checkPending = useCallback(async () => {
    const list = await getPendingAttempts();
    setPendingCount(list.length);
  }, []);

  const triggerSync = useCallback(async () => {
    setSyncing(true);
    await syncPendingAttempts(apiBaseUrl, authToken);
    await checkPending();
    setSyncing(false);
  }, [apiBaseUrl, authToken, checkPending]);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      void triggerSync();
    };
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    const timeout = setTimeout(() => {
      void checkPending();
    }, 0);

    const interval = setInterval(() => {
      void checkPending();
    }, 5000);

    return () => {
      clearTimeout(timeout);
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      clearInterval(interval);
    };
  }, [checkPending, triggerSync]);

  return (
    <header className="navbar" role="banner">
      <div
        className="brand-section"
        onClick={onHomeClick}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            onHomeClick?.();
          }
        }}
        title="SUTRA LEARN — Return to Learning Home"
      >
        <div className="brand-symbol" aria-hidden="true">
          S
        </div>
        <div className="brand-meta">
          <span className="brand-name">
            {activeView === 'teacher' ? 'SUTRA / EDUCATOR' : 'SUTRA / LEARNER'}
          </span>
          <span className="brand-subtitle">
            {activeView === 'teacher' ? 'Faculty & Clinical Oversight' : 'Adaptive Mathematics • Class 8'}
          </span>
        </div>
      </div>

      <div className="nav-controls">
        {onNavigatePortalGateway && (
          <button
            type="button"
            className="btn-ghost"
            style={{
              fontSize: '12px',
              padding: '4px 10px',
              border: '1px solid var(--color-subtle-border)',
              minHeight: '32px',
              fontWeight: 600,
            }}
            onClick={onNavigatePortalGateway}
            title="Switch between Learner Portal and Educator Workspace"
          >
            ⇄ Portals
          </button>
        )}

        {/* Offline & Sync Status Pill */}
        <div
          className="sync-status-indicator"
          title={isOnline ? 'Online: Live connection with server' : 'Offline: Attempts will queue locally'}
        >
          <span className={`sync-dot ${isOnline ? '' : 'offline'}`} aria-hidden="true" />
          <span>{isOnline ? 'Online' : 'Offline'}</span>
          {pendingCount > 0 && (
            <button
              type="button"
              className="sync-action-btn"
              onClick={() => void triggerSync()}
              disabled={syncing || !isOnline}
              title="Synchronize offline attempts with database"
            >
              {syncing ? 'Syncing...' : `Sync (${pendingCount})`}
            </button>
          )}
        </div>

        {/* Persona Selector */}
        <div className="persona-selector">
          <label htmlFor="learner-picker" className="persona-label">
            Active User:
          </label>
          <select
            id="learner-picker"
            className="persona-select"
            value={currentLearner.id}
            onChange={(e) => {
              const selected = allLearners.find((l) => l.id === e.target.value);
              if (selected) {
                onSelectLearner(selected);
                if (selected.role === 'teacher') {
                  onSelectView('teacher');
                } else if (activeView === 'teacher' && selected.role === 'student') {
                  onSelectView('student');
                }
              }
            }}
          >
            {allLearners.map((l) => (
              <option key={l.id} value={l.id}>
                {l.name} ({l.role})
              </option>
            ))}
          </select>
        </div>

        {/* Role Mode View Toggle */}
        <div className="view-mode-tabs" role="tablist">
          <button
            type="button"
            role="tab"
            aria-selected={activeView === 'student'}
            className={`view-mode-tab ${activeView === 'student' ? 'active' : ''}`}
            onClick={() => onSelectView('student')}
          >
            Student View
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={activeView === 'teacher'}
            className={`view-mode-tab ${activeView === 'teacher' ? 'active' : ''}`}
            onClick={() => onSelectView('teacher')}
          >
            Teacher Workspace
          </button>
        </div>
      </div>
    </header>
  );
}
