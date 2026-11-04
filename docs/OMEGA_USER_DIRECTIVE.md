<USER_REQUEST>
# SUTRA LEARN — OMEGA ∞


API - {AQ.Ab8...fiVQ [REDACTED_FOR_SECURITY]}
# ULTIMATE API INTEGRATION, INTELLIGENCE ENGINEERING AND PRODUCTION EXCELLENCE DIRECTIVE



## MISSION



You are not acting as a code-completion assistant.



You are operating as a complete principal engineering organisation responsible for the technical excellence of SUTRA LEARN.



Your responsibilities include:



- Principal Software Architect

- Senior Backend Engineer

- Senior Frontend Engineer

- AI/ML Integration Engineer

- AI Evaluation Researcher

- Cybersecurity Engineer

- Database Architect

- Site Reliability Engineer

- Performance Engineer

- QA Automation Lead

- Educational Technology Specialist

- Production Release Manager



Your mission is to integrate the newly supplied API into the existing SUTRA LEARN platform and make the entire affected system exceptionally reliable.



The objective is not merely to add a provider.



The objective is to build a robust, secure, observable, testable and educationally valuable AI system.



**Do not manufacture perfection. Engineer it.**



---



# COMMAND 00 — ABSOLUTE OPERATING PRINCIPLES



These rules override convenience and speed.



1. Inspect before modifying.

2. Understand before redesigning.

3. Verify before assuming.

4. Implement before claiming completion.

5. Test before deploying.

6. Measure before optimizing.

7. Preserve existing functionality.

8. Never invent API specifications.

9. Never expose secrets.

10. Never weaken security to make tests pass.

11. Never replace real functionality with fake success states.

12. Never award yourself points without evidence.



Maintain a persistent engineering task register.



For each task record:

- Identifier.

- Priority.

- Description.

- Root cause.

- Affected files.

- Dependencies.

- Implementation status.

- Test status.

- Verification evidence.

- Remaining risks.



Use the following status classifications:



PASS, PARTIAL, FAIL, BLOCKED, NOT VERIFIED, NOT APPLICABLE.



Do not confuse a successful local test with production verification.



---



# COMMAND 01 — FORENSIC REPOSITORY DISCOVERY



Before modifying anything, investigate the complete repository.



Inspect:

- Project directory structure.

- Backend architecture.

- Frontend architecture.

- AI provider implementations.

- AI orchestration.

- Authentication.

- Authorization.

- Database.

- API routers.

- Request and response schemas.

- Environment configuration.

- Dependencies.

- Test suites.

- Deployment configuration.

- Documentation.

- Git history.

- Existing modifications.



Identify:

- Dead code.

- Duplicate logic.

- Circular dependencies.

- Inconsistent schemas.

- Unused dependencies.

- Missing dependencies.

- Incorrect imports.

- Hidden fallback behavior.

- Unhandled exceptions.

- Insecure configuration.

- Incorrect provider attribution.

- Incomplete features.

- Performance bottlenecks.



Establish a baseline before making changes.



Preserve uncommitted user work.



Never overwrite a working newer implementation with an older archived version.



Produce:



`docs/OMEGA_REPOSITORY_BASELINE.md`



---



# COMMAND 02 — API IDENTITY AND SPECIFICATION VERIFICATION



Identify the exact newly supplied API.



Determine:



- Provider.

- Product.

- Official documentation.

- SDK.

- API version.

- Authentication mechanism.

- Base URL.

- Supported endpoints.

- Model identifiers.

- Request schema.

- Response schema.

- Streaming behavior.

- Token limits.

- Rate limits.

- Quotas.

- Error codes.

- Pricing.

- Data processing policy.

- Data retention.

- Regional restrictions, if applicable.



Use official documentation and current provider specifications.



Verify every model identifier against an authoritative source or actual provider response.



Never guess model names.



Never invent endpoints.



If the API documentation or credentials are unavailable, identify precisely what is missing and continue with the portions that can be safely implemented.



Produce:



`docs/OMEGA_API_SPECIFICATION.md`



---



# COMMAND 03 — ARCHITECTURE DECISION AND DESIGN



Evaluate whether the new API should become:



- Primary provider.

- Secondary provider.

- Specialized provider.

- Optional fallback.

- Replacement for an existing provider.



Do not choose based on marketing claims.



Evaluate:

- Educational reasoning quality.

- Mathematical accuracy.

- Context handling.

- Latency.

- Availability.

- Rate limits.

- Cost.

- Reliability.

- Privacy.

- Integration complexity.

- Operational risk.



Create an architecture decision record explaining the selected approach and rejected alternatives.



Build a provider-independent interface wherever justified.



Recommended logical structure:



Configuration

→ Provider Registry

→ Provider Adapter

→ AI Orchestrator

→ Context Builder

→ Response Validator

→ Educational Policy Layer

→ Conversation Persistence

→ Frontend.



Do not introduce unnecessary abstraction or microservices.



Keep the existing deterministic learning engine authoritative.



Produce:



`docs/OMEGA_ARCHITECTURE_DECISION.md`



---



# COMMAND 04 — API IMPLEMENTATION



Implement the actual provider using its verified official SDK or documented HTTP interface.



Requirements:



- Correct authentication.

- Correct endpoint.

- Correct API version.

- Correct model.

- Correct payload.

- Correct response parsing.

- Correct error mapping.

- Connection pooling where supported.

- Configurable timeouts.

- Bounded retries.

- Request cancellation.

- Rate-limit handling.

- Safe concurrency.

- Response validation.

- Usage metadata.

- Provider attribution.



Ensure that:

- API keys remain backend-only.

- Secrets never enter frontend bundles.

- Secrets are never printed.

- Request bodies are appropriately bounded.

- Sensitive student information is minimized.

- Unexpected response structures fail safely.



Do not log complete student conversations unnecessarily.



---



# COMMAND 05 — PROVIDER RESILIENCE ENGINE



Implement reliable provider behavior.



Classify failures into:



1. Authentication failure.

2. Authorization failure.

3. Invalid request.

4. Unsupported model.

5. Rate limit.

6. Quota exhaustion.

7. Timeout.

8. Network failure.

9. Provider outage.

10. Invalid response.

11. Content validation failure.

12. Internal application failure.



Apply retries only when appropriate.



Use exponential backoff with jitter for eligible transient failures.



Respect provider retry instructions where available.



Prevent retry storms.



Prevent duplicate submissions.



Implement circuit breakers with tested state transitions if justified.



Define explicit provider states:



- NOT_CONFIGURED

- CONFIGURED

- UNKNOWN

- OPERATIONAL

- DEGRADED

- UNAVAILABLE

- DISABLED

- CIRCUIT_OPEN



Do not equate configuration with operational health.



Never silently substitute a fallback response while claiming the primary provider succeeded.



---



# COMMAND 06 — SUTRA LEARN AI ORCHESTRATION



Integrate the provider with the existing educational architecture.



Inspect the actual tutor implementation and preserve all existing supported modes:



1. Guided Learning.

2. Worked Example.

3. Practice Question.

4. Check My Work.

5. Quick Revision.

6. Prerequisites.



For every request:



1. Authenticate the learner.

2. Resolve the learner identity from trusted server-side authentication.

3. Validate the selected curriculum concept.

4. Load permitted curriculum context.

5. Resolve the requested teaching mode.

6. Select the provider according to routing policy.

7. Build the provider request.

8. Execute the request.

9. Validate the returned response.

10. Apply educational safety and correctness checks.

11. Persist the conversation safely.

12. Return normalized output.

13. Record sanitized telemetry.



Do not trust a frontend-supplied learner ID as proof of identity.



Do not allow AI output to modify authoritative mastery or progress records.



---



# COMMAND 07 — EDUCATIONAL INTELLIGENCE AND QUALITY



The API must contribute to meaningful learning.



Evaluate:



- Concept explanations.

- Mathematical correctness.

- Step-by-step reasoning.

- Misconception identification.

- Hint quality.

- Question generation.

- Difficulty appropriateness.

- Curriculum alignment.

- Prerequisite support.

- Feedback usefulness.

- Student comprehension.



Implement evaluation datasets using the actual curriculum.



Include:

- Correct answers.

- Incorrect answers.

- Common misconceptions.

- Ambiguous questions.

- Multi-step mathematics.

- Negative integers.

- Fractions.

- Decimals.

- Algebra.

- Word problems.

- Edge cases.



Score output against explicit rubrics.



Use deterministic validation where possible.



A language model's confidence is not proof of mathematical correctness.



Record actual evaluation results.



Never claim improved learning outcomes without learner-study evidence.



---



# COMMAND 08 — AUTHENTICATION AND AUTHORIZATION REPAIR



Treat existing authentication weaknesses as release-blocking.



Audit:



- Password verification.

- Missing password hashes.

- Password hashing.

- Token signing.

- Token expiration.

- Token verification.

- Token claims.

- Role validation.

- Account status.

- Session restoration.

- Session revocation.

- Refresh mechanisms.

- Frontend credential storage.

- API authorization headers.

- Demo authentication.

- Cross-user resource access.



Fix all identified bypasses.



Specifically verify:



- No missing password hash can bypass authentication.

- Failed login cannot invoke persona authentication.

- No unrestricted learner-ID session issuance exists.

- Demo access cannot impersonate arbitrary accounts.

- Production secrets cannot fall back to predictable defaults.

- Current database role is checked for protected actions.

- Deleted or disabled accounts cannot retain effective access.

- Cross-student data access is rejected.



Use secure, documented session lifecycle behavior.



Do not introduce refresh tokens without proper rotation and revocation.



Add security regression tests.



---



# COMMAND 09 — DATABASE AND CONVERSATION INTEGRITY



Inspect all affected database operations.



Verify:



- Transactions.

- Rollbacks.

- Foreign keys.

- Ownership.

- Conversation creation.

- Message persistence.

- Message ordering.

- Duplicate requests.

- Idempotency.

- Concurrent writes.

- Database restart behavior.

- Migration safety.

- Persistent production storage.



Test that an interrupted AI request does not create misleading conversation records.



Test that retrying a request does not accidentally duplicate persisted messages.



Never expose one learner's conversations to another.



---



# COMMAND 10 — COMPLETE FRONTEND INTEGRATION



Inspect the actual frontend components and API client.



Integrate the new provider without placing credentials in browser code.



Create accurate interface states:



- Initializing.

- Connecting.

- Ready.

- Generating.

- Response received.

- Authentication expired.

- Rate limited.

- Provider degraded.

- Network unavailable.

- Request failed.

- Retry available.



The UI must distinguish provider configuration from actual provider health.



Preserve the premium SUTRA LEARN light visual identity.



Verify:

- Desktop.

- Tablet.

- Mobile.

- Keyboard navigation.

- Screen-reader semantics.

- Focus handling.

- Form validation.

- Loading states.

- Empty states.

- Error recovery.



Do not redesign unrelated features.



---



# COMMAND 11 — OFFLINE AND CONNECTIVITY ENGINEERING



Inspect the existing offline architecture.



Test:



- Offline application launch.

- Cached curriculum.

- Local practice.

- Attempt queue.

- Browser refresh.

- Interrupted synchronization.

- Network recovery.

- Duplicate synchronization.

- Conflict resolution.

- Server acknowledgement.



Do not represent an unsubmitted local attempt as server-confirmed evidence.



The AI provider must report unavailable connectivity accurately.



Provide deterministic offline educational functionality where already supported.



---



# COMMAND 12 — ADVERSARIAL SECURITY TESTING



Actively challenge the integration.



Test:



- Missing credentials.

- Invalid credentials.

- Expired credentials.

- Tampered tokens.

- Unauthorized users.

- Privilege escalation.

- Cross-student access.

- Malformed payloads.

- Oversized requests.

- Prompt injection.

- Untrusted curriculum content.

- Malicious URLs in user input.

- Sensitive information leakage.

- Rate-limit abuse.

- Retry abuse.

- Provider error manipulation.



Treat all user input and retrieved external content as untrusted data.



Never allow retrieved content to override system security instructions.



Validate authorization independently of frontend controls.



---



# COMMAND 13 — PERFORMANCE AND COST ENGINEERING



Measure real performance.



Collect:



- Request latency.

- Time to first token.

- Total generation time.

- Error rate.

- Timeout rate.

- Retry rate.

- Provider fallback rate.

- Concurrency behavior.

- Token usage.

- Cost per request, when pricing is verifiable.

- Backend resource usage.



Identify bottlenecks before optimizing.



Implement:

- Appropriate concurrency limits.

- Request-size limits.

- Output limits.

- Timeouts.

- Cancellation.

- Efficient database access.

- Safe telemetry.

- Cost controls.



Do not invent benchmark values.



---



# COMMAND 14 — AUTOMATED TESTING AND QUALITY GATES



Create meaningful tests.



Required layers:



A. Unit tests.

B. Provider adapter tests.

C. API integration tests.

D. Authentication tests.

E. Authorization tests.

F. Database tests.

G. Mathematical validation tests.

H. Educational response evaluation.

I. Frontend component tests.

J. End-to-end student tests.

K. End-to-end teacher tests.

L. Offline synchronization tests.

M. Production smoke tests.



Run tests against both:

- Controlled test environments.

- Real external provider requests, where credentials and access permit.



Clearly distinguish mocks from live integration.



A mocked API response cannot establish that the provider works.



A successful HTTP response cannot establish that the educational answer is correct.



Never:

- Delete tests to obtain a green result.

- Weaken assertions.

- Convert failing tests into skipped tests.

- Count cancelled tests as passed.

- Claim unexecuted tests passed.



---



# COMMAND 15 — PRODUCTION DEPLOYMENT AND VERIFICATION



Inspect the current deployment configuration.



Frontend:

https://sutralearn.vercel.app/



Backend:

https://sutra-learn-api.onrender.com



Verify:

- API base URL.

- CORS.

- Environment variables.

- Backend startup.

- Provider connectivity.

- Authentication.

- Tutor requests.

- Past sessions.

- Conversation persistence.

- Logout.

- Browser refresh.

- Error behavior.



Use a controlled test account.



Do not expose production student data.



Do not destructively modify production records.



Do not deploy without authorization when deployment actions could affect users.



Do not claim live verification unless the actual deployed services were tested.



---



# COMMAND 16 — REGRESSION AND CHANGE VALIDATION



After implementation:



1. Inspect every changed file.

2. Review the final Git diff.

3. Check for unintended modifications.

4. Run dependency validation.

5. Run backend tests.

6. Run frontend lint.

7. Run frontend production build.

8. Run integration tests.

9. Run security regression tests.

10. Run actual provider tests.

11. Verify deployment where authorized.



Ensure unrelated working features remain intact.



---



# COMMAND 17 — OBSERVABILITY AND INCIDENT DIAGNOSIS



Add structured, sanitized telemetry.



Track:



- Provider selected.

- Request identifier.

- Request duration.

- Result category.

- Retry count.

- Fallback reason.

- Token usage where available.

- Validation result.

- Error category.



Never log:

- API keys.

- Passwords.

- Bearer tokens.

- Private signing secrets.

- Unnecessary sensitive student content.



Make errors diagnosable without exposing sensitive data.



Provide correlation identifiers to connect frontend, backend and provider failures.



---



# COMMAND 18 — REQUIRED ENGINEERING DELIVERABLES



Produce:



`docs/OMEGA_REPOSITORY_BASELINE.md`



`docs/OMEGA_API_SPECIFICATION.md`



`docs/OMEGA_ARCHITECTURE_DECISION.md`



`docs/OMEGA_IMPLEMENTATION_REPORT.md`



`docs/OMEGA_SECURITY_AUDIT.md`



`docs/OMEGA_AI_EVALUATION.md`



`docs/OMEGA_MATHEMATICS_VALIDATION.md`



`docs/OMEGA_PERFORMANCE_REPORT.md`



`docs/OMEGA_TEST_MATRIX.md`



`docs/OMEGA_DEPLOYMENT_VERIFICATION.md`



`docs/OMEGA_FINAL_ACCEPTANCE.md`



Every report must reference actual files, tests, results and evidence.



---



# COMMAND 19 — INDEPENDENT ACCEPTANCE SCORING



Evaluate 1,000 points across ten engineering domains:



| Domain | Points |

|---|---:|

| API correctness and specification compliance | 100 |

| Architecture and maintainability | 100 |

| Authentication and cybersecurity | 150 |

| AI reliability and provider resilience | 120 |

| Educational intelligence and correctness | 120 |

| Database integrity and privacy | 100 |

| Frontend and complete user workflows | 80 |

| Testing and adversarial verification | 100 |

| Performance and observability | 60 |

| Deployment and documentation | 70 |

| TOTAL | 1,000 |



Award points only when supported by evidence.



A perfect score requires every applicable acceptance criterion to pass.



Production verification must not be awarded when production access was unavailable.



Report unresolved risks separately.



The 1,000,000/1,000,000 aspiration is not permission to inflate the score.



---



# COMMAND 20 — AUTONOMOUS EXECUTION PROTOCOL



Work through these stages:



STAGE A: Discover.



STAGE B: Establish baseline.



STAGE C: Identify defects.



STAGE D: Design architecture.



STAGE E: Implement.



STAGE F: Test.



STAGE G: Challenge adversarially.



STAGE H: Repair.



STAGE I: Regression test.



STAGE J: Production verification.



STAGE K: Independent acceptance.



Do not stop after producing a plan.



Do not stop after editing files.



Continue until every safely executable task is completed.



If a task is blocked, document the exact blocker and continue with independent tasks.



Do not ask the user for information that already exists in the repository or supplied documentation.



Ask only for information that genuinely cannot be discovered.



Preserve all user work.



---



# FINAL OMEGA STANDARD



The new API must be genuinely integrated into the SUTRA LEARN educational architecture.



The AI Tutor must work.



Authentication must be secure.



Conversation history must work.



Provider health must be truthful.



Fallback must be transparent.



Mathematical output must be evaluated.



Student data must remain protected.



Offline behavior must remain consistent.



Production deployment must be verified honestly.



The architecture must remain maintainable.



The product must improve actual learning workflows.



**DO NOT BUILD A DEMONSTRATION THAT LOOKS SUCCESSFUL.**



**BUILD AN ENGINEERED SYSTEM THAT REMAINS CORRECT UNDER REAL CONDITIONS.**



**DO NOT REPORT PERFECTION. PROVE EXCELLENCE.**



# EXECUTE OMEGA ∞ NOW.
</USER_REQUEST>
<ADDITIONAL_METADATA>
The current local time is: 2026-11-04T12:06:37+05:30.

The user's current state is as follows:
Active Document: c:\Users\Yash\OneDrive\Desktop\Sutra_Learn\docs\design\PAST_SESSIONS_UI_FIX.md (LANGUAGE_UNSPECIFIED)
Cursor is on line: 83
Other open documents:
- c:\Users\Yash\OneDrive\Desktop\Sutra_Learn\backend\app\engine\__init__.py (LANGUAGE_UNSPECIFIED)
- c:\Users\Yash\OneDrive\Desktop\Sutra_Learn\backend\tests\test_educational_excellence.py (LANGUAGE_UNSPECIFIED)
- c:\Users\Yash\OneDrive\Desktop\Sutra_Learn\backend\app\routers\tutor.py (LANGUAGE_UNSPECIFIED)
- c:\Users\Yash\OneDrive\Desktop\Sutra_Learn\backend\app\db\database.py (LANGUAGE_UNSPECIFIED)
- c:\Users\Yash\OneDrive\Desktop\Sutra_Learn\backend\app\ai\registry.py (LANGUAGE_UNSPECIFIED)
</ADDITIONAL_METADATA>