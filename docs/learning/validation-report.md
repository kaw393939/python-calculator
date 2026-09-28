# Author validation report

Date: September 28, 2026. Scope: D-01–D-12 of the teaching specification.
Result: **author walkthrough and document audit passed**, with the limitations below.
This is not a learner pilot, certification of teaching effectiveness, or Safari verification.

## Environment and method

Application reference: `b22b89f`; historical baselines: `4ba5178`, `6ae07a1`, `56444fc`.
Teaching drafts were authored through `5b61523`, then reviewed and corrected in the
validation commit that contains this report. Environment: macOS arm64, Python 3.14.7.
Created independent `git archive` snapshots, initialized local Git repositories with no
remote, made independent venvs, installed editable dev dependencies and used disposable
CSV files outside the project. No application source changed in the teaching repository.
The original separate calculator repository remained clean on its original remote.

Red/green validation uses the real historical fix files as **reference solutions** in
isolated copies. It does not claim a new independent implementation or a student attempt.
The snapshots/venvs were created fresh; package downloads could use the machine's pip cache.
This verifies reproducibility on the stated machine, not every student's platform.

Actual command excerpts, failures, passing summaries and HTTP responses are preserved in
[validation-evidence.txt](validation-evidence.txt). Temporary directory names are replaced
with `$AUDIT_ROOT`; sample UUIDs/timestamps are generated test data. Browser evidence is
summarized below and captured in [browser-validation.png](browser-validation.png).

## Executed checks

| Check | Actual outcome |
| --- | --- |
| Reference editable install, baseline full suite | 109 passed, one dependency deprecation warning |
| Reference Ruff | All checks passed |
| CLI add/subtract/divide/sample deviation | 5, 12, 10, 2 as documented |
| Square installation/discovery and invalid arity | 16; invalid arity exits 1; record still readable after uninstall |
| Independently packaged author cube exercise | 27 and -8; missing/excess operands, unsupported options, infinity and overflow fail; discovered in operations |
| `4ba5178` baseline full suite | 85 passed |
| Help/operand/option regression tests on old revision | 3 intended failures |
| Historical first UX fix applied to isolated copy | Full suite with added regressions: 88 passed; contextual help displays ddof usage |
| `6ae07a1` baseline full suite | 92 passed |
| ans lifecycle test on old revision | 1 intended failure |
| Historical second UX fix applied to isolated copy | 92 passed (one added test and one obsolete parser case replaced); repeated-use and separate-process reload pass |
| CLI-only web starting point | `56444fc` inspected: web adapter absent, as lab requires |
| HTTP operations / add / zero division / history / export | 200 / 201 / 400 / 200 / 200; one saved result 5 |
| Actual web-server process restart | Saved result 5 retained |
| In-app browser workflow at port 8010 | Add 9; deviation 2; ans multiplication 6; zero division reports error without fourth record |
| Browser search/details/reuse/clear cancellation/reload | Search finds stddev, full details show ddof; reuse inserts 6; cancellation/reload retain three records |

The HTTP walkthrough used port 8011 and its own fresh CSV so the browser's records did
not alter the “one retained record” expectation. Test servers were stopped after checks.
CSV response content was verified over HTTP; a browser download/save dialog was not
retested in this author run. The test suite also exercises deletion and confirmed clear;
the browser walkthrough deliberately cancels clear rather than treating API coverage as
proof of every browser interaction.

The dependency warning reports Starlette's future preference for httpx2 over httpx in
TestClient. It did not fail the tests. It is recorded rather than silently suppressed;
updating that dependency is outside this documentation-only release.

## Two completed reference dogfooding journals

### Cycle A: actionable input errors

- Context/revision: repeated additions in a disposable `4ba5178` CLI copy.
- Task: `add 2 three`, `add 2 3`, `add 4 nope`, `add 4 5`.
- Expected: identify bad operand position/value, permit correction, preserve only successes.
- Observed before: Python conversion errors for three/nope; successful outputs 5 and 9.
- Inference: a position-specific repair hint should reduce diagnosis effort; no user study
  was performed to quantify that improvement.
- Severity: medium—task recovers, but the diagnostic requires implementation knowledge.
- Issue/fix: historical #7 / `6ae07a1`; applied corresponding files to the isolated copy.
- Failing tests: operand/option diagnostics plus contextual-help test; all three failed
  for the intended behavior before the fix, not environment setup.
- Retest: 88 full-suite tests pass; the same repeated workflow yields 5/9 and `Operand 2`
  diagnostics. Negative inputs do not prevent later valid commands.
- Requirement disposition: UX iteration 1 amendment in the application specification;
  Lab 4 explicitly asks learners to record their own error-contract amendment.
- Release assessment: meets this error-recovery scope; message readability is not a
  substitute for broader accessibility or learner testing.
- Assistance: AI authored the material and ran the audit; actual command results were
  checked against expected behavior. The historical implementation was disclosed.

### Cycle B: reusable latest result

- Context/revision: repeated calculations in disposable `6ae07a1` copy.
- Task: empty-history `multiply ans 2`, then `add 2 3`, `multiply ans 2`, `add ans 1`.
- Expected: useful empty-history error, then 5, 10, 11 with three saved numeric records.
- Observed before: ans rejected as a nonnumeric operand; only add produced 5.
- Inference: result reuse avoids manual copying; no speed improvement was measured.
- Severity: medium—users can retype numbers, but chaining is unnecessarily cumbersome.
- Issue/fix: historical #8 / `56444fc`, corresponding files applied to isolated copy.
- Failing test: empty-history/chain/failure/delete/clear lifecycle check failed before fix.
- Retest: full suite passes; repeated workflow returns 5/10/11, and initial ans correctly
  reports no previous result. Separate CLI processes also reuse loaded history.
- Requirement disposition: UX iteration 2 defines ans as latest retained history result;
  persisted args are numeric, not the literal token. Lab 4 teaches this boundary.
- Release assessment: meets stated personal-calculator scope; undo and pagination deferred.
- Assistance: reference historical fix used for author validation, not represented as a
  student solution. Evidence remains tied to the specific baseline and fix revision.

## Acceptance audit

| Acceptance | Evidence / disposition |
| --- | --- |
| AT-L01 | Student README provides prerequisites, two access routes, six-lab order, manifest and assessment links; read without conversation context. |
| AT-L02 | All six labs have outcomes/start/time, tasks, vocabulary, copyable prompt, critique prompt, completion checks and reflection. |
| AT-L03 | Glossary audited against LR-04 and source symbols; definitions/examples/misconceptions cover product, Git, design, evidence and web vocabulary; eight checks with answers. |
| AT-L04 | Independent installs, CLI commands, plugins, historical red/green tests and HTTP/browser workflows executed above. Student-authored solutions themselves remain learner work. |
| AT-L05 | Invalid operands/options, zero division, nonfinite results, plugins, malformed CSV, failed saves and restart covered by isolated baseline suite and explicit walkthroughs. |
| AT-L06 | Two reference journals above demonstrate observations, negative/repeated use, failures, historical fixes, retests and requirements. Learners must produce their own records. |
| AT-L07 | Web lab/source trace uses shared command/facade/plugin/persistence and explains lock/process limits; API and browser evidence separately labeled. |
| AT-L08 | Case claims linked to verified commits/issues; conversation-only observations labeled paraphrases; Safari remains unverified. |
| AT-L09 | Six rubric weights total 100; illustrative score totals 84; independent gate separate; all eight outcomes map to evidence/dimensions. |
| AT-L10 | All D-01–D-12 files exist; local file links and lab sections checked; historical refs resolve; no unfinished placeholder sections. |

## Review findings and fixes

1. Added an explicit Tasks heading to the dogfooding lab so its structure matches the
   other labs; both cycles remain clearly separate.
2. Explained that existing `help x` and `history clear` parser assertions must evolve
   when those commands become valid parse results. A change in the contract does not
   justify deleting negative execution coverage.
3. Made archive access and dependency access separate prerequisites. A private source
   link or source tar alone is not a guaranteed offline environment.
4. Clarified the web workload: inspect the reference, then implement a small vertical
   slice; rebuilding the entire polished UI is not a 90-minute expectation.
5. Reserved additional oral-assessment time for large classes and separated its gate
   points from the 100-point rubric to avoid double counting.
6. Replaced root README planning language with navigation to delivered materials and
   updated specification/delivery status without implying classroom validation.

## Limits and next validation

No real students were observed or graded. The score example is illustrative. Safari
was not retested and remains unverified following the earlier automation failures.
Windows/PowerShell setup is not validated; the guide specifies POSIX shell or WSL.
No new undo, pagination, expression engine or product feature was added. An instructor
pilot should evaluate timing, prerequisite gaps, accessibility and inter-rater consistency.
These limits do not block authoring delivery; they constrain the claims made about it.
