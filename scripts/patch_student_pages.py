import os

def patch_student_home():
    path = os.path.join("frontend", "src", "pages", "StudentHome.tsx")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "clearStoredAuth" not in content:
        content = content.replace(
            "import { useState, useEffect } from 'react';",
            "import { useState, useEffect } from 'react';\nimport { clearStoredAuth } from '../services/auth';\nimport { AUTH_EXPIRED_EVENT } from '../api/client';"
        )

    old_fetch = """        // 1. Fetch recent attempts
        const res = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/attempts`, { headers });
        if (res.ok && isMounted) {
          const data = await res.json();
          setRecentAttempts((data.attempts || []).slice(0, 5));
        }

        // 2. Fetch canonical single-source-of-truth metrics
        const mRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/metrics`, { headers });
        if (mRes.ok && isMounted) {
          const mData = await mRes.json();
          setCanonicalMetrics(mData);
        }

        // 3. Fetch spaced retrieval retention queue
        const srRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/spaced-retrieval`, { headers });
        if (srRes.ok && isMounted) {
          const srData = await srRes.json();
          setSpacedQueue(srData);
        }"""

    new_fetch = """        // 1. Fetch recent attempts
        const res = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/attempts`, { headers });
        if (res.status === 401) {
          clearStoredAuth();
          if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
          return;
        }
        if (res.ok && isMounted) {
          const data = await res.json();
          setRecentAttempts((data.attempts || []).slice(0, 5));
        }

        // 2. Fetch canonical single-source-of-truth metrics
        const mRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/metrics`, { headers });
        if (mRes.status === 401) {
          clearStoredAuth();
          if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
          return;
        }
        if (mRes.ok && isMounted) {
          const mData = await mRes.json();
          setCanonicalMetrics(mData);
        }

        // 3. Fetch spaced retrieval retention queue
        const srRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/spaced-retrieval`, { headers });
        if (srRes.status === 401) {
          clearStoredAuth();
          if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
          return;
        }
        if (srRes.ok && isMounted) {
          const srData = await srRes.json();
          setSpacedQueue(srData);
        }"""

    if old_fetch in content:
        content = content.replace(old_fetch, new_fetch, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[PATCHED] StudentHome.tsx updated with 401 session expiration handling.")
    else:
        print("[SKIP] StudentHome.tsx target not found.")

def patch_student_progress():
    path = os.path.join("frontend", "src", "pages", "StudentProgress.tsx")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "clearStoredAuth" not in content:
        content = content.replace(
            "import { useState, useEffect } from 'react';",
            "import { useState, useEffect } from 'react';\nimport { clearStoredAuth } from '../services/auth';\nimport { AUTH_EXPIRED_EVENT } from '../api/client';"
        )

    old_snippet = """        const res = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/attempts`, { headers });
        if (res.ok && isMounted) {
          const data = await res.json();
          setAttempts(data.attempts || []);
        }"""

    new_snippet = """        const res = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/attempts`, { headers });
        if (res.status === 401) {
          clearStoredAuth();
          if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
          return;
        }
        if (res.ok && isMounted) {
          const data = await res.json();
          setAttempts(data.attempts || []);
        }"""

    if old_snippet in content:
        content = content.replace(old_snippet, new_snippet, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[PATCHED] StudentProgress.tsx updated with 401 session expiration handling.")

def patch_student_insights():
    path = os.path.join("frontend", "src", "pages", "StudentInsights.tsx")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "clearStoredAuth" not in content:
        content = content.replace(
            "import { useState, useEffect } from 'react';",
            "import { useState, useEffect } from 'react';\nimport { clearStoredAuth } from '../services/auth';\nimport { AUTH_EXPIRED_EVENT } from '../api/client';"
        )

    old_m = """        const mRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/metrics`, { headers });
        if (mRes.ok && isMounted) {
          const mData = await mRes.json();
          setMetrics(mData);
        }"""

    new_m = """        const mRes = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/metrics`, { headers });
        if (mRes.status === 401) {
          clearStoredAuth();
          if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));
          return;
        }
        if (mRes.ok && isMounted) {
          const mData = await mRes.json();
          setMetrics(mData);
        }"""

    if old_m in content:
        content = content.replace(old_m, new_m, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[PATCHED] StudentInsights.tsx updated with 401 session expiration handling.")

if __name__ == "__main__":
    patch_student_home()
    patch_student_progress()
    patch_student_insights()

