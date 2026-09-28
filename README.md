# Python Calculator

An extensible terminal calculator with a friendly REPL, statistical operations,
and automatically saved CSV history. Built to demonstrate SOLID, Command,
Strategy, Facade, and Observer through a small, usable application.

## Quick start

Requires Python 3.11 or newer.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
calc
```

```text
calc> add 2 3 4
9
calc> stddev 2 4 4 4 5 5 7 9 ddof=0
2
calc> history
calc> exit
```

Use `calc --history ./experiment.csv` to choose a history file, or
`calc --command 'multiply 6 7'` for a single calculation. The default is
`~/.python-calculator/history.csv`. Type `help` or `operations` for guidance.

## Features

- Four arithmetic operations with multiple operands; mean, median, and standard deviation.
- Positional arguments and numeric `key=value` options, without evaluating Python code.
- Discoverable plugins; install the included square example to try extension.
- Readable history tables, stable IDs, deletion, and explicit clearing.
- CSV loaded on startup and atomically saved after each successful mutation.
- Unit, integration, and subprocess end-to-end tests with positive and negative cases.

## Documentation

| Guide | Purpose |
| --- | --- |
| [Specification](docs/specification.md) | Requirements, command contract, data model, and failure semantics |
| [Agile delivery](docs/backlog.md) | Themes, epics, stories, priorities, and acceptance criteria |
| [Architecture tutorial](docs/architecture.md) | Patterns, SOLID, and a calculation walkthrough |
| [Plugin guide](docs/plugins.md) | Build, install, discover, and remove calculation plugins |
| [Acceptance tests](docs/acceptance.md) | User acceptance scenarios and automated test mapping |
| [Review log](docs/review.md) | Documentation review findings and usability refinements |

## Development

```sh
pytest
pytest --cov=calculator --cov-report=term-missing
ruff check .
```

Work is tracked in GitHub issues. Each focused commit references its issue;
completed issue scope is closed by a `Closes #N` commit on the default branch.
See the backlog for the definition of done. This is a finite floating-point,
single-user calculator, not a symbolic algebra or exact financial arithmetic system.
