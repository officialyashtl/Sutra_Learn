import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallbackTitle?: string;
  onReset?: () => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('[SUTRA UI ErrorBoundary] Caught render exception:', error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null });
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div
          className="editorial-card"
          style={{
            maxWidth: 'var(--reading-width, 680px)',
            margin: 'var(--space-8, 32px) auto',
            padding: 'var(--space-8, 32px)',
            backgroundColor: 'var(--surface-white, #ffffff)',
            borderLeft: '4px solid var(--feedback-error, #D32F2F)',
          }}
        >
          <div className="editorial-kicker" style={{ color: 'var(--feedback-error, #D32F2F)' }}>
            RECOVERY &bull; INTERFACE SHIELD
          </div>
          <h2
            className="serif-title"
            style={{
              fontSize: '22px',
              color: 'var(--sutra-espresso, #291C0E)',
              margin: 'var(--space-2, 8px) 0 var(--space-3, 12px) 0',
            }}
          >
            {this.props.fallbackTitle || 'Unable to display view component'}
          </h2>
          <p style={{ color: 'var(--text-secondary, #5C4E44)', fontSize: '14px', lineHeight: 1.5, margin: '0 0 var(--space-6, 24px) 0' }}>
            A rendering issue occurred while displaying this section. Your progress and assessment data remain safely preserved on the server.
          </p>
          <div style={{ display: 'flex', gap: 'var(--space-3, 12px)' }}>
            <button
              type="button"
              className="btn-primary"
              onClick={this.handleReset}
              style={{ padding: '8px 18px', fontSize: '14px' }}
            >
              Retry Display
            </button>
            <button
              type="button"
              className="btn-secondary"
              onClick={() => {
                this.setState({ hasError: false, error: null });
                window.location.reload();
              }}
              style={{ padding: '8px 18px', fontSize: '14px' }}
            >
              Refresh Application
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
