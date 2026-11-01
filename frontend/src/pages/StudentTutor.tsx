import { useState, useEffect, useRef, useCallback } from 'react';
import type { FormEvent } from 'react';
import type { Concept, AIMessage, AIConversation } from '../types';

interface StudentTutorProps {
  currentStudentId: string;
  concepts: Concept[];
  initialConceptId?: string;
  authToken?: string | null;
  apiBaseUrl?: string;
  onNavigateToPathway: () => void;
  onNavigateToLesson: (conceptId: string) => void;
}

type TutorMode =
  | 'guided_learning'
  | 'explain_concept'
  | 'worked_example'
  | 'practice'
  | 'check_my_work'
  | 'quick_revision'
  | 'prerequisite_support';

const TUTOR_MODES: { id: TutorMode; label: string; icon: string; desc: string }[] = [
  { id: 'guided_learning', label: 'Guided Learning', icon: '🧭', desc: 'Step-by-step Socratic inquiry' },
  { id: 'worked_example', label: 'Worked Example', icon: '📝', desc: 'Full step-by-step solution walkthrough' },
  { id: 'practice', label: 'Practice Question', icon: '🎯', desc: 'Diagnostic problem with feedback' },
  { id: 'check_my_work', label: 'Check My Work', icon: '🔍', desc: 'Pinpoint arithmetic and sign errors' },
  { id: 'quick_revision', label: 'Quick Revision', icon: '⚡', desc: 'Core principles and definitions' },
  { id: 'prerequisite_support', label: 'Prerequisites', icon: '🧱', desc: 'Review foundational knowledge' },
];

const SUGGESTED_PROMPTS = [
  'How do I isolate the variable in 2x + 5 = 15?',
  'Why do negative signs become positive when subtracted?',
  'Show me a complete worked solution for two-step equations.',
  'Give me a diagnostic practice question on balance principles.',
];

export function StudentTutor({
  currentStudentId,
  concepts,
  initialConceptId,
  authToken,
  apiBaseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  onNavigateToPathway,
  onNavigateToLesson,
}: StudentTutorProps) {
  const [selectedConceptId, setSelectedConceptId] = useState<string>(
    initialConceptId || concepts[0]?.id || 'MATH-C01'
  );
  const [activeMode, setActiveMode] = useState<TutorMode>('guided_learning');
  const [conversations, setConversations] = useState<AIConversation[]>([]);
  const [conversationsLoading, setConversationsLoading] = useState(!!authToken);
  const [conversationsError, setConversationsError] = useState<string | null>(null);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<AIMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [revealedHints, setRevealedHints] = useState<Record<string, boolean>>({});
  const [copyFeedback, setCopyFeedback] = useState<string | null>(null);
  const [aiStatus, setAiStatus] = useState<{ label: string; color: string; model?: string }>({
    label: 'CHECKING AI INFRASTRUCTURE',
    color: '#8A7A68'
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const activeConcept = concepts.find((c) => c.id === selectedConceptId) || concepts[0];

  const loadConversationDetail = useCallback(
    async (convId: string) => {
      if (!authToken) return;
      try {
        const res = await fetch(`${apiBaseUrl}/api/v1/tutor/conversations/${convId}`, {
          headers: { Authorization: `Bearer ${authToken}` },
        });
        if (res.ok) {
          const data = await res.json();
          setActiveConversationId(convId);
          setMessages(data.messages || []);
          if (data.conversation?.concept_id) {
            setSelectedConceptId(data.conversation.concept_id);
          }
        }
      } catch (err) {
        console.warn('Failed to load conversation detail:', err);
      }
    },
    [authToken, apiBaseUrl]
  );

  const loadConversations = useCallback(
    async (selectFirstIfAvailable = false) => {
      if (!authToken) return;
      setConversationsError(null);
      try {
        const res = await fetch(`${apiBaseUrl}/api/v1/tutor/conversations`, {
          headers: { Authorization: `Bearer ${authToken}` },
        });
        if (res.ok) {
          const data = await res.json();
          setConversations(data);
          if (selectFirstIfAvailable && data.length > 0 && !activeConversationId) {
            void loadConversationDetail(data[0].id);
          }
        } else {
          setConversationsError('Unable to load past sessions.');
        }
      } catch (err) {
        console.warn('Failed to load conversations:', err);
        setConversationsError('Network error connecting to session history.');
      } finally {
        setConversationsLoading(false);
      }
    },
    [authToken, apiBaseUrl, loadConversationDetail, activeConversationId]
  );

  // Load existing conversations on mount
  useEffect(() => {
    let isMounted = true;
    async function fetchOnMount() {
      if (!authToken) {
        setConversationsLoading(false);
        return;
      }
      try {
        const res = await fetch(`${apiBaseUrl}/api/v1/tutor/conversations`, {
          headers: { Authorization: `Bearer ${authToken}` },
        });
        if (res.ok) {
          const data = await res.json();
          if (isMounted) {
            setConversations(data);
            if (data.length > 0 && !activeConversationId) {
              void loadConversationDetail(data[0].id);
            }
          }
        } else if (isMounted) {
          setConversationsError('Unable to load past sessions.');
        }
      } catch (err) {
        console.warn('Failed to load conversations:', err);
        if (isMounted) {
          setConversationsError('Network error connecting to session history.');
        }
      } finally {
        if (isMounted) {
          setConversationsLoading(false);
        }
      }
    }
    void fetchOnMount();
    return () => {
      isMounted = false;
    };
  }, [authToken, apiBaseUrl, loadConversationDetail, activeConversationId]);

  // AI Provider Infrastructure Health Check
  useEffect(() => {
    let isMounted = true;
    async function checkHealth() {
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
    void checkHealth();
    return () => {
      isMounted = false;
    };
  }, [apiBaseUrl]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleStartNewSession = () => {
    setActiveConversationId(null);
    setMessages([]);
    setInputText('');
    setTimeout(() => {
      textareaRef.current?.focus();
    }, 50);
  };

  const handleSendMessage = async (e?: FormEvent) => {
    if (e) e.preventDefault();
    const text = inputText.trim();
    if (!text || loading) return;

    // Optimistically append user message
    const tempUserMsg: AIMessage = {
      id: `temp-${Date.now()}`,
      conversation_id: activeConversationId || 'new',
      sender_role: 'user',
      content: text,
      response_type: 'question',
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, tempUserMsg]);
    setInputText('');
    setLoading(true);

    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/tutor/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        },
        body: JSON.stringify({
          message: text,
          conversation_id: activeConversationId,
          concept_id: selectedConceptId,
          mode: activeMode,
        }),
      });

      if (!res.ok) {
        const errJson = await res.json();
        throw new Error(errJson.detail || 'Failed to receive tutor response.');
      }

      const data = await res.json();
      setActiveConversationId(data.conversation_id);

      const aiMsg: AIMessage = {
        id: data.message_id,
        conversation_id: data.conversation_id,
        sender_role: 'assistant',
        content: data.answer,
        response_type: data.response_type,
        hints: data.hints,
        concept_id: data.concept_id,
        requires_follow_up: data.requires_follow_up,
        provider_metadata: data.provider_metadata,
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, aiMsg]);

      // Refresh conversations list
      if (authToken) {
        void loadConversations(false);
      }
    } catch (err: any) {
      const errorMsg: AIMessage = {
        id: `err-${Date.now()}`,
        conversation_id: activeConversationId || 'new',
        sender_role: 'assistant',
        content: `I encountered an unexpected issue connecting to the learning engine: ${err.message}. Please try again.`,
        response_type: 'error',
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyText = (content: string, msgId: string) => {
    void navigator.clipboard.writeText(content);
    setCopyFeedback(msgId);
    setTimeout(() => setCopyFeedback(null), 2000);
  };

  const toggleHint = (msgId: string) => {
    setRevealedHints((prev) => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  return (
    <div style={{ maxWidth: '1240px', margin: '0 auto' }}>
      {/* Top Navigation & Context Bar */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 'var(--space-6)',
          flexWrap: 'wrap',
          gap: 'var(--space-3)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '13px', paddingLeft: 0 }}
            onClick={onNavigateToPathway}
          >
            &larr; Learning Pathway
          </button>
          <span style={{ color: 'var(--border-default)' }}>|</span>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '13px', color: 'var(--sutra-mocha)', fontWeight: 600 }}
            onClick={() => onNavigateToLesson(selectedConceptId)}
          >
            📖 Open {activeConcept.code} Lesson
          </button>
        </div>

        {/* AI Status Indicator & Concept Selector Dropdown */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '4px 10px',
              borderRadius: 'var(--radius-pill)',
              backgroundColor: 'var(--surface-warm)',
              border: '1px solid var(--border-subtle)',
              fontSize: '11px',
              fontWeight: 700,
              color: 'var(--sutra-espresso)',
              letterSpacing: '0.04em',
            }}
            title={aiStatus.model ? `Active Model: ${aiStatus.model}` : undefined}
          >
            <span
              style={{
                width: '7px',
                height: '7px',
                borderRadius: '50%',
                backgroundColor: aiStatus.color,
                display: 'inline-block',
              }}
            />
            <span>{aiStatus.label}</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <label htmlFor="concept-select" style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-secondary)' }}>
              TOPIC:
            </label>
            <select
              id="concept-select"
              value={selectedConceptId}
              onChange={(e) => setSelectedConceptId(e.target.value)}
              style={{
                padding: '6px 12px',
                fontSize: '13px',
                fontWeight: 600,
                color: 'var(--sutra-espresso)',
                backgroundColor: 'var(--surface-white)',
                border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-sm)',
              }}
            >
              {concepts.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.code}: {c.title}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Main Grid: Sidebar + Chat Interface */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(min(280px, 100%), 1fr))',
          gap: 'var(--space-6)',
          alignItems: 'start',
        }}
      >
        {/* Left Column: Session History & Mode Selector */}
        <aside style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
          {/* Active Concept Info Card */}
          <div
            className="editorial-card"
            style={{
              padding: 'var(--space-5)',
              backgroundColor: 'var(--surface-warm)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
              <div className="editorial-kicker">ACTIVE CURRICULUM CONTEXT</div>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>ID: {currentStudentId}</span>
            </div>
            <h3 className="serif-title" style={{ fontSize: '18px', color: 'var(--sutra-espresso)', marginTop: '2px' }}>
              {activeConcept.title}
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px', lineHeight: 1.5 }}>
              {activeConcept.description}
            </p>
          </div>

          {/* Teaching Modes Card */}
          <div className="editorial-card" style={{ padding: 'var(--space-5)' }}>
            <div className="editorial-kicker" style={{ marginBottom: 'var(--space-3)' }}>
              TEACHING MODES
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {TUTOR_MODES.map((m) => (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => setActiveMode(m.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    padding: '8px 12px',
                    borderRadius: 'var(--radius-sm)',
                    backgroundColor: activeMode === m.id ? 'var(--surface-warm)' : 'transparent',
                    border: activeMode === m.id ? '1px solid var(--sutra-taupe)' : '1px solid transparent',
                    color: activeMode === m.id ? 'var(--sutra-espresso)' : 'var(--text-secondary)',
                    fontWeight: activeMode === m.id ? 700 : 500,
                    fontSize: '12px',
                    textAlign: 'left',
                  }}
                  title={m.desc}
                >
                  <span style={{ fontSize: '15px' }}>{m.icon}</span>
                  <div>
                    <div>{m.label}</div>
                    <div style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 400 }}>{m.desc}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Session History Card */}
          <div
            className="editorial-card"
            style={{
              padding: 'var(--space-5)',
              display: 'flex',
              flexDirection: 'column',
              boxSizing: 'border-box',
              minHeight: '220px',
              maxHeight: '380px',
            }}
          >
            {/* Panel Header: Fixed & Non-Scrolling */}
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                paddingBottom: 'var(--space-3)',
                marginBottom: 'var(--space-3)',
                borderBottom: '1px solid var(--border-subtle)',
                flexShrink: 0,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span className="editorial-kicker" style={{ margin: 0 }}>PAST SESSIONS</span>
                {conversations.length > 0 && (
                  <span
                    style={{
                      fontSize: '10px',
                      fontFamily: 'var(--font-mono)',
                      padding: '1px 5px',
                      borderRadius: '8px',
                      backgroundColor: 'var(--surface-warm)',
                      color: 'var(--sutra-mocha)',
                      fontWeight: 600,
                    }}
                  >
                    {conversations.length}
                  </span>
                )}
              </div>
              <button
                type="button"
                className="btn-ghost"
                style={{
                  fontSize: '11px',
                  fontWeight: 600,
                  padding: '4px 8px',
                  color: 'var(--sutra-mocha)',
                  borderRadius: 'var(--radius-xs)',
                  border: '1px solid var(--border-subtle)',
                  backgroundColor: 'var(--surface-white)',
                  cursor: 'pointer',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                }}
                onClick={handleStartNewSession}
                title="Start a fresh learning session"
              >
                + New Session
              </button>
            </div>

            {/* Scrollable Session List Viewport */}
            <div
              className="editorial-scrollbar"
              style={{
                flex: 1,
                overflowY: 'auto',
                paddingRight: '6px',
                display: 'flex',
                flexDirection: 'column',
                gap: '6px',
                minHeight: '120px',
                boxSizing: 'border-box',
              }}
            >
              {conversationsLoading && conversations.length === 0 ? (
                <div style={{ padding: 'var(--space-4) 0', textAlign: 'center' }}>
                  <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                    Loading past sessions...
                  </span>
                </div>
              ) : conversationsError ? (
                <div
                  style={{
                    padding: 'var(--space-3)',
                    backgroundColor: 'var(--feedback-error-bg)',
                    borderRadius: 'var(--radius-xs)',
                    border: '1px solid var(--feedback-error-border)',
                  }}
                >
                  <p style={{ fontSize: '11px', color: 'var(--feedback-error)', margin: 0 }}>{conversationsError}</p>
                  <button
                    type="button"
                    className="btn-ghost"
                    style={{ fontSize: '11px', padding: '2px 0', marginTop: '4px', color: 'var(--sutra-mocha)', textDecoration: 'underline' }}
                    onClick={() => void loadConversations()}
                  >
                    Retry loading
                  </button>
                </div>
              ) : conversations.length === 0 ? (
                <div style={{ padding: 'var(--space-6) 0', textAlign: 'center' }}>
                  <p style={{ fontSize: '12px', color: 'var(--text-muted)', margin: 0 }}>No previous sessions yet.</p>
                  <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                    Ask a question to begin your first adaptive dialogue.
                  </p>
                </div>
              ) : (
                conversations.map((c) => {
                  const isActive = activeConversationId === c.id;
                  return (
                    <button
                      key={c.id}
                      type="button"
                      onClick={() => void loadConversationDetail(c.id)}
                      title={c.title || 'Untitled Session'}
                      style={{
                        width: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '8px 10px',
                        minHeight: '38px',
                        borderRadius: 'var(--radius-xs)',
                        backgroundColor: isActive ? 'var(--surface-warm)' : 'transparent',
                        border: isActive ? '1px solid var(--sutra-taupe)' : '1px solid var(--border-subtle)',
                        color: isActive ? 'var(--sutra-espresso)' : 'var(--text-primary)',
                        cursor: 'pointer',
                        textAlign: 'left',
                        boxSizing: 'border-box',
                        flexShrink: 0,
                        transition: 'background-color 0.15s ease, border-color 0.15s ease',
                      }}
                    >
                      <span
                        aria-hidden="true"
                        style={{
                          fontSize: '13px',
                          lineHeight: 1,
                          flexShrink: 0,
                          opacity: isActive ? 1 : 0.7,
                        }}
                      >
                        💬
                      </span>
                      <div
                        style={{
                          flex: 1,
                          minWidth: 0,
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '2px',
                        }}
                      >
                        <span
                          style={{
                            fontSize: '12px',
                            fontWeight: isActive ? 600 : 400,
                            lineHeight: 1.4,
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                            display: 'block',
                          }}
                        >
                          {c.title || 'Untitled Session'}
                        </span>
                        {c.updated_at && (
                          <span
                            style={{
                              fontSize: '10px',
                              color: 'var(--text-muted)',
                              fontFamily: 'var(--font-mono)',
                              lineHeight: 1.2,
                            }}
                          >
                            {new Date(c.updated_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                          </span>
                        )}
                      </div>
                    </button>
                  );
                })
              )}
            </div>
          </div>
        </aside>

        {/* Right Column: Chat Conversation Canvas */}
        <div
          className="editorial-card"
          style={{
            gridColumn: 'span 2',
            minHeight: '620px',
            display: 'flex',
            flexDirection: 'column',
            padding: 'var(--space-6)',
            backgroundColor: 'var(--surface-white)',
          }}
        >
          {/* Header */}
          <div
            style={{
              paddingBottom: 'var(--space-4)',
              borderBottom: '1px solid var(--border-subtle)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className="brand-symbol-mark" style={{ width: '24px', height: '24px', fontSize: '12px' }}>
                  S
                </span>
                <span style={{ fontFamily: 'var(--font-display)', fontSize: '18px', fontWeight: 600 }}>
                  SUTRA AI
                </span>
                <span
                  style={{
                    fontSize: '10px',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    letterSpacing: '0.06em',
                    backgroundColor: 'var(--feedback-success-bg)',
                    color: 'var(--feedback-success)',
                    border: '1px solid var(--feedback-success-border)',
                    padding: '2px 6px',
                    borderRadius: 'var(--radius-xs)',
                  }}
                >
                  Curriculum-Grounded
                </span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>
                Mode: <strong>{TUTOR_MODES.find((m) => m.id === activeMode)?.label}</strong> &bull; Concept: {activeConcept.title}
              </p>
            </div>
            <button
              type="button"
              className="btn-secondary"
              style={{ height: '32px', fontSize: '11px', padding: '0 10px' }}
              onClick={handleStartNewSession}
            >
              Clear & Restart
            </button>
          </div>

          {/* Conversation Stream */}
          <div
            style={{
              flex: 1,
              overflowY: 'auto',
              padding: 'var(--space-6) 0',
              display: 'flex',
              flexDirection: 'column',
              gap: 'var(--space-5)',
              maxHeight: '480px',
            }}
          >
            {messages.length === 0 ? (
              <div style={{ textAlign: 'center', margin: 'auto 0', padding: 'var(--space-8)' }}>
                <div style={{ fontSize: '32px', marginBottom: 'var(--space-2)' }}>🧭</div>
                <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)' }}>
                  How can I help you master {activeConcept.title}?
                </h3>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '6px', maxWidth: '440px', margin: '6px auto 0' }}>
                  I explain mathematical concepts from first principles, walk through worked solutions, and diagnose errors without simply giving away answers.
                </p>

                {/* Suggested prompt chips */}
                <div
                  style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    justifyContent: 'center',
                    gap: '8px',
                    marginTop: 'var(--space-6)',
                  }}
                >
                  {SUGGESTED_PROMPTS.map((prompt, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        setInputText(prompt);
                      }}
                      style={{
                        padding: '6px 12px',
                        fontSize: '12px',
                        borderRadius: 'var(--radius-pill)',
                        backgroundColor: 'var(--surface-warm)',
                        border: '1px solid var(--border-default)',
                        color: 'var(--sutra-espresso)',
                        cursor: 'pointer',
                        textAlign: 'left',
                      }}
                    >
                      &ldquo;{prompt}&rdquo;
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((m) => {
                const isUser = m.sender_role === 'user';
                return (
                  <div
                    key={m.id}
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: isUser ? 'flex-end' : 'flex-start',
                    }}
                  >
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        fontSize: '11px',
                        fontWeight: 700,
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em',
                        color: isUser ? 'var(--sutra-mocha)' : 'var(--text-secondary)',
                        marginBottom: '4px',
                      }}
                    >
                      <span>{isUser ? 'You (Learner)' : 'SUTRA AI • Grounded Tutor'}</span>
                      {!isUser && m.provider_metadata && (
                        <span
                          style={{
                            fontSize: '9px',
                            padding: '1px 6px',
                            borderRadius: '4px',
                            backgroundColor: m.provider_metadata.is_fallback ? 'var(--surface-warm)' : '#E8F5E9',
                            color: m.provider_metadata.is_fallback ? 'var(--sutra-mocha)' : '#2E7D32',
                            border: '1px solid var(--border-subtle)',
                            textTransform: 'none',
                            fontWeight: 600,
                          }}
                        >
                          {m.provider_metadata.provider || 'SUTRA AI'} {m.provider_metadata.model ? `(${m.provider_metadata.model})` : ''}
                        </span>
                      )}
                    </div>

                    <div
                      style={{
                        maxWidth: '85%',
                        padding: 'var(--space-4) var(--space-5)',
                        borderRadius: isUser
                          ? 'var(--radius-md) 0 var(--radius-md) var(--radius-md)'
                          : '0 var(--radius-md) var(--radius-md) var(--radius-md)',
                        backgroundColor: isUser ? 'var(--surface-warm)' : 'var(--surface-paper)',
                        border: isUser ? '1px solid var(--sutra-taupe)' : '1px solid var(--border-default)',
                        borderLeft: !isUser ? '3px solid var(--sutra-mocha)' : undefined,
                        color: 'var(--text-primary)',
                        lineHeight: 1.6,
                        fontSize: '14px',
                        whiteSpace: 'pre-wrap',
                      }}
                    >
                      {m.content}

                      {/* Progressive Hints Section */}
                      {m.hints && m.hints.length > 0 && (
                        <div style={{ marginTop: 'var(--space-4)', borderTop: '1px solid var(--border-subtle)', paddingTop: 'var(--space-3)' }}>
                          <button
                            type="button"
                            onClick={() => toggleHint(m.id)}
                            style={{
                              fontSize: '12px',
                              fontWeight: 600,
                              color: 'var(--sutra-mocha)',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '6px',
                              border: 'none',
                              backgroundColor: 'transparent',
                              cursor: 'pointer',
                              padding: 0,
                            }}
                          >
                            <span>💡</span>
                            <span>{revealedHints[m.id] ? 'Hide progressive hints' : `Reveal progressive hint (${m.hints.length} available)`}</span>
                          </button>

                          {revealedHints[m.id] && (
                            <div
                              style={{
                                marginTop: 'var(--space-2)',
                                padding: 'var(--space-3)',
                                backgroundColor: 'var(--feedback-warning-bg)',
                                border: '1px solid var(--feedback-warning-border)',
                                borderRadius: 'var(--radius-sm)',
                                fontSize: '13px',
                              }}
                            >
                              <ol style={{ paddingLeft: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                                {m.hints.map((hint, idx) => (
                                  <li key={idx} style={{ color: 'var(--text-primary)' }}>
                                    {hint}
                                  </li>
                                ))}
                              </ol>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Assistant Actions Bar */}
                      {!isUser && (
                        <div
                          style={{
                            display: 'flex',
                            justifyContent: 'flex-end',
                            gap: '8px',
                            marginTop: 'var(--space-3)',
                            fontSize: '11px',
                            color: 'var(--text-muted)',
                          }}
                        >
                          <button
                            type="button"
                            className="btn-ghost"
                            style={{ fontSize: '11px', padding: '2px 6px' }}
                            onClick={() => handleCopyText(m.content, m.id)}
                          >
                            {copyFeedback === m.id ? '✓ Copied' : '📋 Copy'}
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })
            )}

            {loading && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', fontSize: '13px', fontStyle: 'italic' }}>
                <span className="brand-symbol-mark" style={{ width: '20px', height: '20px', fontSize: '10px' }}>S</span>
                <span>SUTRA AI is synthesizing mathematical steps and diagnostic hints...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Bottom Message Input Form */}
          <form
            onSubmit={handleSendMessage}
            style={{
              paddingTop: 'var(--space-4)',
              borderTop: '1px solid var(--border-subtle)',
              display: 'flex',
              gap: 'var(--space-3)',
            }}
          >
            <textarea
              ref={textareaRef}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  void handleSendMessage();
                }
              }}
              placeholder={`Ask about ${activeConcept.title} (e.g. "Why do we subtract 5 first?", "Give me a practice problem")...`}
              rows={2}
              style={{
                flex: 1,
                padding: 'var(--space-3)',
                fontSize: '13px',
                fontFamily: 'var(--font-sans)',
                border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--surface-paper)',
                resize: 'none',
              }}
            />
            <button
              type="submit"
              className="btn-primary"
              disabled={loading || !inputText.trim()}
              style={{ alignSelf: 'flex-end', height: '44px' }}
            >
              {loading ? 'Thinking...' : 'Send Inquiry ↵'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
