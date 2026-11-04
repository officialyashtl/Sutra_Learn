import os

def patch_unified_login():
    path = os.path.join("frontend", "src", "pages", "UnifiedLogin.tsx")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    target = "  const [error, setError] = useState<string | null>(null);"
    replacement = """  const [error, setError] = useState<string | null>(() => {
    if (typeof window !== 'undefined' && window.location.search.includes('session_expired=true')) {
      return 'Your session has expired. Please sign in again with your credentials.';
    }
    return null;
  });"""
    if target in content:
        content = content.replace(target, replacement, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[PATCHED] UnifiedLogin.tsx updated with session expiration banner.")
    else:
        print("[SKIP] UnifiedLogin.tsx already patched or target not found.")

def patch_student_tutor():
    path = os.path.join("frontend", "src", "pages", "StudentTutor.tsx")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure clearStoredAuth and AUTH_EXPIRED_EVENT can be dispatched
    if "AUTH_EXPIRED_EVENT" not in content:
        content = content.replace(
            "import { useState, useEffect, useRef, useCallback } from 'react';",
            "import { useState, useEffect, useRef, useCallback } from 'react';\nimport { clearStoredAuth } from '../services/auth';\nimport { AUTH_EXPIRED_EVENT } from '../api/client';"
        )

    # 2. In loadConversationDetail: check for 401
    old_detail = """        if (res.ok) {
          const data = await res.json();
          setActiveConversationId(convId);
          setMessages(data.messages || []);
          if (data.conversation?.concept_id) {
            setSelectedConceptId(data.conversation.concept_id);
          }
        }"""
    new_detail = """        if (res.status === 401) {
          clearStoredAuth();
          if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
          return;
        }
        if (res.ok) {
          const data = await res.json();
          setActiveConversationId(convId);
          setMessages(data.messages || []);
          if (data.conversation?.concept_id) {
            setSelectedConceptId(data.conversation.concept_id);
          }
        }"""
    if old_detail in content:
        content = content.replace(old_detail, new_detail, 1)

    # 3. In loadConversations: check for 401
    old_load = """        if (res.ok) {
          const data = await res.json();
          setConversations(data);
          if (selectFirstIfAvailable && data.length > 0 && !activeConversationId) {
            void loadConversationDetail(data[0].id);
          }
        } else {
          setConversationsError('Unable to load past sessions.');
        }"""
    new_load = """        if (res.status === 401) {
          clearStoredAuth();
          if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
          return;
        }
        if (res.ok) {
          const data = await res.json();
          setConversations(data);
          if (selectFirstIfAvailable && data.length > 0 && !activeConversationId) {
            void loadConversationDetail(data[0].id);
          }
        } else {
          setConversationsError('Unable to load past sessions.');
        }"""
    if old_load in content:
        content = content.replace(old_load, new_load, 1)

    # 4. In handleSendMessage: check for 401
    old_chat = """      if (!res.ok) {
        const errJson = await res.json();
        throw new Error(errJson.detail || 'Failed to receive tutor response.');
      }"""
    new_chat = """      if (res.status === 401) {
        clearStoredAuth();
        if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
        throw new Error('Your session has expired. Please sign in again.');
      }
      if (!res.ok) {
        const errJson = await res.json();
        throw new Error(errJson.detail || 'Failed to receive tutor response.');
      }"""
    if old_chat in content:
        content = content.replace(old_chat, new_chat, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[PATCHED] StudentTutor.tsx 401 handling updated.")

def patch_app_component():
    path = os.path.join("frontend", "src", "App.tsx")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update handleAuthExpired to include query param session_expired=true
    old_expired = """    const handleAuthExpired = () => {
      clearStoredAuth();
      setAuthToken(null);
      navigate('/login');
    };"""
    new_expired = """    const handleAuthExpired = () => {
      clearStoredAuth();
      setAuthToken(null);
      navigate('/login?session_expired=true');
    };"""
    if old_expired in content:
        content = content.replace(old_expired, new_expired, 1)

    # 2. In syncStudentData: if progressRes returns 401, clear and redirect
    old_sync = """      const progressRes = await fetch(`${API_BASE_URL}/api/v1/learners/${learnerId}/progress`, { headers: authHeader });
      if (progressRes.ok) {
        const pData = await progressRes.json();
        if (pData.concept_progress) {
          const map: Record<string, ConceptProgress> = {};
          pData.concept_progress.forEach((cp: any) => {
            map[cp.concept_id] = {
              status: cp.status || 'not_started',
              accuracy: cp.accuracy || 0,
              attempts: cp.attempts || 0,
              mastery_score: cp.mastery_score || 0,
            };
          });
          setProgressMap(map);
        }
      } else {
        throw new Error(`Progress API returned status ${progressRes.status}`);
      }"""
    new_sync = """      const progressRes = await fetch(`${API_BASE_URL}/api/v1/learners/${learnerId}/progress`, { headers: authHeader });
      if (progressRes.status === 401) {
        clearStoredAuth();
        setAuthToken(null);
        navigate('/login?session_expired=true');
        return;
      }
      if (progressRes.ok) {
        const pData = await progressRes.json();
        if (pData.concept_progress) {
          const map: Record<string, ConceptProgress> = {};
          pData.concept_progress.forEach((cp: any) => {
            map[cp.concept_id] = {
              status: cp.status || 'not_started',
              accuracy: cp.accuracy || 0,
              attempts: cp.attempts || 0,
              mastery_score: cp.mastery_score || 0,
            };
          });
          setProgressMap(map);
        }
      } else {
        throw new Error(`Progress API returned status ${progressRes.status}`);
      }"""
    if old_sync in content:
        content = content.replace(old_sync, new_sync, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[PATCHED] App.tsx 401 redirect updated.")

if __name__ == "__main__":
    patch_unified_login()
    patch_student_tutor()
    patch_app_component()

