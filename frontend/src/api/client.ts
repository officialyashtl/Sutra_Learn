/**
 * SUTRA LEARN — Unified API Client & Request Trace Interceptor
 * Automatically injects Bearer credentials and correlation IDs.
 * Intercepts 401 Unauthorized responses to prevent cascade auth failures.
 */

import { getStoredToken, clearStoredAuth } from '../services/auth';

export const API_BASE_URL: string =
  import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export interface RequestOptions extends RequestInit {
  authToken?: string | null;
  correlationId?: string;
  skipAuth?: boolean;
}

/**
 * Custom event dispatched when a 401 Unauthorized response is received,
 * alerting App.tsx to cleanly reset state and prompt for re-authentication.
 */
export const AUTH_EXPIRED_EVENT = 'sutra:auth-expired';

export function generateCorrelationId(): string {
  return `req_fe_${Math.random().toString(36).substring(2, 10)}_${Date.now()}`;
}

export async function apiClient<T = any>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
  const token = options.authToken !== undefined ? options.authToken : getStoredToken();
  const correlationId = options.correlationId || generateCorrelationId();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-Correlation-ID': correlationId,
    ...(options.headers as Record<string, string> || {}),
  };

  if (!options.skipAuth && token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(url, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    console.warn(`[API Client 401] Session expired or invalid on ${endpoint} (CID: ${correlationId})`);
    clearStoredAuth();
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT, { detail: { endpoint, correlationId } }));
    }
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Authentication required or session expired.');
  }

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Request failed with HTTP ${res.status}`);
  }

  if (res.status === 204) {
    return {} as T;
  }

  return (await res.json()) as T;
}

export function apiGet<T = any>(endpoint: string, options?: RequestOptions): Promise<T> {
  return apiClient<T>(endpoint, { ...options, method: 'GET' });
}

export function apiPost<T = any>(endpoint: string, body?: any, options?: RequestOptions): Promise<T> {
  return apiClient<T>(endpoint, {
    ...options,
    method: 'POST',
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
}

export function apiDelete<T = any>(endpoint: string, options?: RequestOptions): Promise<T> {
  return apiClient<T>(endpoint, { ...options, method: 'DELETE' });
}

