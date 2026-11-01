import { useState, useEffect, useCallback } from 'react';
import type { Concept, Question, Learner, AttemptResult } from '../types';
import { savePendingAttempt, getPendingAttempts } from '../offline/db';

type AssessmentLifecycle = 'READY' | 'ANSWERING' | 'SUBMITTED' | 'FEEDBACK';

interface AssessmentViewProps {
  concept: Concept;
  learner: Learner;
  apiBaseUrl: string;
  authToken?: string | null;
  onBack: () => void;
  onCompleteEvaluation: (conceptId: string) => void;
}

export function AssessmentView({
  concept,
  learner,
  apiBaseUrl,
  authToken,
  onBack,
  onCompleteEvaluation,
}: AssessmentViewProps) {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [lifecycle, setLifecycle] = useState<AssessmentLifecycle>('READY');
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [hintRevealed, setHintRevealed] = useState<boolean>(false);
  const [attemptResult, setAttemptResult] = useState<AttemptResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [pendingQueueCount, setPendingQueueCount] = useState<number>(0);

  const updatePendingCount = useCallback(async () => {
    const list = await getPendingAttempts();
    setPendingQueueCount(list.length);
  }, []);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const res = await fetch(`${apiBaseUrl}/api/v1/concepts/${concept.id}/questions`);
        if (!res.ok) throw new Error('Failed to load assessment items.');
        const data = await res.json();
        setQuestions(data);
        setLifecycle('READY');
      } catch (err: any) {
        setError(err.message || 'Error fetching assessment questions.');
      } finally {
        setLoading(false);
      }
      await updatePendingCount();
    }
    const timeout = setTimeout(() => {
      void loadData();
    }, 0);
    return () => clearTimeout(timeout);
  }, [concept.id, apiBaseUrl, updatePendingCount]);

  const currentQ = questions[currentIndex];

  const handleSelectOption = (optId: string) => {
    if (lifecycle === 'SUBMITTED' || lifecycle === 'FEEDBACK') return;
    setSelectedOption(optId);
    setLifecycle('ANSWERING');
  };

  const handleRevealHint = () => {
    setHintRevealed(true);
  };

  const handleSubmit = async () => {
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
      client_timestamp: new Date().toISOString(),
    };

    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/attempts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        },
        body: JSON.stringify(payload),
      });

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

  const handleNext = () => {
    setAttemptResult(null);
    setSelectedOption(null);
    setHintRevealed(false);
    setLifecycle('READY');
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  if (loading) {
    return (
      <div className="editorial-card" style={{ textAlign: 'center', padding: 'var(--space-12)', maxWidth: 'var(--reading-width)', margin: '0 auto' }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading verified diagnostic assessment items...</p>
      </div>
    );
  }

  if (error || !currentQ) {
    return (
      <div className="editorial-card" style={{ padding: 'var(--space-8)', maxWidth: 'var(--reading-width)', margin: '0 auto' }}>
        <h3 style={{ color: 'var(--feedback-error)' }}>Unable to load questions</h3>
        <p style={{ color: 'var(--text-secondary)', margin: 'var(--space-3) 0' }}>{error || 'No questions available.'}</p>
        <button type="button" className="btn-secondary" onClick={onBack}>
          &larr; Back to Concepts
        </button>
      </div>
    );
  }

  const progressPercent = Math.round(((currentIndex + (lifecycle === 'FEEDBACK' ? 1 : 0)) / questions.length) * 100);

  return (
    <div style={{ maxWidth: 'var(--reading-width)', margin: '0 auto' }}>
      {/* Top Meta Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)', flexWrap: 'wrap', gap: '8px' }}>
        <button type="button" className="btn-ghost" style={{ fontSize: '13px', paddingLeft: 0 }} onClick={onBack}>
          &larr; Exit Practice
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
              onClick={handleSubmit}
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
              {currentIndex + 1 < questions.length ? (
                <button type="button" className="btn-primary" onClick={handleNext}>
                  Next Question &rarr;
                </button>
              ) : (
                <button
                  type="button"
                  className="btn-primary"
                  onClick={() => onCompleteEvaluation(concept.id)}
                >
                  Complete & See Adaptive Path &rarr;
                </button>
              )}
            </div>
          </div>
        )}
      </article>
    </div>
  );
}
