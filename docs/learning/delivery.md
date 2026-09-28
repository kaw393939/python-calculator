# Teaching-package delivery plan

The [specification](specification.md) is the source of truth. These issues author the
teaching materials; they do not imply those materials are already complete.

Planning and review: [#10](https://github.com/kaw393939/python-calculator/issues/10).

| Deliverable | Atomic issue | Dependencies |
| --- | --- | --- |
| `glossary.md` | [#11: Write the engineering vocabulary glossary](https://github.com/kaw393939/python-calculator/issues/11) | Specification |
| `case-study.md` | [#12: Write an evidence-backed annotated project case study](https://github.com/kaw393939/python-calculator/issues/12) | Specification |
| `labs/01-requirements.md` | [#13: Author Lab 1: requirements and issue-driven delivery](https://github.com/kaw393939/python-calculator/issues/13) | #11, #12 |
| `labs/02-cli-design.md` | [#14: Author Lab 2: CLI architecture, patterns and plugins](https://github.com/kaw393939/python-calculator/issues/14) | #13 |
| `labs/03-testing.md` | [#15: Author Lab 3: layered testing and evidence](https://github.com/kaw393939/python-calculator/issues/15) | #14 |
| `labs/04-dogfooding.md` | [#16: Author Lab 4: two dogfooding improvement cycles](https://github.com/kaw393939/python-calculator/issues/16) | #15, #12 |
| `labs/05-web-adapter.md` | [#17: Author Lab 5: FastAPI and JavaScript over the shared core](https://github.com/kaw393939/python-calculator/issues/17) | #15 |
| `labs/06-engineering-review.md` | [#18: Author Lab 6: evidence-based engineering review](https://github.com/kaw393939/python-calculator/issues/18) | #16, #17 |
| `assessment.md` | [#19: Create the assessment rubric and proficiency checks](https://github.com/kaw393939/python-calculator/issues/19) | #18 |
| `instructor-guide.md` | [#20: Write the six-session instructor facilitation guide](https://github.com/kaw393939/python-calculator/issues/20) | #19, #11, #12 |
| `README.md` | [#21: Publish the student guide and package navigation](https://github.com/kaw393939/python-calculator/issues/21) | #20 |
| `validation-report.md` | [#22: Audit and dry-run the complete teaching package](https://github.com/kaw393939/python-calculator/issues/22) | #21 |

## Recommended execution order

1. Glossary and case study establish vocabulary and evidence.
2. Requirements → CLI design → testing establish the working engineering sequence.
3. Dogfooding and web-adapter labs follow testing; neither requires the other to be authored first.
4. Engineering review → assessment → instructor guide → student guide finish the learning experience.
5. Final audit exercises the complete package and closes remaining documentation findings.

Each issue owns one primary file. Keep commits focused and reference the actual issue number.
Review acceptance criteria before closure. If a task exposes a new software defect or needs a
runnable fixture, create a separate scoped issue rather than quietly broadening the document task.

All teaching delivery issues remain open until their artifacts and verification are complete.
