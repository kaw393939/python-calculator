# Lab 6 — Defend an engineering result

## Outcomes and starting state

LO-01–08: make an evidence-backed release decision and explain the system independently.
Allow 90 minutes plus 30 minutes preparation. Complete Labs 1–5; use your learner repository,
reference copy and accumulated evidence. No new product feature is required for this review.
Vocabulary: **traceability**, **definition of done**, **limitations**, and **regression**
connect the specification to what you can responsibly claim.

## Tasks

1. Record revision, environment, status and remote. Run the applicable full suite and
   lint in each changed exercise copy. Distinguish a historical reproduction branch
   from the version you recommend releasing; do not combine incompatible test counts.
2. Create `evidence/submission.md` linking these artifacts:

   | Artifact | Required contents |
   | --- | --- |
   | Requirements | IDs, boundaries, assumptions, themes/epics/stories and acceptance checks |
   | Architecture | Code-linked diagram, patterns/SOLID rationale and tradeoffs |
   | Changes | Issues, focused commits and reviewed diffs for plugin, regressions and web slice |
   | Verification | Scenario/layer matrix, red/green logs, CI or documented local equivalent |
   | Dogfooding | Two complete journals with negative/repeated-use checks and requirement updates |
   | Web | Endpoint contract, API logs, browser observations or explicit unverified items |
   | Assistance | AI tool used, delegated work, rejected suggestions and independent checks |
   | Release assessment | Ready/not ready for a stated scope, remaining defects and deferred work |

3. Build a trace table with columns: requirement → issue → commit → test → observed result
   → limitation. Include arithmetic, save failure and one usability change. Missing evidence
   is a finding; do not fill gaps with hypothetical outputs.
4. Peer review: give a partner the repo and manifest without the original chat. Have them
   follow one valid and one failing workflow using a fresh temporary history. Ask them to
   identify an oversized commit, an unsupported AI claim and an unnecessary abstraction
   if any exist. “None found” is acceptable when supported by inspection, not assumed.
5. Without AI, explain `stddev 2 4 6 ddof=1` from parsing to save and output. Then explain
   what changes when saving fails. Your instructor chooses an unfamiliar small task,
   such as a new negative test for fractional ddof or a clearer empty-history message.
   Read the relevant code, make the change in a learner branch, run the targeted check,
   and explain the diff. This is a supervised reasoning check, not a memorized demo.
6. Write a release decision with at least two limitations and one next improvement
   prioritized by user impact. Optional future work includes undo, pagination and exact
   decimal arithmetic; do not describe these as delivered features.

## AI prompt

```text
Inspect my learner repository, remote and submission manifest before editing; preserve
all work. Audit requirement→issue→commit→test→observed-result links. Challenge unsupported
claims and distinguish historical results from current checks. Propose targeted checks
for gaps, run only agreed checks with disposable data, and report actual outcomes.
Do not fabricate missing logs or complete the individual no-AI assessment for me.
```

The assistant is a critic of evidence, while the student owns the release decision.

### Critique prompt

```text
Act as a reviewer unfamiliar with our chat. Can you reproduce one success and one
failure from the manifest? What scope is justified by the evidence? Identify remaining
risks, missing docs, or a reason to withhold release. Separate observations from inference,
and give me questions to answer myself rather than writing my individual defense.
```

## Completion checks

Every artifact in the manifest is available and identifies its revision. Both dogfooding
cycles are complete, and the individual explanation passes the [assessment](../assessment.md).
No secret, home-history file or fabricated output appears in the evidence. Record any
unverified browser explicitly. The release statement matches the actual submitted version.

## Reflection

Which AI suggestion did you reject and why? Which test changed your confidence most?
What evidence is still absent? Would you trust yourself to maintain this code without
access to the original conversation? Explain why.
