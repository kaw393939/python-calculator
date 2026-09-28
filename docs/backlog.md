# Agile delivery plan

## Product goal and themes

Make repeatable calculations easy while making software design visible to learners.
Themes: **T1 Everyday usability**, **T2 Safe history**, **T3 Extension and learning**,
**T4 Reliable delivery**. All stories below are Must-have for this release.

| Epic | Theme | Story | User story | Acceptance |
| --- | --- | --- | --- | --- |
| E1 Foundation | T3,T4 | US-01 | As a learner, I want setup and architecture docs so I can understand and run the system. | Fresh editable install; linked docs; reviewed contracts |
| E2 Operations | T1,T3 | US-02 | As a user, I want multiple operands so I can calculate without repetitive commands. | UAT-01,02,03 |
| E2 Operations | T1 | US-03 | As an analyst, I want mean, median and population/sample deviation so I can summarize data. | UAT-04,05 |
| E3 Extension | T3 | US-04 | As a plugin author, I want discovery and clear interfaces so I can add operations independently. | UAT-06,07 |
| E4 History | T2 | US-05 | As a user, I want automatic save/load so results survive restarts. | UAT-08,09,10 |
| E4 History | T1,T2 | US-06 | As a user, I want readable history and deletion so I can maintain my records. | UAT-11,12 |
| E5 CLI | T1 | US-07 | As a terminal user, I want help, useful errors and scripting so the calculator fits my workflow. | UAT-13,14 |
| E6 Quality | T4 | US-08 | As a maintainer, I want layered tests and CI so changes are safe. | All UAT scenarios automated; lint and CI pass |

## Delivery order

1. Specification and educational docs; review and resolve contradictions.
2. Installable project, virtual environment, test/lint configuration, CI.
3. Built-in strategies, registry, plugin example, unit tests.
4. Records, observer, facade, CSV repository, persistence integration tests.
5. Commands, REPL, formatting, subprocess tests.
6. Hands-on CLI trial, documentation reconciliation, final verification.

Each stage has a GitHub issue and focused commits referencing it. A stage can have
multiple commits when production and test changes form separately reviewable units.
Do not mix unrelated changes merely to close an issue.

## Definition of ready

Story names its user value, measurable acceptance criteria, dependencies, and
failure cases. Ambiguous command or data contracts are resolved in the specification.

## Definition of done

Implementation and positive/negative tests pass; documentation reflects actual
behavior; interactive use has been exercised where relevant; commit references its
issue; acceptance evidence is recorded; CI is green before final delivery.

## Future backlog (not release promises)

Exact decimal arithmetic; units and conversions; filtering/large history pagination;
optional alternative repositories; concurrent writers with locking or a database.
