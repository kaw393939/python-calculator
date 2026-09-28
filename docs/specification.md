# System specification

## Scope and goals

Deliver a usable Python 3.11+ terminal calculator that is easy to extend and teach.
Users calculate, inspect results, and manage persisted history. Plugin authors add
operations without editing orchestration or parsing. Maintainers can trace stories
to acceptance tests and issue-linked commits.

## Functional requirements

- **FR-01:** REPL and `--command` mode accept operation names, positional finite
  floats, and unique numeric `key=value` options. Positional arguments precede
  options. Empty REPL input does nothing. Python expressions are never evaluated.
- **FR-02:** `add`, `subtract`, `multiply`, `divide` require at least two operands.
  Subtraction and division reduce left to right. Zero divisors fail.
- **FR-03:** `mean`, `median` require at least one operand. `stddev` accepts
  `ddof=0` (default population) or `ddof=1` (sample), requiring n > ddof.
  Unknown options, nonfinite values, and nonfinite results fail.
- **FR-04:** Discover installed entry points in `python_calculator.operations`.
  Each resolves to a no-argument plugin class with name, description, usage, and
  `execute(*args, **kwargs)`. Invalid, colliding, or broken plugins produce a warning
  and are skipped; built-ins remain available. Names use lowercase letters,
  digits and underscores, starting with a letter; CLI command names are reserved.
- **FR-05:** Successful calculations add immutable records: UUID, UTC ISO timestamp,
  operation, JSON positional arguments, JSON keyword options, and float result.
- **FR-06:** Load the chosen CSV on startup. Missing means empty; empty/corrupt files,
  wrong columns, invalid records, and duplicate IDs fail startup without overwriting.
  Old records remain readable when their operation plugin is absent.
- **FR-07:** History changes notify a persistence observer with the proposed complete
  snapshot. Save via pandas to a temporary file in the same directory, flush/fsync,
  then replace atomically. Publish in-memory state only after persistence succeeds.
  Save failure leaves existing history and memory unchanged and reports an error.
- **FR-08:** `history` prints unique ID prefixes (at least eight characters), UTC timestamps
  to the second, expressions, and results in a table. Full UUIDs and timestamp
  precision remain in CSV.
  `history delete ID` accepts a full UUID or unique prefix; missing or ambiguous IDs
  fail. `history clear --yes` explicitly clears all records; omission does not clear.
- **FR-09:** `help`, `operations`, `exit`, and `quit` are available. EOF exits cleanly;
  Ctrl-C exits with status 130. Interactive errors print a message and allow retry.
  One-shot command errors and startup failures exit 1; argparse usage errors exit 2.
- **FR-10:** Default history is `~/.python-calculator/history.csv`; `--history PATH`
  overrides it. Success output uses 12 significant digits; CSV retains float precision.

## Nonfunctional requirements and boundaries

- **NFR-01:** Separate CLI, commands, domain facade, plugins, and persistence using
  narrow protocols and constructor injection; no pandas dependency in the facade.
- **NFR-02:** Tests run without network, real home-directory writes, or installed
  third-party plugins. CI checks Python 3.11–3.14, lint, and the full test suite.
- **NFR-03:** Plugin failures must not terminate a running REPL. Plugins are trusted
  installed Python code, not sandboxed. No automatic package downloading.
- **NFR-04:** One process owns a history file at a time. Concurrent writers and
  distributed storage are outside scope; atomic replacement is not a file lock.
- **NFR-05:** Floating-point results are approximate. No arbitrary code evaluation,
  symbolic algebra, complex numbers, undo, or replay of historical calculations.
- **NFR-06:** Whole-history CSV rewrites favor clarity and small personal histories.
  Streaming, pagination, and databases can be future repository implementations.

## CLI grammar

```text
calc [--history PATH] [--command TEXT]
OPERATION NUMBER NUMBER... [KEY=NUMBER ...]
help | operations | history | history delete ID | history clear --yes | exit | quit
```

`shlex` tokenization supports shell-style quoting. Numeric options remain floats;
plugins interpret allowed values. History clear uses a flag instead of a secondary
prompt so scripts and interactive use share one predictable command contract.

## UX iteration 1 amendment

Commands are case-insensitive. `help OPERATION` reads description and usage from the
registry, including installed plugins. Unknown names suggest a close match; malformed
numbers identify the operand or option. `--help` documents examples and default storage.
Interactive terminals use optional standard-library readline for session-local command
recall, editing, and completion of operation/command words. Without readline, basic
input remains available. No extra command-history file is saved.

## UX iteration 2 amendment

`ans` is a positional operand referencing the latest retained history result, including
loaded history. It errors when history is empty. Deleted results are not reused.
`history` shows the latest 20 records; `history last N` requires a positive integer;
`history all` lists everything; `history show ID` displays full precision and identity.
`history clear` explains the record count and required confirmation flag.

## Web extension requirements (FR-11–FR-15)

- **FR-11:** FastAPI exposes the same registered operations and calculation command path.
- **FR-12:** A responsive JavaScript UI offers guided and command input, numeric options,
  readable population/sample selection, ans reuse, results and validation messages.
- **FR-13:** Searchable history supports reuse, full details, deletion, clear confirmation,
  and CSV export. Successful mutations automatically persist before reporting success.
- **FR-14:** A single web server serializes access to its history. Web and CLI default to
  different CSV paths to avoid accidental simultaneous writers.
- **FR-15:** Document setup, API routes, plugin discovery, failure behavior and limitations.

The complete interface, API contract and UAT-15–18 are specified in [web.md](web.md).
