# Lab 4 — Use, observe, improve, repeat

## Outcomes and starting state

LO-06/08: complete two evidence-based iteration cycles and decide what is good enough.
Allow 90 minutes plus 90 minutes practice. Complete Lab 3. Use separate isolated snapshots
at `4ba5178` (cycle A) and `6ae07a1` (cycle B), with different disposable CSV paths. These
exercises intentionally revisit historical missing features; current main already has them.
The Lab 3 help change is background practice, not one of these two cycles.

Vocabulary: **dogfooding** means using your own product; **usability** concerns task effort
and recovery. An **observation** is what happened; an **inference** is your explanation.
For example, “`ans` caused a conversion error” is observable; “the user will abandon the
product” needs more evidence.

## Observation journal template

Copy this block for each cycle and fill it with real evidence:

```text
Cycle / date / revision / environment:
User task and context:
Exact commands or browser actions (including history path):
Expected behavior:
Actual behavior and output:
Observation versus inference:
Severity and reason (blocker, high, medium, low):
Reproduction steps:
Issue and acceptance criteria:
Failing test command / exit status / relevant output:
Fix commit and reviewed files:
Retest command / status / output:
Repeated-use and negative-workflow results:
Specification change (or reason none is needed):
Remaining limitations and release decision:
AI assistance used / claims independently checked:
```

## Tasks

Complete both cycles below in separate copies and record each in the journal.

### Cycle A — Errors that help people recover

In `4ba5178`, use the real CLI:

```sh
printf 'add 2 three\nadd 2 3\nadd 4 nope\nadd 4 5\nexit\n' | calc --history "$LAB_HISTORY"
```

The old CLI exposes conversion errors; valid calculations should still return 5 and 9.
This is both a negative workflow and repeated use. Confirm only two records were saved.
Create an issue specifying an operand-position diagnostic with the rejected value and a
repair hint. Prioritize it by the task disruption, not your preference for wording.

Before the fix, add a parser test asserting that `parse('add 2 three')` raises ValueError
whose text includes `Operand 2` and `three`. Test `stddev 1 2 ddof=true` separately so
options get their own label. Include NaN/infinity checks and retain their rejection.
Implement readable diagnostics; run the tests and the same five-command sequence again.
Record the change to the error-message contract in your learner specification. Compare
with `6ae07a1` only after attempting your solution.

### Cycle B — Reusing results without retyping

In a clean `6ae07a1` copy, run:

```sh
printf 'multiply ans 2\nadd 2 3\nmultiply ans 2\nadd ans 1\nhistory\nexit\n' | calc --history "$LAB_HISTORY"
```

Expected new behavior: the first command explains there is no previous result; then 5,
10 and 11, with three saved records. Old behavior rejects every `ans` operand and saves
only the add result. Write the acceptance criteria before fixing it.

Add a test around `parse(...).execute(calculator)` that first rejects empty-history ans,
then saves add 2 3 and uses it in multiply ans 2. Verify an intervening failed divide
does not replace the last result. After deleting the latest record, ans should refer to
the latest **retained** record; after clear, it should fail again. Restart and verify
loaded history supports ans. Store numeric operands in CSV, not the literal token.

If adding clear guidance too, replace the obsolete parser rejection of `history clear`
with a check that executing it refuses to clear without confirmation.

Implement the change in the command adapter; do not make every arithmetic strategy
understand the word ans. Re-run targeted tests, the full suite and the repeated workflow.
Record a focused commit and the new ans semantics. Historical `56444fc` provides a later
reference implementation, including additional history improvements outside this exercise.

## AI prompt

```text
Inspect my isolated exercise revision, status, remote and test paths; preserve my work.
Act as a user performing the cycle's exact task. Record actual observations before
proposing changes. Agree on measurable acceptance criteria, write a failing test,
make the smallest fix, rerun it and the relevant suite, and use the CLI again.
Use temporary histories only. Update the specification when behavior changes. Report
commands and outcomes; if tool control fails, mark the workflow unverified.
```

This prevents “I improved it” from replacing an observed before/after comparison.

### Critique prompt

```text
Audit both journal entries against the lab template. Find inferred claims presented
as observations, missing negative/repeated-use checks, unverified fixes or untracked
requirements. Read the tests and logs. Identify one improvement worth doing next and
one that should wait; explain the user impact rather than generating more features.
```

## Completion checks

Both cycles have their own issue, red evidence, focused fix commit, green tests, actual
CLI retest and documentation disposition. Each includes negative and repeated use.
A failed tool connection is not a successful retest: use a manual terminal and capture
its output, or explicitly leave that acceptance check unresolved.

## Reflection and stopping rule

Would you release if arithmetic passed but error recovery failed? Is undo essential for
your user, or a future story? Stop when the agreed criteria pass and remaining limitations
are acceptable for the stated scope. Two author's trials do not substitute for a learner
or customer study. Report “ready for this scope,” not “perfect for anything.”
