/**
 * SUTRA LEARN - Client Authentication and Token Storage Service
 * Manages Bearer tokens for student and teacher personas.
 */

const TOKEN_KEY = 'sutra_auth_token';
const USER_KEY = 'sutra_auth_user';

export interface AuthSession {
  access_token: string;
  token_type: string;
  user_id: string;
  name: string;
  role: string;
  expires_in: number;
  redirect_to?: string;
  user?: {
    id: string;
    name: string;
    role: string;
    grade: number;
  };
}

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function getStoredUser(): AuthSession | null {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function clearStoredAuth(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

/**
 * Standard username & password login against backend PBKDF2 hashes.
 */
export async function loginWithCredentials(
  apiBaseUrl: string,
  identifier: string,
  password: string
): Promise<AuthSession> {
  const res = await fetch(`${apiBaseUrl}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ identifier, username: identifier, password }),
  });

  if (!res.ok) {
    const errorJson = await res.json().catch(() => ({}));
    throw new Error(errorJson.detail || 'Invalid username or password.');
  }

  const session: AuthSession = await res.json();
  setStoredToken(session.access_token);
  localStorage.setItem(USER_KEY, JSON.stringify(session));
  return session;
}

/**
 * Request a cryptographically signed Bearer token from the server for a verified persona.
 */
export async function authenticatePersona(apiBaseUrl: string, learnerId: string): Promise<string> {
  try {
    const res = await fetch(`${apiBaseUrl}/api/v1/auth/session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ learner_id: learnerId }),
    });

    if (!res.ok) {
      throw new Error(`Session creation failed: ${res.statusText}`);
    }

    const data: AuthSession = await res.json();
    setStoredToken(data.access_token);
    localStorage.setItem(USER_KEY, JSON.stringify(data));
    return data.access_token;
  } catch (err) {
    console.error('Failed to authenticate persona:', err);
    throw err;
  }
}

/**
 * Standard headers helper to include the Bearer token
 */
export function getAuthHeaders(token?: string | null): Record<string, string> {
  const currentToken = token || getStoredToken();
  const headers: Record<string, string> = {};
  if (currentToken) {
    headers['Authorization'] = `Bearer ${currentToken}`;
  }
  return headers;
}
