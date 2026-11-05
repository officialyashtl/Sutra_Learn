import urllib.request
import ssl
import json
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

print('=== 1. HOMEPAGE HTML PROBE ===')
try:
    req = urllib.request.Request('https://sutralearn.vercel.app/', headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=15) as res:
        html = res.read().decode('utf-8')
        print('HTTP Status:', res.status)
        print('HTML Length:', len(html))
        
        # Check title
        title_m = re.search(r'<title>(.*?)</title>', html)
        print('Title:', title_m.group(1) if title_m else 'MISSING')
        
        # Check canonical
        canonical_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html)
        print('Canonical:', canonical_m.group(1) if canonical_m else 'MISSING')
        
        # Check meta description
        desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html)
        print('Description:', desc_m.group(1) if desc_m else 'MISSING')
        
        # Check OpenGraph
        og_title = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', html)
        og_img = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', html)
        print('OG Title:', og_title.group(1) if og_title else 'MISSING')
        print('OG Image:', og_img.group(1) if og_img else 'MISSING')
        
        # Check JSON-LD
        json_ld = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html, re.DOTALL)
        print(f'JSON-LD Scripts Found: {len(json_ld)}')
        for idx, s in enumerate(json_ld):
            try:
                data = json.loads(s.strip())
                print(f'  Script {idx+1}: @type = {data.get("@type")} -> {data.get("name") or data.get("headline") or "Schema OK"}')
            except Exception as e:
                print(f'  Script {idx+1} parse error: {e}')
except Exception as e:
    print('Homepage probe error:', e)

print('\n=== 2. ROBOTS.TXT PROBE ===')
try:
    req_rob = urllib.request.Request('https://sutralearn.vercel.app/robots.txt', headers=headers)
    with urllib.request.urlopen(req_rob, context=ctx, timeout=15) as res:
        rob_txt = res.read().decode('utf-8')
        print('HTTP Status:', res.status)
        print('Content:\n' + rob_txt.strip())
except Exception as e:
    print('Robots probe error:', e)

print('\n=== 3. SITEMAP.XML PROBE ===')
try:
    req_sm = urllib.request.Request('https://sutralearn.vercel.app/sitemap.xml', headers=headers)
    with urllib.request.urlopen(req_sm, context=ctx, timeout=15) as res:
        sm_txt = res.read().decode('utf-8')
        print('HTTP Status:', res.status)
        locs = re.findall(r'<loc>(.*?)</loc>', sm_txt)
        print(f'Sitemap URLs ({len(locs)}):', locs)
except Exception as e:
    print('Sitemap probe error:', e)

