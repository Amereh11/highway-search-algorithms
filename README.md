# Highway Search Algorithms

**Course:** CS (NW) 36210 002 — Introduction to Artificial Intelligence (Fall 2026)  
**University:** Purdue University Northwest  
**Report date:** October 8, 2026  
**Team:** Motasem Amereh, Tamanna Devi, Manjot Singh, Thomas Zangrilli, Parv Alphonso Bhatia

This project compares **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, **Uniform-Cost Search (UCS)**, and **A\*** on a highway network with 11 cities and 17 bidirectional roads.

The road weights are driving miles, `g(n)`; A* also uses the team's straight-line distance estimates, `h(n)`. The program prints travel results and draws a four-panel visualization of the routes and city expansion orders. A direct-flight time at 250 mph is displayed separately; it does not affect route selection.

## Files

| File | Purpose |
|---|---|
| `highway_search.py` | Interactive menu, four algorithms, results, and Matplotlib maps |
| `city_data.py` | City names, coordinates, 17 roads, and 55 straight-line distance pairs |
| `tests/test_highway_search.py` | Checks against the report, route correctness, and graph data |
| `docs/Highway_Search_Project_Report.pdf` | Full illustrated project report |
| `assets/usa-city-map.png` | Reference map included in the supplied project archive |
| `docs/RESULTS.md` | Quick reference for the reproducible results |

## Run

Install Python 3.8+ and Matplotlib. From this folder:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 highway_search.py
```

In the menu, choose **1** to select the start and target city, **2** to run five reproducible random pairs, or **3** to exit. For the main report demonstration, enter **1**, choose **2 (Chicago)**, and then choose **10 (Atlanta)**. Close the figure window after each route to return to the menu; in random mode close each figure to see the next.

## Report example: Chicago → Atlanta

| Search | Driving miles | Expanded cities |
|---|---:|---:|
| BFS | 823 | 10 |
| DFS | 3,046 | 10 |
| UCS | 719 | 7 |
| A* | 719 | 5 |

UCS and A* find the shortest road route, **Chicago → Indianapolis → Nashville → Atlanta (719 miles)**. BFS chooses a different three-road route, and DFS follows a much longer route in this neighbor order.

## Notes

- **Distance data:** Values are the team's recorded project measurements, not live Google Maps queries; actual road distances can change.
- **Algorithm comparison:** BFS minimizes the number of highway connections, not total driving miles. DFS does not promise a shortest path. UCS and A* minimize total miles on this network.
- **Source version:** The Python source here matches the version-1.0 implementation described in the supplied project report. That implementation uses Python `set` objects for visited cities. If a **2D adjacency array with no sets** is a current requirement, revise the code **and the report appendix/explanation together** before submitting. An earlier matrix-based version is recoverable in the repository's Git history.
- **Academic work:** Team members should review and understand the code and follow their course's authorship and assistance-disclosure rules.
