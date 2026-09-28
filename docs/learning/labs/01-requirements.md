# Lab 1 — Turn intent into an engineering contract

## Outcomes and starting state

LO-01/02: distinguish requirements from solutions and connect user value to verifiable work.
Allow 90 minutes plus 45 minutes independent practice. Prerequisites: basic shell/Git,
[glossary](../glossary.md), and the [student setup](../README.md). Start in your isolated
reference copy at `b22b89f`; keep the course documents separately available. You are
writing your own proposal, not pretending the reference application is unimplemented.

Vocabulary in context: a **theme** gives direction, an **epic** groups capabilities, a
**story** names user value, and an **issue** scopes executable work. An acceptance
criterion states success; a test supplies evidence for it.

## Tasks

1. Inspect before editing:

   ```sh
   pwd
   git status --short --branch
   git remote -v
   git log -1 --oneline
   ```

   Confirm this is your learner copy. Record which remote, if any, receives your commits.
   An archive initialized with `git init` has no remote; that is expected, not an error.
2. Analyze this reconstructed brief: “Build a calculator with a CLI, four arithmetic
   operations, plugins, statistical calculations and CSV history. Later add a web UI.”
   Write `evidence/requirements.md` with at least six numbered functional requirements,
   three nonfunctional requirements, three out-of-scope items, and unresolved questions.
3. Resolve subtraction/division order, minimum operands, ddof, failed-save behavior,
   history deletion, plugin failure, and simultaneous writers explicitly. Compare your
   decisions with `docs/specification.md`; label differences, don't silently copy them.
4. Write two themes, two epics and four stories. For each story supply at least one
   positive and one negative Given/When/Then criterion. Example:

   > Given two saved records, when division by zero is attempted, then report an error
   > and retain exactly the same records in memory and CSV.

5. Create three small issues in your own GitHub repository. Each must name the user
   value, owned deliverable, dependencies, acceptance checks and verification method.
   If offline, write three Markdown issue drafts in `evidence/issues/`; publish later.
   Do not create student practice issues in the instructor's repository.
6. Make a focused requirements commit, referring to your actual issue number when one
   exists. Use `Refs`, not `Closes`, while acceptance work remains. Record the commit SHA.

## AI prompt

```text
Inspect my working directory, status, remote and existing calculator docs before
changing anything. Preserve existing work. Help turn the brief in this lab into
numbered requirements, explicit boundaries and three independently reviewable issues.
Ask about contradictions that affect behavior; label assumptions. For each story,
propose positive/negative verification and explain what observable result would pass.
Do not implement the calculator yet. Show the draft and report what you inspected.
```

This separates problem definition from code generation and asks for falsifiable claims.

### Critique prompt

```text
Review the draft as a skeptical maintainer. Find ambiguous words, requirements that
are really implementation choices, missing failure behavior and oversized issues.
Trace one story to its acceptance checks. Revise only the affected text and distinguish
checks actually performed from checks merely proposed.
```

## Completion checks

A peer must be able to decide whether each criterion passes without consulting your
chat. Verify the issue dependency order is feasible and the commit contains only related
planning changes. Submit requirements, story/issue mapping, assumptions and commit link.

## Reflection

What did the assistant assume that you changed? Which requirement prevented a likely
failure? Why isn't “make the ultimate calculator” an executable acceptance criterion?
