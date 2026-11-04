path = 'frontend/src/pages/AssessmentView.tsx'
content = open(path, encoding='utf-8').read()
content = content.replace(
    "import { savePendingAttempt, getPendingAttempts } from '../offline/db';",
    "import { savePendingAttempt, getPendingAttempts } from '../offline/db';\nimport { clearStoredAuth } from '../services/auth';\nimport { AUTH_EXPIRED_EVENT } from '../api/client';"
)
open(path, 'w', encoding='utf-8').write(content)
print('Fixed AssessmentView imports.')

