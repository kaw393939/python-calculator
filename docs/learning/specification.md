# Specification: Engineering with AI, from CLI to web

Status: approved for planning by the user's request; instructional materials not yet authored.
Version: 1.0. Audience: early-career, AI-forward software engineering students.

## Purpose

Produce an executable teaching module from this calculator project and its development
conversation. Students learn engineering vocabulary by applying it, directing an AI
coding assistant, checking its work, and improving software through real use.
The goal is defensible engineering decisions, not a large volume of generated code.

This document specifies the teaching deliverables. It does not replace the
[application specification](../specification.md) or claim that the lessons already exist.
The implementation backlog is tracked in [delivery.md](delivery.md).

## Audience, prerequisites, and teaching assumptions

Assume basic Python functions, collections, exceptions, terminal navigation, and basic
Git. Provide a readiness checklist and remedial links in the student guide. Do not
assume prior design-pattern, API, testing, or AI-agent experience.
Plan six 90-minute sessions plus approximately six hours of independent practice.
This schedule is a planning assumption instructors may adjust, not a user-imposed limit.
Students need Python 3.11+, Git, a GitHub account, an editor, and an AI coding assistant.
No paid model or specific vendor is required. Provide manual alternatives when browser
control or other agent capabilities are unavailable. Browser automation failure must
be recorded as unverified evidence, never a passed test.

Students work in their own fork or isolated copy. Before any write, they inspect the
working directory, Git status, and remote. The original is218-oop-calculator repository
is preserved and is not a student exercise target. Use temporary history files for tests.

## Learning outcomes

| ID | By the end, the learner can demonstrate |
| --- | --- |
| LO-01 | Translate an informal request into numbered functional/nonfunctional requirements, scope boundaries, and measurable acceptance criteria. |
| LO-02 | Organize themes, epics and user stories into small issues and trace an issue to a focused commit and verification evidence. |
| LO-03 | Explain and locate Command, Strategy, Facade, Observer, repository, protocols, dependency injection, and SOLID; justify their cost as well as benefit. |
| LO-04 | Implement and test variable-argument CLI operations, plugins, and CSV history; distinguish parsing, validation, domain logic, and persistence. |
| LO-05 | Design positive and negative unit, integration, and E2E tests; distinguish coverage, correctness, and usability. |
| LO-06 | Run at least two observe–test–change–verify dogfooding cycles and update requirements when behavior changes. |
| LO-07 | Add a FastAPI/JavaScript adapter that reuses the domain; explain requests, JSON, HTTP statuses, concurrency, and storage ownership. |
| LO-08 | Critique AI-generated claims with evidence, explain code without the assistant, and disclose limitations and assistance. |

## Themes, epics, and learner stories

| Theme | Epic | Story and user value | Outcomes |
| --- | --- | --- | --- |
| T-L1 Problem definition | E-L1 Requirements and delivery | LS-01: As a learner, I can turn a rough prompt into a reviewable contract so that AI has a clear target. | LO-01,02 |
| T-L2 Explainable design | E-L2 CLI architecture | LS-02: As a learner, I can follow one calculation through the patterns and add a plugin without changing the core. | LO-03,04 |
| T-L3 Evidence and iteration | E-L3 Testing and dogfooding | LS-03: As a learner, I can reproduce a usability defect and verify an improvement rather than accepting an AI assurance. | LO-05,06,08 |
| T-L4 Multiple interfaces | E-L4 Web adapter | LS-04: As a learner, I can reuse the CLI's domain behind an API and UI without copying arithmetic logic. | LO-07 |
| T-L3 Evidence and iteration | E-L5 Assessment and facilitation | LS-05: As an instructor, I can evaluate reasoning, vocabulary and evidence consistently, regardless of the AI tool used. | All |

## Required deliverables

Paths below are planned outputs, not existing resources or completed promises.

| ID | Planned path under docs/learning/ | Required content |
| --- | --- | --- |
| D-01 | glossary.md | Plain-language terms, project examples, misconceptions and knowledge checks |
| D-02 | case-study.md | Annotated, evidence-backed development story and critical analysis |
| D-03 | labs/01-requirements.md | Informal brief → specification, stories, acceptance criteria and GitHub issues |
| D-04 | labs/02-cli-design.md | CLI, variable arguments, patterns, plugin contract and CSV history |
| D-05 | labs/03-testing.md | Positive/negative unit, integration and subprocess E2E tests; CI and coverage critique |
| D-06 | labs/04-dogfooding.md | Two complete use–observe–test–fix–reuse cycles and a reusable observation template |
| D-07 | labs/05-web-adapter.md | FastAPI endpoints, JS interface, shared domain, persistence and failure handling |
| D-08 | labs/06-engineering-review.md | Final integrated review, change explanation, limitations and evidence-based release decision |
| D-09 | assessment.md | 100-point rubric, submission manifest, oral checks and proficiency anchors |
| D-10 | instructor-guide.md | Six-session pacing, prerequisites, facilitation, model answers and troubleshooting |
| D-11 | README.md | Student entry point, setup, sequence, deliverables and links to all finished materials |
| D-12 | validation-report.md | Reproducible walkthrough results, link/command audit, rubric alignment and unresolved limits |

## Instructional content requirements

- **LR-01:** Each lab includes outcomes, prerequisites, estimated time, starting state,
  explicit tasks, vocabulary-in-context, completion checks, and reflection questions.
- **LR-02:** Each lab includes a copyable AI prompt with goal, relevant context,
  constraints, requested evidence, and success criteria. Pair it with a critique or
  follow-up prompt; explain why the prompt helps. Avoid vendor-specific tool guarantees.
- **LR-03:** Prompts must ask the assistant to inspect before changing files, preserve
  user work, propose concrete verification, and report what actually ran. Students
  review generated code and remain accountable for correctness.
- **LR-04:** The vocabulary covers requirements, scope, constraints, acceptance criteria,
  themes, epics, stories, backlog, definition of ready/done, repository, remote, branch,
  commit, PR, traceability, regression, coverage, CI, test isolation, mocking, dogfooding,
  usability, validation, error recovery, interface, protocol, dependency injection,
  SOLID (all five principles), each implemented pattern, facade vs adapter, plugins,
  discovery, *args/**kwargs, serialization, persistence, atomic writes, HTTP, endpoint,
  JSON, status code, request/response, concurrency and single-writer ownership.
  Distinguish a Git repository from a persistence repository, and a class interface
  from a user interface. Terms must have concrete project examples, not definitions alone.
- **LR-05:** Explain the path from command parsing through facade and plugin to observer
  and CSV storage. The web lab must reuse it. Address synchronous persistence-before-
  publish semantics and why atomic replacement is not cross-process locking.
- **LR-06:** Testing exercises include invalid operands/options, zero division,
  nonfinite results, plugin failures, corrupt CSV, failed saves, restart persistence,
  and API error responses. Explain why 100% statement coverage is not proof of quality.
- **LR-07:** Dogfooding distinguishes observation from inference. Each record includes
  context, command/action, expected/actual result, severity, reproduction, issue,
  failing test, fix commit, retest and specification change. Include at least one
  negative workflow and one repeated-use workflow in each student's two cycles.
- **LR-08:** Case study includes original/new repository separation, evolving history
  schema, ddof semantics, CLI error and editing friction, ans/history improvements,
  CLI-to-web reuse, and failed Safari automation. Historical test counts must be dated
  and tied to a commit; do not present them as permanent guarantees.
- **LR-09:** Conversation excerpts must be brief, accurately labeled quotations or
  explicitly labeled paraphrases. Cite accessible repository issues/commits for facts;
  mark conversation-only claims as such. Never invent prompts, test outputs or a
  successful Safari run. Avoid reproducing local usernames, credentials or private paths.
- **LR-10:** Separate baseline behavior from student exercises and future ideas.
  In particular, undo, arbitrary expression parsing and pagination are not implemented
  features. Do not ask students to reproduce a defect on a revision where it is fixed.
- **LR-11:** Identify exact, verified historical revisions or safe exercise fixtures for
  reproduction. Use detached worktrees/copies and never reset a student's working branch.
  Include a route that works without private repository access, using an instructor-
  supplied snapshot or learner copy; document prerequisites honestly.
- **LR-12:** Instructor notes contain expected reasoning, likely misconceptions,
  intervention points, alternate solutions and offline/manual fallbacks. Student labs
  should not rely on instructor-only answer text to be executable.
- **LR-13:** Grade student reasoning and observable evidence more heavily than polished
  prose or code volume. Require explanation of one unfamiliar change without AI.
- **LR-14:** Use Markdown, relative links, accessible tables and diagrams with prose
  equivalents. A PDF, slides, hosted course, LMS integration, and new calculator features
  are outside this documentation release.

## Lesson progression and evidence

| Session | Time allocation | Student evidence |
| --- | --- | --- |
| 1. Specify before building | 15 vocabulary; 20 brief analysis; 40 lab; 15 critique | Requirements, stories, acceptance scenarios, issues |
| 2. Explain the CLI design | 15 walkthrough; 20 patterns; 40 lab; 15 tradeoff review | Architecture diagram, plugin/CLI change and explanation |
| 3. Test claims | 15 test levels; 20 failure reproduction; 40 lab; 15 evidence review | Positive/negative test matrix, failing/passing output, CI result |
| 4. Use what you built | 10 observation technique; 55 dogfooding; 15 retest; 10 reflection | Two documented cycles, linked fixes and specification amendments |
| 5. Add a web adapter | 15 HTTP vocabulary; 20 request tracing; 40 lab; 15 browser review | API/UI work, tests, browser observations and concurrency explanation |
| 6. Defend the result | 15 evidence audit; 30 peer review; 30 oral/change exercise; 15 retrospective | Final manifest, release assessment and individual explanation |

## Assessment contract

The detailed rubric must total 100 points: requirements/traceability 15; architecture
and vocabulary 20; verification and failure handling 25; dogfooding and iteration 20;
web/domain reuse 10; individual explanation and honest AI disclosure 10.
Each dimension needs observable excellent, adequate and insufficient anchors. Overall
proficiency requires at least 70/100 plus passing the individual explanation check.
The submission must include code, docs, issues/commit links, test evidence, two dogfooding
cycles, API/browser evidence, limitations and an assistance log. Fabricated evidence or
exposed secrets requires correction before proficiency can be demonstrated; institutional
academic-integrity policy remains the instructor's responsibility.

## Acceptance tests for the teaching package

| ID | Given / When / Then |
| --- | --- |
| AT-L01 | Given the student entry point, when a prepared learner follows it, then prerequisites, sequence, expected outputs and assessment are discoverable without chat context. |
| AT-L02 | Given each lab, when reviewed against LR-01/02, then it contains every required section and an actionable prompt/verification pair. |
| AT-L03 | Given a glossary entry, when sampled against the source, then its definition, concrete example and misconception are accurate. Audit all required terms for coverage. |
| AT-L04 | Given a clean isolated environment, when setup and commands are followed, then results match stated expectations or documented version-dependent variations. |
| AT-L05 | Given negative workflows, when executed, then expected failures are identified and no real user history is modified. |
| AT-L06 | Given two dogfooding cycles, when traced, then each has observation, failing evidence, fix, retest and requirement/documentation disposition. |
| AT-L07 | Given the web lab, when tracing a request, then it reaches the shared facade/plugin/persistence path and explains serialization of writes and process boundaries. |
| AT-L08 | Given case-study claims, when audited, then citations support them, paraphrases are labeled, and Safari remains unverified. |
| AT-L09 | Given an exemplar submission, when scored, then the rubric totals 100 and each criterion maps to an outcome and evidence item. |
| AT-L10 | Given the final package, when links and planned artifacts are audited, then no broken local links, placeholder sections or undocumented dependencies remain. |

## Execution rules and definition of done

Use the issue dependency graph in delivery.md. Each issue owns one primary artifact;
small supporting link or example changes are acceptable. Every implementation commit
references its issue. Close an issue only after its acceptance checklist passes; don't
close all teaching issues because this specification is written. Dependencies guide
execution order, not permission to create new autonomous chats or agents.

Examples: `docs: define calculator vocabulary (Refs #N)` and, once verified,
`docs: complete vocabulary review (Closes #N)`. Review and revise each deliverable before
closure. If executable fixtures or application code changes are needed, first scope
those changes in a separate issue; do not silently broaden a documentation issue.

Release is complete when D-01–D-12 exist, AT-L01–10 pass with recorded evidence, every
outcome maps to learning and assessment, examples have been exercised, and remaining
limitations are stated. Author verification does not establish learner effectiveness;
a real instructor/student pilot is a recommended later validation, not fabricated evidence.

## Specification review (planning stage)

Reviewed for scope, traceability, runnable examples and claim accuracy. Corrections
incorporated: distinguished teaching requirements from application requirements;
separated planned files from existing resources; defined accessible historical starting
states rather than assuming old bugs remain; made Safari failure an explicit evidence
lesson; retained separate-repository protection; added measurable assessment and final
walkthrough criteria. No lesson execution or learner pilot is claimed in this review.
