# Experiment results (2D adjacency-matrix version 3.0)

Dataset: 11 cities, 17 undirected roads. All 15 automated tests passed locally.

## Main case: Saint Paul → New York

| Method | Driving miles | Expanded cities |
|---|---:|---:|
| BFS | 1287 | 11 |
| DFS | 2356 | 10 |
| UCS | 1287 | 10 |
| A* | 1287 | 6 |

The minimum route (BFS/UCS/A*): Saint Paul → Chicago → Columbus → Philadelphia → New York.

## Five seeded pairs (`python3 main.py --random 5 --seed 42`)

| Start | Goal | BFS | DFS | UCS | A* |
|---|---|---:|---:|---:|---:|
| Washington | Chicago | 723 | 1411 | 723 | 723 |
| Atlanta | Indianapolis | 536 | 964 | 536 | 536 |
| Columbus | Washington | 398 | 1736 | 398 | 398 |
| Columbia | Chicago | 933 | 933 | 933 | 933 |
| Washington | Saint Paul | 1121 | 1809 | 1121 | 1121 |

| Method | Average route miles | Average expanded |
|---|---:|---:|
| BFS | 742.2 | 7.4 |
| DFS | 1370.6 | 6.4 |
| UCS | 742.2 | 7.6 |
| A* | 742.2 | 3.8 |

Numbers are based on the revised v3 source, not the earlier DFS results. Routes are over the selected 17 roads, not a full real-world road map.
