import os

with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import_target = "import { getStoredToken, getStoredUser, clearStoredAuth } from './services/auth';"
import_replacement = "import { getStoredToken, getStoredUser, clearStoredAuth } from './services/auth';\nimport { AUTH_EXPIRED_EVENT } from './api/client';"

if import_target in content:
    content = content.replace(import_target, import_replacement, 1)
    print("Import target replaced.")
else:
    print("Import target not found.")

listener_target = "  useEffect(() => {\n    const handlePopState = () => {"
listener_replacement = """  useEffect(() => {
    const handleAuthExpired = () => {
      clearStoredAuth();
      setAuthToken(null);
      navigate('/login');
    };
    window.addEventListener(AUTH_EXPIRED_EVENT, handleAuthExpired);
    return () => window.removeEventListener(AUTH_EXPIRED_EVENT, handleAuthExpired);
  }, [navigate]);

  useEffect(() => {
    const handlePopState = () => {"""

if listener_target in content:
    content = content.replace(listener_target, listener_replacement, 1)
    print("Listener target replaced.")
else:
    # Try with CRLF
    listener_target_crlf = "  useEffect(() => {\r\n    const handlePopState = () => {"
    listener_replacement_crlf = listener_replacement.replace("\n", "\r\n")
    if listener_target_crlf in content:
        content = content.replace(listener_target_crlf, listener_replacement_crlf, 1)
        print("Listener target CRLF replaced.")
    else:
        print("Listener target not found.")

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated frontend/src/App.tsx")

