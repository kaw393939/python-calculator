# Engineering with AI: from calculator CLI to web

Learn to direct an AI coding assistant, understand the resulting software and verify its
claims. You will specify behavior, extend a CLI through plugins, test failures, complete
two dogfooding cycles and build a web adapter around the same core.

Plan six 90-minute sessions plus approximately six hours independent work. Work in your
own copy. You are responsible for the code and claims you submit, even if AI wrote them.

## Readiness checklist

- Explain a Python function, list/dict, exception and module import.
- Navigate directories, create a venv and run a command in a terminal.
- Understand Git status, a commit and the difference between local work and a remote.
- Have Python 3.11+, Git, an editor and an AI coding assistant. GitHub access is useful;
  local issue drafts are an accepted temporary fallback.

For review, use the [Python tutorial](https://docs.python.org/3/tutorial/),
[venv reference](https://docs.python.org/3/library/venv.html) and
[Git introductory book](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control).
Ask the instructor for prerequisite practice rather than letting an assistant hide gaps.
Commands below assume macOS/Linux bash or zsh. On Windows use WSL or ask the instructor
for platform-specific adaptations; these shell commands are not PowerShell syntax.

## Safe setup: choose one access route

**Route A — authorized source checkout:** obtain this repository through your authorized
GitHub access or a learner fork, then run the following from its root. Do not run it from
the separate original `is218-oop-calculator` repository.

```sh
pwd
git status --short --branch
git remote -v
COURSE_SOURCE="$PWD"
LEARNER_COPY="$(mktemp -d)"
git archive b22b89f | tar -x -C "$LEARNER_COPY"
cd "$LEARNER_COPY"
git init -b main
git add .
git commit -m 'chore: start learner reference from b22b89f'
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
LAB_DATA="$(mktemp -d)"
export LAB_HISTORY="$LAB_DATA/history.csv"
printf 'Learner copy: %s\nDisposable history: %s\n' "$LEARNER_COPY" "$LAB_HISTORY"
calc --history "$LAB_HISTORY" --command 'add 2 3'
```

Expect 5. Record the printed locations. The snapshot has no connection to the original
remote; `git remote -v` should be empty until you deliberately add your own destination.
If Git asks for identity, configure your chosen author identity for this learner repo;
do not paste someone else's credentials. Keep this lesson folder open in the source
checkout because historical snapshots predate the course docs.

**Route B — no private repository access:** obtain the instructor-provided `b22b89f.tar`
and this learning folder. Make a new directory with `mktemp -d`, extract the archive there
using `tar -x -f /path/to/b22b89f.tar -C "$LEARNER_COPY"` (replace the archive path with its
actual location), then start at `cd "$LEARNER_COPY"` in the commands above. For later
historical exercises request `4ba5178.tar`, `6ae07a1.tar` and `56444fc.tar`. Never pretend an
unavailable private link has been read. Dependencies still require package access or an
instructor-prepared wheelhouse; offline materials alone do not install packages.

### Historical exercise copies

Make each exercise independent. In a fresh terminal, set `COURSE_SOURCE` to your authorized
source checkout's actual path. Then, for the first historical exercise:

```sh
EXERCISE_COPY="$(mktemp -d)"
git -C "$COURSE_SOURCE" archive 4ba5178 | tar -x -C "$EXERCISE_COPY"
cd "$EXERCISE_COPY"
git init -b main
git add .
git commit -m 'chore: start isolated 4ba5178 exercise'
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
LAB_DATA="$(mktemp -d)"
export LAB_HISTORY="$LAB_DATA/history.csv"
```

For the second dogfooding cycle use `6ae07a1`; for the CLI-only web exercise use `56444fc`.
Replace the revision in both archive and initial commit message. Route B substitutes the
corresponding supplied tar extraction for `git archive`. Each copy needs its own venv;
check `python -c 'import calculator; print(calculator.__file__)'` before testing.
Create `evidence/` in learner copies for logs, issue drafts and reflections. No Git reset,
force-push, deletion of your original repository or clearing of home-history files is needed.

## Learning sequence

| Session | Lab | Deliverable |
| --- | --- | --- |
| 1 | [Requirements and delivery](labs/01-requirements.md) | Requirements, stories, small issues and traceability |
| 2 | [CLI design and plugins](labs/02-cli-design.md) | Diagram, cube plugin and contract tests |
| 3 | [Testing](labs/03-testing.md) | Scenario matrix, actual red/green evidence and coverage critique |
| 4 | [Dogfooding](labs/04-dogfooding.md) | Two complete improvement journals and verified fixes |
| 5 | [Web adapter](labs/05-web-adapter.md) | Shared-core API/JS slice and separate API/browser evidence |
| 6 | [Engineering review](labs/06-engineering-review.md) | Submission manifest, release decision and individual defense |

Consult the [glossary](glossary.md) while reading source. The [case study](case-study.md)
explains the real project's decisions and mistakes; the [assessment](assessment.md)
defines scoring and the independent explanation gate. The
[instructor guide](instructor-guide.md) contains facilitation and model answers.
[Validation report](validation-report.md) records the author dry-run and limitations.
[Specification](specification.md) and [delivery plan](delivery.md) govern this package.

## How to work with AI

Start with each lab's prompt and adapt it to your inspected environment. Ask for a plan,
constraints and verification before a change; then inspect the diff, run tests and use
the product. Keep a short assistance log: task, delegated work, suggestion accepted/rejected,
and what you checked yourself. Don't submit AI assurances as test results.

A tool outage is not a pass. Use a manual terminal/browser when possible and record the
actual steps. If unavailable, mark the workflow unverified and agree a later check with
the instructor. You may use the reference solution after attempting an exercise if you
disclose that comparison. Don't let the assistant perform the final no-AI explanation.

## Completion and cleanup

Submit the Lab 6 manifest and artifacts. Proficiency needs 70/100 plus the individual gate.
Evidence must include positive/negative unit, integration and E2E checks, two complete
cycles, documented API/browser results and honest limitations. Keep commits focused and
reference your own issue numbers. An empty local remote is safer than accidentally pushing
student work to the instructor project.

Stop only the test servers you started with Ctrl-C. Keep temporary paths until evidence is
reviewed, then remove only your identified disposable copies/data if desired. Application
features such as undo, exact decimal arithmetic and large-history pagination remain future
work; they are not graduation requirements for this module.
