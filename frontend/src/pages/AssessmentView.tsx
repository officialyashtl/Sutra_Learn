import { useState, useEffect, useCallback, useRef } from 'react';
import type { Concept, Question, Learner, AttemptResult, AssessmentResultResponse } from '../types';
import { savePendingAttempt, getPendingAttempts } from '../offline/db';
import { clearStoredAuth } from '../services/auth';
import { AUTH_EXPIRED_EVENT } from '../api/client';
import { SutraPageLoader } from '../components/SutraLoaders';

type AssessmentLifecycle = 'READY' | 'ANSWERING' | 'SUBMITTED' | 'FEEDBACK';

interface AssessmentSubmissionRecord {
  question_id: string;
  selected_option_id: string;
  hint_used: boolean;
  client_timestamp: string;
}

interface AssessmentViewProps {
  concept: Concept;
  learner: Learner;
  apiBaseUrl: string;
  authToken?: string | null;
  onBack: () => void;
  onCompleteEvaluation: (conceptId: string) => void;
  onOpenLesson?: (conceptId: string) => void;
}

export function AssessmentView({
  concept,
  learner,
  apiBaseUrl,
  authToken,
  onBack,
  onCompleteEvaluation,
  onOpenLesson,
}: AssessmentViewProps) {
  // Assessment Quiz State
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [lifecycle, setLifecycle] = useState<AssessmentLifecycle>('READY');
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [hintRevealed, setHintRevealed] = useState<boolean>(false);
  const [attemptResult, setAttemptResult] = useState<AttemptResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [evaluating, setEvaluating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [pendingQueueCount, setPendingQueueCount] = useState<number>(0);

  // Completed Evaluation / Results State
  const [completedResult, setCompletedResult] = useState<AssessmentResultResponse | null>(null);

  // Submissions accumulator & session tracking
  const sessionIdRef = useRef<string>(`sess-${crypto.randomUUID()}`);
  const submissionsMapRef = useRef<Map<string, AssessmentSubmissionRecord>>(new Map());

  const updatePendingCount = useCallback(async () => {
    try {
      const list = await getPendingAttempts();
      setPendingQueueCount(list.length);
    } catch {
      // Ignore offline store lookup failures
    }
  }, []);

  // Check for existing persisted assessment result, or fetch questions
  const loadAssessment = useCallback(async (forceRetake = false) => {
    setLoading(true);
    setError(null);
    setAttemptResult(null);
    setSelectedOption(null);
    setHintRevealed(false);
    setCurrentIndex(0);

    const authHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
    };

    try {
      // 1. Check if an assessment was already completed (unless forced retake)
      if (!forceRetake) {
        try {
          const resResult = await fetch(`${apiBaseUrl}/api/v1/assessments/results/${concept.id}`, {
            headers: authHeaders,
          });
          if (resResult.ok) {
            const resultData: AssessmentResultResponse = await resResult.json();
            if (resultData && resultData.id) {
              setCompletedResult(resultData);
              setLoading(false);
              return;
            }
          }
        } catch (err) {
          console.warn('No prior completed assessment found, loading fresh items:', err);
        }
      }

      // 2. Fetch fresh questions for the concept
      sessionIdRef.current = `sess-${crypto.randomUUID()}`;
      submissionsMapRef.current.clear();
      setCompletedResult(null);

      const resQ = await fetch(`${apiBaseUrl}/api/v1/concepts/${concept.id}/questions`, {
        headers: authHeaders,
      });
      if (resQ.status === 401) {
        clearStoredAuth();
        if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
        throw new Error('Your session has expired. Please sign in again.');
      }
      if (!resQ.ok) {
        throw new Error('Failed to load assessment items.');
      }
      const data = await resQ.json();
      setQuestions(data);
      setLifecycle('READY');
    } catch (err: any) {
      setError(err.message || 'Error fetching assessment questions.');
    } finally {
      setLoading(false);
      void updatePendingCount();
    }
  }, [apiBaseUrl, authToken, concept.id, updatePendingCount]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      void loadAssessment(false);
    }, 0);
    return () => clearTimeout(timeout);
  }, [loadAssessment]);

  const currentQ = questions[currentIndex];

  const handleSelectOption = (optId: string) => {
    if (lifecycle === 'SUBMITTED' || lifecycle === 'FEEDBACK') return;
    setSelectedOption(optId);
    setLifecycle('ANSWERING');
  };

  const handleRevealHint = () => {
    setHintRevealed(true);
  };

  // Submit single question attempt
  const handleSubmitQuestion = async () => {
    if (!selectedOption || !currentQ || lifecycle === 'SUBMITTED') return;

    setLifecycle('SUBMITTED');
    const attemptId = 'att-' + crypto.randomUUID();
    const payload = {
      attempt_id: attemptId,
      learner_id: learner.id,
      question_id: currentQ.id,
      concept_id: concept.id,
      selected_option_id: selectedOption,
      hint_used: hintRevealed,
      session_id: sessionIdRef.current,
      client_timestamp: new Date().toISOString(),
    };

    // Store in our submissions accumulator
    submissionsMapRef.current.set(currentQ.id, {
      question_id: currentQ.id,
      selected_option_id: selectedOption,
      hint_used: hintRevealed,
      client_timestamp: payload.client_timestamp,
    });

    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/attempts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        },
        body: JSON.stringify(payload),
      });

      if (res.status === 401) {
        clearStoredAuth();
        if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
        setError('Your session has expired. Please sign in again.');
        return;
      }

      if (res.ok) {
        const result: AttemptResult = await res.json();
        setAttemptResult({
          ...result,
          is_offline_queued: false,
        });
        setLifecycle('FEEDBACK');
      } else {
        throw new Error('Server returned error response');
      }
    } catch {
      await savePendingAttempt(payload);
      await updatePendingCount();

      const chosenOpt = currentQ.options.find((o) => o.id === selectedOption);
      const isCorrect = !!chosenOpt?.is_correct;
      setAttemptResult({
        attempt_id: attemptId,
        is_duplicate: false,
        is_correct: isCorrect,
        hint_used: hintRevealed,
        selected_option_id: selectedOption,
        correct_option_id: currentQ.options.find((o) => o.is_correct)?.id || 'A',
        explanation: currentQ.explanation || 'Attempt recorded offline. Explanation will be refreshed upon server synchronization.',
        misconception_tag: chosenOpt?.misconception_tag || 'none',
        misconception_explanation: chosenOpt?.misconception_explanation,
        message: 'Stored offline in IndexedDB queue.',
        is_offline_queued: true,
      });
      setLifecycle('FEEDBACK');
    }
  };

  const handleNextQuestion = () => {
    setAttemptResult(null);
    setSelectedOption(null);
    setHintRevealed(false);
    setLifecycle('READY');
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  // Final evaluation submission
  const handleFinalizeAssessment = async () => {
    setEvaluating(true);
    setError(null);

    const submissionsArray = Array.from(submissionsMapRef.current.values());
    const completePayload = {
      concept_id: concept.id,
      session_id: sessionIdRef.current,
      submissions: submissionsArray,
    };

    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/assessments/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        },
        body: JSON.stringify(completePayload),
      });

      if (res.status === 401) {
        clearStoredAuth();
        if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
        setError('Your session has expired. Please sign in again.');
        return;
      }

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.detail || 'Failed to complete assessment.');
      }

      const resultData: AssessmentResultResponse = await res.json();
      setCompletedResult(resultData);

      // Trigger parent callback to synchronize unlocked concepts and progress
      onCompleteEvaluation(concept.id);
    } catch (err: any) {
      console.error('Assessment evaluation error:', err);
      setError(err.message || 'Error calculating assessment outcome.');
    } finally {
      setEvaluating(false);
    }
  };

  // ==========================================
  // VIEW 1: LOADING STATE
  // ==========================================
  if (loading) {
    return (
      <div style={{ maxWidth: 'var(--reading-width)', margin: 'var(--space-8) auto' }}>
        <SutraPageLoader
          message="Preparing verified diagnostic assessment items..."
          subMessage="Aligning curriculum depth and SUTRA cognitive milestones"
        />
      </div>
    );
  }

  // ==========================================
  // VIEW 2: EVALUATION IN PROGRESS LOADER
  // ==========================================
  if (evaluating) {
    return (
      <div style={{ maxWidth: 'var(--reading-width)', margin: 'var(--space-8) auto' }}>
        <SutraPageLoader
          message="Synthesizing assessment results with SUTRA AI..."
          subMessage="Analyzing cognitive patterns and formulating your personalized next lesson"
        />
      </div>
    );
  }

  // ==========================================
  // VIEW 3: ERROR STATE
  // ==========================================
  if (error && !completedResult) {
    return (
      <div className="editorial-card" style={{ padding: 'var(--space-8)', maxWidth: 'var(--reading-width)', margin: 'var(--space-8) auto' }}>
        <h3 style={{ color: 'var(--feedback-error)', fontFamily: 'var(--font-serif)', fontSize: '20px' }}>
          Unable to Complete Assessment
        </h3>
        <p style={{ color: 'var(--text-secondary)', margin: 'var(--space-3) 0 var(--space-6) 0' }}>
          {error}
        </p>
        <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <button type="button" className="btn-secondary" onClick={() => void loadAssessment(false)}>
            Try Again
          </button>
          <button type="button" className="btn-ghost" onClick={onBack}>
            &larr; Back to Concepts
          </button>
        </div>
      </div>
    );
  }

  // ==========================================
  // VIEW 4: COMPLETED RESULTS & AI GUIDANCE VIEW
  // ==========================================
  if (completedResult) {
    const isPassed = completedResult.passed;
    const isStretch = completedResult.outcome === 'STRETCH';
    const isScaffold = completedResult.outcome === 'SCAFFOLD' || completedResult.outcome === 'BRIDGE_BACK';

    return (
      <div style={{ maxWidth: 'var(--reading-width)', margin: '0 auto', paddingBottom: 'var(--space-12)' }}>
        {/* Top Meta Bar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-4)', flexWrap: 'wrap', gap: '8px' }}>
          <button type="button" className="btn-ghost" style={{ fontSize: '13px', paddingLeft: 0 }} onClick={onBack}>
            &larr; Back to Concepts
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
              {concept.code} &bull; {new Date(completedResult.created_at).toLocaleDateString()}
            </span>
            {completedResult.can_advance && (
              <span
                style={{
                  fontSize: '11px',
                  backgroundColor: 'var(--feedback-success-bg)',
                  color: 'var(--feedback-success)',
                  border: '1px solid var(--feedback-success-border)',
                  padding: '3px 8px',
                  borderRadius: 'var(--radius-xs)',
                  fontWeight: 600,
                }}
              >
                Ready to Advance ✓
              </span>
            )}
          </div>
        </div>

        {/* Hero Score Card */}
        <section
          className="editorial-card"
          style={{
            padding: 'var(--space-8)',
            backgroundColor: 'var(--surface-white)',
            borderLeft: `4px solid ${isPassed ? 'var(--feedback-success)' : 'var(--sutra-mocha)'}`,
            marginBottom: 'var(--space-6)',
          }}
        >
          <div className="editorial-kicker" style={{ marginBottom: 'var(--space-2)' }}>
            Official Assessment Result &bull; {completedResult.concept_title}
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
            <div>
              <h1 className="serif-title" style={{ fontSize: '28px', color: 'var(--sutra-espresso)', margin: '0 0 var(--space-2) 0' }}>
                {isPassed ? (isStretch ? 'Concept Mastered!' : 'Assessment Passed') : 'Reinforcement Recommended'}
              </h1>
              <p style={{ color: 'var(--text-secondary)', fontSize: '15px', margin: 0 }}>
                {isPassed
                  ? 'You demonstrated reliable conceptual command across core mathematical principles.'
                  : 'Targeted practice is recommended to solidify foundational understanding before moving forward.'}
              </p>
            </div>

            {/* Score & Percentage Pill */}
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'flex-end',
                backgroundColor: isPassed ? 'var(--surface-warm)' : 'var(--feedback-warning-bg)',
                padding: 'var(--space-3) var(--space-5)',
                borderRadius: 'var(--radius-md)',
                border: `1px solid ${isPassed ? 'var(--border-subtle)' : 'var(--feedback-warning-border)'}`,
              }}
            >
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>
                Mastery Score
              </span>
              <div style={{ fontSize: '26px', fontWeight: 700, color: isPassed ? 'var(--sutra-espresso)' : 'var(--feedback-warning)', fontFamily: 'var(--font-serif)' }}>
                {completedResult.score} / {completedResult.total_questions}
              </div>
              <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--sutra-mocha)' }}>
                {completedResult.percentage}% &bull; {completedResult.outcome}
              </span>
            </div>
          </div>
        </section>

        {/* SUTRA AI Personalized Guidance Card */}
        {completedResult.ai_guidance && (
          <section
            className="editorial-card"
            style={{
              padding: 'var(--space-8)',
              backgroundColor: 'var(--surface-paper)',
              marginBottom: 'var(--space-6)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)', marginBottom: 'var(--space-3)' }}>
              <div
                style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: 'var(--radius-sm)',
                  backgroundColor: 'var(--sutra-mocha)',
                  color: '#ffffff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '12px',
                  fontWeight: 700,
                  fontFamily: 'var(--font-serif)',
                }}
              >
                S
              </div>
              <span className="editorial-kicker" style={{ margin: 0 }}>
                SUTRA AI &bull; Personalized Learning Guidance
              </span>
            </div>

            <p style={{ fontSize: '15px', color: 'var(--sutra-espresso)', lineHeight: 1.6, margin: '0 0 var(--space-4) 0' }}>
              {completedResult.ai_guidance.summary}
            </p>

            {/* Strengths */}
            {completedResult.ai_guidance.strengths && completedResult.ai_guidance.strengths.length > 0 && (
              <div style={{ marginBottom: 'var(--space-4)' }}>
                <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--sutra-mocha)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Demonstrated Strengths
                </span>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-2)', marginTop: 'var(--space-2)' }}>
                  {completedResult.ai_guidance.strengths.map((str, idx) => (
                    <span
                      key={idx}
                      style={{
                        fontSize: '13px',
                        backgroundColor: 'var(--surface-white)',
                        color: 'var(--feedback-success)',
                        border: '1px solid var(--feedback-success-border)',
                        padding: '4px 10px',
                        borderRadius: 'var(--radius-sm)',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                      }}
                    >
                      <span>✓</span> {str}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Focus Area & Recommended Action Step */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                gap: 'var(--space-4)',
                marginTop: 'var(--space-4)',
              }}
            >
              <div
                style={{
                  backgroundColor: 'var(--surface-white)',
                  padding: 'var(--space-4)',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                }}
              >
                <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 'var(--space-1)' }}>
                  Focus Area
                </div>
                <div style={{ fontSize: '14px', color: 'var(--text-primary)', lineHeight: 1.4 }}>
                  {completedResult.ai_guidance.focus_area}
                </div>
              </div>

              <div
                style={{
                  backgroundColor: 'var(--surface-white)',
                  padding: 'var(--space-4)',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                }}
              >
                <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 'var(--space-1)' }}>
                  Recommended Action Step
                </div>
                <div style={{ fontSize: '14px', color: 'var(--text-primary)', lineHeight: 1.4 }}>
                  {completedResult.ai_guidance.action_step}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Adaptive Progression Action Panel */}
        <section
          className="editorial-card"
          style={{
            padding: 'var(--space-6) var(--space-8)',
            backgroundColor: 'var(--surface-white)',
            marginBottom: 'var(--space-8)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: 'var(--space-4)',
          }}
        >
          <div>
            <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--sutra-mocha)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Adaptive Next Step
            </div>
            <div style={{ fontSize: '16px', fontWeight: 600, color: 'var(--sutra-espresso)', marginTop: '2px' }}>
              {completedResult.can_advance && completedResult.next_concept_title
                ? `Next Unlocked Lesson: ${completedResult.next_concept_title}`
                : isScaffold
                ? 'Review Current Concept Lesson Before Retaking'
                : 'Next Pathway Milestone Available'}
            </div>
          </div>

          <div style={{ display: 'flex', gap: 'var(--space-3)', flexWrap: 'wrap' }}>
            {completedResult.can_advance && completedResult.next_concept_id && onOpenLesson && (
              <button
                type="button"
                className="btn-primary"
                onClick={() => onOpenLesson(completedResult.next_concept_id!)}
                style={{ padding: 'var(--space-3) var(--space-6)', fontWeight: 600 }}
              >
                Continue to Next Lesson &rarr;
              </button>
            )}

            {onOpenLesson && (
              <button
                type="button"
                className="btn-secondary"
                onClick={() => onOpenLesson(concept.id)}
              >
                Review Lesson
              </button>
            )}

            <button
              type="button"
              className="btn-secondary"
              onClick={() => void loadAssessment(true)}
            >
              Retake Assessment
            </button>
          </div>
        </section>

        {/* Question-by-Question Deep Dive */}
        <section>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-4)' }}>
            <h2 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', margin: 0 }}>
              Question-by-Question Review ({completedResult.questions_detail.length})
            </h2>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Complete diagnostic record & mathematical solutions
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-5)' }}>
            {completedResult.questions_detail.map((qDetail, idx) => {
              const isCorrect = qDetail.is_correct;

              return (
                <article
                  key={qDetail.question_id || idx}
                  className="editorial-card"
                  style={{
                    padding: 'var(--space-6)',
                    backgroundColor: 'var(--surface-white)',
                    borderLeft: `4px solid ${isCorrect ? 'var(--feedback-success)' : 'var(--feedback-warning)'}`,
                  }}
                >
                  {/* Question Header */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                      <span
                        style={{
                          fontSize: '12px',
                          fontWeight: 700,
                          padding: '2px 8px',
                          borderRadius: 'var(--radius-xs)',
                          backgroundColor: isCorrect ? 'var(--feedback-success-bg)' : 'var(--feedback-warning-bg)',
                          color: isCorrect ? 'var(--feedback-success)' : 'var(--feedback-warning)',
                          border: `1px solid ${isCorrect ? 'var(--feedback-success-border)' : 'var(--feedback-warning-border)'}`,
                        }}
                      >
                        {isCorrect ? '✓ Correct' : '✗ Incorrect'}
                      </span>
                      <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)' }}>
                        Question {idx + 1}
                      </span>
                      {qDetail.hint_used && (
                        <span style={{ fontSize: '11px', color: 'var(--sutra-mocha)', fontWeight: 500 }}>
                          [💡 Hint Used]
                        </span>
                      )}
                    </div>
                    <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                      Demand: {qDetail.cognitive_demand} &bull; Difficulty {qDetail.difficulty}/5
                    </span>
                  </div>

                  {/* Question Prompt */}
                  <h3 style={{ fontSize: '16px', color: 'var(--sutra-espresso)', fontWeight: 600, lineHeight: 1.4, margin: '0 0 var(--space-3) 0' }}>
                    {qDetail.prompt}
                  </h3>

                  {/* Math Display */}
                  {qDetail.equation_display && (
                    <div className="math-display-block" style={{ marginBottom: 'var(--space-4)' }}>
                      {qDetail.equation_display}
                    </div>
                  )}

                  {/* Options List */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)', margin: 'var(--space-4) 0' }}>
                    {qDetail.options.map((opt) => {
                      const isStudentSelection = qDetail.selected_option_id === opt.id;
                      const isCorrectAnswer = qDetail.correct_option_id === opt.id;

                      let borderCol = 'var(--border-subtle)';
                      let bgCol = 'var(--surface-white)';
                      let badgeText = null;
                      let badgeBg = '';
                      let badgeCol = '';

                      if (isCorrectAnswer) {
                        borderCol = 'var(--feedback-success)';
                        bgCol = 'var(--feedback-success-bg)';
                        badgeText = 'Correct Answer ✓';
                        badgeBg = 'var(--feedback-success)';
                        badgeCol = '#ffffff';
                      } else if (isStudentSelection && !isCorrect) {
                        borderCol = 'var(--feedback-error)';
                        bgCol = 'var(--feedback-error-bg)';
                        badgeText = 'Your Selection ✗';
                        badgeBg = 'var(--feedback-error)';
                        badgeCol = '#ffffff';
                      }

                      return (
                        <div
                          key={opt.id}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            padding: 'var(--space-3) var(--space-4)',
                            backgroundColor: bgCol,
                            border: `1.5px solid ${borderCol}`,
                            borderRadius: 'var(--radius-sm)',
                          }}
                        >
                          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                            <span
                              style={{
                                width: '24px',
                                height: '24px',
                                borderRadius: 'var(--radius-xs)',
                                backgroundColor: isStudentSelection ? 'var(--sutra-mocha)' : 'var(--surface-warm)',
                                color: isStudentSelection ? '#ffffff' : 'var(--text-primary)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontFamily: 'var(--font-mono)',
                                fontSize: '12px',
                                fontWeight: 700,
                              }}
                            >
                              {opt.id}
                            </span>
                            <span style={{ fontSize: '14px', color: 'var(--text-primary)' }}>
                              {opt.text}
                            </span>
                          </div>

                          {badgeText && (
                            <span
                              style={{
                                fontSize: '11px',
                                fontWeight: 600,
                                backgroundColor: badgeBg,
                                color: badgeCol,
                                padding: '2px 8px',
                                borderRadius: 'var(--radius-xs)',
                              }}
                            >
                              {badgeText}
                            </span>
                          )}
                        </div>
                      );
                    })}
                  </div>

                  {/* Misconception Diagnostic Pattern (if incorrect) */}
                  {!isCorrect && (qDetail.misconception_explanation || qDetail.misconception_tag) && (
                    <div
                      style={{
                        margin: 'var(--space-3) 0',
                        padding: 'var(--space-3) var(--space-4)',
                        backgroundColor: 'var(--feedback-warning-bg)',
                        border: '1px solid var(--feedback-warning-border)',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: '13px',
                        color: 'var(--feedback-warning)',
                      }}
                    >
                      <div style={{ fontWeight: 700, marginBottom: '2px' }}>
                        Cognitive Pattern Identified: {qDetail.misconception_tag || 'Arithmetic Sign Misconception'}
                      </div>
                      <div style={{ lineHeight: 1.4 }}>
                        {qDetail.misconception_explanation || 'This misconception occurs when applying rules from addition to subtraction, or assuming sign signs invert symmetrically.'}
                      </div>
                    </div>
                  )}

                  {/* Explanation Block */}
                  <div
                    style={{
                      marginTop: 'var(--space-3)',
                      padding: 'var(--space-3) var(--space-4)',
                      backgroundColor: 'var(--surface-paper)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '13px',
                      color: 'var(--text-secondary)',
                      lineHeight: 1.5,
                      borderLeft: '3px solid var(--sutra-mocha)',
                    }}
                  >
                    <strong style={{ color: 'var(--sutra-espresso)', display: 'block', marginBottom: '2px' }}>
                      Mathematical Explanation:
                    </strong>
                    {qDetail.explanation}
                  </div>
                </article>
              );
            })}
          </div>
        </section>
      </div>
    );
  }

  // ==========================================
  // VIEW 5: ACTIVE ASSESSMENT QUESTION FLOW
  // ==========================================
  if (!currentQ) {
    return (
      <div className="editorial-card" style={{ padding: 'var(--space-8)', maxWidth: 'var(--reading-width)', margin: 'var(--space-8) auto' }}>
        <h3 style={{ color: 'var(--feedback-error)' }}>No questions available</h3>
        <p style={{ color: 'var(--text-secondary)', margin: 'var(--space-3) 0' }}>
          This concept does not have diagnostic items loaded.
        </p>
        <button type="button" className="btn-secondary" onClick={onBack}>
          &larr; Back to Concepts
        </button>
      </div>
    );
  }

  const isFinalQuestion = currentIndex + 1 === questions.length;
  const progressPercent = Math.round(((currentIndex + (lifecycle === 'FEEDBACK' ? 1 : 0)) / questions.length) * 100);

  return (
    <div style={{ maxWidth: 'var(--reading-width)', margin: '0 auto' }}>
      {/* Top Meta Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)', flexWrap: 'wrap', gap: '8px' }}>
        <button type="button" className="btn-ghost" style={{ fontSize: '13px', paddingLeft: 0 }} onClick={onBack}>
          &larr; Exit Assessment
        </button>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
          {pendingQueueCount > 0 && (
            <span style={{ fontSize: '11px', background: 'var(--feedback-warning-bg)', color: 'var(--feedback-warning)', padding: '3px 8px', borderRadius: 'var(--radius-xs)', fontWeight: 600 }}>
              ⚡ {pendingQueueCount} offline queued
            </span>
          )}
          <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)' }}>
            Question {currentIndex + 1} of {questions.length} &bull; {concept.code}
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div style={{ width: '100%', height: '4px', backgroundColor: 'var(--surface-warm)', borderRadius: '2px', marginBottom: 'var(--space-6)', overflow: 'hidden' }}>
        <div
          style={{
            width: `${progressPercent}%`,
            height: '100%',
            backgroundColor: 'var(--sutra-mocha)',
            transition: 'width 200ms ease',
          }}
        />
      </div>

      {/* Main Question Card */}
      <article className="editorial-card" style={{ padding: 'var(--space-8)', backgroundColor: 'var(--surface-white)' }} aria-labelledby="question-prompt">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
          <span className="editorial-kicker">
            Demand: {currentQ.cognitive_demand} &bull; Difficulty {currentQ.difficulty}/5
          </span>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
            {currentQ.id}
          </span>
        </div>

        {/* Prompt */}
        <h2 id="question-prompt" className="serif-title" style={{ fontSize: '22px', color: 'var(--sutra-espresso)', lineHeight: 1.35, marginBottom: 'var(--space-4)' }}>
          {currentQ.prompt}
        </h2>

        {/* Math Display */}
        {currentQ.equation_display && (
          <div className="math-display-block">
            {currentQ.equation_display}
          </div>
        )}

        {/* Option Selection Group */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)', margin: 'var(--space-6) 0' }} role="radiogroup" aria-labelledby="question-prompt">
          {currentQ.options.map((opt) => {
            const isSelected = selectedOption === opt.id;
            let borderCol = 'var(--border-default)';
            let bgCol = 'var(--surface-white)';

            if (isSelected) {
              borderCol = 'var(--sutra-mocha)';
              bgCol = 'var(--surface-warm)';
            }
            if (lifecycle === 'FEEDBACK' && attemptResult) {
              if (opt.id === attemptResult.correct_option_id) {
                borderCol = 'var(--feedback-success)';
                bgCol = 'var(--feedback-success-bg)';
              } else if (isSelected && !attemptResult.is_correct) {
                borderCol = 'var(--feedback-error)';
                bgCol = 'var(--feedback-error-bg)';
              }
            }

            return (
              <button
                key={opt.id}
                type="button"
                onClick={() => handleSelectOption(opt.id)}
                disabled={lifecycle === 'SUBMITTED' || lifecycle === 'FEEDBACK'}
                aria-checked={isSelected}
                role="radio"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-4)',
                  padding: 'var(--space-4) var(--space-5)',
                  backgroundColor: bgCol,
                  border: `1.5px solid ${borderCol}`,
                  borderRadius: 'var(--radius-md)',
                  textAlign: 'left',
                  cursor: lifecycle === 'FEEDBACK' ? 'default' : 'pointer',
                  transition: 'all var(--transition-fast)',
                }}
              >
                <span
                  style={{
                    width: '28px',
                    height: '28px',
                    borderRadius: 'var(--radius-sm)',
                    backgroundColor: isSelected ? 'var(--sutra-mocha)' : 'var(--surface-warm)',
                    color: isSelected ? '#ffffff' : 'var(--text-primary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '13px',
                    fontWeight: 700,
                  }}
                >
                  {opt.id}
                </span>
                <span style={{ flex: 1, fontSize: '15px', color: 'var(--text-primary)' }}>
                  {opt.text}
                </span>
              </button>
            );
          })}
        </div>

        {/* Guiding Scaffolding Hint */}
        {lifecycle !== 'FEEDBACK' && (
          <div style={{ margin: 'var(--space-4) 0' }}>
            {!hintRevealed ? (
              <button
                type="button"
                onClick={handleRevealHint}
                className="btn-ghost"
                style={{ padding: 0, height: 'auto', color: 'var(--sutra-mocha)', fontWeight: 600, fontSize: '13px' }}
              >
                💡 Need a hint? Reveal guiding step
              </button>
            ) : (
              <div
                style={{
                  backgroundColor: 'var(--outcome-scaffold-bg)',
                  border: '1px solid var(--outcome-scaffold-border)',
                  borderRadius: 'var(--radius-md)',
                  padding: 'var(--space-3) var(--space-4)',
                  fontSize: '13px',
                  color: 'var(--sutra-mocha)',
                }}
              >
                <strong>Guiding Step:</strong> {currentQ.hint}
              </div>
            )}
          </div>
        )}

        {/* Submit Action */}
        {lifecycle !== 'FEEDBACK' && (
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 'var(--space-6)', borderTop: '1px solid var(--border-subtle)', paddingTop: 'var(--space-5)' }}>
            <button
              type="button"
              className="btn-primary"
              disabled={!selectedOption || lifecycle === 'SUBMITTED'}
              onClick={handleSubmitQuestion}
              style={{ minWidth: '160px' }}
            >
              {lifecycle === 'SUBMITTED' ? 'Verifying...' : 'Submit Answer'}
            </button>
          </div>
        )}

        {/* Diagnostic Feedback Section */}
        {lifecycle === 'FEEDBACK' && attemptResult && (
          <div
            style={{
              marginTop: 'var(--space-6)',
              padding: 'var(--space-5)',
              backgroundColor: attemptResult.is_correct ? 'var(--feedback-success-bg)' : 'var(--feedback-warning-bg)',
              border: `1.5px solid ${attemptResult.is_correct ? 'var(--feedback-success-border)' : 'var(--feedback-warning-border)'}`,
              borderRadius: 'var(--radius-md)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-2)' }}>
              <span style={{ fontSize: '15px', fontWeight: 700, color: attemptResult.is_correct ? 'var(--feedback-success)' : 'var(--feedback-warning)' }}>
                {attemptResult.is_correct ? '✓ Correct Reasoning' : '🔍 Investigation Signal'}
              </span>
              {attemptResult.hint_used && (
                <span style={{ fontSize: '11px', color: 'var(--sutra-mocha)', fontWeight: 600 }}>
                  [💡 Hint Assisted]
                </span>
              )}
            </div>

            {/* Misconception Diagnostic Pattern */}
            {!attemptResult.is_correct && attemptResult.misconception_explanation && (
              <div
                style={{
                  margin: 'var(--space-3) 0',
                  padding: 'var(--space-3) var(--space-4)',
                  backgroundColor: 'var(--surface-white)',
                  border: '1px solid var(--feedback-warning-border)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '13px',
                  color: 'var(--feedback-warning)',
                }}
              >
                <strong>Diagnosed Cognitive Pattern:</strong> {attemptResult.misconception_explanation}
              </div>
            )}

            <p style={{ fontSize: '14px', color: 'var(--text-primary)', lineHeight: 1.6, marginTop: 'var(--space-2)' }}>
              {attemptResult.explanation}
            </p>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 'var(--space-5)' }}>
              {!isFinalQuestion ? (
                <button type="button" className="btn-primary" onClick={handleNextQuestion}>
                  Next Question &rarr;
                </button>
              ) : (
                <button
                  type="button"
                  className="btn-primary"
                  onClick={handleFinalizeAssessment}
                >
                  Complete Assessment & View Analysis &rarr;
                </button>
              )}
            </div>
          </div>
        )}
      </article>
    </div>
  );
}
