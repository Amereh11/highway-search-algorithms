# Highway Search Algorithms

A graph-search project that compares **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, **Uniform-Cost Search (UCS)**, and **A\*** on a U.S. highway-routing graph.

## Project Motivation

This project demonstrates how classic search algorithms behave on a practical route-finding problem.

The project models cities as graph nodes and road connections as weighted edges:

- **g(n):** accumulated driving distance in miles.
- **h(n):** straight-line (great-circle) distance from the current city to the destination.
- **Estimated airplane time:** `h(n) / 250 mph`, included because the assignment assumes an airplane speed of 250 miles per hour.

> **Important:** A\* uses straight-line **miles** as the heuristic because `g(n)` is also measured in miles. Keeping both values in the same unit makes the A\* cost calculation `f(n) = g(n) + h(n)` mathematically consistent.

## Algorithms

| Algorithm | Uses edge weights? | Uses heuristic? | Main idea |
|---|---:|---:|---|
| BFS | No | No | Explores level by level |
| DFS | No | No | Goes deep before backtracking |
| UCS | Yes | No | Expands the lowest accumulated-cost path |
| A* | Yes | Yes | Expands the lowest `g(n) + h(n)` path |

## Cities

The included starter graph contains 12 cities in 12 states:

1. Chicago, Illinois
2. Indianapolis, Indiana
3. Columbus, Ohio
4. Detroit, Michigan
5. Milwaukee, Wisconsin
6. St. Louis, Missouri
7. Louisville, Kentucky
8. Nashville, Tennessee
9. Atlanta, Georgia
10. Charlotte, North Carolina
11. Pittsburgh, Pennsylvania
12. New York, New York

## Data

`data/cities.csv` contains city coordinates.

`data/roads.csv` contains starter driving-distance values so the program works immediately.

`data/google_maps_collection_template.csv` is the file your team should fill in with the exact Google Maps values required by the assignment.

### Before final submission

The driving-distance values in this repository are **starter/demo values** and should be checked against Google Maps by your team before submitting the course project. Replace the corresponding values in `data/roads.csv` with the verified Google Maps distances.

The heuristic is calculated automatically from latitude/longitude using the Haversine formula.

## Project Structure

```text
highway-search-algorithms/
├── README.md
├── main.py
├── requirements.txt
├── .gitignore
├── data/
│   ├── cities.csv
│   ├── roads.csv
│   └── google_maps_collection_template.csv
├── src/
│   ├── __init__.py
│   ├── graph.py
│   ├── search.py
│   └── visualization.py
├── tests/
│   └── test_search.py
├── docs/
│   ├── REPORT_OUTLINE.md
│   └── PRESENTATION_OUTLINE.md
└── outputs/
    └── .gitkeep
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/highway-search-algorithms.git
cd highway-search-algorithms
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run One Route

```bash
python main.py --start "Chicago, IL" --goal "New York, NY" --algorithm all
```

To save route maps:

```bash
python main.py --start "Chicago, IL" --goal "New York, NY" --algorithm all --save-maps
```

## Run Five Random Start/Target Pairs

```bash
python main.py --random 5 --seed 42
```

With route maps:

```bash
python main.py --random 5 --seed 42 --save-maps
```

## Example Output

```text
BFS
Path: Chicago, IL -> Detroit, MI -> Pittsburgh, PA -> New York, NY
Driving distance: ...
Nodes expanded: ...

UCS
Path: ...
Driving distance: ...
Nodes expanded: ...

A*
Path: ...
Driving distance: ...
Nodes expanded: ...
Straight-line heuristic from start: ... miles
Estimated direct-flight time at 250 mph: ... hours
```

Exact output depends on the road-distance values stored in `data/roads.csv`.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Assignment Coverage

This repository supports the project requirements by providing:

- 10–15 cities
- Multiple U.S. states
- Driving-distance edge costs
- Straight-line heuristic estimates
- BFS
- DFS
- UCS
- A*
- User-selected start and target cities
- Five random start/target test cases
- Route visualization
- Distance reporting
- Report outline
- Presentation outline

## Team Workflow

A simple team workflow is:

1. One member verifies city coordinates.
2. One or more members collect Google Maps driving distances.
3. One member reviews/testing the algorithms.
4. One member prepares visuals/results.
5. The team combines findings into the report and presentation.
6. Every contributor participates in the recorded presentation.

## Academic Note

Use the code as your project foundation, but make sure every team member understands how BFS, DFS, UCS, A\*, `g(n)`, and `h(n)` work because the professor may ask contributors to demonstrate their skills individually.
