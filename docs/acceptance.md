# Acceptance scenarios and verification

Use a temporary history path for every scenario. Assertions use numeric tolerances
where floating-point arithmetic requires them. Test names are traceable by UAT ID.

| ID | Given / When / Then | Layer |
| --- | --- | --- |
| UAT-01 | Given fresh history, when add 2 3 4, then result 9 and one record | Integration, E2E |
| UAT-02 | When subtract 20 5 3 and divide 100 2 5, then 12 and 10 | Unit, E2E |
| UAT-03 | When too few arguments, zero division, NaN, infinity, overflow or unknown options are supplied, then a clear error and no record | Unit, integration, E2E |
| UAT-04 | When mean/median 1 2 6 or stddev 2 4 6 ddof=1, then 3, 2, and 2 | Unit, E2E |
| UAT-05 | When stddev has n <= ddof or ddof outside 0/1, then validation fails | Unit, E2E |
| UAT-06 | Given an installed square plugin, when operations and square 4 run, then discover it and return 16 | Integration, manual installed-package smoke |
| UAT-07 | Given a broken/colliding/invalid plugin, when discovery runs, then warn and retain built-ins | Unit |
| UAT-08 | Given successful calculations, when restarted, then IDs, timestamps, args, kwargs and results survive | Integration, E2E |
| UAT-09 | Given malformed history, when starting, then exit 1 and preserve the file | Integration, E2E |
| UAT-10 | Given a repository write failure, when add/delete/clear runs, then memory and existing file remain unchanged | Integration |
| UAT-11 | Given saved history, when listing then deleting a unique ID prefix, then show a readable table and persist removal | Integration, E2E |
| UAT-12 | Given history, when deleting an unknown/ambiguous ID or clearing without --yes, then preserve history; explicit clear persists empty history | Unit, integration, E2E |
| UAT-13 | Given REPL input errors followed by valid input, when run, then recover; help, blank input, EOF and exit work | E2E |
| UAT-14 | Given one-shot commands, when valid/invalid, then exit 0/1; invalid process flags exit 2 | E2E |

## Manual release exercise

Create a disposable CSV; try help and operations; calculate multi-operand arithmetic
and both standard deviation modes; trigger bad syntax and zero division; inspect and
delete a record by prefix; restart; clear explicitly; install the example plugin and
verify discovery. Record observations and any specification amendments in review.md.
