# Case study: a calculator becomes an engineering workflow

This is a critical reconstruction, not a verbatim chat transcript. All descriptions of
the conversation below are **paraphrases**. Repository links support implementation
facts; events seen only in the conversation are identified separately. GitHub links
require access to this private repository; instructor-provided snapshots are the fallback.

## 1. Start with intent, then resolve decisions

Conversation paraphrase: the user wanted a new Python repository, virtual environment,
pytest, a REPL, four arithmetic operations, design patterns, automatic CSV history,
and positive/negative unit, integration and E2E testing. They asked to see the design first.

The [initial specification commit](https://github.com/kaw393939/python-calculator/commit/3c4c823)
and [issue #1](https://github.com/kaw393939/python-calculator/issues/1) turned that request
into contracts. Variable operands and keyword options later required JSON argument cells,
rather than fixed operand columns. Population deviation uses ddof=0; sample uses ddof=1.
These are product decisions, not details an assistant should silently invent.

Conversation-only observation: an existing calculator checkout already pointed at another
repository. The assistant created a sibling project and later verified the original stayed
clean. Lesson: inspect working directory, status and remote; a chat's attached folder may
not be the target of the current task. Do not treat confidence as evidence of repository identity.

## 2. Design boundaries that support change

[Issue #2](https://github.com/kaw393939/python-calculator/issues/2) established packaging and CI.
[Issue #3](https://github.com/kaw393939/python-calculator/issues/3) and
[commit b1bd355](https://github.com/kaw393939/python-calculator/commit/b1bd355) added strategies
and plugin discovery. [Issue #4](https://github.com/kaw393939/python-calculator/issues/4) and
[commit 50a2a88](https://github.com/kaw393939/python-calculator/commit/50a2a88) added the facade,
immutable records, persistence observer and pandas repository.

The domain does not import pandas. `History.replace` calls the required observer before
assigning new records: a failed save prevents publishing the new snapshot. This is one
synchronous observer, not a general transactional event bus. Students should challenge
whether this abstraction is justified rather than praising the presence of a pattern name.

## 3. Tests and actual use reveal different things

[Issue #5](https://github.com/kaw393939/python-calculator/issues/5) produced the command-driven
CLI. [Issue #6](https://github.com/kaw393939/python-calculator/issues/6) tracked release use
and review. A coverage configuration initially missed subprocess execution; enabling
coverage's subprocess support made the measurement more representative.

Conversation paraphrase: the assistant used arithmetic/statistics, errors, history deletion,
restart, and an installed square plugin. It shortened displayed IDs while retaining full
UUIDs in CSV. The conversation reported 85 tests and 100% statement coverage for revision
[4ba5178](https://github.com/kaw393939/python-calculator/commit/4ba5178), on September 28, 2026.
These are historical observations, not a guarantee about later versions or usability.

## 4. Dogfooding changes what “done” means

An intentional usability trial exposed raw float-conversion errors, no contextual help,
and literal escape sequences from Up-arrow. Those observations motivated
[issue #7](https://github.com/kaw393939/python-calculator/issues/7) and
[commit 6ae07a1](https://github.com/kaw393939/python-calculator/commit/6ae07a1): optional
readline editing, contextual help, case normalization and typo suggestions.

A second trial found that repeated calculations needed a reusable last result and manageable
history. [Issue #8](https://github.com/kaw393939/python-calculator/issues/8) and
[commit 56444fc](https://github.com/kaw393939/python-calculator/commit/56444fc) added `ans`,
recent/all/detail views and clear guidance. Notice the cycle: observe, reproduce, test,
change, retest, amend the specification. Adding more mathematical operations would not
have solved these interaction problems.

## 5. Reuse the domain when the interface changes

[Issue #9](https://github.com/kaw393939/python-calculator/issues/9),
[API commit 8dc6182](https://github.com/kaw393939/python-calculator/commit/8dc6182), and
[frontend commit 0f4b57d](https://github.com/kaw393939/python-calculator/commit/0f4b57d)
put FastAPI and JavaScript around the existing command/facade path. The server lock protects
concurrent requests inside one process. Web and CLI have separate default history files;
sharing a file across live processes is not supported.

Conversation report, September 28, 2026: 109 tests and 98.31% statement coverage on the
application represented by [b22b89f](https://github.com/kaw393939/python-calculator/commit/b22b89f).
A browser trial exercised guided addition, deviation, command-mode ans, errors, search,
details, clear cancellation and reload. These observed workflows do not prove every
browser feature, accessibility criterion or plugin combination.

## 6. A failed tool call is still evidence

Conversation-only observation: subsequent attempts to control Safari timed out. The
assistant disclosed that failure and based its review on earlier in-app browser use.
**Safari compatibility was not verified.** Neither a screenshot from another browser nor
passing API tests would justify changing that statement.

The review also criticized small/low-contrast controls, a result far below the inputs,
and ambiguous “Reuse.” These are candidate improvements, not implemented features.
Undo, arbitrary expression parsing and history pagination remain outside the application.

## Reproducible study revisions

| Revision | Use | Known state |
| --- | --- | --- |
| `4ba5178` | CLI usability starting point | No contextual help, numeric errors are technical |
| `6ae07a1` | After first UX iteration | Help/errors/editing improved; no ans or recent-history commands |
| `56444fc` | Before web adapter | CLI improvements present; web adapter not yet present |
| `b22b89f` | Reference application | CLI plus FastAPI/JS and 109-test historical baseline |

Never reset your working branch to reproduce history. The [student guide](README.md)
shows isolated snapshot setup, including instructor tar archives when Git history is
unavailable. Instructors should distribute these four snapshots plus this learning folder.
Use your own implementation for a learning task; inspect historical fixes only after
attempting it, and disclose any reference solution you used.

## Discussion

Which assumptions should have been clarified earlier? Where did tests provide evidence
but leave usability uncertain? Which abstraction would you remove from a four-function-only
calculator? What evidence would be needed before hosting this for multiple users?

Review basis: source symbols and the listed commits were inspected; reproduction results
are recorded in [validation-report.md](validation-report.md). No learner pilot is claimed.
