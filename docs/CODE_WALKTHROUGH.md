# Code walkthrough and professor preparation

## How the data structure works

`graph.roads[i][j]` gives the driving miles from city index i to j; zero means no road. There are 11 rows with 11 columns. Each undirected road appears in both directions. Coordinates are stored in another list, while `graph.estimate` reads collected straight-line miles or computes Haversine miles for an unmeasured city pair.

## How four algorithms work

- **BFS:** First-in-first-out `deque`, a `visited` Boolean list, and a `parent` list. Finds fewest road connections, not necessarily fewest miles.
- **DFS:** Last-in-first-out stack of `(city,parent)` pairs, a `visited` Boolean list, and a `parent` list. Returns the first route it discovers in neighbor order.
- **UCS:** `heapq` orders cities by cumulative road cost `g`. A list `best` records cheapest cost so far.
- **A*:** `heapq` orders cities by `f=g+h`. Straight-line miles `h` estimate the remaining road distance. The 250 mph assumption is only for the separate flight-time display.

`make_result` follows parent indices from destination to start and reverses them. `run_route` prints the found route and optionally generates a PNG.

## Likely questions

1. **Why a 2D array?** Direct edge lookup and simple indexing on 11 cities; space cost is O(V²).
2. **Where are sets used?** Nowhere in the project code; boolean lists do the visit tracking.
3. **Why are distances symmetric?** Every measured road is inserted in both directions.
4. **What is in `visited[i]`?** `True` if city index i was discovered or visited.
5. **What does `parent[i]` mean?** The predecessor city index for reconstructing a route; -1 means root.
6. **How is BFS different from DFS?** FIFO queue versus LIFO stack.
7. **Why does DFS return 2356 miles?** Neighbor ordering drives it down a longer branch; it doesn't optimize miles.
8. **What makes UCS optimal?** It expands the lowest accumulated road cost when all edge weights are nonnegative.
9. **What makes A* efficient here?** The straight-line estimate prioritizes promising destinations.
10. **Why keep `h` in miles?** `g+h` requires compatible units; flight time is reported separately.
11. **How did you test?** 15 unit tests, including a Dijkstra cost comparison over all 121 ordered city pairs.
12. **How do you show maps?** Run the CLI with `--save-maps` and open `outputs/`.

Before presenting, trace two loops in `search.py`, explain a row of the road matrix, predict a result for a changed goal, and run the tests yourself.

**Review note:** Team attribution should be confirmed. This is a proposed learning/reference implementation, not proof of independently-authored coursework.
