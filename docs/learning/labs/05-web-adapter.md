# Lab 5 — Put another interface around the same domain

## Outcomes and starting state

LO-07: explain and extend an API/UI adapter without duplicating mathematical logic.
Allow 90 minutes plus 90 minutes practice. Complete Lab 3. Keep `b22b89f` as the working
reference; make a separate `56444fc` copy if implementing the web adapter from the CLI-only
starting point. This is a guided reference-first exercise followed by one implemented
vertical slice, not an expectation to recreate the entire reference UI in 90 minutes.

Vocabulary: **HTTP endpoint**, **request/response**, **JSON**, **status code**, **frontend**,
**backend**, **adapter**, **concurrency** and **single-writer ownership** all describe
boundaries a four-function algorithm alone does not solve.

## Trace the request

```text
Guided fields / command text in app.js
    → POST /api/calculations {"command":"add 2 3"}
    → CalculationInput validation → parse → CalculateCommand
    → Calculator facade → strategy → persistence observer → CSV
    → HTTP 201 with saved record → JavaScript updates result/history
```

Read `web.py` and `static/app.js`. The API delegates to the same command/facade used by
the CLI. Browser validation is helpful feedback; server validation remains authoritative.
A response is successful only after required persistence succeeds.

## Tasks

1. In the reference copy start a disposable local workspace (keep this terminal open):

   ```sh
   calc-web --port 8010 --history "$LAB_HISTORY"
   ```

   Use a different file from any active CLI. In a second terminal:

   ```sh
   curl -i http://127.0.0.1:8010/api/operations
   curl -i -H 'Content-Type: application/json' -d '{"command":"add 2 3"}' http://127.0.0.1:8010/api/calculations
   curl -i -H 'Content-Type: application/json' -d '{"command":"divide 1 0"}' http://127.0.0.1:8010/api/calculations
   curl -i http://127.0.0.1:8010/api/history
   curl -i http://127.0.0.1:8010/api/history.csv
   ```

   Expect 200, 201 with result 5, 400 with an error, one retained record, and CSV.
   `curl` can exit 0 for HTTP 400; inspect the status, not just the shell exit code.
2. Open http://127.0.0.1:8010. Try Guided add 2 3 4, population deviation on
   `2 4 4 4 5 5 7 9`, and Command `multiply ans 3`. Record 9, 2 and 6. Try zero
   division and confirm no extra history. Search stddev, inspect Details, use a result,
   export CSV, open Clear history and cancel. Reload and verify records remain.
   Note that “Reuse” inserts the result; it does not replay the calculation. Stop the
   server with Ctrl-C in its own terminal and restart against the same disposable file.
3. Read and run `pytest tests/integration/test_web.py -q`. Locate checks for 422 invalid
   request schema, 503 persistence failure and no lost records under concurrent requests.
   A TestClient test is API integration; it does not exercise JavaScript rendering.
4. In the **CLI-only `56444fc` exercise copy**, create a small web adapter and page:
   add FastAPI, uvicorn and test httpx dependencies to your learner pyproject; implement
   an app factory receiving a temporary CSV path, GET operations, POST calculation,
   and GET history. Serve an HTML/JS form with operation, operands, optional numeric
   key=value input and Calculate. Use Fetch and `textContent`; return saved records.
   Do not import the reference `web.py` or copy its arithmetic into the handler.
5. Before implementing, write TestClient checks for successful add, invalid command,
   empty request, save failure and restart. Once working, install the square plugin
   and demonstrate that it appears without editing the frontend. Build choices from
   registry metadata rather than a hardcoded list of four operations.
6. Serialize modifications inside the server process. Explain why this does not permit
   simultaneous CLI/server writers. Bind the exercise server to loopback. Record the
   API contract and commit the coherent API slice and UI slice separately with issue links.

## AI prompt

```text
Inspect this learner copy and starting revision before edits; preserve existing work.
Build the lab's small FastAPI/JavaScript slice around the existing command and facade.
Do not duplicate arithmetic. Inject the history path; use temporary files in tests and
one server process per file. Propose API positive/negative tests first. Implement and
run them, then use the page in a browser if available. Report API and browser evidence
separately, including failed or unavailable checks, and update our endpoint contract.
```

The constraints preserve the design's investment and make the interface boundary testable.

### Critique prompt

```text
Trace a browser request all the way to CSV and back. Identify where validation, locking,
serialization and presentation occur. Inspect whether a successful response can happen
before saving. Compare the API tests with actual browser observations: which claims
remain unverified? Explain why an in-process lock does not coordinate another process.
```

## Completion checks

The slice supports valid calculation and failure without duplicating domain rules. Tests
use an injected CSV, and the browser evidence is independently labeled. Dynamic operations
include the installed example after restart. Stop test servers and record temporary
history locations; never remove or clear an unknown user's history for cleanup.

## Reflection

What changed when the second interface arrived, and what did not? Why are different
HTTP status codes useful? What new requirements would multi-user public hosting introduce?
If Safari control times out, what exactly can you claim about Safari support?
