import { getPendingAttempts, deletePendingAttempt } from './db';
import { getAuthHeaders } from '../services/auth';

export async function syncPendingAttempts(apiBaseUrl: string, token?: string | null): Promise<{ synced: number; failed: number }> {
  const pending = await getPendingAttempts();
  if (pending.length === 0) {
    return { synced: 0, failed: 0 };
  }

  let synced = 0;
  let failed = 0;
  const authHeaders = getAuthHeaders(token);

  for (const attempt of pending) {
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/attempts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify({
          attempt_id: attempt.attempt_id,
          learner_id: attempt.learner_id,
          question_id: attempt.question_id,
          concept_id: attempt.concept_id,
          selected_option_id: attempt.selected_option_id,
          hint_used: attempt.hint_used,
          client_timestamp: attempt.client_timestamp || new Date().toISOString(),
        }),
      });

      if (response.ok) {
        // Acknowledged by server (either newly recorded or acknowledged duplicate)
        await deletePendingAttempt(attempt.attempt_id);
        synced++;
      } else {
        failed++;
      }
    } catch (err) {
      console.warn(`Sync failed for attempt ${attempt.attempt_id}:`, err);
      failed++;
    }
  }

  return { synced, failed };
}
