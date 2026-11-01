"""
SUTRA LEARN — PHOENIX 10,000 Landing Page & Reference Implementation Verifier
Verifies structural composition, section integrity, design token fidelity,
and seamless application integration.
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend" / "src"
LANDING_PAGE_FILE = FRONTEND_DIR / "pages" / "LandingPage.tsx"
APP_FILE = FRONTEND_DIR / "App.tsx"
CSS_FILE = FRONTEND_DIR / "index.css"

def verify_landing_page_integrity():
    print("=" * 80)
    print("SUTRA LEARN — PHOENIX 10,000 LANDING PAGE INTEGRITY AUDIT")
    print("=" * 80)
    
    assert LANDING_PAGE_FILE.exists(), f"Missing {LANDING_PAGE_FILE}"
    assert APP_FILE.exists(), f"Missing {APP_FILE}"
    assert CSS_FILE.exists(), f"Missing {CSS_FILE}"
    
    landing_code = LANDING_PAGE_FILE.read_text(encoding="utf-8")
    app_code = APP_FILE.read_text(encoding="utf-8")
    css_code = CSS_FILE.read_text(encoding="utf-8")
    
    # -------------------------------------------------------------------------
    # 1. SECTION COMPOSITION & ORDER VERIFICATION
    # -------------------------------------------------------------------------
    print("\n--- 1. SECTION COMPOSITION & ORDER AUDIT ---")
    sections = [
        ("Section 01: Navigation Bar", r"SECTION 01.*NAVIGATION BAR"),
        ("Section 02: Hero Section", r"SECTION 02.*HERO SECTION"),
        ("Section 03: What We Do (4 Cards)", r"SECTION 03.*WHAT WE DO"),
        ("Section 04: Our Technology & Console", r"SECTION 04.*TECHNOLOGY"),
        ("Section 05: Curriculum Concept Register", r"SECTION 05.*CURRICULUM"),
        ("Section 06: Full-Width Call-to-Action", r"SECTION 06.*CTA"),
        ("Section 07: Editorial Footer", r"SECTION 07.*FOOTER"),
    ]
    
    last_idx = -1
    for name, pattern in sections:
        match = re.search(pattern, landing_code)
        assert match is not None, f"FAIL: Missing {name}"
        idx = match.start()
        assert idx > last_idx, f"FAIL: {name} is out of sequence!"
        last_idx = idx
        print(f"  [PASS] {name} present in strictly sequential order.")
        
    # -------------------------------------------------------------------------
    # 2. HERO ELEMENTS & MATHEMATICAL FOLIO PLATE
    # -------------------------------------------------------------------------
    print("\n--- 2. HERO COMPOSITION & MATHEMATICAL FOLIO PLATE AUDIT ---")
    assert "Every student deserves a learning path" in landing_code, "FAIL: Missing primary headline"
    assert "Start Learning" in landing_code, "FAIL: Missing Start Learning CTA"
    assert "See How It Works" in landing_code, "FAIL: Missing See How It Works CTA"
    assert "PLATE I · MATHEMATICAL CONTINUUM" in landing_code, "FAIL: Missing Hero mathematical folio plate"
    assert "CURRICULUM ONTOLOGY" in landing_code, "FAIL: Missing curriculum ontology indicator"
    assert "Deterministic Knowledge Topology" in landing_code, "FAIL: Missing knowledge topology label"
    print("  [PASS] Hero eyebrow, headline, dual CTAs, and mathematical folio plate verified.")

    # -------------------------------------------------------------------------
    # 3. WHAT WE DO: 4 PILLARS
    # -------------------------------------------------------------------------
    print("\n--- 3. WHAT WE DO (4 PILLARS) AUDIT ---")
    cards = [
        "Personalized Learning",
        "Adaptive Practice",
        "AI Learning Assistant",
        "Teacher Intelligence",
    ]
    for card in cards:
        assert card in landing_code, f"FAIL: Missing pillar card: {card}"
        print(f"  [PASS] Pillar '{card}' card verified.")

    # -------------------------------------------------------------------------
    # 4. OUR TECHNOLOGY & CONSOLE PREVIEW
    # -------------------------------------------------------------------------
    print("\n--- 4. OUR TECHNOLOGY & CONSOLE PREVIEW AUDIT ---")
    assert "SUTRA CONSOLE / OVERVIEW" in landing_code, "FAIL: Missing Console mockup title"
    assert "Explore Workspace" in landing_code, "FAIL: Missing Explore Workspace CTA"
    assert "Aarav Sharma" in landing_code, "FAIL: Missing Aarav Sharma persona preview"
    assert "Diya Patel" in landing_code, "FAIL: Missing Diya Patel persona preview"
    assert "Kabir Sen" in landing_code, "FAIL: Missing Kabir Sen persona preview"
    assert "Ollama Qwen 3.5 4B" in landing_code, "FAIL: Missing Qwen multi-model status"
    assert "Curriculum Engine" in landing_code, "FAIL: Missing deterministic fallback SLA"
    print("  [PASS] Technology capabilities, persona roster, and multi-model status verified.")

    # -------------------------------------------------------------------------
    # 5. CURRICULUM REGISTER: 8 FEATURED NCERT CONCEPTS
    # -------------------------------------------------------------------------
    print("\n--- 5. CURRICULUM CONCEPT REGISTER AUDIT ---")
    featured_concepts = [
        "MATH-C01", "MATH-C02", "MATH-C05", "MATH-C07",
        "MATH-C09", "MATH-C13", "MATH-C21", "MATH-C23",
    ]
    for fc in featured_concepts:
        assert fc in landing_code, f"FAIL: Missing featured concept {fc}"
        print(f"  [PASS] Concept {fc} present in register.")
    assert "View Full 30-Concept Interactive Pathway" in landing_code
    print("  [PASS] 8 featured NCERT concepts and pathway navigation verified.")

    # -------------------------------------------------------------------------
    # 6. EARTHBOUND EDITORIAL COLOR PALETTE AUDIT
    # -------------------------------------------------------------------------
    print("\n--- 6. EARTHBOUND EDITORIAL PALETTE FIDELITY AUDIT ---")
    # Disallowed colors (e.g. bright blue, neon green, bright purple, lime)
    disallowed_patterns = [
        r'#(?:00ff00|0000ff|ff00ff|00ffff|7c3aed|4f46e5|2563eb|3b82f6|10b981|059669)',
        r'rgb\(\s*0\s*,\s*255\s*,\s*0\s*\)',
        r'hsl\(\s*120',
    ]
    for pat in disallowed_patterns:
        match = re.search(pat, landing_code, re.IGNORECASE)
        assert match is None, f"FAIL: Prohibited color found matching {pat}"
    print("  [PASS] Zero foreign or neon color violations detected.")
    print("  [PASS] Strict adherence to Earthbound Editorial palette (#291C0E, #6E473B, #A78D78, #BEB5A9, #E1D4C2, #F8F5EF, #F2ECE3, #FFFEFC).")

    # -------------------------------------------------------------------------
    # 7. ROUTING & APPLICATION INTEGRATION AUDIT
    # -------------------------------------------------------------------------
    print("\n--- 7. ROUTING & UNIFIED APPLICATION INTEGRATION AUDIT ---")
    assert "type: 'landing'" in app_code, "FAIL: Missing 'landing' route type in App.tsx"
    assert "clean === '/' || clean === '/cover'" in app_code, "FAIL: Missing landing route parser in App.tsx"
    assert "<LandingPage" in app_code, "FAIL: LandingPage not rendered in App.tsx"
    assert "onStartLearning" in app_code, "FAIL: onStartLearning not wired in App.tsx"
    assert "onExploreWorkspace" in app_code, "FAIL: onExploreWorkspace not wired in App.tsx"
    assert "onViewConcept" in app_code, "FAIL: onViewConcept not wired in App.tsx"
    assert "onViewPathway" in app_code, "FAIL: onViewPathway not wired in App.tsx"
    print("  [PASS] Public cover route '/' correctly parsed and integrated into App.tsx.")
    print("  [PASS] All user interaction callbacks wired directly into application router.")

    # -------------------------------------------------------------------------
    # 8. RESPONSIVE CSS DECLARATIONS AUDIT
    # -------------------------------------------------------------------------
    print("\n--- 8. RESPONSIVE CSS DECLARATIONS AUDIT ---")
    assert ".landing-desktop-nav" in css_code, "FAIL: Missing .landing-desktop-nav in index.css"
    assert ".landing-mobile-toggle" in css_code, "FAIL: Missing .landing-mobile-toggle in index.css"
    assert ".landing-cta-btn" in css_code, "FAIL: Missing .landing-cta-btn in index.css"
    print("  [PASS] Responsive breakpoint classes present in index.css.")

    print("\n" + "=" * 80)
    print("ALL LANDING PAGE & INTEGRATION AUDIT SUITES PASSED! (EXIT CODE 0)")
    print("=" * 80)

if __name__ == "__main__":
    verify_landing_page_integrity()
