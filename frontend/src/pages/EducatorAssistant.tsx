import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import type { Learner, EducatorAnalysisResponse } from '../types';

interface EducatorAssistantProps {
  currentTeacher: Learner;
  authToken?: string | null;
  apiBaseUrl?: string;
  onNavigateToInterventions: () => void;
  onInspectLearner?: (learnerId: string) => void;
}

const PRESET_QUERIES = [
  'Identify students requiring immediate prerequisite review in linear equations.',
  'Analyze common misconception patterns across our Class 8 cohort.',
  'What targeted intervention strategies will address inverse operation confusion?',
  'Summarize recent assessment attempts and overall cohort readiness.',
];

export function EducatorAssistant({
  currentTeacher,
  authToken,
  apiBaseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  onNavigateToInterventions,
  onInspectLearner,
}: EducatorAssistantProps) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<EducatorAnalysisResponse | null>(null);
  const [quickInsights, setQuickInsights] = useState<{
    total_learners: number;
    struggling_learner_count: number;
    low_accuracy_concept_count: number;
    low_accuracy_concepts: any[];
    struggling_learners: any[];
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [aiStatus, setAiStatus] = useState<{ label: string; color: string; model?: string }>({
    label: 'CHECKING AI INFRASTRUCTURE',
    color: '#8A7A68'
  });

  // Fetch quick diagnostic highlights on mount
  useEffect(() => {
    let isMounted = true;
    async function loadQuickInsights() {
      if (!authToken) return;
      try {
        const res = await fetch(`${apiBaseUrl}/api/v1/teacher/assistant/insights`, {
          headers: { Authorization: `Bearer ${authToken}` },
        });
        if (res.ok) {
          const data = await res.json();
          if (isMounted) {
            setQuickInsights(data);
          }
        }
      } catch (err) {
        console.warn('Failed to load educator insights:', err);
      }
    }
    void loadQuickInsights();
    return () => {
      isMounted = false;
    };
  }, [authToken, apiBaseUrl]);

  useEffect(() => {
    let isMounted = true;
    async function loadHealth() {
      try {
        const res = await fetch(`${apiBaseUrl}/api/v1/ai/health`);
        if (res.ok) {
          const data = await res.json();
          if (!isMounted) return;
          if (data.offline_mode) {
            setAiStatus({ label: 'OFFLINE MODE', color: '#6E473B' });
          } else {
            const gemini = data.providers?.find((p: { provider_id: string; health_status: string }) => p.provider_id === 'gemini');
            const qwen = data.providers?.find((p: { provider_id: string; health_status: string }) => p.provider_id === 'ollama_qwen');
            const gemma = data.providers?.find((p: { provider_id: string; health_status: string }) => p.provider_id === 'ollama_gemma');

            if (gemini?.health_status === 'AVAILABLE') {
              setAiStatus({ label: 'GEMINI ACTIVE', color: '#2E7D32', model: gemini.model_id });
            } else if (qwen?.health_status === 'AVAILABLE') {
              setAiStatus({ label: 'QWEN 3.5 4B ACTIVE', color: '#1565C0', model: qwen.model_id });
            } else if (gemma?.health_status === 'AVAILABLE') {
              setAiStatus({ label: 'GEMMA 4 E2B ACTIVE', color: '#6A1B9A', model: gemma.model_id });
            } else {
              setAiStatus({ label: 'DETERMINISTIC FALLBACK', color: '#8D6E63', model: 'NCERT Rules' });
            }
          }
        }
      } catch {
        if (isMounted) {
          setAiStatus({ label: 'DETERMINISTIC FALLBACK', color: '#8D6E63', model: 'Offline Curriculum' });
        }
      }
    }
    void loadHealth();
    return () => {
      isMounted = false;
    };
  }, [apiBaseUrl]);

  const handleRunAnalysis = async (customQuery?: string) => {
    const text = customQuery || query.trim();
    if (!text || loading || !authToken) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/teacher/assistant/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authToken}`,
        },
        body: JSON.stringify({ query: text }),
      });

      if (!res.ok) {
        const errJson = await res.json();
        throw new Error(errJson.detail || 'Analysis generation failed.');
      }

      const data = await res.json();
      setAnalysisResult(data);
    } catch (err: any) {
      setError(err.message || 'Error communicating with Educator Intelligence service.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    void handleRunAnalysis();
  };

  return (
    <div style={{ maxWidth: 'var(--educator-max-width)', margin: '0 auto' }}>
      {/* Editorial Workspace Header */}
      <header className="card-header-line" style={{ display: 'block', marginBottom: 'var(--space-6)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
          <div>
            <div className="editorial-kicker">EDUCATOR INTELLIGENCE &bull; COHORT SYNTHESIS</div>
            <h1 className="serif-display" style={{ fontSize: '32px', color: 'var(--sutra-espresso)', marginTop: '4px' }}>
              SUTRA AI Educator Intelligence
            </h1>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '6px' }}>
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '3px 8px',
                borderRadius: 'var(--radius-pill)',
                backgroundColor: 'var(--surface-warm)',
                border: '1px solid var(--border-subtle)',
                fontSize: '10px',
                fontWeight: 700,
                color: 'var(--sutra-espresso)',
                letterSpacing: '0.04em',
              }}
              title={aiStatus.model ? `Active Model: ${aiStatus.model}` : undefined}
            >
              <span
                style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  backgroundColor: aiStatus.color,
                  display: 'inline-block',
                }}
              />
              <span>{aiStatus.label}</span>
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', textAlign: 'right' }}>
              Faculty: <strong style={{ color: 'var(--sutra-mocha)' }}>{currentTeacher.name}</strong> ({currentTeacher.id})
            </div>
          </div>
        </div>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '4px', maxWidth: '680px' }}>
          Evidence-grounded classroom analysis distinguishing verified database facts, calculated friction statistics,
          and teacher-approved pedagogical interventions.
        </p>
      </header>

      {/* Top Highlight Summary Tiles */}
      {quickInsights && (
        <>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(min(220px, 100%), 1fr))',
              gap: 'var(--space-4)',
              marginBottom: 'var(--space-4)',
            }}
          >
            <div className="metric-tile">
              <div className="metric-num">{quickInsights.total_learners}</div>
              <div className="metric-label">Enrolled Learners</div>
            </div>
            <div className="metric-tile" style={{ borderLeft: '3px solid var(--feedback-warning)' }}>
              <div className="metric-num" style={{ color: 'var(--feedback-warning)' }}>
                {quickInsights.struggling_learner_count}
              </div>
              <div className="metric-label">Learners Requiring Review</div>
            </div>
            <div className="metric-tile" style={{ borderLeft: '3px solid var(--feedback-error)' }}>
              <div className="metric-num" style={{ color: 'var(--sutra-mocha)' }}>
                {quickInsights.low_accuracy_concept_count}
              </div>
              <div className="metric-label">Friction Concepts (&lt;70% Acc)</div>
            </div>
          </div>

          {quickInsights.struggling_learners && quickInsights.struggling_learners.length > 0 && onInspectLearner && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: 'var(--space-6)', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-secondary)' }}>Focus Profiles:</span>
              {quickInsights.struggling_learners.map((sl: any) => (
                <button
                  key={sl.learner_id}
                  type="button"
                  className="btn-ghost"
                  style={{ fontSize: '11px', padding: '2px 8px', border: '1px solid var(--border-default)' }}
                  onClick={() => onInspectLearner(sl.learner_id)}
                >
                  🔍 {sl.name} ({sl.learner_id})
                </button>
              ))}
            </div>
          )}
        </>
      )}

      {/* Inquiry Formulation Card */}
      <div className="editorial-card" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-6)' }}>
        <h3 className="serif-title" style={{ fontSize: '18px', color: 'var(--sutra-espresso)', marginBottom: 'var(--space-3)' }}>
          Formulate Diagnostic Classroom Inquiry
        </h3>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: 'var(--space-4)' }}>
          Select a high-yield inquiry below or write a custom analytical question grounded in your cohort data:
        </p>

        {/* Preset Query Chips */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: 'var(--space-4)' }}>
          {PRESET_QUERIES.map((pq, idx) => (
            <button
              key={idx}
              type="button"
              className="btn-secondary"
              style={{ fontSize: '12px', height: 'auto', padding: '6px 12px', textAlign: 'left' }}
              onClick={() => {
                setQuery(pq);
                void handleRunAnalysis(pq);
              }}
            >
              💡 {pq}
            </button>
          ))}
        </div>

        {/* Custom Query Input */}
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="E.g., Analyze Aarav Sharma's struggle with negative distribution signs..."
            style={{
              flex: 1,
              padding: '10px 14px',
              fontSize: '13px',
              border: '1px solid var(--border-default)',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--surface-paper)',
            }}
          />
          <button
            type="submit"
            className="btn-primary"
            disabled={loading || !query.trim()}
          >
            {loading ? 'Synthesizing...' : 'Run Intelligence Query &rarr;'}
          </button>
        </form>

        {error && (
          <div
            style={{
              marginTop: 'var(--space-4)',
              padding: 'var(--space-3)',
              backgroundColor: 'var(--feedback-error-bg)',
              color: 'var(--feedback-error)',
              borderRadius: 'var(--radius-sm)',
              fontSize: '13px',
            }}
          >
            ⚠️ {error}
          </div>
        )}
      </div>

      {/* Analysis Results Canvas: Strict Evidence Hierarchy */}
      {analysisResult && (
        <div
          className="editorial-card"
          style={{
            padding: 'var(--space-8)',
            backgroundColor: 'var(--surface-white)',
            borderLeft: '4px solid var(--sutra-mocha)',
            marginBottom: 'var(--space-8)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-4)' }}>
            <div>
              <span className="editorial-kicker">ANALYSIS RESULTS &bull; EVIDENCE HIERARCHY</span>
              <h2 className="serif-title" style={{ fontSize: '24px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
                Classroom Intelligence Synthesis
              </h2>
            </div>
            <span
              style={{
                fontSize: '11px',
                fontWeight: 700,
                textTransform: 'uppercase',
                backgroundColor: 'var(--surface-warm)',
                color: 'var(--sutra-espresso)',
                border: '1px solid var(--border-default)',
                padding: '4px 8px',
                borderRadius: 'var(--radius-xs)',
              }}
            >
              Verified NCERT Analytics
            </span>
          </div>

          {/* Section 1: Verified Database Facts */}
          {analysisResult.observations && analysisResult.observations.length > 0 && (
            <div style={{ marginBottom: 'var(--space-6)' }}>
              <h3 style={{ fontSize: '13px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--sutra-mocha)', letterSpacing: '0.06em', marginBottom: 'var(--space-2)' }}>
                1. Verified Database Evidence
              </h3>
              <div
                style={{
                  backgroundColor: 'var(--surface-paper)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: 'var(--space-4)',
                }}
              >
                <ul style={{ paddingLeft: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {analysisResult.observations.map((obs, idx) => (
                    <li key={idx} style={{ fontSize: '13px', color: 'var(--text-primary)', lineHeight: 1.5 }}>
                      {obs}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Section 2: Detailed Synthesis */}
          <div style={{ marginBottom: 'var(--space-6)' }}>
            <h3 style={{ fontSize: '13px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--sutra-mocha)', letterSpacing: '0.06em', marginBottom: 'var(--space-2)' }}>
              2. Analytical Interpretation & Diagnosis
            </h3>
            <div
              style={{
                padding: 'var(--space-5)',
                backgroundColor: 'var(--surface-warm)',
                border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-md)',
                fontSize: '14px',
                lineHeight: 1.6,
                color: 'var(--text-primary)',
                whiteSpace: 'pre-wrap',
              }}
            >
              {analysisResult.summary}
            </div>
          </div>

          {/* Section 3: Recommended Differentiated Interventions */}
          {analysisResult.recommended_actions && analysisResult.recommended_actions.length > 0 && (
            <div style={{ marginBottom: 'var(--space-6)' }}>
              <h3 style={{ fontSize: '13px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--sutra-mocha)', letterSpacing: '0.06em', marginBottom: 'var(--space-2)' }}>
                3. Recommended Pedagogical Actions (Human-in-the-Loop)
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {analysisResult.recommended_actions.map((act, idx) => (
                  <div
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: 'var(--space-3) var(--space-4)',
                      backgroundColor: 'var(--surface-paper)',
                      border: '1px solid var(--border-default)',
                      borderRadius: 'var(--radius-sm)',
                    }}
                  >
                    <span style={{ fontSize: '13px', color: 'var(--text-primary)' }}>
                      <strong>Action {idx + 1}:</strong> {act}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Human-in-the-Loop Action Trigger */}
          <div
            style={{
              paddingTop: 'var(--space-5)',
              borderTop: '1px solid var(--border-subtle)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: 'var(--space-3)',
            }}
          >
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              🔒 Consequential changes require explicit faculty confirmation & substantive pedagogical rationale.
            </span>
            <button
              type="button"
              className="btn-primary"
              onClick={onNavigateToInterventions}
            >
              Open Interventions Workspace &rarr;
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
