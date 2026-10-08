# Rechecked search results

The graph contains 11 cities and 17 undirected roads. Commands:
```bash
python3 -m unittest discover -s tests -v
python3 main.py --start "Saint Paul" --goal "New York" --algorithm all --save-maps
python3 main.py --random 5 --seed 42
```

## Main route (Saint Paul -> New York)

| Search | Miles | Cities expanded |
|---|---:|---:|
| BFS | 1287 | 11 |
| DFS | 2356 | 10 |
| UCS | 1287 | 10 |
| A* | 1287 | 6 |

BFS, UCS and A* return Saint Paul -> Chicago -> Columbus -> Philadelphia -> New York. DFS follows a longer branch through Indianapolis, Nashville, Atlanta, Columbia and Washington.

## Five reproducible pairs (seed 42)

| Start | Goal | BFS miles | DFS miles | UCS miles | A* miles |
|---|---|---:|---:|---:|---:|
| Washington | Chicago | 723 | 1411 | 723 | 723 |
| Atlanta | Indianapolis | 536 | 964 | 536 | 536 |
| Columbus | Washington | 398 | 1736 | 398 | 398 |
| Columbia | Chicago | 933 | 933 | 933 | 933 |
| Washington | Saint Paul | 1121 | 1809 | 1121 | 1121 |

| Search | Average miles | Average expanded |
|---|---:|---:|
| BFS | 742.2 | 7.4 |
| DFS | 1370.6 | 6.4 |
| UCS | 742.2 | 7.6 |
| A* | 742.2 | 3.8 |

These numbers were reproduced locally on the revised code. They replace the results in the earlier report for the previous DFS implementation.
