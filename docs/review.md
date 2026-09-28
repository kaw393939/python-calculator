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

Pending implementation, automated tests, and hands-on CLI exercise.
