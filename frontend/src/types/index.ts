export interface Option {
  id: string;
  text: string;
  is_correct: boolean;
  misconception_tag?: string;
  misconception_explanation?: string;
}

export interface WorkedStep {
  step_number: number;
  action: string;
  expression: string;
  reasoning: string;
}

export interface Lesson {
  concept_id: string;
  title: string;
  objective: string;
  key_principles: string[];
  worked_steps: WorkedStep[];
  common_pitfalls: string[];
  interactive_prompt: string;
}

export interface Concept {
  id: string;
  code: string;
  title: string;
  grade: number;
  subject: string;
  description: string;
  prerequisites: string[];
  order_index: number;
  is_unlocked?: boolean;
  missing_prerequisites?: string[];
  lesson?: Lesson;
}

export interface Question {
  id: string;
  concept_id: string;
  prompt: string;
  equation_display?: string;
  options: Option[];
  hint: string;
  explanation?: string;
  difficulty: number;
  cognitive_demand: string;
}

export interface AttemptSubmission {
  attempt_id: string;
  learner_id: string;
  question_id: string;
  concept_id: string;
  selected_option_id: string;
  hint_used: boolean;
  session_id?: string;
  client_timestamp?: string;
  sync_status?: 'pending' | 'syncing' | 'synced';
}

export interface AttemptResult {
  attempt_id: string;
  is_duplicate: boolean;
  is_correct: boolean;
  hint_used: boolean;
  selected_option_id: string;
  correct_option_id: string;
  explanation: string;
  misconception_tag: string;
  misconception_explanation?: string;
  message: string;
  is_offline_queued?: boolean;
}

export interface Recommendation {
  id: string;
  learner_id: string;
  concept_id: string;
  outcome: 'BRIDGE_BACK' | 'SCAFFOLD' | 'STRETCH' | 'CONFIRM' | 'TEACHER_REVIEW';
  target_concept_id: string;
  target_concept_title: string;
  target_activity_type: string;
  target_activity_id?: string;
  reason_code: string;
  explanation: string;
  confidence_score: number;
  evidence_summary: Record<string, any>;
  policy_version: string;
}

export interface ConceptProgress {
  concept_id: string;
  status: 'not_started' | 'in_progress' | 'needs_reinforcement' | 'mastered';
  unassisted_correct: number;
  assisted_correct: number;
  total_attempts: number;
  mastery_percentage: number;
  last_recommended_outcome?: string;
  updated_at: string;
}

export interface Learner {
  id: string;
  name: string;
  grade: number;
  role: 'student' | 'teacher';
}

export interface CohortStudentSummary {
  learner_id: string;
  name: string;
  grade: number;
  total_attempts: number;
  total_correct: number;
  latest_outcome?: string;
  last_evaluated_at?: string;
  needs_review: number | boolean;
}

export interface TeacherOverrideRecord {
  id: string;
  learner_id: string;
  learner_name?: string;
  concept_id: string;
  previous_outcome: string;
  overridden_outcome: string;
  reason: string;
  teacher_id: string;
  created_at: string;
}

export interface StudentAttemptHistoryItem {
  id: string;
  question_id: string;
  concept_id: string;
  selected_option_id: string;
  is_correct: boolean;
  hint_used: boolean;
  misconception_tag: string;
  server_timestamp: string;
}

export interface ConceptAnalytics {
  concept_id: string;
  total_attempts: number;
  total_correct: number;
  total_assisted: number;
  unassisted_correct: number;
  accuracy_percentage: number;
  top_misconceptions: string[];
}

export interface AIMessage {
  id: string;
  conversation_id: string;
  sender_role: 'user' | 'assistant' | 'system';
  content: string;
  response_type: string;
  hints?: string[];
  concept_id?: string;
  requires_follow_up?: boolean;
  provider_metadata?: {
    provider?: string;
    model?: string;
    is_fallback?: boolean;
    fallback_reason?: string;
  };
  created_at?: string;
}

export interface AIConversation {
  id: string;
  owner_id: string;
  owner_role: 'student' | 'teacher';
  conversation_type: 'tutor' | 'educator_assistant';
  title: string;
  concept_id?: string;
  created_at: string;
  updated_at: string;
}

export interface EducatorAnalysisResponse {
  conversation_id: string;
  message_id: string;
  summary: string;
  observations: string[];
  recommended_actions: string[];
  struggling_learner_count: number;
  low_accuracy_concepts: string[];
  provider_metadata: {
    provider?: string;
    model?: string;
    is_fallback?: boolean;
  };
}

export interface LearnerMetrics {
  learner_id: string;
  timestamp: string;
  curriculum: {
    total_concepts: number;
    unlocked_concepts_count: number;
    unlocked_concepts: string[];
    in_progress_concepts: number;
    mastered_concepts: number;
    needs_review_concepts: number;
    not_started_concepts: number;
    prerequisite_gaps_count: number;
    curriculum_completion_pct: number;
  };
  accuracy: {
    overall_accuracy_pct: number | null;
    first_attempt_accuracy_pct: number | null;
    unassisted_accuracy_pct: number | null;
    assisted_accuracy_pct: number | null;
    rolling_7d_accuracy_pct: number | null;
    accuracy_trend_direction: 'improving' | 'stable' | 'declining';
  };
  attempts: {
    total_attempts: number;
    correct_attempts: number;
    incorrect_attempts: number;
    distinct_questions_attempted: number;
    hints_requested_total: number;
    solutions_viewed_total: number;
    avg_attempts_per_concept: number;
    attempt_to_mastery_ratio: number;
  };
  mastery: {
    average_mastery_pct: number;
    highest_mastery_concept: { concept_id: string; title: string; mastery_pct: number } | null;
    lowest_mastery_concept: { concept_id: string; title: string; mastery_pct: number } | null;
    mastery_streak_days: number;
    mastery_velocity_concepts_per_week: number;
    mastery_distribution: {
      mastered: number;
      in_progress: number;
      needs_reinforcement: number;
      not_started: number;
    };
  };
  misconceptions: {
    total_misconceptions_detected: number;
    active_misconceptions_count: number;
    resolved_misconceptions_count: number;
    top_recurring_misconception: string;
    misconception_severity_index: number;
  };
  assistance: {
    hint_dependency_ratio: number;
    scaffold_utilization_pct: number;
    unassisted_to_assisted_ratio: number;
    independent_problem_solving_index: number;
  };
  efficiency: {
    avg_time_per_item_seconds: number;
    avg_time_to_mastery_minutes: number;
    cognitive_struggle_index: number;
    learning_efficiency_score: number;
  };
  outcomes: {
    baseline_score_pct: number | null;
    post_learning_score_pct: number | null;
    absolute_gain_pct: number | null;
    normalized_gain_g: number | null;
    effect_size_d: number | null;
    delayed_retention_score_pct: number | null;
    retention_status: 'NOT SCHEDULED' | 'PENDING' | 'REASSESSED' | 'RETAINED' | 'NEEDS REINFORCEMENT' | 'INSUFFICIENT EVIDENCE';
    retention_decay_rate: number;
  };
}

export interface CohortMetrics {
  cohort_size: number;
  active_learners_count: number;
  cohort_avg_mastery_pct: number;
  cohort_avg_accuracy_pct: number;
  cohort_mastered_concepts_total: number;
  students_at_risk_count: number;
  bottleneck_concepts_count: number;
  interventions_pending_count: number;
  interventions_completed_count: number;
  intervention_success_rate_pct: number;
}



