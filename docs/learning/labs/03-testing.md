# Lab 3 — Test behavior, not confidence

## Outcomes and starting state

LO-05/08: choose appropriate test levels and evaluate evidence. Allow 90 minutes plus
60 minutes practice. Complete Lab 2 and activate the reference copy's venv. For the
regression exercise, make a separate copy at `4ba5178` using the setup guide. Never
reset your current branch. Keep the reference and exercise environments separate.

Vocabulary: a **unit test** isolates a behavior; an **integration test** exercises
collaborators; **E2E** drives an external entry point. A **mock** can force an I/O failure;
that does not make a mocked test an end-to-end proof. **Coverage** measures execution.

## Scenario matrix

| Scenario | Level and assertion |
| --- | --- |
| Add several numbers / reject too few | Unit: value and intended exception |
| Divide by zero / reject nonfinite result | Unit + integration: error and unchanged records |
| Unsupported keyword / malformed numeric token | Parser/strategy unit: useful diagnostic |
| Broken or colliding plugin | Registry unit: warning, built-ins remain usable |
| CSV round trip | Integration: IDs, timestamps, args, kwargs, results preserved |
| Corrupt CSV or failed replacement | Integration: explicit error, old file/memory unchanged |
| REPL error followed by valid input | E2E: subprocess survives and saves only valid result |
| Process restart | E2E: a second process can read saved history |
| Invalid API command or save failure | Web integration in Lab 5: HTTP status and unchanged history |

## Tasks

1. Run the reference tests and capture the complete output, environment and revision:

   ```sh
   python --version
   git log -1 --oneline
   pytest --cov=calculator --cov-report=term-missing --cov-fail-under=90
   ruff check .
   ```

   Count tests from your run, not the case study. Subprocess coverage is configured in
   `pyproject.toml`; explain which code would otherwise be missed.
2. Read `tests/integration/test_history.py`. In `test_uat_10_atomic_failure`, explain
   what replacing `os.replace` with a failing function simulates. Point to assertions
   covering both in-memory state and original file bytes. Do not actually fill a disk.
3. In the **separate `4ba5178` exercise copy**, save this regression test as
   `tests/unit/test_contextual_help_lab.py`:

   ```python
   from types import SimpleNamespace
   from calculator.commands import parse
   from calculator.operations import Registry

   def test_contextual_help_has_usage():
       registry = Registry.discover(lambda _: None, entries=[])
       context = SimpleNamespace(registry=registry)
       assert 'ddof=0|1' in parse('help stddev').execute(context)
   ```

   Run `pytest tests/unit/test_contextual_help_lab.py -q`. It should fail because the old
   parser rejects help arguments. A missing import or broken venv is not the intended red.
4. Implement contextual help in the exercise copy. Preserve generic help and reject
   extra arguments (`help stddev extra`). Add a test for unknown topics and a plugin
   whose metadata appears in help. Update the historical `help x` parser test: parsing
   one topic is now valid; resolving an unknown topic should fail during execution.
   Do not delete tests just to turn the suite green.
5. Run the regression, then the whole exercise suite. Use the CLI to check `help stddev`.
   Save red and green evidence, a focused diff, and a linked commit. The historical
   implementation `6ae07a1` is a comparison after your attempt, not a substitute for it.
6. In your evidence log, audit the claim “coverage is 100%, therefore the UI is usable.”
   List two missing types of evidence and one test that executes a line without meaningfully
   asserting the outcome. Avoid adding tests solely to increase the percentage.

## AI prompt

```text
Inspect this isolated exercise copy, its revision, remote and existing tests first;
preserve my files. Reproduce the contextual-help failure with the lab's test before
editing. Propose the smallest fix and positive/negative regression checks. Then implement,
run the targeted and full tests, use the CLI, and report commands, exit codes and results.
Do not claim browser usability from Python coverage and do not change the reference copy.
```

This asks for the causal chain from reproduced defect to measured improvement.

### Critique prompt

```text
Challenge our evidence. Did the red test fail for the intended reason? Did we weaken
an assertion or mask an exception? Which collaborator is real versus mocked? What
could still be wrong with persistence or usability despite green tests? Inspect the
diff and actual logs before answering, and propose a targeted check for any real gap.
```

## Completion checks

Submit the scenario matrix, red/green logs, relevant diff, updated help requirement and
full-suite result. A reviewer should see the intended failure disappear while generic
help and invalid-topic behavior remain checked. All I/O uses disposable paths.

## Reflection

Why is a wrong result with status 0 not a passing positive test? How would you tell a
regression in the product from a dependency/setup failure? What could API tests miss?
