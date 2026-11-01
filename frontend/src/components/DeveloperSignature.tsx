import type { CSSProperties } from 'react';

interface DeveloperSignatureProps {
  style?: CSSProperties;
}

export function DeveloperSignature({ style }: DeveloperSignatureProps) {
  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        fontSize: '11px',
        color: 'var(--text-muted)',
        fontFamily: 'inherit',
        lineHeight: 1.4,
        ...style,
      }}
      aria-label="Designed & Developed by YASH TL"
      title="Designed & Developed by YASH TL"
    >
      {/* Subtle Outlined YT Monogram Stamp */}
      <span
        style={{
          width: '18px',
          height: '18px',
          borderRadius: '3px',
          border: '1px solid var(--border-default)',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'var(--font-mono)',
          fontSize: '8.5px',
          fontWeight: 700,
          color: 'var(--sutra-mocha)',
          backgroundColor: 'var(--surface-paper)',
          letterSpacing: '0.04em',
          lineHeight: 1,
          flexShrink: 0,
        }}
        aria-hidden="true"
      >
        YT
      </span>

      {/* Credit Text in Existing Footer Style */}
      <span>
        Designed &amp; Developed by{' '}
        <strong style={{ color: 'var(--sutra-espresso)', fontWeight: 600 }}>
          Yash TL
        </strong>
      </span>
    </div>
  );
}
