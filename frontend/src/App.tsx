import { useState, useEffect, useCallback } from 'react';
import type { Concept, ConceptProgress, Learner, Recommendation, CohortStudentSummary, ConceptAnalytics } from './types';
import { StudentHeader } from './components/StudentHeader';
import { EducatorShell } from './components/EducatorShell';
import type { EducatorTab } from './components/EducatorShell';
import { StudentHome } from './pages/StudentHome';
import { StudentPathway } from './pages/StudentPathway';
import { StudentProgress } from './pages/StudentProgress';
import { StudentInsights } from './pages/StudentInsights';
import { LessonView } from './pages/LessonView';
import { AssessmentView } from './pages/AssessmentView';
import { RecommendationModal } from './pages/RecommendationModal';
import { StudentTutor } from './pages/StudentTutor';
import { UnifiedLogin } from './pages/UnifiedLogin';
import { LandingPage } from './pages/LandingPage';
import { DeveloperSignature } from './components/DeveloperSignature';
import { TeacherDashboard } from './pages/TeacherDashboard';
import { TeacherLearners } from './pages/TeacherLearners';
import { TeacherLearnerProfile } from './pages/TeacherLearnerProfile';
import { TeacherInsights } from './pages/TeacherInsights';
import { TeacherInterventions } from './pages/TeacherInterventions';
import { TeacherAudit } from './pages/TeacherAudit';
import { EducatorAssistant } from './pages/EducatorAssistant';
import { cacheConcepts, getCachedConcepts } from './offline/db';
import { getStoredToken, getStoredUser, clearStoredAuth } from './services/auth';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const DEFAULT_LEARNERS: Learner[] = [
  { id: 'student-01', name: 'Aarav Sharma', grade: 8, role: 'student' },
  { id: 'student-02', name: 'Diya Patel', grade: 8, role: 'student' },
  { id: 'student-03', name: 'Kabir Sen', grade: 8, role: 'student' },
  { id: 'teacher-01', name: 'Ms. Ananya Roy', grade: 8, role: 'teacher' },
];

export type ParsedRoute =
  | { type: 'landing' }
  | { type: 'gateway' }
  | { type: 'student-login' }
  | { type: 'teacher-login' }
  | {
      type: 'student';
      tab: 'home' | 'pathway' | 'progress' | 'insights' | 'tutor';
      action?: 'lesson' | 'assessment';
      conceptId?: string;
    }
  | {
      type: 'teacher';
      tab: EducatorTab;
      learnerId?: string;
    };

function parsePath(pathname: string): ParsedRoute {
  const clean = pathname.replace(/\/+$/, '') || '/';

  if (clean === '/' || clean === '/cover') {
    return { type: 'landing' };
  }
  if (clean === '/portal' || clean === '/gateway' || clean === '/login') {
    return { type: 'gateway' };
  }
  if (clean === '/student/login') {
    return { type: 'gateway' };
  }
  if (clean === '/teacher/login') {
    return { type: 'gateway' };
  }

  // Student Routes
  if (clean === '/student' || clean === '/student/home') {
    return { type: 'student', tab: 'home' };
  }
  if (clean === '/student/pathway' || clean === '/student/my-learning') {
    return { type: 'student', tab: 'pathway' };
  }
  if (clean === '/student/progress') {
    return { type: 'student', tab: 'progress' };
  }
  if (clean === '/student/insights') {
    return { type: 'student', tab: 'insights' };
  }
  if (clean === '/student/tutor') {
    return { type: 'student', tab: 'tutor' };
  }
  const lessonMatch = clean.match(/^\/student\/lesson\/([^/]+)/);
  if (lessonMatch) {
    return { type: 'student', tab: 'home', action: 'lesson', conceptId: lessonMatch[1] };
  }
  const assessMatch = clean.match(/^\/student\/assessment\/([^/]+)/);
  if (assessMatch) {
    return { type: 'student', tab: 'home', action: 'assessment', conceptId: assessMatch[1] };
  }

  // Educator Routes
  if (clean === '/teacher' || clean === '/teacher/dashboard' || clean === '/teacher/overview') {
    return { type: 'teacher', tab: 'overview' };
  }
  if (clean === '/teacher/learners') {
    return { type: 'teacher', tab: 'learners' };
  }
  const learnerProfileMatch = clean.match(/^\/teacher\/learners\/([^/]+)/);
  if (learnerProfileMatch) {
    return { type: 'teacher', tab: 'learners', learnerId: learnerProfileMatch[1] };
  }
  if (clean === '/teacher/insights') {
    return { type: 'teacher', tab: 'insights' };
  }
  if (clean === '/teacher/interventions') {
    return { type: 'teacher', tab: 'interventions' };
  }
  if (clean === '/teacher/assistant') {
    return { type: 'teacher', tab: 'assistant' };
  }
  if (clean === '/teacher/audit') {
    return { type: 'teacher', tab: 'audit' };
  }

  return { type: 'gateway' };
}

export function App() {
  const [learners, setLearners] = useState<Learner[]>(DEFAULT_LEARNERS);
  const [authToken, setAuthToken] = useState<string | null>(getStoredToken());
  const [currentLearner, setCurrentLearner] = useState<Learner>(() => {
    const stored = getStoredUser();
    if (stored) {
      return {
        id: stored.user_id,
        name: stored.name,
        grade: 8,
        role: stored.role as 'student' | 'teacher',
      };
    }
    return DEFAULT_LEARNERS[0];
  });

  // Browser Navigation & Routing State
  const [route, setRoute] = useState<ParsedRoute>(() => {
    if (typeof window !== 'undefined') {
      return parsePath(window.location.pathname);
    }
    return { type: 'landing' };
  });

  // Core Data States
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [progressMap, setProgressMap] = useState<Record<string, ConceptProgress>>({});
  const [cohort, setCohort] = useState<CohortStudentSummary[]>([]);
  const [conceptAnalytics, setConceptAnalytics] = useState<ConceptAnalytics[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Modal State for Adaptive Recommendations
  const [activeRecommendation, setActiveRecommendation] = useState<Recommendation | null>(null);

  const navigate = useCallback((path: string) => {
    window.history.pushState({}, '', path);
    setRoute(parsePath(path));
  }, []);

  useEffect(() => {
    const handlePopState = () => {
      setRoute(parsePath(window.location.pathname));
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Fetch initial learners directory from backend
  useEffect(() => {
    async function loadLearners() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/learners`);
        if (res.ok) {
          const data = await res.json();
          if (data && data.length > 0) setLearners(data);
        }
      } catch (err) {
        console.warn('Could not load learner personas from backend:', err);
      }
    }
    void loadLearners();
  }, []);

  // Fetch public curriculum concepts on initial startup
  useEffect(() => {
    async function loadInitialConcepts() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/concepts`);
        if (res.ok) {
          const data = await res.json();
          const list = data.concepts || [];
          if (list.length > 0) {
            setConcepts(list);
            void cacheConcepts(list);
          }
        }
      } catch (err) {
        console.warn('Could not load initial concepts from backend:', err);
      }
    }
    void loadInitialConcepts();
  }, []);

  // Redirect authenticated users visiting root to their designated dashboard
  useEffect(() => {
    if (route.type === 'landing' && typeof window !== 'undefined' && window.location.pathname !== '/cover') {
      const stored = getStoredUser();
      const token = authToken || getStoredToken();
      if (token && stored) {
        if (stored.role === 'teacher') {
          navigate('/teacher/dashboard');
        } else {
          navigate('/student/home');
        }
      }
    }
  }, [route.type, authToken, navigate]);

  // Sync Student Data (Concepts + Individual Progress)
  const syncStudentData = useCallback(async (learnerId: string, token: string | null) => {
    try {
      setLoading(true);
      setError(null);
      const authHeader: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {};

      const conceptsRes = await fetch(`${API_BASE_URL}/api/v1/concepts`, { headers: authHeader });
      if (conceptsRes.ok) {
        const cData = await conceptsRes.json();
        const list = cData.concepts || [];
        setConcepts(list);
        await cacheConcepts(list);
      } else {
        throw new Error('Failed to fetch curriculum concepts');
      }

      const pRes = await fetch(`${API_BASE_URL}/api/v1/learners/${learnerId}/progress`, { headers: authHeader });
      if (pRes.ok) {
        const pData = await pRes.json();
        const map: Record<string, ConceptProgress> = {};
        (pData.progress || []).forEach((p: ConceptProgress) => {
          map[p.concept_id] = p;
        });
        setProgressMap(map);
      }
    } catch {
      const cached = await getCachedConcepts();
      if (cached && cached.length > 0) {
        setConcepts(cached);
      } else {
        setError('Network unavailable and no cached concepts present. Please connect to continue.');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  // Sync Educator Data (Cohort Diagnostics + Concept Difficulty Analytics)
  const syncEducatorData = useCallback(async (token: string | null) => {
    try {
      setLoading(true);
      setError(null);
      const authHeader: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {};

      const conceptsRes = await fetch(`${API_BASE_URL}/api/v1/concepts`, { headers: authHeader });
      if (conceptsRes.ok) {
        const cData = await conceptsRes.json();
        setConcepts(cData.concepts || []);
      }

      const cohortRes = await fetch(`${API_BASE_URL}/api/v1/teacher/cohort`, { headers: authHeader });
      if (cohortRes.ok) {
        const chData = await cohortRes.json();
        setCohort(chData);
      }

      const analyticsRes = await fetch(`${API_BASE_URL}/api/v1/teacher/analytics/concepts`, { headers: authHeader });
      if (analyticsRes.ok) {
        const aData = await analyticsRes.json();
        setConceptAnalytics(aData);
      }
    } catch (err: any) {
      setError(err.message || 'Error fetching educator cohort diagnostics.');
    } finally {
      setLoading(false);
    }
  }, []);

  // Sync data depending on active route and role
  useEffect(() => {
    let isMounted = true;
    async function initSession() {
      if (route.type === 'student') {
        const stored = getStoredUser();
        const token = authToken || getStoredToken();
        if (!token || stored?.role !== 'student') {
          if (isMounted) navigate('/student/login');
          return;
        }
        if (isMounted && currentLearner.id !== stored.user_id) {
          setCurrentLearner({
            id: stored.user_id,
            name: stored.name,
            grade: 8,
            role: 'student',
          });
        }
        void syncStudentData(stored.user_id, token);
      } else if (route.type === 'teacher') {
        const stored = getStoredUser();
        const token = authToken || getStoredToken();
        if (!token || stored?.role !== 'teacher') {
          if (isMounted) navigate('/teacher/login');
          return;
        }
        if (isMounted && currentLearner.id !== stored.user_id) {
          setCurrentLearner({
            id: stored.user_id,
            name: stored.name,
            grade: 8,
            role: 'teacher',
          });
        }
        void syncEducatorData(token);
      }
    }

    void initSession();
    return () => {
      isMounted = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [route.type]);

  // Handlers for Student Learning Flow
  const handleOpenLesson = async (conceptId: string) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/concepts/${conceptId}`);
      if (res.ok) {
        const detail = await res.json();
        setConcepts((prev) =>
          prev.map((c) => (c.id === conceptId ? { ...c, lesson: detail.lesson } : c))
        );
      }
    } catch (err) {
      console.warn('Using cached lesson detail:', err);
    }
    navigate(`/student/lesson/${conceptId}`);
  };

  const handleOpenAssessment = (conceptId: string) => {
    navigate(`/student/assessment/${conceptId}`);
  };

  const handleCompleteEvaluation = async (conceptId: string) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/recommendations/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        },
        body: JSON.stringify({
          learner_id: currentLearner.id,
          concept_id: conceptId,
        }),
      });

      if (res.ok) {
        const recData: Recommendation = await res.json();
        setActiveRecommendation(recData);
        void syncStudentData(currentLearner.id, authToken);
      }
    } catch (err) {
      console.error('Error running adaptive evaluation:', err);
    }
  };

  const handleRecommendationContinue = (targetConceptId: string, activityType: string) => {
    setActiveRecommendation(null);
    if (activityType === 'lesson') {
      void handleOpenLesson(targetConceptId);
    } else if (['practice', 'diagnostic', 'challenge'].includes(activityType)) {
      handleOpenAssessment(targetConceptId);
    } else {
      navigate('/student/home');
    }
  };

  const handleSignOut = () => {
    clearStoredAuth();
    setAuthToken(null);
    navigate('/');
  };

  // =========================================================================
  // VIEW RENDERER 0: SUTRA LEARN PUBLIC COVER (Earthbound Editorial Landing)
  // =========================================================================
  if (route.type === 'landing') {
    const isAuthed = !!authToken && !!currentLearner;
    return (
      <LandingPage
        concepts={concepts}
        isAuthenticated={isAuthed}
        currentUserRole={isAuthed ? currentLearner.role : undefined}
        onStartLearning={() => {
          if (isAuthed) {
            navigate(currentLearner.role === 'teacher' ? '/teacher/dashboard' : '/student/home');
          } else {
            navigate('/login');
          }
        }}
        onExploreWorkspace={() => {
          if (isAuthed) {
            navigate(currentLearner.role === 'teacher' ? '/teacher/dashboard' : '/student/home');
          } else {
            navigate('/login');
          }
        }}
        onViewConcept={(conceptId) => {
          if (isAuthed) {
            if (currentLearner.role === 'teacher') {
              navigate('/teacher/dashboard');
            } else {
              void handleOpenLesson(conceptId);
            }
          } else {
            navigate('/login');
          }
        }}
        onViewPathway={() => {
          if (isAuthed) {
            navigate(currentLearner.role === 'teacher' ? '/teacher/dashboard' : '/student/pathway');
          } else {
            navigate('/login');
          }
        }}
      />
    );
  }

  // =========================================================================
  // VIEW RENDERER 1: UNIFIED SUTRA IDENTITY & LOGIN (Single Landing & Form)
  // =========================================================================
  if (route.type === 'gateway' || route.type === 'student-login' || route.type === 'teacher-login') {
    return (
      <UnifiedLogin
        apiBaseUrl={API_BASE_URL}
        onLoginSuccess={(user, token, dest) => {
          setCurrentLearner(user);
          setAuthToken(token);
          navigate(dest);
        }}
      />
    );
  }

  // =========================================================================
  // VIEW RENDERER 4: EDUCATOR WORKSPACE (Dedicated Left Rail Shell)
  // =========================================================================
  if (route.type === 'teacher') {
    const activeTab = route.tab;
    const inspectingLearnerId = route.learnerId;

    return (
      <EducatorShell
        currentTeacher={currentLearner.role === 'teacher' ? currentLearner : (learners.find((l) => l.role === 'teacher') || DEFAULT_LEARNERS[3])}
        activeTab={activeTab}
        onSelectTab={(tab) => {
          navigate(`/teacher/${tab === 'overview' ? 'dashboard' : tab}`);
        }}
        onSignOut={handleSignOut}
      >
        {inspectingLearnerId ? (
          <TeacherLearnerProfile
            learnerId={inspectingLearnerId}
            concepts={concepts}
            apiBaseUrl={API_BASE_URL}
            authToken={authToken}
            onBack={() => navigate('/teacher/learners')}
            onIntervene={() => navigate('/teacher/interventions')}
          />
        ) : (
          <>
            {activeTab === 'overview' && (
              <TeacherDashboard
                currentTeacher={currentLearner.role === 'teacher' ? currentLearner : (learners.find((l) => l.role === 'teacher') || DEFAULT_LEARNERS[3])}
                concepts={concepts}
                cohort={cohort}
                conceptAnalytics={conceptAnalytics}
                apiBaseUrl={API_BASE_URL}
                authToken={authToken}
                onRefreshData={() => void syncEducatorData(authToken)}
                onInspectLearner={(learnerId) => navigate(`/teacher/learners/${learnerId}`)}
                onNavigateToLearners={() => navigate('/teacher/learners')}
                onNavigateToInsights={() => navigate('/teacher/insights')}
                onNavigateToInterventions={() => navigate('/teacher/interventions')}
                onNavigateToAudit={() => navigate('/teacher/audit')}
              />
            )}

            {activeTab === 'learners' && (
              <TeacherLearners
                cohort={cohort}
                onInspectLearner={(learnerId) => navigate(`/teacher/learners/${learnerId}`)}
                onInterveneLearner={() => navigate('/teacher/interventions')}
              />
            )}

            {activeTab === 'insights' && (
              <TeacherInsights
                concepts={concepts}
                analytics={conceptAnalytics}
                onRefresh={() => void syncEducatorData(authToken)}
              />
            )}

            {activeTab === 'interventions' && (
              <TeacherInterventions
                cohort={cohort}
                concepts={concepts}
                currentTeacher={currentLearner.role === 'teacher' ? currentLearner : (learners.find((l) => l.role === 'teacher') || DEFAULT_LEARNERS[3])}
                apiBaseUrl={API_BASE_URL}
                authToken={authToken}
                onInterventionSuccess={() => void syncEducatorData(authToken)}
              />
            )}

            {activeTab === 'assistant' && (
              <EducatorAssistant
                currentTeacher={currentLearner.role === 'teacher' ? currentLearner : (learners.find((l) => l.role === 'teacher') || DEFAULT_LEARNERS[3])}
                apiBaseUrl={API_BASE_URL}
                authToken={authToken}
                onNavigateToInterventions={() => navigate('/teacher/interventions')}
                onInspectLearner={(learnerId) => navigate(`/teacher/learners/${learnerId}`)}
              />
            )}

            {activeTab === 'audit' && (
              <TeacherAudit
                apiBaseUrl={API_BASE_URL}
                authToken={authToken}
              />
            )}
          </>
        )}
      </EducatorShell>
    );
  }

  // =========================================================================
  // VIEW RENDERER 5: STUDENT PORTAL (Dedicated Top Bar Shell)
  // =========================================================================
  const studentActiveTab = route.tab;
  const isLessonActive = route.action === 'lesson' && !!route.conceptId;
  const isAssessmentActive = route.action === 'assessment' && !!route.conceptId;
  const activeConcept =
    concepts.find((c) => c.id === route.conceptId) ||
    (route.conceptId
      ? {
          id: route.conceptId,
          code: route.conceptId,
          title: route.conceptId === 'MATH-C01' ? 'Integer Arithmetic' : route.conceptId,
          grade: 8,
          subject: 'Mathematics',
          description: 'Class 8 foundational curriculum module',
          prerequisites: [],
          order_index: 1,
        }
      : undefined);

  return (
    <div className="student-shell">
      <StudentHeader
        learner={currentLearner}
        activeTab={studentActiveTab}
        onSelectTab={(tab) => {
          navigate(`/student/${tab === 'pathway' ? 'pathway' : tab === 'progress' ? 'progress' : tab === 'insights' ? 'insights' : tab === 'tutor' ? 'tutor' : 'home'}`);
        }}
        onSignOut={handleSignOut}
      />

      <main className="student-main-content">
        {loading && (
          <div className="editorial-card" style={{ textAlign: 'center', padding: 'var(--space-12)' }}>
            <p style={{ color: 'var(--text-secondary)' }}>Synchronizing SUTRA LEARN Curriculum & Evidence State...</p>
          </div>
        )}

        {!loading && error && (
          <div className="editorial-card" style={{ padding: 'var(--space-6)', borderColor: 'var(--feedback-error-border)', backgroundColor: 'var(--feedback-error-bg)' }}>
            <h3 className="serif-title" style={{ color: 'var(--feedback-error)' }}>Connection Notice</h3>
            <p style={{ color: 'var(--feedback-error)', marginTop: '6px' }}>{error}</p>
          </div>
        )}

        {!loading && !error && (
          <>
            {/* 5A. Active Lesson Screen */}
            {isLessonActive && activeConcept && (
              <LessonView
                concept={activeConcept}
                onBack={() => navigate('/student/home')}
                onStartAssessment={handleOpenAssessment}
                onOpenTutor={() => navigate('/student/tutor')}
              />
            )}

            {/* 5B. Active Diagnostic / Practice Assessment Screen */}
            {isAssessmentActive && activeConcept && (
              <AssessmentView
                concept={activeConcept}
                learner={currentLearner}
                apiBaseUrl={API_BASE_URL}
                authToken={authToken}
                onBack={() => navigate('/student/home')}
                onCompleteEvaluation={(cId) => void handleCompleteEvaluation(cId)}
              />
            )}

            {/* 5C. Main Tab Navigation Views */}
            {!isLessonActive && !isAssessmentActive && (
              <>
                {studentActiveTab === 'home' && (
                  <StudentHome
                    learner={currentLearner}
                    concepts={concepts}
                    progressMap={progressMap}
                    apiBaseUrl={API_BASE_URL}
                    authToken={authToken}
                    onOpenLesson={(cId) => void handleOpenLesson(cId)}
                    onOpenAssessment={handleOpenAssessment}
                    onViewPathway={() => navigate('/student/pathway')}
                  />
                )}

                {studentActiveTab === 'pathway' && (
                  <StudentPathway
                    concepts={concepts}
                    progressMap={progressMap}
                    onOpenLesson={(cId) => void handleOpenLesson(cId)}
                    onOpenAssessment={handleOpenAssessment}
                    onBackToHome={() => navigate('/student/home')}
                  />
                )}

                {studentActiveTab === 'progress' && (
                  <StudentProgress
                    learner={currentLearner}
                    concepts={concepts}
                    progressMap={progressMap}
                    apiBaseUrl={API_BASE_URL}
                    authToken={authToken}
                    onBackToHome={() => navigate('/student/home')}
                    onPracticeConcept={handleOpenAssessment}
                  />
                )}

                {studentActiveTab === 'insights' && (
                  <StudentInsights
                    learner={currentLearner}
                    concepts={concepts}
                    apiBaseUrl={API_BASE_URL}
                    authToken={authToken}
                    onBackToHome={() => navigate('/student/home')}
                    onNavigateToPathway={() => navigate('/student/pathway')}
                    onPracticeConcept={handleOpenAssessment}
                  />
                )}

                {studentActiveTab === 'tutor' && (
                  <StudentTutor
                    currentStudentId={currentLearner.id}
                    concepts={concepts}
                    authToken={authToken}
                    apiBaseUrl={API_BASE_URL}
                    onNavigateToPathway={() => navigate('/student/pathway')}
                    onNavigateToLesson={(cId) => void handleOpenLesson(cId)}
                  />
                )}
              </>
            )}

            {/* 5D. Adaptive Recommendation Modal */}
            {activeRecommendation && (
              <RecommendationModal
                recommendation={activeRecommendation}
                onContinue={handleRecommendationContinue}
                onClose={() => setActiveRecommendation(null)}
              />
            )}
          </>
        )}
      </main>
      <footer
        style={{
          borderTop: '1px solid var(--border-subtle)',
          padding: 'var(--space-3) var(--space-6)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 'var(--space-2)',
          backgroundColor: 'var(--surface-paper)',
          marginTop: 'auto',
          fontSize: '11px',
          color: 'var(--text-muted)',
        }}
      >
        <span>SUTRA LEARN &bull; Student Learning Workspace</span>
        <DeveloperSignature />
      </footer>
    </div>
  );
}

export default App;
