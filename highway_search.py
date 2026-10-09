# Project: Highway Search Algorithms - Intro to Artificial Intelligence
# Project team: Motasem Amereh, Tamanna Devi, Manjot Singh,
#               Thomas Zangrilli, Parv Alphonso Bhatia
# File: highway_search.py
# Version: 1.0
# Updated: 2026-10-08
# Purpose: Find a route between two of 11 cities with BFS, DFS, UCS, and A*,
#          and show each route and its distance on a map.
# Data: g(n) = Google Maps driving distance, h(n) = Google Maps straight-line
#       distance, airplane time = h / 250 mph (all in city_data.py)
# Requires: Python 3.8+, matplotlib (pip install matplotlib)
# Run: python highway_search.py

import heapq
import random
import matplotlib.pyplot as plt

from city_data import CITIES, CITY_COORDS, GRAPH, AIRPLANE_SPEED_MPH, heuristic


def path_distance(path):
    total = 0
    for i in range(len(path) - 1):
        total += GRAPH[path[i]][path[i + 1]]
    return total


# ---------------------------------------------------------------
# Search algorithms
#
# All four keep whole paths in the frontier, so when the goal is
# reached its path is already built. They differ only in WHICH
# path is taken out next:
#   BFS -> oldest path (queue)      DFS -> newest path (stack)
#   UCS -> lowest g (driving miles) A*  -> lowest f = g + h
#
# Each returns (final_path, expanded_order).
# ---------------------------------------------------------------

def bfs(start, goal):
    queue = [[start]]
    visited = {start}
    expanded = []

    while queue:
        path = queue.pop(0)
        city = path[-1]
        expanded.append(city)
        if city == goal:
            return path, expanded

        for neighbor in GRAPH[city]:
            # Mark visited when added, so no city enters the queue twice.
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return [], expanded


def dfs(start, goal):
    stack = [[start]]
    visited = set()
    expanded = []

    while stack:
        path = stack.pop()
        city = path[-1]
        # A city can be pushed more than once; only expand it the first time.
        if city in visited:
            continue
        visited.add(city)
        expanded.append(city)
        if city == goal:
            return path, expanded

        # Pushed in reverse so the first listed neighbor is popped first.
        for neighbor in reversed(list(GRAPH[city])):
            if neighbor not in visited:
                stack.append(path + [neighbor])

    return [], expanded


def ucs(start, goal):
    # heapq always pops the smallest tuple, i.e. the path with the lowest g.
    frontier = [(0, [start])]
    visited = set()
    expanded = []

    while frontier:
        g, path = heapq.heappop(frontier)
        city = path[-1]
        # The first time a city is popped is its cheapest route; skip later copies.
        if city in visited:
            continue
        visited.add(city)
        expanded.append(city)
        if city == goal:
            return path, expanded

        for neighbor, miles in GRAPH[city].items():
            if neighbor not in visited:
                heapq.heappush(frontier, (g + miles, path + [neighbor]))

    return [], expanded


def astar(start, goal):
    # Same as UCS, but ordered by f = g + h. Since h (straight-line miles)
    # never overestimates the real driving distance, A* still finds the
    # shortest route while expanding fewer cities.
    frontier = [(heuristic(start, goal), 0, [start])]
    visited = set()
    expanded = []

    while frontier:
        f, g, path = heapq.heappop(frontier)
        city = path[-1]
        if city in visited:
            continue
        visited.add(city)
        expanded.append(city)
        if city == goal:
            return path, expanded

        for neighbor, miles in GRAPH[city].items():
            if neighbor not in visited:
                new_g = g + miles
                new_f = new_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (new_f, new_g, path + [neighbor]))

    return [], expanded


ALGORITHMS = {"BFS": bfs, "DFS": dfs, "UCS": ucs, "A*": astar}


# ---------------------------------------------------------------
# Output: printed summary and travel maps
# ---------------------------------------------------------------

def run_all(start, goal):
    h = heuristic(start, goal)
    print(f"\n{start} -> {goal}")
    print(f"Straight-line h = {h:.1f} miles | Airplane @ 250 mph = {h / AIRPLANE_SPEED_MPH:.2f} hours")

    results = {}
    for name, algorithm in ALGORITHMS.items():
        path, expanded = algorithm(start, goal)
        results[name] = (path, expanded)
        print(f"  {name:<4} {path_distance(path):>5} miles | {len(expanded):>2} expanded | {' -> '.join(path)}")
    return results


def draw_map(ax, path, expanded, title):
    # Longitude is used as x and latitude as y, so cities appear roughly
    # where they are on a real map.

    # Highways (gray) with driving distances.
    for city in GRAPH:
        for neighbor, miles in GRAPH[city].items():
            if city < neighbor:  # each road is stored both ways; draw it once
                lat1, lon1 = CITY_COORDS[city]
                lat2, lon2 = CITY_COORDS[neighbor]
                ax.plot([lon1, lon2], [lat1, lat2], color="lightgray", zorder=1)
                ax.text((lon1 + lon2) / 2, (lat1 + lat2) / 2, str(miles), fontsize=6, color="gray")

    # Final path (blue).
    for i in range(len(path) - 1):
        lat1, lon1 = CITY_COORDS[path[i]]
        lat2, lon2 = CITY_COORDS[path[i + 1]]
        ax.plot([lon1, lon2], [lat1, lat2], color="blue", linewidth=3, zorder=2)

    # Cities: orange = expanded (numbered in expansion order), red = never expanded.
    for city, (lat, lon) in CITY_COORDS.items():
        color = "orange" if city in expanded else "red"
        ax.scatter(lon, lat, color=color, s=60, zorder=3)
        ax.text(lon, lat - 0.6, city, fontsize=7, ha="center")
        if city in expanded:
            ax.text(lon - 0.5, lat + 0.3, str(expanded.index(city) + 1), fontsize=8, color="darkorange", weight="bold")

    ax.set_title(title, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])


def show_maps(start, goal, results):
    # One window, 2x2 grid: one map per algorithm for side-by-side comparison.
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle(f"{start} -> {goal}   (blue = path, orange # = expansion order)")

    for ax, (name, (path, expanded)) in zip(axes.flat, results.items()):
        title = f"{name}: {path_distance(path)} miles, {len(expanded)} cities expanded"
        draw_map(ax, path, expanded, title)

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------
# Menu
# ---------------------------------------------------------------

def choose_city(prompt):
    for i, city in enumerate(CITIES, 1):
        print(f"  {i:>2}. {city}")
    while True:
        choice = input(prompt)
        if choice.isdigit() and 1 <= int(choice) <= len(CITIES):
            return CITIES[int(choice) - 1]
        print("  Please enter a number from the list.")


def main():
    while True:
        print("\n=== Highway Search ===")
        print("1. Pick a start and target city")
        print("2. Run 5 random tests")
        print("3. Quit")
        option = input("Choose 1, 2, or 3: ")

        if option == "1":
            start = choose_city("Start city number: ")
            goal = choose_city("Target city number: ")
            if start == goal:
                print("Start and target must be different.")
                continue
            results = run_all(start, goal)
            show_maps(start, goal, results)

        elif option == "2":
            # Fixed seed so the same 5 tests appear in the report and the video.
            random.seed(42)
            for test in range(1, 6):
                start, goal = random.sample(CITIES, 2)
                print(f"\n--- Random test {test} ---")
                results = run_all(start, goal)
                show_maps(start, goal, results)  # close the window to see the next test

        elif option == "3":
            break


if __name__ == "__main__":
    main()