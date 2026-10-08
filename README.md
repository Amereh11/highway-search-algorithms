# Highway Search Algorithms

This project compares four graph-search algorithms on the same small U.S. highway network: Breadth-First Search (BFS), Depth-First Search (DFS), Uniform-Cost Search (UCS), and A*.

## Data and route costs

The data files contain 11 cities and 17 undirected road connections. Each road has a driving distance in miles. The original team-collected figures are retained in `data/google_maps_collected.csv`; the running program reads `data/roads.csv` and `data/cities.csv`.

- **BFS** uses a queue and finds a route with the fewest road connections.
- **DFS** uses a stack and follows one branch before backtracking.
- **UCS** chooses the path with the smallest driving-distance cost so far.
- **A*** chooses a path according to `f(n) = g(n) + h(n)`, where `g(n)` is actual driving miles so far and `h(n)` estimates straight-line miles to the goal.

For a directly measured pair, A* uses the straight-line value recorded in the CSV. Otherwise it uses the Haversine formula and the coordinates in `cities.csv`. The flight-time comparison divides straight-line miles by the assignment's assumed 250 mph; flight time is **not** included in highway path cost.

## Start the program

From the folder containing `main.py`, run:

```bash
python3 -m pip install -r requirements.txt
python3 main.py --start "Saint Paul" --goal "New York" --algorithm all
```

To produce four PNG maps inside `outputs/`:

```bash
python3 main.py --start "Saint Paul" --goal "New York" --algorithm all --save-maps
```

For five repeatable random routes:

```bash
python3 main.py --random 5 --seed 42
```

To run automated checks:

```bash
python3 -m unittest discover -s tests -v
```

Valid algorithm choices are `bfs`, `dfs`, `ucs`, `astar`, and `all`. City names must exactly match the dataset. The available names appear in an error message if an invalid city is entered.

## Understanding the code

Start with `main.py` for user input and printing; `src/graph.py` for the dataset and distance calculations; `src/search.py` for all four search methods; and `src/visualization.py` for map figures. `tests/test_search.py` checks the expected behavior, including comparing UCS and A* against independently computed shortest distances for all 121 ordered city pairs.

This is an educational graph on selected connections, not a turn-by-turn navigation system. Road lengths are snapshot values, edges are undirected, and plotted lines connect city coordinates rather than tracing actual roads.

## Main demonstration

Saint Paul to New York:

| Search | Driving miles | Expanded cities |
|---|---:|---:|
| BFS | 1287 | 11 |
| DFS | 2356 | 10 |
| UCS | 1287 | 10 |
| A* | 1287 | 6 |

DFS returns a longer route here than the other three searches. The difference follows from its exploration order: it is not designed to minimize road miles. See the full report for the random-pair comparison.

## Team

Motasem Amereh, Tamanna Devi, Manjot Singh, Thomas Zangrilli, and Parv Alphonso Bhatia.

Team members should review and be able to explain their submitted implementation, results, and individual contributions in accordance with course policy.
