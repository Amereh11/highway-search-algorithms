# Highway Search Algorithms — Version 3.0

**Course:** Introduction to Artificial Intelligence, Project 1  
**Project team:** Motasem Amereh, Tamanna Devi, Manjot Singh, Thomas Zangrilli, Parv Alphonso Bhatia  
**Updated:** October 8, 2026

This version uses an **11 × 11 two-dimensional adjacency matrix** to represent 11 cities and 17 undirected roads. There is no set collection in the project code. BFS/DFS track visits with Boolean lists, and UCS/A* track their best known costs with lists.

## Files

- `main.py`: command-line inputs, results, optional plots
- `src/graph.py`: two-dimensional distance matrix and straight-line estimates
- `src/search.py`: BFS, DFS, UCS and A*
- `src/visualization.py`: road graph and highlighted routes
- `tests/test_search.py`: 15 tests, including all 121 ordered city pairs
- `data/*.csv`: original road and city dataset
- `docs/FINAL_RESULTS.md`: updated measured results
- `docs/CODE_WALKTHROUGH.md`: explanation and professor-practice questions

## Run

From the project folder:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 main.py --start "Saint Paul" --goal "New York" --algorithm all
python3 main.py --start "Saint Paul" --goal "New York" --algorithm all --save-maps
python3 main.py --random 5 --seed 42
```

## Main demonstration

| Algorithm | Route miles | Cities expanded |
|---|---:|---:|
| BFS | 1287 | 11 |
| DFS | 2356 | 10 |
| UCS | 1287 | 10 |
| A* | 1287 | 6 |

BFS, UCS and A* return Saint Paul → Chicago → Columbus → Philadelphia → New York. DFS follows a longer route. A* uses `f(n)=g(n)+h(n)`, where both terms are in miles. Estimated direct-flight hours are shown separately as `h(n)/250`.

**Academic-use note:** This is a review draft for understanding and team revision. Follow the professor's independently-authored-work and assistance-disclosure requirements. Project-team file headers do not establish individual code authorship. The illustrated PDF/Word report is included in the downloadable submission ZIP, rather than this source-only branch.

