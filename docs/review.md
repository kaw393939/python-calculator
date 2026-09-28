# Review and release notes

## Pre-implementation specification review

Reviewed README, requirements, story acceptance, architecture, and plugin guide as
one contract. Resolved these findings before implementation:

1. **Ambiguous clear confirmation:** replaced an interactive prompt with explicit
   `history clear --yes`, usable in scripts and REPL without hidden input states.
2. **Save-failure inconsistency:** specified persist-before-publish observer behavior
   so a reported failure cannot leave an apparently saved in-memory record.
3. **Variable-argument CSV:** specified JSON cells for args/kwargs instead of fixed
   operand columns. This preserves plugin options and arbitrary argument counts.
4. **Statistical ambiguity:** population deviation defaults to ddof=0; sample uses 1;
   all other ddof values fail. Documented minimum sample size.
5. **Extension lifetime:** historical records do not depend on installed plugins.
6. **Atomicity scope:** explicitly excluded concurrent writers and multi-observer
   distributed transactions; atomic replacement only protects one file update.
7. **Numeric scope:** finite floats only, including plugin results; no eval or exact
   financial arithmetic claims.

## Implementation and CLI review

The first real PTY session exercised help, operations, addition, both deviation
modes, negative operands, zero-division recovery, history, deletion by prefix, and
rejection of an unconfirmed clear. It exposed overly wide history output.

Changed displayed IDs to unique prefixes of at least eight characters and timestamps
to UTC seconds. Full values stay in CSV. Prefixes expand automatically on collisions;
FR-08 and acceptance tests now specify that behavior. This makes everyday history
readable without sacrificing stable identity or persistence precision.

Code review also found that Python API callers could pass invalid option names even
though the CLI rejected them. Added facade validation to prevent writing a record
that the strict CSV reader would later reject.

The initial coverage run missed subprocess execution; enabled coverage's subprocess
patch rather than weakening the threshold. Unit, integration, and real subprocess
tests now contribute to the same report.

## Release verification (2026-09-28)

- 85 positive/negative tests passed across unit, integration, and subprocess E2E.
- Combined statement coverage: 100%; enforced CI minimum: 90%.
- Ruff lint passed.
- Installed the separate example package, discovered `square` in operations, and
  calculated `square 4` = 16. Uninstalled it and verified its historical record
  still loaded and displayed. Explicit clear persisted an empty CSV.
- Reopened the CLI against the same temporary CSV and verified compact history,
  deletion persistence, and both standard deviation modes.
- Original sibling `calculator` checkout remains clean on its original remote;
  this project lives separately in `python-calculator`.

## Final documentation review

Checked all relative Markdown links, CLI examples, plugin installation commands,
requirements against implemented behavior, and UAT references against test names.
The release supports seven built-ins plus independently installed plugins. “Extensible”
does not mean every mathematical operation is already included. Single-writer and
finite floating-point limitations remain explicit in the specification and README.

## UX iteration 1

Added failing tests before implementation, then verified 92 passing tests and lint.
In a real PTY, Up recalled `multipy 2 3`; Ctrl-U cleared it; typing `mul` then Tab
completed `multiply`, and `6 7` returned 42. Contextual help, capitalized commands,
numeric errors, and typo suggestions behaved as expected. A further trial exposed
missing result reuse and recent-history navigation, motivating issue #8.
