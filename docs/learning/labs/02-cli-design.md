# Lab 2 — Understand and extend the CLI

## Outcomes and starting state

LO-03/04: trace the design and implement a separately packaged operation. Allow 90 minutes
plus 75 minutes practice. Complete Lab 1; start from isolated `b22b89f` with `.venv` active.
Use `LAB_HISTORY` from the [setup guide](../README.md), never a home-directory history.

Vocabulary: **Strategy** is the interchangeable algorithm; **plugin discovery** finds
installed strategies. `*args` collects operands and `**kwargs` collects named options.
A **protocol** describes a contract but cannot prove that a plugin obeys it.

## Read and trace

```text
CLI text → parse → CalculateCommand → Calculator.calculate → Registry.get → execute
                                             ↓
                                     proposed immutable Record
                                             ↓
                          History.replace → PersistenceObserver → CsvRepository
                                             ↓
                              publish new records after save succeeds
```

The command represents intent; the facade coordinates; the strategy calculates; the
observer reacts to proposed history changes; the repository serializes CSV. On startup,
load supplies the initial history. Failure before publication leaves old memory intact.
Read `commands.py`, `core.py`, `operations.py`, `history.py` and `storage.py` in
`src/calculator/`. Mark the exact function for every arrow in your own diagram.

| Principle | Example to inspect | Question to challenge the design |
| --- | --- | --- |
| Single responsibility | `parse` vs `CsvRepository.save` | Do they change for the same reason? |
| Open/closed | `Registry.register` | Can a cube plugin avoid facade edits? |
| Liskov substitution | `Operation.execute` | What if a plugin returns a string or infinity? |
| Interface segregation | Operation vs repository protocols | Does either require irrelevant methods? |
| Dependency inversion | Constructor-injected registry/history | Can the facade run without importing pandas? |

For a four-function script with no persistence or extension, direct functions could be
clearer. Here, extension and failure isolation motivate boundaries; pattern counts do not.

## Tasks

1. Exercise the existing CLI and explain each result:

   ```sh
   calc --history "$LAB_HISTORY" --command 'subtract 20 5 3'
   calc --history "$LAB_HISTORY" --command 'divide 100 2 5'
   calc --history "$LAB_HISTORY" --command 'stddev 2 4 6 ddof=1'
   calc --history "$LAB_HISTORY" --command history
   ```

   Expect 12, 10 and 2, then records with unique IDs. Read the CSV and identify the
   JSON args/options cells. Explain why fixed operand columns no longer suffice.
2. Read `examples/square_plugin/pyproject.toml` and its `Square` class. Install and test:

   ```sh
   python -m pip install -e examples/square_plugin
   calc --history "$LAB_HISTORY" --command 'square 4'
   calc --history "$LAB_HISTORY" --command 'square 4 5'
   ```

   Expect 16, then a nonzero exit and usage error. Failed execution adds no record.
3. In your learner copy, create a separate `examples/cube_plugin` distribution modeled
   on square: unique distribution/module names, entry point group
   `python_calculator.operations`, name `cube`, and a no-argument class. Require one
   finite operand and no options; return its cube. Do not modify built-in operations.
4. Write tests for `cube(3)=27`, `cube(-2)=-8`, missing/excess operands, unsupported
   options and overflow/nonfinite output. Include one facade-level test proving a
   failed cube calculation does not append history; the facade validates plugin results.
5. Install cube in the learner venv, restart the CLI and inspect `operations`. Calculate,
   restart and inspect history. Uninstall only the example package you installed:

   ```sh
   python -m pip uninstall -y calculator-square-example
   calc --history "$LAB_HISTORY" --command history
   ```

   The saved square record still displays. Record the analogous cube package name for
   cleanup; do not uninstall arbitrary globally installed packages.
6. Commit the plugin, metadata and related tests together, referencing your plugin issue.

## AI prompt

```text
Inspect this learner repository, its remote and plugin example before edits. Preserve
my work. Help add a cube plugin as an independent distribution using the existing
contract, with no parser/facade changes. Explain every packaging name. Propose positive
and negative unit/integration checks before implementation. Run the agreed checks in
my venv with temporary history, report actual outputs and show the focused diff.
```

The prompt makes packaging part of correctness and limits unnecessary core changes.

### Critique prompt

```text
Review the cube plugin contract and tests. Check arity, unsupported kwargs, nonfinite
values, installation discovery and failed-history behavior. Explain where each
validation occurs and why importing the class is not proof of entry-point discovery.
Identify one simpler design and its tradeoff. Report only checks actually performed.
```

## Completion checks

The plugin appears after restart and produces 27 through the installed CLI. Its tests
include failures and history preservation. Diagram arrows map to source functions.
Your commit does not duplicate the facade or bypass CSV persistence. Submit a short
SOLID explanation that includes one limitation, not just five favorable labels.

## Reflection

Would an observer be worth introducing without automatic persistence? Why does a
returned finite number matter even if the plugin accepts valid operands? What happens
if one process replaces a CSV generated from another process's stale snapshot?
