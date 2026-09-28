# Instructor guide

Teach this as a six-session engineering module, not a prompt-writing contest. Learners
should leave able to explain why a change is correct and what remains unknown. Budget
six 90-minute sessions plus about six hours independent work; adapt to experience.
The web exercise builds a small vertical slice rather than the full reference interface.
For a large class, schedule individual defenses separately from the 90-minute review.

## Preparation and access

Use the [student guide](README.md) yourself first. Confirm Python 3.11+, venv creation,
Git, dependency installation and a working terminal. Identify students needing review of
functions, exceptions and shell paths. Provide an editor and any AI coding assistant;
no particular paid model is necessary. Do not require credentials in assignment files.

This reference repository is private unless its owner changes visibility. Verify access
before class or distribute approved source snapshots plus the complete `docs/learning`
folder. From an authorized source checkout, produce archives without user files or `.git`:

```sh
COURSE_BUNDLES="$(mktemp -d)"
for revision in 4ba5178 6ae07a1 56444fc b22b89f; do
  git archive --format=tar --output="$COURSE_BUNDLES/$revision.tar" "$revision"
done
printf '%s\n' "$COURSE_BUNDLES"
```

Distribute the archives only through an owner-approved course channel. They are prepared
locally here, not automatically published. Include source SHA labels and this lesson pack;
old snapshots do not contain the later learning documents. If teaching without network,
prepare compatible dependency wheels for the students' Python/OS combinations in advance.
A source archive alone does not guarantee an offline pip installation. GitHub issue drafts
can stay local until connectivity/access is available.

## Session plans and interventions

| Session | Agenda (minutes) | Checkpoint and intervention |
| --- | --- | --- |
| 1 | 15 vocabulary; 20 brief critique; 40 Lab 1; 15 peer criteria review | Stop “user friendly” as an acceptance criterion; demand an observable example. Verify remote before issues/pushes. |
| 2 | 15 request trace; 20 patterns; 40 Lab 2; 15 tradeoff review | Ask what changes when adding cube. If parser/facade math grows, revisit plugin boundary. Finish packaging practice independently. |
| 3 | 15 levels; 20 intended failure; 40 Lab 3; 15 evidence audit | Confirm a red test failed for behavior, not import/setup. Contrast statement coverage with assertions. |
| 4 | 10 observation method; 55 Lab 4 cycles; 15 retest; 10 reflection | Require negative and repeated-use workflows in both journals. Finish code changes independently if needed. |
| 5 | 15 HTTP; 20 request trace; 40 Lab 5 slice; 15 browser review | API green is not browser green. Inspect where lock and persistence act; finish slice independently. |
| 6 | 15 manifest audit; 30 peer review; 30 sampled defenses/change work; 15 retrospective | Record unresolved checks honestly; individual defenses for everyone may need additional appointments. |

## Expected reasoning and model answers

**Lab 1:** A strong failure criterion says exactly which state remains unchanged. Theme
“safe history” can contain epic “persistence,” story “results survive restart,” and separate
issues for serialization and reload validation. Different groupings are valid when scope,
dependencies and evidence remain clear. “Use pandas” is an implementation constraint here,
not the user's underlying benefit.

**Lab 2:** Expected path: parse → command → facade → registry-selected execute → record →
history notification → CSV save → publish snapshot. Domain doesn't import pandas. All five
SOLID principles should be connected to specific code, not merely named. A cube plugin
returns 27 for 3 and rejects wrong arity/options. Contract checking occurs at several
boundaries: parser handles syntax, plugin handles operation rules, facade validates finite
results. A plugin does not provide isolation from malicious code. Direct function calls
would be a reasonable simpler solution without extension/persistence requirements.

**Lab 3:** `4ba5178` rejects `help stddev` during parsing; that's the intended red. After
supporting one topic, an old assertion that parsing `help x` must fail is obsolete. Replace
it with execution-time unknown-topic coverage and retain rejection of multiple topics.
Mocking `os.replace` tests failure rollback with real serialization but not a real full disk.
The CLI E2E tests run subprocesses; API TestClient uses the app in process. Neither proves
every browser interaction. See the glossary answer key for the eight retrieval questions.

**Lab 4:** Cycle A should identify a bad operand/option and preserve later successful
commands; old successful results are 5 and 9. Cycle B should reject ans before history,
then produce 5, 10, 11; old revision produces only 5. A failed calculation doesn't replace
ans. Deleting the latest record changes the latest retained result, and clearing removes
it. Students may choose different wording or designs if the acceptance criteria and stored
numeric operands remain correct. Require observation/inference separation.

**Lab 5:** JSON commands become `CalculateCommand`, not raw `eval`. A saved record returns
201; invalid calculation 400; invalid request schema 422; save failure 503. Locking covers
read/compute/save/publication within the server process, not all processes. A frontend
must build choices from registry metadata to discover plugins without HTML changes.
A simpler server-rendered page is a reasonable comparison but does not replace this lab's
requested JavaScript slice. Browser failures are limitations, not permissions to invent evidence.

**Lab 6:** Good decisions are scope-specific. “Ready for a personal finite-float calculator;
not suitable for concurrent independent writers or exact financial arithmetic” is defensible
when checks pass. There is no universal requirement to add undo before release, but its
absence must be acknowledged. Check that the student's independent explanation follows the
real order: persistence before assignment, not an imagined rollback after memory mutation.

## Troubleshooting and alternatives

| Symptom | Investigation / action |
| --- | --- |
| `calc` not found or wrong code runs | Check active venv, `python -c 'import calculator; print(calculator.__file__)'`, editable installation and working directory. |
| Historical SHA missing | Use the supplied labeled tar snapshot; never reset a student's current work. |
| Pip cannot reach network | Use preprepared compatible wheelhouse or arrange access; don't claim dependencies installed. |
| Plugin absent | Verify entry-point group, module/class name, active environment and restart. Importing alone is insufficient. |
| CSV startup failure | Preserve the suspect file; reproduce with a disposable copy. Do not “fix” by deleting real history. |
| Port 8010 busy | Select another port consistently in server/browser/curl commands; don't kill an unknown process. |
| AI cannot control browser | Student performs the same actions manually and records environment/results; mark unattempted browsers unverified. |
| Readline unavailable | Use plain input and document lack of editing/completion; don't fail mathematics criteria for an optional terminal facility. |
| Learner has no GitHub access | Keep local issue drafts/commits; use instructor-approved repository or upload route later. |

## Accessibility, assessment and pilot

Allow keyboard-only workflows, screen-reader-compatible Markdown, enlarged text and extended
time where appropriate. Use prose equivalents of diagrams and explain command output aloud.
Do not score typing speed, subscription level or screenshot aesthetics. Students can use
manual tools to supply equivalent evidence.

Use [assessment.md](assessment.md) and calibrate using its illustrative 84-point example.
Apply institutional integrity rules yourself; missing or fabricated evidence is not fixed
by asking an assistant to invent logs. Require a specific assistance log and provide a
remediation path for the independent explanation gate.

The author dry-run is in [validation-report.md](validation-report.md); **no real learner
pilot has been conducted**. For a later pilot, observe 2–3 learners following setup without
extra chat context, record time/blockers and vocabulary misconceptions, compare rubric
scores between two graders, then revise the affected instructions. Seek normal institutional
permission before collecting identifiable student data.
