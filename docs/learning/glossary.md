# Engineering vocabulary in the calculator

Use this as a working reference, not a memorization list. Source examples were reviewed
against application revision `b22b89f`. Find the named symbols in
[the source](../../src/calculator) and explain their behavior before using the label.

## Product and delivery

| Term | Meaning and project example | Common misconception |
| --- | --- | --- |
| Requirement | A needed behavior or quality: save every successful calculation. | A proposed implementation is automatically a requirement. |
| Functional requirement | Something the program does: `history delete ID`. | Only the happy path counts. |
| Nonfunctional requirement | A quality/constraint: preserve history if a save fails. | These are always vague statements such as “fast.” |
| Scope | What this release includes: finite numeric calculations and personal CSV history. | An extensible system already implements everything. |
| Constraint | A boundary on solutions: one process owns a CSV. | Every constraint is a permanent limitation. |
| Acceptance criteria | Observable conditions of success: failed division creates no record. | “Works well” is measurable. |
| Acceptance test | A concrete check of a criterion: divide by zero, inspect unchanged history. | A criterion and the script checking it are the same artifact. |
| Theme | Broad direction: safe history. | A theme is a small implementation task. |
| Epic | Related work toward a larger outcome: history persistence and management. | Every epic belongs in one commit. |
| User story | User, capability, benefit: as an analyst, I want sample deviation to summarize observations. | A story is just a technical to-do with “as a user” attached. |
| Backlog | Ordered work not necessarily committed to this release: undo may remain future work. | Everything in it is already promised. |
| Definition of ready | Conditions for starting: defined semantics, examples, dependencies and failures. | It requires knowing every implementation detail. |
| Definition of done | Shared completion gate: tests, review, docs and evidence. | Generated code or a closed issue alone means done. |
| Traceability | Connections from FR-08 to issue, commit and history test. | A long document automatically provides traceability. |
| Atomic commit | One coherent reviewable change, such as contextual help with its tests. | It must contain exactly one file. |
| Git repository | Versioned source and history: the learner's calculator fork. | It is the same thing as the CSV repository class. |
| Remote | Named Git destination, such as the learner fork's `origin`. | Changing folders necessarily changes the configured remote. |
| Branch | A movable name for a line of commits: `codex/student-plugin`. | It is a complete independent copy of all external state. |
| Commit | A recorded source snapshot with ancestry and message. | It proves the code was tested. |
| Pull request (PR) | A proposed change for review between branches. | A push is automatically a PR or deployment. |

## Design and Python

| Term | Meaning and project example | Common misconception |
| --- | --- | --- |
| Domain logic | The application's rules: finite results and calculation history semantics. | All code belongs in the UI handler. |
| Class interface | Callable contract: operation metadata and `execute`. | It describes the visual interface. |
| User interface | How a person interacts: CLI commands or guided web fields. | A usable UI proves the underlying architecture is sound. |
| Protocol | Python structural typing contract, e.g. `HistoryRepository.load/save`. | Type hints enforce every runtime behavior. |
| Dependency injection | Supply collaborators to `Calculator(registry, history)`. | A dependency-injection framework is required. |
| SOLID | Five design principles used to reason about change boundaries below. | A checklist proves the design is optimal. |
| Single responsibility | Each component has a coherent reason to change: CSV storage differs from parsing. | Every class must have one method. |
| Open/closed | New registered operations can extend behavior without editing the facade. | Existing code must never change. |
| Liskov substitution | An operation replacement honors the calling/result/error contract. | Matching a method name is sufficient. |
| Interface segregation | A persistence observer needs `save`, not terminal controls. | More tiny interfaces are always better. |
| Dependency inversion | Core logic depends on contracts and injected collaborators, not pandas. | The core cannot depend on any concrete object at runtime. |
| Command pattern | `CalculateCommand` represents an action and delegates execution. | Every command automatically supports undo. |
| Strategy pattern | Registry-selected algorithms share an operation contract. | Each algorithm must be an elaborate class hierarchy. |
| Facade pattern | `Calculator` offers calculate/find/delete/clear while coordinating collaborators. | It should contain parsing, HTML and all mathematics. |
| Observer pattern | `History.replace` notifies `PersistenceObserver` before publishing a snapshot. | Observers must run asynchronously or support unlimited subscribers. |
| Repository pattern | `CsvRepository` encapsulates load/save of records. | It means a Git hosting service. |
| Adapter | CLI/web translate external input into the shared calling contract. | An adapter and a facade have identical purposes: one translates, the other simplifies access. |
| Plugin | Independently installed operation such as the example square package. | Plugin code is sandboxed or automatically trustworthy. |
| Discovery | Entry-point lookup locates installed plugin classes at startup. | Installing a package updates an already-running server's registry. |
| `*args` | Captures positional operands: `execute(2, 3, 4)` receives three values. | It disables argument validation. |
| `**kwargs` | Captures named options: `ddof=1` selects sample deviation. | Any keyword must be accepted by every operation. |
| Validation | Check a contract before accepting data: reject infinity and unsupported options. | Parsing a token as float makes it a valid operand. |
| Serialization | Encode args/options into JSON cells inside a CSV row. | Python tuples/dicts can be stored without a representation decision. |
| Persistence | Keep records beyond process lifetime through CSV load/save. | An in-memory list survives restart. |
| Atomic write | Replace the CSV only after a complete temporary file is flushed. | This prevents two processes from overwriting each other's updates. |
| Single-writer ownership | Only one process writes a given history file. | A thread lock automatically coordinates separate CLI/server processes. |

## Evidence and interfaces

| Term | Meaning and project example | Common misconception |
| --- | --- | --- |
| Unit test | Narrow behavior, such as `divide(100, 2, 5)`. | Anything fast is necessarily a unit test. |
| Integration test | Collaborating parts, e.g. facade → observer → real temporary CSV. | It must use the production database/file. |
| End-to-end (E2E) test | Drive an external entry point: subprocess CLI input and restart. | An API test proves browser controls work. |
| Positive test | Valid input yields the expected result and effects. | “No exception” is a sufficient assertion. |
| Negative test | Invalid input/failure yields the intended error and preserves state. | Any crash counts as passing. |
| Regression | Previously correct behavior breaks, or a test protects a reproduced defect. | Every new test is automatically a useful regression test. |
| Coverage | Which measured statements/branches executed under tests. | 100% coverage proves requirements, usability or all inputs. |
| Continuous integration (CI) | Automated checks for repository changes across supported Python versions. | Green CI verifies whatever wasn't included in those checks. |
| Test isolation | Temporary files and controlled registries prevent tests from sharing user state. | Tests may safely use the default home CSV if they later delete it. |
| Mocking | Substitute a boundary to force a condition: make `os.replace` fail. | Mock all collaborators and still claim end-to-end verification. |
| Dogfooding | Use the product yourself to discover friction: try `help stddev`. | It replaces systematic automated testing. |
| Usability | How effectively people accomplish tasks; useful errors reduce recovery effort. | Passing arithmetic tests means a pleasant experience. |
| Error recovery | A bad REPL command reports a problem and permits the next valid command. | Silently ignoring invalid input is helpful. |
| HTTP | Request/response protocol used by the browser and FastAPI. | It defines the calculator's mathematical rules. |
| Endpoint | Address/method contract such as POST `/api/calculations`. | A URL alone completely specifies an API. |
| API | Programmatic interface: JSON calculation requests and history responses. | It is necessarily a public internet service. |
| JSON | Structured interchange format used in requests and CSV argument cells. | It can represent infinity or arbitrary Python objects portably. |
| Status code | HTTP outcome category: 201 created; 400 invalid command; 503 save failure. | Every failure is an HTTP 500. |
| Request/response | Browser sends a command; server returns a saved record or error. | The client can declare that persistence succeeded without server evidence. |
| Frontend/backend | Browser presentation vs server validation and persistence. | Checking input in JavaScript removes the need for server validation. |
| Concurrency | Requests overlap; the web app serializes access with an `RLock`. | Atomic CSV replacement alone prevents lost updates. |

## Retrieval and application checks

1. Why is `NaN` not a valid calculator operand even though `float('nan')` parses?
2. What would a passing arithmetic unit test fail to establish about CSV persistence?
3. Where should a new cube operation go? Which files should usually stay unchanged?
4. Is changing two files inconsistent with an atomic commit? Give an example.
5. Why could a CLI and web server lose records despite atomic writes?
6. What should an assistant report when Safari automation times out?
7. How does a plugin differ from its strategy implementation?
8. Which requirement would justify an observer here, and what complexity does it add?

### Answer key: check after attempting

1. Numeric syntax and finite-domain validity are different contracts.
2. That the observer runs, writes safely, and reload preserves data.
3. A plugin package plus tests/metadata; facade and parser generally remain unchanged.
4. No: help behavior and its regression test form one coherent change.
5. Each process can save a stale snapshot; the in-process lock is not cross-process locking.
6. The attempt failed and Safari remains unverified; offer separately labeled evidence.
7. Strategy is the callable mathematical behavior; plugin includes packaging/discovery.
8. Automatic persistence on every mutation; notification order and failure propagation
   must be specified. Direct repository calls could be simpler for a smaller program.
