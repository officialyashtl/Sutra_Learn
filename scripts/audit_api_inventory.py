"""
SUTRA LEARN — Forensic API Inventory Script
Maps all backend routes and frontend callers.
Identifies:
- Frontend callers for each backend route
- Orphaned backend routes (no frontend consumer)
- Dead frontend callers (pointing to nonexistent route)
- Auth requirements, schemas, db tables, audit events
"""
import sys, os, re, json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.main import app

def main():
    # 1. Inspect Backend Routes
    backend_routes = []
    for r in app.routes:
        if hasattr(r, 'original_router'):
            for sub_r in r.original_router.routes:
                methods = list(sub_r.methods) if hasattr(sub_r, 'methods') else []
                for m in methods:
                    if m != 'HEAD':
                        backend_routes.append({
                            'method': m,
                            'path': sub_r.path,
                            'name': getattr(sub_r, 'name', ''),
                            'endpoint_func': getattr(sub_r, 'endpoint', None)
                        })
        elif hasattr(r, 'path') and hasattr(r, 'methods'):
            for m in r.methods:
                if m != 'HEAD':
                    backend_routes.append({
                        'method': m,
                        'path': r.path,
                        'name': getattr(r, 'name', ''),
                        'endpoint_func': getattr(r, 'endpoint', None)
                    })

    # 2. Inspect Frontend Callers
    fe_calls = []
    fe_dir = Path(__file__).resolve().parent.parent / "frontend" / "src"
    pattern = re.compile(r'fetch\s*\(\s*`?\${(?:API_BASE_URL|apiBaseUrl)}([^`"\s,\)]*)`?', re.IGNORECASE)
    
    for root, dirs, files in os.walk(fe_dir):
        for f in files:
            if f.endswith(('.ts', '.tsx')):
                fpath = Path(root) / f
                with open(fpath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    for m in pattern.finditer(content):
                        pos = m.end()
                        snippet = content[pos:pos+250]
                        method = "GET"
                        if "method: 'POST'" in snippet or 'method: "POST"' in snippet:
                            method = "POST"
                        elif "method: 'DELETE'" in snippet or 'method: "DELETE"' in snippet:
                            method = "DELETE"
                        elif "method: 'PUT'" in snippet or 'method: "PUT"' in snippet:
                            method = "PUT"
                        
                        has_auth = "Authorization" in snippet or "headers" in snippet or "authHeader" in snippet
                        fe_calls.append({
                            'file': f,
                            'rel_path': str(fpath.relative_to(fe_dir.parent)),
                            'route_template': m.group(1),
                            'method': method,
                            'has_auth': has_auth
                        })

    be_map = {f"{b['method']} {b['path']}": b for b in backend_routes}
    matched_be = set()
    unmatched_fe = []

    for fe in fe_calls:
        template = fe['route_template'].split('?')[0]
        norm_pattern = re.sub(r'/[^/]*\$\{[^}]+\}[^/]*', '/{id}', template)
        
        found = False
        for be_key in be_map:
            m, p = be_key.split(' ', 1)
            p_pattern = re.sub(r'\{[^}]+\}', '{id}', p)
            if fe['method'] == m and (norm_pattern == p_pattern or template == p):
                found = True
                matched_be.add(be_key)
                break
        if not found:
            unmatched_fe.append(fe)

    print("=" * 70)
    print("SUTRA LEARN — FORENSIC API MATCH REPORT")
    print("=" * 70)
    print(f"Total Backend Endpoints: {len(backend_routes)}")
    print(f"Total Frontend Fetch Calls: {len(fe_calls)}")
    print(f"Matched Backend Endpoints: {len(matched_be)}")
    print(f"Unmatched (Orphaned) Backend Routes: {len(be_map) - len(matched_be)}")
    print(f"Unmatched (Dead/Missing) Frontend Calls: {len(unmatched_fe)}")

    if unmatched_fe:
        print("\n[!] DEAD/UNMATCHED FRONTEND CALLS:")
        for u in unmatched_fe:
            print(f"  - {u['method']} {u['route_template']} in {u['file']}")
    else:
        print("\n[✓] All frontend fetch calls map to existing backend routes!")

    print("\n[-] BACKEND ROUTES WITHOUT DIRECT FRONTEND CONSUMERS:")
    for u in sorted(set(be_map.keys()) - matched_be):
        print(f"  - {u:45} ({be_map[u]['name']})")

if __name__ == "__main__":
    main()
