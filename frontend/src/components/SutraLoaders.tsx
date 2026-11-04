import React from 'react';

/**
 * SUTRA LEARN — Premium Loading & Shimmer System
 * Design System: Earthbound Editorial (Warm Ivory, Deep Espresso, Muted Mocha, Restrained Gold)
 * Implements full accessibility with ARIA live regions and prefers-reduced-motion support.
 */

export interface SutraLoaderProps {
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  className?: string;
}

/**
 * Centralized SUTRA emblem loader.
 */
export const SutraLoader: React.FC<SutraLoaderProps> = ({
  size = 'md',
  label,
  className = '',
}) => {
  const dimensions = size === 'sm' ? 24 : size === 'lg' ? 44 : 34;
  const fontSize = size === 'sm' ? 12 : size === 'lg' ? 22 : 17;

  return (
    <div
      role="status"
      aria-live="polite"
      className={`inline-flex items-center gap-3 ${className}`}
      style={{ display: 'inline-flex', alignItems: 'center', gap: '10px' }}
    >
      <div
        className="sutra-emblem-animated"
        style={{
          width: `${dimensions}px`,
          height: `${dimensions}px`,
          fontSize: `${fontSize}px`,
        }}
        aria-hidden="true"
      >
        S
      </div>
      {label && (
        <span
          style={{
            fontFamily: 'var(--font-sans)',
            fontSize: size === 'sm' ? '12px' : '13px',
            color: 'var(--sutra-mocha)',
            fontWeight: 500,
          }}
        >
          {label}
        </span>
      )}
    </div>
  );
};

export interface SutraPageLoaderProps {
  message?: string;
  subMessage?: string;
}

/**
 * Full container / section loading experience with warm ivory backdrop.
 */
export const SutraPageLoader: React.FC<SutraPageLoaderProps> = ({
  message = 'Preparing your new learning space...',
  subMessage = 'Aligning curriculum knowledge and conversational memory',
}) => {
  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 'var(--space-12) var(--space-6)',
        backgroundColor: 'var(--surface-paper)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--border-subtle)',
        minHeight: '280px',
        textAlign: 'center',
      }}
    >
      <div
        className="sutra-emblem-animated"
        style={{
          width: '46px',
          height: '46px',
          fontSize: '24px',
          marginBottom: 'var(--space-4)',
        }}
        aria-hidden="true"
      >
        S
      </div>
      <h4
        className="serif-title"
        style={{
          fontSize: '18px',
          color: 'var(--sutra-espresso)',
          margin: '0 0 var(--space-2) 0',
          fontWeight: 600,
        }}
      >
        {message}
      </h4>
      {subMessage && (
        <p
          style={{
            fontSize: '13px',
            color: 'var(--text-secondary)',
            margin: 0,
            maxWidth: '380px',
            lineHeight: 1.5,
          }}
        >
          {subMessage}
        </p>
      )}
    </div>
  );
};

export interface SutraButtonLoaderProps {
  label?: string;
}

/**
 * Compact inline spinner for buttons.
 */
export const SutraButtonLoader: React.FC<SutraButtonLoaderProps> = ({ label }) => {
  return (
    <span
      role="status"
      aria-live="polite"
      style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
    >
      <span
        className="sutra-spinner-ring"
        style={{
          width: '13px',
          height: '13px',
          borderWidth: '2px',
          display: 'inline-block',
        }}
        aria-hidden="true"
      />
      {label && <span>{label}</span>}
    </span>
  );
};

export interface SutraSkeletonProps {
  width?: string | number;
  height?: string | number;
  borderRadius?: string;
  style?: React.CSSProperties;
  className?: string;
}

/**
 * Atomic skeleton block with Earthbound Editorial shimmer.
 */
export const SutraSkeleton: React.FC<SutraSkeletonProps> = ({
  width = '100%',
  height = '16px',
  borderRadius = 'var(--radius-xs)',
  style = {},
  className = '',
}) => {
  return (
    <div
      className={`sutra-skeleton-shimmer ${className}`}
      style={{
        width: typeof width === 'number' ? `${width}px` : width,
        height: typeof height === 'number' ? `${height}px` : height,
        borderRadius,
        ...style,
      }}
      aria-hidden="true"
    />
  );
};

/**
 * Dedicated chat stream thinking loader:
 * "SUTRA AI is thinking..."
 */
export const SutraChatLoader: React.FC = () => {
  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: 'flex',
        alignItems: 'flex-start',
        gap: 'var(--space-3)',
        padding: 'var(--space-4)',
        backgroundColor: 'var(--surface-white)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-sm)',
        maxWidth: '85%',
        alignSelf: 'flex-start',
        boxShadow: '0 1px 3px rgba(41, 28, 14, 0.05)',
      }}
    >
      <div
        style={{
          width: '26px',
          height: '26px',
          backgroundColor: 'var(--sutra-espresso)',
          color: 'var(--surface-paper)',
          borderRadius: 'var(--radius-xs)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'var(--font-display)',
          fontSize: '13px',
          fontWeight: 700,
          flexShrink: 0,
        }}
        aria-hidden="true"
      >
        S
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span
            style={{
              fontSize: '12px',
              fontFamily: 'var(--font-display)',
              fontWeight: 600,
              color: 'var(--sutra-espresso)',
            }}
          >
            SUTRA AI
          </span>
          <span
            style={{
              fontSize: '11px',
              color: 'var(--text-muted)',
              fontStyle: 'italic',
            }}
          >
            is thinking...
          </span>
          <span
            style={{ display: 'inline-flex', gap: '3px', marginLeft: '2px' }}
            aria-hidden="true"
          >
            <span
              className="sutra-dot-1"
              style={{
                width: '4px',
                height: '4px',
                borderRadius: '50%',
                backgroundColor: 'var(--sutra-mocha)',
                display: 'inline-block',
              }}
            />
            <span
              className="sutra-dot-2"
              style={{
                width: '4px',
                height: '4px',
                borderRadius: '50%',
                backgroundColor: 'var(--sutra-mocha)',
                display: 'inline-block',
              }}
            />
            <span
              className="sutra-dot-3"
              style={{
                width: '4px',
                height: '4px',
                borderRadius: '50%',
                backgroundColor: 'var(--sutra-mocha)',
                display: 'inline-block',
              }}
            />
          </span>
        </div>
        <SutraSkeleton width="180px" height="10px" borderRadius="3px" />
      </div>
    </div>
  );
};

export interface SutraSessionLoaderProps {
  state: 'loading' | 'empty' | 'error';
  onRetry?: () => void;
  onNewSession?: () => void;
}

/**
 * Past Sessions list loader & empty/error state handler.
 */
export const SutraSessionLoader: React.FC<SutraSessionLoaderProps> = ({
  state,
  onRetry,
  onNewSession,
}) => {
  if (state === 'loading') {
    return (
      <div
        role="status"
        aria-live="polite"
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '8px',
          padding: '4px 0',
        }}
      >
        {[1, 2, 3, 4].map((i) => (
          <div
            key={i}
            style={{
              padding: '10px 12px',
              borderRadius: 'var(--radius-xs)',
              border: '1px solid var(--border-subtle)',
              backgroundColor: 'var(--surface-white)',
              display: 'flex',
              flexDirection: 'column',
              gap: '6px',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <SutraSkeleton width="60px" height="12px" borderRadius="3px" />
              <SutraSkeleton width="40px" height="10px" borderRadius="2px" />
            </div>
            <SutraSkeleton width="90%" height="13px" borderRadius="3px" />
            <SutraSkeleton width="50%" height="11px" borderRadius="3px" />
          </div>
        ))}
      </div>
    );
  }

  if (state === 'error') {
    return (
      <div
        role="alert"
        style={{
          padding: 'var(--space-4)',
          textAlign: 'center',
          backgroundColor: 'var(--surface-paper)',
          borderRadius: 'var(--radius-xs)',
          border: '1px solid var(--border-subtle)',
        }}
      >
        <p style={{ fontSize: '12px', color: 'var(--sutra-mocha)', margin: '0 0 var(--space-2) 0' }}>
          Unable to connect to past sessions.
        </p>
        {onRetry && (
          <button
            type="button"
            className="btn-secondary"
            onClick={onRetry}
            style={{ fontSize: '11px', height: '26px', padding: '0 10px' }}
          >
            Retry Connection
          </button>
        )}
      </div>
    );
  }

  // Empty state
  return (
    <div
      style={{
        padding: 'var(--space-6) var(--space-3)',
        textAlign: 'center',
        border: '1px dashed var(--border-strong)',
        borderRadius: 'var(--radius-xs)',
        backgroundColor: 'var(--surface-paper)',
      }}
    >
      <div style={{ fontSize: '20px', marginBottom: '6px' }}>📜</div>
      <p
        style={{
          fontSize: '12px',
          color: 'var(--sutra-espresso)',
          fontWeight: 600,
          margin: '0 0 4px 0',
        }}
      >
        No past sessions yet
      </p>
      <p style={{ fontSize: '11px', color: 'var(--text-secondary)', margin: '0 0 10px 0', lineHeight: 1.4 }}>
        Your learning conversations with SUTRA AI will be preserved here.
      </p>
      {onNewSession && (
        <button
          type="button"
          className="btn-secondary"
          onClick={onNewSession}
          style={{ fontSize: '11px', height: '28px', padding: '0 10px' }}
        >
          + Start First Session
        </button>
      )}
    </div>
  );
};

export interface SutraInlineLoaderProps {
  label?: string;
}

/**
 * Compact inline loader for session switching or background sync.
 */
export const SutraInlineLoader: React.FC<SutraInlineLoaderProps> = ({
  label = 'Updating...',
}) => {
  return (
    <span
      role="status"
      aria-live="polite"
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        fontSize: '11px',
        color: 'var(--sutra-mocha)',
        fontWeight: 500,
      }}
    >
      <span
        className="sutra-spinner-ring"
        style={{
          width: '11px',
          height: '11px',
          borderWidth: '2px',
          display: 'inline-block',
        }}
        aria-hidden="true"
      />
      <span>{label}</span>
    </span>
  );
};
