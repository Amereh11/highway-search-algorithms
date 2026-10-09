# Results reproduced from the submitted source

Distances are in driving miles; expanded is the number of cities removed from the frontier and expanded. The program uses `random.seed(42)` for the five random test cases.

## Chicago → Atlanta (chosen route)

| Algorithm | Miles | Expanded | Route |
|---|---:|---:|---|
| BFS | 823 | 10 | Chicago → Springfield → Nashville → Atlanta |
| DFS | 3,046 | 10 | Chicago → Saint Paul → Springfield → Nashville → Indianapolis → Columbus → Philadelphia → Washington DC → Columbia → Atlanta |
| UCS | 719 | 7 | Chicago → Indianapolis → Nashville → Atlanta |
| A* | 719 | 5 | Chicago → Indianapolis → Nashville → Atlanta |

Straight-line distance: 588.091 miles. Airplane estimate at 250 mph: 2.35 hours.

## Five reproducible random tests

| # | Cities | BFS | DFS | UCS | A* |
|---|---|---:|---:|---:|---:|
| 1 | Nashville → Chicago | 575 (7) | 1,287 (4) | 471 (7) | 471 (3) |
| 2 | Saint Paul → Columbus | 723 (5) | 1,435 (6) | 723 (5) | 723 (3) |
| 3 | Indianapolis → Nashville | 288 (4) | 2,994 (9) | 288 (5) | 288 (2) |
| 4 | Springfield → Chicago | 201 (3) | 913 (3) | 201 (2) | 201 (2) |
| 5 | Nashville → Columbia | 462 (4) | 2,727 (9) | 462 (5) | 462 (3) |

Numbers in parentheses are expanded city counts. The detailed maps, discussion, full data tables, and source appendix are in the illustrated PDF report in this project bundle.
