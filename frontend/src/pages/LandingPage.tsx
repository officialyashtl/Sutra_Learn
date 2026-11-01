import { useState } from 'react';
import type { Concept } from '../types';
import { DeveloperSignature } from '../components/DeveloperSignature';

interface LandingPageProps {
  onStartLearning: () => void;
  onExploreWorkspace: () => void;
  onViewConcept: (conceptId: string) => void;
  onViewPathway: () => void;
  concepts: Concept[];
  isAuthenticated: boolean;
  currentUserRole?: 'student' | 'teacher';
}

const FALLBACK_FEATURED_CONCEPTS: Concept[] = [
  {
    id: 'MATH-C01',
    code: 'MATH-C01',
    title: 'Integer Arithmetic & Sign Rules',
    grade: 8,
    subject: 'Mathematics',
    description: 'Master operations on negative numbers and sign transformation across equation balances.',
    prerequisites: [],
    order_index: 1,
  },
  {
    id: 'MATH-C02',
    code: 'MATH-C02',
    title: 'One-Step Linear Equations',
    grade: 8,
    subject: 'Mathematics',
    description: 'Solve single-variable linear equations using additive and multiplicative inverses.',
    prerequisites: ['MATH-C01'],
    order_index: 2,
  },
  {
    id: 'MATH-C05',
    code: 'MATH-C05',
    title: 'Equations with Variables on Both Sides',
    grade: 8,
    subject: 'Mathematics',
    description: 'Rearrange and isolate variable terms across the equality balance with rigorous transpositions.',
    prerequisites: ['MATH-C03', 'MATH-C04'],
    order_index: 5,
  },
  {
    id: 'MATH-C07',
    code: 'MATH-C07',
    title: 'Rational Numbers & Closure Properties',
    grade: 8,
    subject: 'Mathematics',
    description: 'Properties of rational numbers: closure, commutativity, and associativity under arithmetic.',
    prerequisites: [],
    order_index: 7,
  },
  {
    id: 'MATH-C09',
    code: 'MATH-C09',
    title: 'Understanding Quadrilaterals & Angle Sums',
    grade: 8,
    subject: 'Mathematics',
    description: 'Convex and concave polygons, interior and exterior angle sums, and quadrilateral classifications.',
    prerequisites: [],
    order_index: 9,
  },
  {
    id: 'MATH-C13',
    code: 'MATH-C13',
    title: 'Squares & Square Roots by Prime Factorisation',
    grade: 8,
    subject: 'Mathematics',
    description: 'Perfect square patterns, Pythagorean triplets, and extracting square roots via prime factors.',
    prerequisites: [],
    order_index: 13,
  },
  {
    id: 'MATH-C21',
    code: 'MATH-C21',
    title: 'Area of Trapezium & General Quadrilaterals',
    grade: 8,
    subject: 'Mathematics',
    description: 'Derivation and application of area formulas for trapeziums, rhombuses, and irregular polygons.',
    prerequisites: [],
    order_index: 21,
  },
  {
    id: 'MATH-C23',
    code: 'MATH-C23',
    title: 'Powers with Negative Exponents & Exponent Laws',
    grade: 8,
    subject: 'Mathematics',
    description: 'Multiplicative and quotient laws of integral exponents, scientific notation, and scale comparisons.',
    prerequisites: [],
    order_index: 23,
  },
];

export function LandingPage({
  onStartLearning,
  onExploreWorkspace,
  onViewConcept,
  onViewPathway,
  concepts,
  isAuthenticated,
  currentUserRole,
}: LandingPageProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Featured concepts to show in the register
  const featuredIds = ['MATH-C01', 'MATH-C02', 'MATH-C05', 'MATH-C07', 'MATH-C09', 'MATH-C13', 'MATH-C21', 'MATH-C23'];
  const resolvedConcepts = concepts.length > 0 ? concepts : FALLBACK_FEATURED_CONCEPTS;
  const featuredConcepts = featuredIds
    .map((id) => resolvedConcepts.find((c) => c.id === id) || FALLBACK_FEATURED_CONCEPTS.find((c) => c.id === id))
    .filter((c): c is Concept => !!c);

  const scrollTo = (id: string) => {
    setMobileMenuOpen(false);
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const getChapterName = (conceptId: string): string => {
    switch (conceptId) {
      case 'MATH-C07':
      case 'MATH-C08':
        return 'Ch 1 · Rational Numbers';
      case 'MATH-C01':
      case 'MATH-C02':
      case 'MATH-C03':
      case 'MATH-C04':
      case 'MATH-C05':
      case 'MATH-C06':
        return 'Ch 2 · Linear Equations';
      case 'MATH-C09':
      case 'MATH-C10':
        return 'Ch 3 · Quadrilaterals';
      case 'MATH-C11':
      case 'MATH-C12':
        return 'Ch 4 · Data Handling';
      case 'MATH-C13':
      case 'MATH-C14':
        return 'Ch 5 · Squares & Roots';
      case 'MATH-C15':
      case 'MATH-C16':
        return 'Ch 6 · Cubes & Roots';
      case 'MATH-C17':
      case 'MATH-C18':
        return 'Ch 7 · Comparing Quantities';
      case 'MATH-C19':
      case 'MATH-C20':
        return 'Ch 8 · Algebraic Identities';
      case 'MATH-C21':
      case 'MATH-C22':
        return 'Ch 9 · Mensuration';
      case 'MATH-C23':
      case 'MATH-C24':
        return 'Ch 10 · Exponents & Powers';
      case 'MATH-C25':
      case 'MATH-C26':
        return 'Ch 11 · Direct & Inverse';
      case 'MATH-C27':
      case 'MATH-C28':
        return 'Ch 12 · Factorisation';
      case 'MATH-C29':
      case 'MATH-C30':
        return 'Ch 13 · Intro to Graphs';
      default:
        return 'NCERT Class 8';
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: 'var(--surface-paper)', color: 'var(--text-primary)', display: 'flex', flexDirection: 'column' }}>
      {/* =========================================================================
          SECTION 01 — NAVIGATION BAR
          ========================================================================= */}
      <nav
        aria-label="Main Navigation"
        style={{
          position: 'sticky',
          top: 0,
          zIndex: 100,
          backgroundColor: 'rgba(248, 245, 239, 0.94)',
          backdropFilter: 'blur(10px)',
          borderBottom: '1px solid var(--border-subtle)',
          padding: '0 var(--space-6)',
          height: '68px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        {/* Left: Brand Identity */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
          <div
            style={{
              width: '36px',
              height: '36px',
              backgroundColor: 'var(--sutra-espresso)',
              color: 'var(--surface-paper)',
              borderRadius: 'var(--radius-sm)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontFamily: 'var(--font-display)',
              fontWeight: 700,
              fontSize: '20px',
              boxShadow: '0 1px 3px rgba(41,28,14,0.12)',
            }}
          >
            S
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="brand-wordmark" style={{ fontSize: '18px', letterSpacing: '0.04em', color: 'var(--sutra-espresso)' }}>
                SUTRA LEARN
              </span>
              <span
                style={{
                  fontSize: '10px',
                  fontFamily: 'var(--font-mono)',
                  padding: '1px 6px',
                  borderRadius: '10px',
                  backgroundColor: 'var(--surface-linen)',
                  color: 'var(--sutra-mocha)',
                  fontWeight: 600,
                }}
              >
                CLASS 8
              </span>
            </div>
            <span style={{ display: 'block', fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginTop: '-2px' }}>
              Adaptive Learning &bull; Educational Intelligence
            </span>
          </div>
        </div>

        {/* Center: Desktop Navigation Links */}
        <div className="landing-desktop-nav" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-6)' }}>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '13px', fontWeight: 600, color: 'var(--sutra-espresso)', padding: '6px 10px' }}
            onClick={() => scrollTo('home')}
          >
            Home
          </button>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '13px', fontWeight: 500, color: 'var(--text-secondary)', padding: '6px 10px' }}
            onClick={() => scrollTo('how-it-works')}
          >
            How It Works
          </button>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '13px', fontWeight: 500, color: 'var(--text-secondary)', padding: '6px 10px' }}
            onClick={() => scrollTo('technology')}
          >
            Technology
          </button>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '13px', fontWeight: 500, color: 'var(--text-secondary)', padding: '6px 10px' }}
            onClick={() => scrollTo('curriculum')}
          >
            Learning
          </button>
          <button
            type="button"
            className="btn-ghost"
            style={{ fontSize: '13px', fontWeight: 500, color: 'var(--text-secondary)', padding: '6px 10px' }}
            onClick={onExploreWorkspace}
          >
            Workspace
          </button>
        </div>

        {/* Right: Primary Action & Mobile Hamburger */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
          <button
            type="button"
            className="btn-primary landing-cta-btn"
            style={{
              fontSize: '13px',
              padding: '9px 18px',
              height: '38px',
              backgroundColor: 'var(--sutra-mocha)',
              color: 'var(--surface-white)',
              borderRadius: 'var(--radius-sm)',
            }}
            onClick={onStartLearning}
          >
            {isAuthenticated ? (currentUserRole === 'teacher' ? 'Open Dashboard' : 'Continue Study') : 'Explore SUTRA'} &rarr;
          </button>

          {/* Mobile Menu Toggle Button */}
          <button
            type="button"
            className="landing-mobile-toggle"
            aria-label="Toggle navigation menu"
            aria-expanded={mobileMenuOpen}
            style={{
              display: 'none',
              background: 'transparent',
              border: '1px solid var(--border-default)',
              borderRadius: 'var(--radius-sm)',
              padding: '6px 10px',
              cursor: 'pointer',
              color: 'var(--sutra-espresso)',
              fontSize: '18px',
            }}
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>
      </nav>

      {/* Mobile Dropdown Menu */}
      {mobileMenuOpen && (
        <div
          style={{
            position: 'fixed',
            top: '68px',
            left: 0,
            right: 0,
            backgroundColor: 'var(--surface-paper)',
            borderBottom: '1px solid var(--border-default)',
            padding: 'var(--space-4) var(--space-6)',
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--space-3)',
            zIndex: 99,
            boxShadow: '0 8px 16px rgba(41,28,14,0.08)',
          }}
        >
          <button type="button" className="btn-ghost" style={{ textAlign: 'left', padding: '10px 0' }} onClick={() => scrollTo('home')}>
            Home
          </button>
          <button type="button" className="btn-ghost" style={{ textAlign: 'left', padding: '10px 0' }} onClick={() => scrollTo('how-it-works')}>
            How It Works
          </button>
          <button type="button" className="btn-ghost" style={{ textAlign: 'left', padding: '10px 0' }} onClick={() => scrollTo('technology')}>
            Technology
          </button>
          <button type="button" className="btn-ghost" style={{ textAlign: 'left', padding: '10px 0' }} onClick={() => scrollTo('curriculum')}>
            Curriculum Concepts
          </button>
          <button type="button" className="btn-ghost" style={{ textAlign: 'left', padding: '10px 0' }} onClick={onExploreWorkspace}>
            Workspace
          </button>
          <button type="button" className="btn-primary" style={{ marginTop: 'var(--space-2)', width: '100%' }} onClick={onStartLearning}>
            {isAuthenticated ? 'Open Dashboard' : 'Explore SUTRA'} &rarr;
          </button>
        </div>
      )}

      {/* =========================================================================
          SECTION 02 — TWO-COLUMN HERO SECTION
          ========================================================================= */}
      <header
        id="home"
        style={{
          maxWidth: '1240px',
          width: '100%',
          margin: '0 auto',
          padding: 'var(--space-12) var(--space-6) var(--space-16)',
        }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(min(320px, 100%), 1fr))',
            gap: 'var(--space-10)',
            alignItems: 'center',
          }}
        >
          {/* Left Column: Editorial Value Proposition */}
          <div style={{ maxWidth: '640px' }}>
            <div className="editorial-kicker">ADAPTIVE LEARNING / EDUCATIONAL INTELLIGENCE</div>
            <h1
              className="serif-display"
              style={{
                fontSize: 'clamp(34px, 4.5vw, 52px)',
                color: 'var(--sutra-espresso)',
                lineHeight: 1.15,
                marginTop: 'var(--space-2)',
                letterSpacing: '-0.01em',
              }}
            >
              Every student deserves a learning path{' '}
              <span style={{ color: 'var(--sutra-mocha)', fontStyle: 'italic', fontWeight: 600 }}>
                that understands them.
              </span>
            </h1>
            <p
              style={{
                fontSize: '16px',
                color: 'var(--text-secondary)',
                marginTop: 'var(--space-5)',
                lineHeight: 1.65,
                maxWidth: '560px',
              }}
            >
              SUTRA LEARN transforms everyday learning into a personalized journey through structured lessons,
              adaptive practice, intelligent assistance, and measurable progress.
            </p>

            {/* Buttons */}
            <div style={{ display: 'flex', gap: 'var(--space-4)', marginTop: 'var(--space-8)', flexWrap: 'wrap' }}>
              <button
                type="button"
                className="btn-primary"
                style={{
                  height: '48px',
                  padding: '0 var(--space-6)',
                  fontSize: '14px',
                  backgroundColor: 'var(--sutra-mocha)',
                  color: 'var(--surface-white)',
                  borderRadius: 'var(--radius-sm)',
                  boxShadow: '0 2px 6px rgba(110, 71, 59, 0.25)',
                }}
                onClick={onStartLearning}
              >
                Start Learning &rarr;
              </button>
              <button
                type="button"
                className="btn-secondary"
                style={{
                  height: '48px',
                  padding: '0 var(--space-6)',
                  fontSize: '14px',
                  border: '1px solid var(--border-default)',
                  backgroundColor: 'var(--surface-white)',
                  color: 'var(--sutra-espresso)',
                  borderRadius: 'var(--radius-sm)',
                }}
                onClick={() => scrollTo('how-it-works')}
              >
                See How It Works
              </button>
            </div>

            {/* Four Compact Platform Indicators */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(2, 1fr)',
                gap: 'var(--space-4)',
                marginTop: 'var(--space-10)',
                paddingTop: 'var(--space-6)',
                borderTop: '1px solid var(--border-subtle)',
              }}
            >
              <div>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', display: 'block' }}>
                  Supported Curriculum
                </span>
                <strong style={{ fontSize: '14px', color: 'var(--sutra-espresso)', marginTop: '2px', display: 'block' }}>
                  NCERT Class 8 Mathematics
                </strong>
              </div>
              <div>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', display: 'block' }}>
                  Learning Concepts
                </span>
                <strong style={{ fontSize: '14px', color: 'var(--sutra-espresso)', marginTop: '2px', display: 'block' }}>
                  30 Concepts &bull; 13 Chapters
                </strong>
              </div>
              <div>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', display: 'block' }}>
                  Adaptive Pathways
                </span>
                <strong style={{ fontSize: '14px', color: 'var(--sutra-espresso)', marginTop: '2px', display: 'block' }}>
                  4 Deterministic Decisions
                </strong>
              </div>
              <div>
                <span style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', display: 'block' }}>
                  Platform Experience
                </span>
                <strong style={{ fontSize: '14px', color: 'var(--sutra-espresso)', marginTop: '2px', display: 'block' }}>
                  Unified Student & Educator Portals
                </strong>
              </div>
            </div>
          </div>

          {/* Right Column: Architectural Curriculum & Mathematical Continuum Folio Plate */}
          <div style={{ width: '100%', maxWidth: '640px', justifySelf: 'center' }}>
            <div
              className="editorial-card"
              style={{
                backgroundColor: 'var(--surface-white)',
                border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-md)',
                boxShadow: '0 16px 40px -8px rgba(41,28,14,0.07)',
                padding: 'clamp(20px, 3.5vw, 32px)',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              {/* Plate Header: Fine Archival Registration */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: 'var(--space-4)',
                  paddingBottom: 'var(--space-3)',
                  borderBottom: '1px solid var(--border-subtle)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span
                    style={{
                      fontFamily: 'var(--font-mono)',
                      fontSize: '11px',
                      fontWeight: 700,
                      letterSpacing: '0.08em',
                      color: 'var(--sutra-espresso)',
                    }}
                  >
                    PLATE I · MATHEMATICAL CONTINUUM
                  </span>
                </div>
                <span
                  style={{
                    fontSize: '10px',
                    fontFamily: 'var(--font-mono)',
                    color: 'var(--text-muted)',
                    letterSpacing: '0.05em',
                  }}
                >
                  CURRICULUM ONTOLOGY
                </span>
              </div>

              {/* Central Graphic: Premium SVG Vector Representation */}
              <div
                style={{
                  width: '100%',
                  aspectRatio: '16 / 11',
                  backgroundColor: 'var(--surface-paper)',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  padding: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  position: 'relative',
                }}
              >
                <svg
                  viewBox="0 0 540 370"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  style={{ width: '100%', height: '100%', display: 'block' }}
                  aria-label="Mathematical knowledge continuum diagram"
                >
                  <defs>
                    <linearGradient id="pathwayGradient" x1="40" y1="310" x2="500" y2="70" gradientUnits="userSpaceOnUse">
                      <stop offset="0%" stopColor="#A78D78" />
                      <stop offset="50%" stopColor="#6E473B" />
                      <stop offset="100%" stopColor="#291C0E" />
                    </linearGradient>
                    <linearGradient id="surfaceWash" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#BEB5A9" stopOpacity="0.12" />
                      <stop offset="100%" stopColor="#BEB5A9" stopOpacity="0.02" />
                    </linearGradient>
                    <linearGradient id="haloGlow" x1="0" y1="0" x2="1" y2="1">
                      <stop offset="0%" stopColor="#6E473B" stopOpacity="0.25" />
                      <stop offset="100%" stopColor="#A78D78" stopOpacity="0" />
                    </linearGradient>
                  </defs>

                  {/* Architectural Cartesian & Polar Guides */}
                  <g opacity="0.65">
                    <line x1="30" y1="100" x2="510" y2="100" stroke="#E1D4C2" strokeWidth="0.75" strokeDasharray="3 4" />
                    <line x1="30" y1="185" x2="510" y2="185" stroke="#E1D4C2" strokeWidth="0.75" strokeDasharray="3 4" />
                    <line x1="30" y1="270" x2="510" y2="270" stroke="#E1D4C2" strokeWidth="0.75" strokeDasharray="3 4" />

                    <line x1="120" y1="30" x2="120" y2="340" stroke="#E1D4C2" strokeWidth="0.75" strokeDasharray="3 4" />
                    <line x1="270" y1="30" x2="270" y2="340" stroke="#E1D4C2" strokeWidth="0.75" strokeDasharray="3 4" />
                    <line x1="420" y1="30" x2="420" y2="340" stroke="#E1D4C2" strokeWidth="0.75" strokeDasharray="3 4" />

                    <circle cx="270" cy="185" r="145" stroke="#E1D4C2" strokeWidth="0.8" strokeDasharray="4 4" />
                    <circle cx="270" cy="185" r="95" stroke="#E1D4C2" strokeWidth="0.8" />
                    <circle cx="270" cy="185" r="45" stroke="#BEB5A9" strokeWidth="0.8" strokeDasharray="2 3" />

                    <line x1="80" y1="330" x2="460" y2="40" stroke="#E1D4C2" strokeWidth="0.7" />
                    <line x1="40" y1="185" x2="500" y2="185" stroke="#BEB5A9" strokeWidth="1" />
                    <line x1="270" y1="25" x2="270" y2="345" stroke="#BEB5A9" strokeWidth="1" />
                  </g>

                  {/* Shaded Area Under Primary Adaptive Curve */}
                  <path
                    d="M 60 320 C 130 310, 160 220, 240 210 C 320 200, 390 120, 480 65 L 480 320 Z"
                    fill="url(#surfaceWash)"
                  />

                  {/* Prerequisite & Convergence Connector Sutras (Fine Threads) */}
                  <g stroke="#BEB5A9" strokeWidth="1">
                    <line x1="90" y1="300" x2="180" y2="235" strokeDasharray="2 3" />
                    <line x1="180" y1="235" x2="270" y2="185" strokeDasharray="2 3" />
                    <line x1="270" y1="185" x2="380" y2="135" strokeDasharray="2 3" />
                    <line x1="380" y1="135" x2="465" y2="75" strokeDasharray="2 3" />

                    <line x1="90" y1="300" x2="90" y2="320" stroke="#A78D78" strokeWidth="0.8" strokeDasharray="2 2" />
                    <line x1="180" y1="235" x2="180" y2="320" stroke="#A78D78" strokeWidth="0.8" strokeDasharray="2 2" />
                    <line x1="270" y1="185" x2="270" y2="320" stroke="#A78D78" strokeWidth="0.8" strokeDasharray="2 2" />
                    <line x1="380" y1="135" x2="380" y2="320" stroke="#A78D78" strokeWidth="0.8" strokeDasharray="2 2" />
                    <line x1="465" y1="75" x2="465" y2="320" stroke="#A78D78" strokeWidth="0.8" strokeDasharray="2 2" />
                  </g>

                  {/* Primary Adaptive Pathway Spine */}
                  <path
                    d="M 60 320 C 130 310, 160 220, 240 210 C 320 200, 390 120, 480 65"
                    stroke="#E1D4C2"
                    strokeWidth="8"
                    strokeLinecap="round"
                    opacity="0.5"
                  />
                  <path
                    d="M 60 320 C 130 310, 160 220, 240 210 C 320 200, 390 120, 480 65"
                    stroke="url(#pathwayGradient)"
                    strokeWidth="2.5"
                    strokeLinecap="round"
                  />

                  {/* Harmonic Wave Secondary Thread */}
                  <path
                    d="M 60 280 Q 170 330, 270 185 T 480 110"
                    stroke="#A78D78"
                    strokeWidth="1.2"
                    strokeDasharray="5 4"
                    fill="none"
                    opacity="0.75"
                  />

                  {/* Mathematical Equilibrium Nodes */}
                  <g>
                    <circle cx="90" cy="300" r="14" fill="#F8F5EF" stroke="#BEB5A9" strokeWidth="1.2" />
                    <circle cx="90" cy="300" r="5" fill="#6E473B" />
                    <text x="90" y="328" textAnchor="middle" fill="#291C0E" fontFamily="var(--font-mono)" fontSize="9" fontWeight="600" letterSpacing="0.04em">
                      I · AXIOM
                    </text>
                    <text x="90" y="280" textAnchor="middle" fill="#6E473B" fontFamily="var(--font-serif)" fontSize="10" fontStyle="italic">
                      a + (-a) = 0
                    </text>
                  </g>

                  <g>
                    <circle cx="180" cy="235" r="15" fill="#F8F5EF" stroke="#A78D78" strokeWidth="1.2" />
                    <circle cx="180" cy="235" r="5" fill="#6E473B" />
                    <text x="180" y="263" textAnchor="middle" fill="#291C0E" fontFamily="var(--font-mono)" fontSize="9" fontWeight="600" letterSpacing="0.04em">
                      II · BALANCE
                    </text>
                    <text x="180" y="214" textAnchor="middle" fill="#6E473B" fontFamily="var(--font-serif)" fontSize="10" fontStyle="italic">
                      ax + b = c
                    </text>
                  </g>

                  <g>
                    <circle cx="270" cy="185" r="24" fill="url(#haloGlow)" />
                    <circle cx="270" cy="185" r="17" fill="#FFFEFC" stroke="#6E473B" strokeWidth="1.8" />
                    <circle cx="270" cy="185" r="7" fill="#291C0E" />
                    <text x="270" y="148" textAnchor="middle" fill="#291C0E" fontFamily="var(--font-serif)" fontSize="12" fontWeight="600" fontStyle="italic">
                      LHS ≡ RHS
                    </text>
                    <text x="270" y="222" textAnchor="middle" fill="#291C0E" fontFamily="var(--font-mono)" fontSize="9.5" fontWeight="700" letterSpacing="0.06em">
                      III · EQUILIBRIUM
                    </text>
                  </g>

                  <g>
                    <circle cx="380" cy="135" r="15" fill="#F8F5EF" stroke="#A78D78" strokeWidth="1.2" />
                    <circle cx="380" cy="135" r="5" fill="#6E473B" />
                    <text x="380" y="163" textAnchor="middle" fill="#291C0E" fontFamily="var(--font-mono)" fontSize="9" fontWeight="600" letterSpacing="0.04em">
                      IV · SYNTHESIS
                    </text>
                    <text x="380" y="114" textAnchor="middle" fill="#6E473B" fontFamily="var(--font-serif)" fontSize="10" fontStyle="italic">
                      Σ Δ → f(x)
                    </text>
                  </g>

                  <g>
                    <circle cx="465" cy="75" r="16" fill="#F8F5EF" stroke="#291C0E" strokeWidth="1.5" />
                    <polygon points="465,66 468,73 475,75 468,77 465,84 462,77 455,75 462,73" fill="#6E473B" />
                    <text x="465" y="103" textAnchor="middle" fill="#291C0E" fontFamily="var(--font-mono)" fontSize="9" fontWeight="600" letterSpacing="0.04em">
                      V · MASTERY
                    </text>
                    <text x="465" y="55" textAnchor="middle" fill="#6E473B" fontFamily="var(--font-serif)" fontSize="10" fontStyle="italic">
                      Q.E.D.
                    </text>
                  </g>

                  <text x="40" y="55" fill="#BEB5A9" fontFamily="var(--font-serif)" fontSize="11" fontStyle="italic">
                    ∀ x ∈ ℝ · Invariant Foundations
                  </text>
                  <text x="500" y="335" textAnchor="end" fill="#BEB5A9" fontFamily="var(--font-mono)" fontSize="9">
                    DIM: 2D · CONTINUOUS
                  </text>
                </svg>
              </div>

              {/* Plate Footer: Minimal, Dignified Architectural Notes */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginTop: 'var(--space-4)',
                  paddingTop: 'var(--space-3)',
                  borderTop: '1px solid var(--border-subtle)',
                  fontSize: '11px',
                  color: 'var(--text-secondary)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span
                    style={{
                      width: '6px',
                      height: '6px',
                      borderRadius: '50%',
                      backgroundColor: 'var(--sutra-mocha)',
                      display: 'inline-block',
                    }}
                  />
                  <span style={{ fontWeight: 500 }}>
                    Deterministic Knowledge Topology
                  </span>
                </div>
                <span
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: '10px',
                    color: 'var(--text-muted)',
                    letterSpacing: '0.04em',
                  }}
                >
                  30 CONCEPTS · 13 CHAPTERS
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* =========================================================================
          SECTION 03 — WHAT WE DO (FOUR EQUAL CARDS)
          ========================================================================= */}
      <section
        id="how-it-works"
        style={{
          backgroundColor: 'var(--surface-warm)',
          borderTop: '1px solid var(--border-subtle)',
          borderBottom: '1px solid var(--border-subtle)',
          padding: 'var(--space-16) var(--space-6)',
        }}
      >
        <div style={{ maxWidth: '1240px', margin: '0 auto' }}>
          {/* Section Header */}
          <div style={{ textAlign: 'center', maxWidth: '680px', margin: '0 auto var(--space-12)' }}>
            <div className="editorial-kicker">WHAT WE DO</div>
            <h2 className="serif-display" style={{ fontSize: 'clamp(28px, 3.5vw, 40px)', color: 'var(--sutra-espresso)', marginTop: 'var(--space-2)' }}>
              From learning content to confident understanding.
            </h2>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: 'var(--space-3)', lineHeight: 1.6 }}>
              SUTRA connects curriculum, adaptive practice, intelligent assistance, and measurable progress into one connected learning experience.
            </p>
          </div>

          {/* Four Equal Cards Grid */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(min(260px, 100%), 1fr))',
              gap: 'var(--space-6)',
            }}
          >
            {/* Card 01: Personalized Learning */}
            <div
              className="editorial-card"
              style={{
                backgroundColor: 'var(--surface-white)',
                border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-md)',
                padding: 'var(--space-6)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                transition: 'transform 0.2s ease, box-shadow 0.2s ease',
              }}
            >
              <div>
                <div
                  style={{
                    width: '38px',
                    height: '38px',
                    borderRadius: 'var(--radius-xs)',
                    backgroundColor: 'var(--surface-paper)',
                    border: '1px solid var(--border-default)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: 'var(--space-4)',
                    fontSize: '18px',
                  }}
                >
                  📖
                </div>
                <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginBottom: 'var(--space-2)' }}>
                  Personalized Learning
                </h3>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  Structured NCERT Class 8 lessons with clear pedagogical objectives, verified key principles, and progressive worked examples.
                </p>
              </div>

              <div style={{ marginTop: 'var(--space-6)', paddingTop: 'var(--space-4)', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--sutra-mocha)', fontWeight: 600 }}>
                  01 &bull; LESSONS
                </span>
                <button
                  type="button"
                  className="btn-ghost"
                  style={{ fontSize: '13px', color: 'var(--sutra-mocha)', padding: 0, fontWeight: 700 }}
                  onClick={onStartLearning}
                >
                  &rarr;
                </button>
              </div>
            </div>

            {/* Card 02: Adaptive Practice */}
            <div
              className="editorial-card"
              style={{
                backgroundColor: 'var(--surface-white)',
                border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-md)',
                padding: 'var(--space-6)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                transition: 'transform 0.2s ease, box-shadow 0.2s ease',
              }}
            >
              <div>
                <div
                  style={{
                    width: '38px',
                    height: '38px',
                    borderRadius: 'var(--radius-xs)',
                    backgroundColor: 'var(--surface-paper)',
                    border: '1px solid var(--border-default)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: 'var(--space-4)',
                    fontSize: '18px',
                  }}
                >
                  ⚖️
                </div>
                <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginBottom: 'var(--space-2)' }}>
                  Adaptive Practice
                </h3>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  Deterministic diagnostic assessments that pinpoint exact misconception traps and automatically bridge upstream prerequisite gaps.
                </p>
              </div>

              <div style={{ marginTop: 'var(--space-6)', paddingTop: 'var(--space-4)', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--sutra-mocha)', fontWeight: 600 }}>
                  02 &bull; ADAPTIVE ENGINE
                </span>
                <button
                  type="button"
                  className="btn-ghost"
                  style={{ fontSize: '13px', color: 'var(--sutra-mocha)', padding: 0, fontWeight: 700 }}
                  onClick={onStartLearning}
                >
                  &rarr;
                </button>
              </div>
            </div>

            {/* Card 03: AI Learning Assistant */}
            <div
              className="editorial-card"
              style={{
                backgroundColor: 'var(--surface-white)',
                border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-md)',
                padding: 'var(--space-6)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                transition: 'transform 0.2s ease, box-shadow 0.2s ease',
              }}
            >
              <div>
                <div
                  style={{
                    width: '38px',
                    height: '38px',
                    borderRadius: 'var(--radius-xs)',
                    backgroundColor: 'var(--surface-paper)',
                    border: '1px solid var(--border-default)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: 'var(--space-4)',
                    fontSize: '18px',
                  }}
                >
                  💡
                </div>
                <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginBottom: 'var(--space-2)' }}>
                  AI Learning Assistant
                </h3>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  Curriculum-grounded Socratic tutor with deterministic mathematical validation to explain concepts, guide steps, and eliminate hallucinations.
                </p>
              </div>

              <div style={{ marginTop: 'var(--space-6)', paddingTop: 'var(--space-4)', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--sutra-mocha)', fontWeight: 600 }}>
                  03 &bull; SOCRATIC TUTOR
                </span>
                <button
                  type="button"
                  className="btn-ghost"
                  style={{ fontSize: '13px', color: 'var(--sutra-mocha)', padding: 0, fontWeight: 700 }}
                  onClick={onStartLearning}
                >
                  &rarr;
                </button>
              </div>
            </div>

            {/* Card 04: Teacher Intelligence */}
            <div
              className="editorial-card"
              style={{
                backgroundColor: 'var(--surface-white)',
                border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-md)',
                padding: 'var(--space-6)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                transition: 'transform 0.2s ease, box-shadow 0.2s ease',
              }}
            >
              <div>
                <div
                  style={{
                    width: '38px',
                    height: '38px',
                    borderRadius: 'var(--radius-xs)',
                    backgroundColor: 'var(--surface-paper)',
                    border: '1px solid var(--border-default)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: 'var(--space-4)',
                    fontSize: '18px',
                  }}
                >
                  📊
                </div>
                <h3 className="serif-title" style={{ fontSize: '20px', color: 'var(--sutra-espresso)', marginBottom: 'var(--space-2)' }}>
                  Teacher Intelligence
                </h3>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  Real-time classroom cohort diagnostics, prerequisite bottleneck tracking, and pedagogical intervention tools for educators.
                </p>
              </div>

              <div style={{ marginTop: 'var(--space-6)', paddingTop: 'var(--space-4)', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--sutra-mocha)', fontWeight: 600 }}>
                  04 &bull; EDUCATOR SUITE
                </span>
                <button
                  type="button"
                  className="btn-ghost"
                  style={{ fontSize: '13px', color: 'var(--sutra-mocha)', padding: 0, fontWeight: 700 }}
                  onClick={onStartLearning}
                >
                  &rarr;
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 04 — TECHNOLOGY SHOWCASE (TWO-COLUMN SPLIT)
          ========================================================================= */}
      <section
        id="technology"
        style={{
          maxWidth: '1240px',
          width: '100%',
          margin: '0 auto',
          padding: 'var(--space-16) var(--space-6)',
        }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(min(320px, 100%), 1fr))',
            gap: 'var(--space-12)',
            alignItems: 'center',
          }}
        >
          {/* Left Column: Tech Description & 4 Concise Capabilities */}
          <div>
            <div className="editorial-kicker">OUR TECHNOLOGY</div>
            <h2 className="serif-display" style={{ fontSize: 'clamp(28px, 3.5vw, 42px)', color: 'var(--sutra-espresso)', marginTop: 'var(--space-2)' }}>
              Intelligent learning. Grounded decisions.
            </h2>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: 'var(--space-4)', lineHeight: 1.65 }}>
              SUTRA LEARN couples a deterministic adaptive engine with multi-model AI infrastructure. Every pedagogical recommendation is reproducible,
              and all generated explanations undergo mathematical step-consistency validation.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)', marginTop: 'var(--space-6)' }}>
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 'var(--space-3)' }}>
                <span style={{ color: 'var(--sutra-mocha)', fontWeight: 700, fontSize: '16px' }}>✓</span>
                <div>
                  <strong style={{ fontSize: '14px', color: 'var(--sutra-espresso)' }}>Curriculum-Grounded Learning</strong>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px', lineHeight: 1.5 }}>
                    All 30 concepts across 13 NCERT chapters follow a verified Directed Acyclic Graph (DAG) with zero circular dependencies.
                  </p>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 'var(--space-3)' }}>
                <span style={{ color: 'var(--sutra-mocha)', fontWeight: 700, fontSize: '16px' }}>✓</span>
                <div>
                  <strong style={{ fontSize: '14px', color: 'var(--sutra-espresso)' }}>Deterministic Adaptive Engine</strong>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px', lineHeight: 1.5 }}>
                    Rule-based policy enforcing Stretch ($\ge 85\%$), Scaffold, Bridge Back, and Teacher Review with bit-exact reproducibility.
                  </p>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 'var(--space-3)' }}>
                <span style={{ color: 'var(--sutra-mocha)', fontWeight: 700, fontSize: '16px' }}>✓</span>
                <div>
                  <strong style={{ fontSize: '14px', color: 'var(--sutra-espresso)' }}>Mathematical Validation</strong>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px', lineHeight: 1.5 }}>
                    Dedicated AST and algebraic transformation verifier that automatically rejects contradictory AI steps or arithmetic falsehoods.
                  </p>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 'var(--space-3)' }}>
                <span style={{ color: 'var(--sutra-mocha)', fontWeight: 700, fontSize: '16px' }}>✓</span>
                <div>
                  <strong style={{ fontSize: '14px', color: 'var(--sutra-espresso)' }}>Multi-Model AI Orchestration</strong>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '2px', lineHeight: 1.5 }}>
                    Transparent cascade from Google Gemini to local Ollama (Qwen 3.5 4B & Gemma 4 E2B) with sub-2ms deterministic fallback.
                  </p>
                </div>
              </div>
            </div>

            <button
              type="button"
              className="btn-primary"
              style={{
                marginTop: 'var(--space-8)',
                height: '46px',
                padding: '0 var(--space-6)',
                fontSize: '13px',
                backgroundColor: 'var(--sutra-espresso)',
                color: 'var(--surface-paper)',
                borderRadius: 'var(--radius-sm)',
              }}
              onClick={onExploreWorkspace}
            >
              Explore Workspace &rarr;
            </button>
          </div>

          {/* Right Column: SUTRA CONSOLE / OVERVIEW Mockup */}
          <div>
            <div
              className="editorial-card"
              style={{
                backgroundColor: 'var(--surface-white)',
                border: '1px solid var(--border-default)',
                borderRadius: 'var(--radius-md)',
                boxShadow: '0 8px 28px rgba(41,28,14,0.07)',
                padding: 'var(--space-6)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-4)', paddingBottom: 'var(--space-3)', borderBottom: '1px solid var(--border-subtle)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--feedback-success)' }} />
                  <span style={{ fontSize: '11px', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--sutra-espresso)', letterSpacing: '0.06em' }}>
                    SUTRA CONSOLE / OVERVIEW
                  </span>
                </div>
                <span style={{ fontSize: '10px', fontFamily: 'var(--font-mono)', color: 'var(--sutra-mocha)' }}>
                  SQLITE WAL &bull; FASTAPI
                </span>
              </div>

              {/* Console KPI Metrics */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 'var(--space-3)', marginBottom: 'var(--space-5)' }}>
                <div style={{ backgroundColor: 'var(--surface-paper)', padding: 'var(--space-3)', borderRadius: 'var(--radius-xs)', border: '1px solid var(--border-subtle)' }}>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', display: 'block' }}>Verified Concepts</span>
                  <strong style={{ fontSize: '18px', color: 'var(--sutra-espresso)' }}>30 / 30</strong>
                </div>
                <div style={{ backgroundColor: 'var(--surface-paper)', padding: 'var(--space-3)', borderRadius: 'var(--radius-xs)', border: '1px solid var(--border-subtle)' }}>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', display: 'block' }}>Diagnostic Items</span>
                  <strong style={{ fontSize: '18px', color: 'var(--sutra-espresso)' }}>81 Questions</strong>
                </div>
                <div style={{ backgroundColor: 'var(--surface-paper)', padding: 'var(--space-3)', borderRadius: 'var(--radius-xs)', border: '1px solid var(--border-subtle)' }}>
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', display: 'block' }}>Fallback Latency</span>
                  <strong style={{ fontSize: '18px', color: 'var(--feedback-success)' }}>1.56 ms</strong>
                </div>
              </div>

              {/* Cohort Learner Persona Roster Preview */}
              <div style={{ marginBottom: 'var(--space-5)' }}>
                <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
                  Active Class 8 Cohort Personas
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: 'var(--space-2)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '6px 10px', backgroundColor: 'var(--surface-paper)', borderRadius: 'var(--radius-xs)', fontSize: '12px' }}>
                    <span><strong>Aarav Sharma</strong> (student-01)</span>
                    <span className="status-pill mastered" style={{ fontSize: '10px' }}>88% Accuracy &bull; Stretch</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '6px 10px', backgroundColor: 'var(--surface-paper)', borderRadius: 'var(--radius-xs)', fontSize: '12px' }}>
                    <span><strong>Diya Patel</strong> (student-02)</span>
                    <span className="status-pill in_progress" style={{ fontSize: '10px' }}>72% Accuracy &bull; Scaffold</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '6px 10px', backgroundColor: 'var(--surface-paper)', borderRadius: 'var(--radius-xs)', fontSize: '12px' }}>
                    <span><strong>Kabir Sen</strong> (student-03)</span>
                    <span className="status-pill needs_reinforcement" style={{ fontSize: '10px' }}>Bridge to MATH-C01</span>
                  </div>
                </div>
              </div>

              {/* Provider Cascade Status */}
              <div>
                <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
                  Multi-Model AI Infrastructure Status
                </span>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px', marginTop: 'var(--space-2)', fontSize: '11px' }}>
                  <div style={{ padding: '6px 8px', backgroundColor: 'var(--surface-paper)', borderRadius: 'var(--radius-xs)', borderLeft: '3px solid var(--sutra-mocha)' }}>
                    <span>Ollama Qwen 3.5 4B: <strong>Available</strong></span>
                  </div>
                  <div style={{ padding: '6px 8px', backgroundColor: 'var(--surface-paper)', borderRadius: 'var(--radius-xs)', borderLeft: '3px solid var(--feedback-success)' }}>
                    <span>Curriculum Engine: <strong>100% SLA</strong></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 05 — CURRICULUM AND LEARNING CONCEPTS (REGISTER STYLE)
          ========================================================================= */}
      <section
        id="curriculum"
        style={{
          backgroundColor: 'var(--surface-warm)',
          borderTop: '1px solid var(--border-subtle)',
          borderBottom: '1px solid var(--border-subtle)',
          padding: 'var(--space-16) var(--space-6)',
        }}
      >
        <div style={{ maxWidth: '1240px', margin: '0 auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 'var(--space-8)', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
            <div>
              <div className="editorial-kicker">CURRICULUM / CONCEPT REGISTER</div>
              <h2 className="serif-display" style={{ fontSize: 'clamp(28px, 3.5vw, 40px)', color: 'var(--sutra-espresso)', marginTop: 'var(--space-2)' }}>
                Structured learning. One concept at a time.
              </h2>
              <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: 'var(--space-2)', maxWidth: '640px' }}>
                Explore the curriculum through connected chapters, concepts, prerequisites, and measurable learning progression.
              </p>
            </div>
            <button
              type="button"
              className="btn-secondary"
              style={{ fontSize: '13px', padding: '8px 16px', backgroundColor: 'var(--surface-white)' }}
              onClick={onViewPathway}
            >
              View Full 30-Concept Interactive Pathway &rarr;
            </button>
          </div>

          {/* Cards Grid */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(min(280px, 100%), 1fr))',
              gap: 'var(--space-5)',
            }}
          >
            {featuredConcepts.map((c) => (
              <div
                key={c.id}
                className="editorial-card"
                style={{
                  backgroundColor: 'var(--surface-white)',
                  border: '1px solid var(--border-default)',
                  borderRadius: 'var(--radius-md)',
                  padding: 'var(--space-5)',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  borderTop: '3px solid var(--sutra-mocha)',
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                    <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                      {c.id} &bull; {c.code}
                    </span>
                    <span style={{ fontSize: '10px', color: 'var(--sutra-mocha)', fontWeight: 600 }}>
                      {getChapterName(c.id)}
                    </span>
                  </div>

                  <h3 className="serif-title" style={{ fontSize: '17px', color: 'var(--sutra-espresso)', marginBottom: '6px' }}>
                    {c.title}
                  </h3>
                  <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: 'var(--space-3)' }}>
                    {c.description}
                  </p>

                  {c.prerequisites && c.prerequisites.length > 0 && (
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: 'var(--space-3)' }}>
                      Prerequisites: <strong style={{ color: 'var(--sutra-mocha)' }}>{c.prerequisites.join(', ')}</strong>
                    </div>
                  )}
                </div>

                <div style={{ marginTop: 'var(--space-4)', paddingTop: 'var(--space-3)', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span className="status-pill not_started" style={{ fontSize: '10px' }}>
                    Grade 8 Core
                  </span>
                  <button
                    type="button"
                    className="btn-ghost"
                    style={{ fontSize: '12px', color: 'var(--sutra-mocha)', padding: 0, fontWeight: 600 }}
                    onClick={() => onViewConcept(c.id)}
                  >
                    View Concept &rarr;
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 06 — FINAL CTA BANNER
          ========================================================================= */}
      <section
        style={{
          maxWidth: '1240px',
          width: '100%',
          margin: '0 auto',
          padding: 'var(--space-16) var(--space-6)',
        }}
      >
        <div
          className="editorial-card"
          style={{
            backgroundColor: 'var(--sutra-espresso)',
            color: 'var(--surface-paper)',
            borderRadius: 'var(--radius-lg)',
            padding: 'var(--space-12) var(--space-8)',
            textAlign: 'center',
            boxShadow: '0 12px 32px rgba(41,28,14,0.18)',
          }}
        >
          <div style={{ maxWidth: '640px', margin: '0 auto' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--sutra-stone)' }}>
              GET STARTED TODAY
            </span>
            <h2 className="serif-display" style={{ fontSize: 'clamp(28px, 4vw, 44px)', color: 'var(--surface-paper)', margin: 'var(--space-3) 0 var(--space-4) 0' }}>
              Make every learning journey meaningful.
            </h2>
            <p style={{ fontSize: '15px', color: 'var(--sutra-linen)', lineHeight: 1.6, marginBottom: 'var(--space-8)' }}>
              Give students a clearer path to understanding and teachers the insight to make every next step count.
            </p>
            <button
              type="button"
              className="btn-primary"
              style={{
                height: '50px',
                padding: '0 var(--space-8)',
                fontSize: '14px',
                backgroundColor: 'var(--surface-paper)',
                color: 'var(--sutra-espresso)',
                fontWeight: 700,
                borderRadius: 'var(--radius-sm)',
              }}
              onClick={onStartLearning}
            >
              Start Learning &rarr;
            </button>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 07 — FOOTER (THREE COLUMNS)
          ========================================================================= */}
      <footer
        style={{
          backgroundColor: 'var(--surface-warm)',
          borderTop: '1px solid var(--border-default)',
          padding: 'var(--space-12) var(--space-6) var(--space-8)',
          marginTop: 'auto',
        }}
      >
        <div
          style={{
            maxWidth: '1240px',
            margin: '0 auto',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(min(220px, 100%), 1fr))',
            gap: 'var(--space-8)',
            marginBottom: 'var(--space-10)',
          }}
        >
          {/* Column 1: Brand Wordmark & Description */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', marginBottom: 'var(--space-3)' }}>
              <div
                style={{
                  width: '30px',
                  height: '30px',
                  backgroundColor: 'var(--sutra-espresso)',
                  color: 'var(--surface-paper)',
                  borderRadius: 'var(--radius-xs)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontFamily: 'var(--font-display)',
                  fontWeight: 700,
                  fontSize: '16px',
                }}
              >
                S
              </div>
              <span className="brand-wordmark" style={{ fontSize: '17px', color: 'var(--sutra-espresso)' }}>
                SUTRA LEARN
              </span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.6, maxWidth: '300px' }}>
              Adaptive, evidence-driven educational platform grounding artificial intelligence in verified curriculum architectures.
            </p>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: 'var(--space-4)' }}>
              &copy; 2026 SUTRA LEARN &bull; All rights reserved.
            </div>
          </div>

          {/* Column 2: Navigation Links */}
          <div>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--sutra-mocha)' }}>
              Navigation
            </span>
            <ul style={{ listStyle: 'none', padding: 0, margin: 'var(--space-3) 0 0 0', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              <li>
                <button type="button" className="btn-ghost" style={{ padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }} onClick={() => scrollTo('home')}>
                  Home
                </button>
              </li>
              <li>
                <button type="button" className="btn-ghost" style={{ padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }} onClick={() => scrollTo('how-it-works')}>
                  How It Works
                </button>
              </li>
              <li>
                <button type="button" className="btn-ghost" style={{ padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }} onClick={() => scrollTo('technology')}>
                  Technology
                </button>
              </li>
              <li>
                <button type="button" className="btn-ghost" style={{ padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }} onClick={() => scrollTo('curriculum')}>
                  Learning
                </button>
              </li>
              <li>
                <button type="button" className="btn-ghost" style={{ padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }} onClick={onExploreWorkspace}>
                  Workspace
                </button>
              </li>
            </ul>
          </div>

          {/* Column 3: Platform Architecture */}
          <div>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--sutra-mocha)' }}>
              Platform Architecture
            </span>
            <ul style={{ listStyle: 'none', padding: 0, margin: 'var(--space-3) 0 0 0', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              <li>
                <button type="button" className="btn-ghost" style={{ padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }} onClick={() => scrollTo('technology')}>
                  Educational Intelligence
                </button>
              </li>
              <li>
                <button type="button" className="btn-ghost" style={{ padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }} onClick={() => scrollTo('how-it-works')}>
                  Adaptive Learning Engine
                </button>
              </li>
              <li>
                <button type="button" className="btn-ghost" style={{ padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }} onClick={onStartLearning}>
                  Student Experience
                </button>
              </li>
              <li>
                <button type="button" className="btn-ghost" style={{ padding: 0, fontSize: '12px', color: 'var(--text-secondary)' }} onClick={onExploreWorkspace}>
                  Teacher Experience
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div style={{ maxWidth: '1240px', margin: '0 auto', paddingTop: 'var(--space-4)', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 'var(--space-3)', fontSize: '11px', color: 'var(--text-muted)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <span>SUTRA LEARN v2.0 &bull; Release Candidate 10,000</span>
            <span style={{ color: 'var(--border-default)' }}>&bull;</span>
            <span>NCERT Class 8 Mathematics</span>
          </div>
          <DeveloperSignature />
        </div>
      </footer>

      {/* Responsive Styles Injection */}
      <style>{`
        @media (max-width: 880px) {
          .landing-desktop-nav {
            display: none !important;
          }
          .landing-mobile-toggle {
            display: block !important;
          }
          .landing-cta-btn {
            font-size: 11px !important;
            padding: 6px 12px !important;
          }
        }
      `}</style>
    </div>
  );
}
