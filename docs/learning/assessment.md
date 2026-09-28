# Assessment: explain, verify, improve

Assess the evidence in the [Lab 6 manifest](labs/06-engineering-review.md), not the number
of lines generated or the sophistication of the student's AI tool. Total: **100 points**.
Proficiency requires **70/100 and a passing individual explanation check**. A polished
AI-written narrative cannot compensate for an inability to explain the submitted code.

## Rubric

Award within the indicated band using the listed evidence. Missing evidence earns zero
for the affected dimension; document the rationale. Use partial points within a band for
partially met indicators, not arbitrary preference for style.

| Dimension / outcomes | Excellent | Adequate | Insufficient |
| --- | --- | --- | --- |
| Requirements and traceability — 15; LO-01/02 | 13–15: measurable success/failure criteria, clear scope, linked story→issue→commit→check | 10–12: mostly measurable requirements and usable links; minor gaps | 0–9: vague criteria, missing failures or untraceable changes |
| Architecture and vocabulary — 20; LO-03/04 | 17–20: correct code-path diagram, all patterns/SOLID justified with tradeoffs; plugin adds behavior without core duplication | 13–16: accurate main path and functional plugin; some explanations superficial | 0–12: labels without understanding, broken contract or copied domain rules |
| Verification and failure handling — 25; LO-05/08 | 22–25: meaningful positive/negative tests at all levels, intended red/green evidence, save/restart checks, coverage limits explained | 16–21: most key scenarios covered; small evidence/isolation gaps | 0–15: happy-path-only assertions, wrong failure reason, production data use or unsupported claims |
| Dogfooding and iteration — 20; LO-06/08 | 17–20: two complete cycles with negative/repeated use, observed friction, linked fixes, retest and spec disposition | 13–16: both cycles present; minor journal/retest detail gaps | 0–12: fewer than two cycles, speculative observations or no verified change |
| Web/domain reuse — 10; LO-07 | 9–10: functional API/UI slice shares core, dynamic operations, accurate status/persistence/concurrency reasoning | 7–8: working slice and shared core with limited edge/browser evidence | 0–6: duplicated arithmetic, missing API tests or falsely claimed browser verification |
| Individual explanation and AI disclosure — 10; LO-08 | 9–10: independently traces success/failure, reasons through unfamiliar change, discloses assistance and challenges suggestions | 7–8: correct independent account with minor prompting and honest disclosure | 0–6: cannot explain core behavior or misrepresents AI/verification work |

## Individual explanation gate

Run for each learner, including group-project members. They may consult source and
language documentation, but not an AI assistant or a prewritten answer. Allow roughly
10–15 minutes; for larger classes schedule additional assessment time outside Session 6.

Ask the learner to:

1. Trace a calculation through parser, command, facade, strategy and persistence (2 points).
2. Explain exactly why memory does not change when saving fails (2 points).
3. Explain one unfamiliar small change, implement or accurately sketch it, and identify
   an appropriate positive/negative test (2 points).

Pass the gate with at least 4/6 and a correct save-failure explanation. These six points
are gate evidence, not extra points added to the 100-point rubric. Use the same evidence
when scoring the individual-explanation dimension. Offer a reassessment after remediation.

Possible questions: Where is ans resolved? Why is a plugin's return validated? Why doesn't
an `RLock` solve two separate processes writing a CSV? What changes if `history` is empty?
For an unfamiliar change, ask for rejection of fractional ddof or validation of another
operation's minimum operand count; do not assign a large unannounced feature.

## Evidence rules

The manifest contains requirements, design rationale, actual issues/commits, tests/logs,
two dogfooding journals, API/browser observations, limitations and an assistance log.
Record tool/version when practical, the task delegated, rejected or corrected suggestions,
and what the learner independently verified. Chat transcripts alone are not verification.

Label examples and simulations. Fabricated logs or exposed secrets require correction
before proficiency is established; instructors apply their institution's integrity policy.
An unavailable browser is an honest limitation, not automatic fabrication. Provide a manual
browser path or schedule a check; don't award the missing browser evidence as completed.

## Illustrative scoring calibration (not a real student)

A hypothetical submission has clear requirements but one weak link (12/15), strong design
with a shallow interface-segregation explanation (17/20), good three-level tests but limited
API failure coverage (20/25), two fully documented cycles (18/20), working shared-core UI
with manual browser evidence (9/10), and an independent explanation with honest disclosure
(8/10). Total: **84/100**. Gate: **5/6**, including correct save-failure reasoning. Proficient.
If the same submission scored 3/6 on the gate, 84 points would not establish proficiency.

Review a second hypothetical case: excellent screenshots with no negative tests, no failing
regression evidence and only one dogfooding cycle must fall in the insufficient bands for
verification and iteration, regardless of UI polish. Do not infer tests from screenshots.

## Outcome alignment

| Outcome | Primary learning evidence | Assessment dimension |
| --- | --- | --- |
| LO-01 | Lab 1 numbered requirements and acceptance examples | Requirements |
| LO-02 | Lab 1 issues and focused commits throughout | Traceability |
| LO-03 | Lab 2 diagram, source walkthrough and design tradeoffs | Architecture |
| LO-04 | Lab 2 installed plugin and CSV checks | Architecture + verification |
| LO-05 | Lab 3 matrix and red/green evidence | Verification |
| LO-06 | Lab 4 journals and actual repeated use | Dogfooding |
| LO-07 | Lab 5 API/UI slice and request trace | Web/domain reuse |
| LO-08 | Lab 6 evidence audit, limitations and individual defense | Verification + disclosure/gate |
