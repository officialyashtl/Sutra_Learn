import type { AttemptSubmission, Concept } from '../types';

const DB_NAME = 'sutra_learn_db';
const DB_VERSION = 1;

export function openOfflineDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    if (!('indexedDB' in window)) {
      return reject(new Error('IndexedDB not supported in this environment'));
    }

    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      if (!db.objectStoreNames.contains('pending_attempts')) {
        db.createObjectStore('pending_attempts', { keyPath: 'attempt_id' });
      }
      if (!db.objectStoreNames.contains('cached_content')) {
        db.createObjectStore('cached_content', { keyPath: 'key' });
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export async function savePendingAttempt(attempt: AttemptSubmission): Promise<void> {
  const db = await openOfflineDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('pending_attempts', 'readwrite');
    const store = tx.objectStore('pending_attempts');
    const record = { ...attempt, sync_status: 'pending' };
    const req = store.put(record);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export async function getPendingAttempts(): Promise<AttemptSubmission[]> {
  try {
    const db = await openOfflineDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('pending_attempts', 'readonly');
      const store = tx.objectStore('pending_attempts');
      const req = store.getAll();
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = () => reject(req.error);
    });
  } catch (err) {
    console.warn('Could not read from IndexedDB:', err);
    return [];
  }
}

export async function deletePendingAttempt(attempt_id: string): Promise<void> {
  const db = await openOfflineDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('pending_attempts', 'readwrite');
    const store = tx.objectStore('pending_attempts');
    const req = store.delete(attempt_id);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export async function cacheConcepts(concepts: Concept[]): Promise<void> {
  try {
    const db = await openOfflineDB();
    const tx = db.transaction('cached_content', 'readwrite');
    const store = tx.objectStore('cached_content');
    store.put({ key: 'concepts_list', data: concepts, timestamp: Date.now() });
  } catch (err) {
    console.warn('Failed to cache concepts locally:', err);
  }
}

export async function getCachedConcepts(): Promise<Concept[] | null> {
  try {
    const db = await openOfflineDB();
    return new Promise((resolve) => {
      const tx = db.transaction('cached_content', 'readonly');
      const store = tx.objectStore('cached_content');
      const req = store.get('concepts_list');
      req.onsuccess = () => resolve(req.result ? req.result.data : null);
      req.onerror = () => resolve(null);
    });
  } catch {
    return null;
  }
}
