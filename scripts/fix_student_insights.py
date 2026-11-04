path = 'frontend/src/pages/StudentInsights.tsx'
lines = open(path, encoding='utf-8').read().splitlines()
out = []
for l in lines:
    out.append(l)
    if 'const res = await fetch(`${apiBaseUrl}/api/v1/learners/${learner.id}/metrics`' in l:
        out.append('        if (res.status === 401) {')
        out.append('          clearStoredAuth();')
        out.append('          if (typeof window !== "undefined") window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT));')
        out.append('          return;')
        out.append('        }')
open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('Successfully fixed StudentInsights.tsx')

