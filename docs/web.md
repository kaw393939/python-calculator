# Calculator Studio: FastAPI + JavaScript

## Start the web app

```sh
source .venv/bin/activate
python -m pip install -e '.[dev]'
calc-web
```

Open **http://127.0.0.1:8000**. Interactive API documentation is at `/docs`.
Choose another port or CSV with `calc-web --port 8001 --history ./web.csv`.
The default is `~/.python-calculator/web-history.csv`, deliberately separate from
the CLI's default file to avoid two processes overwriting each other's history.
`CALCULATOR_HISTORY` can set the web history location; `--history` takes precedence.
To use a CLI history file on the web, stop the CLI first, then pass that path.

## Interface guide

- **Guided:** choose an operation, type space-separated operands, and calculate.
  Negative numbers, scientific notation and `ans` are supported. `ans` references
  the latest retained result, including results loaded after a restart.
- **Statistics:** choose population or sample standard deviation by name.
  Advanced numeric `key=value` options remain available; explicit `ddof` in named
  options overrides the selection. Unsupported options produce an error.
- **Command:** enter the same calculation syntax as the CLI, e.g.
  `stddev 2 4 6 ddof=1`. Management commands use the dedicated history controls.
- **History:** newest first, searchable by expression/result. Reuse places a result
  into the operands field; details show full precision and identity. Delete removes
  one record. Clear all asks for confirmation and can be cancelled. Deletion has no undo.
- **Export CSV:** downloads an interoperable snapshot including full IDs, timestamps,
  numeric results and JSON argument/options cells. Loading remains server-side through
  the configured CSV; browser CSV upload is not implemented.
- **Plugins:** installed entry-point plugins appear automatically after server restart,
  including their descriptions and usage. The Plugins category excludes built-ins.
- **Keyboard:** Tab navigates controls; Ctrl/Cmd+Enter submits. Result copy retains the
  stored number, while visible numbers use 12 significant digits.

## Architecture

The web application is another adapter around the existing system:

```text
Browser form / command → JSON API → CalculateCommand → Calculator facade
                       → plugin strategy → persistence observer → pandas CSV
```

Vanilla JavaScript uses Fetch to call the same-origin API and builds record views with
`textContent`, avoiding HTML interpretation of plugin data. CSS provides desktop and
small-screen layouts without a build step or third-party asset requests. Assets are
included in the Python wheel as package data.

`create_app(path, registry)` supports dependency injection for isolated tests. A lock
serializes calculation and history mutation requests inside the server process;
parallel requests cannot overwrite the same in-memory snapshot. Plugin execution is
synchronous and trusted. This is a local single-user application, not a hosted service.
Run one server worker per CSV. Multiple processes, authentication, remote deployment,
and cross-process locking are outside this release. The launcher binds to loopback;
mutation requests from another browser origin are rejected.

## API contract

| Endpoint | Behavior |
| --- | --- |
| GET `/api/operations` | Plugin names, descriptions, usage and discovery warnings |
| POST `/api/calculations` | `{ "command": "add 2 3" }`; 201 and the saved record |
| GET `/api/history` | Records newest first |
| DELETE `/api/history/{id}` | Delete exact ID or unique prefix; 204 |
| DELETE `/api/history?confirm=true` | Explicitly clear history; 204 |
| GET `/api/history.csv` | Download complete CSV snapshot |

Invalid calculations return 400 and create no record. Invalid request schema returns
422. Persistence failure returns 503 and preserves state. Browser-origin rejection
returns 403. Startup fails on a corrupt CSV instead of silently discarding data.
Calculation commands are limited to 4096 characters. The UI loads personal histories
in full; pagination and larger data volumes remain future work.

## Acceptance and verification

- **US-09 / E7 / T1:** As a user, I can calculate in a browser without remembering syntax.
- **US-10 / E7 / T2:** As a user, I can search, reuse, inspect, delete and export saved results.
- **US-11 / E7 / T3:** As a plugin author, my operation appears without frontend edits.
- **UAT-15:** Addition and plugin calculation return 201 and persist; ans chains results.
- **UAT-16:** Invalid syntax, insufficient operands, division by zero, unknown operation,
  plugin exception and storage failure preserve history and report actionable errors.
- **UAT-17:** Reload retains results; delete and explicit clear persist; cancelled clear
  leaves records unchanged; export contains original IDs and arguments.
- **UAT-18:** Concurrent API calls retain every result. Cross-origin mutations are rejected.

Automated API tests live in `tests/integration/test_web.py`. CLI/unit tests continue
to verify the shared domain behavior. Browser verification is recorded in review.md.

References: [FastAPI static files](https://fastapi.tiangolo.com/tutorial/static-files/)
and [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/).
