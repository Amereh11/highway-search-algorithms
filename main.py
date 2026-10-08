# Project: Highway Search Algorithms - Intro to Artificial Intelligence
# Project team: Motasem Amereh, Tamanna Devi, Manjot Singh,
#               Thomas Zangrilli, Parv Alphonso Bhatia
# Version: 3.0 (matrix-based review draft)
# Updated: 2026-10-08
# Purpose: Accept a route request and display BFS, DFS, UCS, and A* results.

import argparse
import random
from pathlib import Path

from src.graph import HighwayGraph
from src.search import astar, bfs, dfs, ucs
from src.visualization import plot_route

BASE = Path(__file__).resolve().parent
ALGORITHMS = {"bfs": bfs, "dfs": dfs, "ucs": ucs, "astar": astar}


def run_route(graph, start, goal, algorithm, save_maps):
    """Run the requested methods on the same highway data."""
    choices = ALGORITHMS if algorithm == "all" else {algorithm: ALGORITHMS[algorithm]}
    print(f"\nRoute: {start} -> {goal}")

    for name, method in choices.items():
        result = method(graph, start, goal)
        print(f"\n{name.upper()}")
        if result.path is None:
            print("No route found")
            continue
        print("Path:", " -> ".join(result.path))
        print(f"Driving distance: {result.distance:.0f} miles")
        print(f"Nodes expanded: {len(result.expanded)}")
        print("Expansion order:", " -> ".join(result.expanded))
        print(f"Straight line: {graph.heuristic_miles(start, goal):.1f} miles")
        print(f"Estimated direct flight at 250 mph: {graph.flight_hours(start, goal):.2f} hours")

        # Route images are optional, because a console run works without maps.
        if save_maps:
            folder = BASE / "outputs"
            folder.mkdir(exist_ok=True)
            start_part = start.replace(" ", "_")
            goal_part = goal.replace(" ", "_")
            file = folder / f"{name}_{start_part}_to_{goal_part}.png"
            plot_route(graph, result.path, result.expanded,
                       f"{name.upper()}: {start} to {goal} ({result.distance:.0f} mi)", file)
            print(f"Map saved: {file}")


def main():
    parser = argparse.ArgumentParser(description="Compare four highway search algorithms")
    parser.add_argument("--start", help="Starting city, such as 'Saint Paul'")
    parser.add_argument("--goal", help="Destination city, such as 'New York'")
    parser.add_argument("--algorithm", choices=["bfs", "dfs", "ucs", "astar", "all"],
                        default="all")
    parser.add_argument("--random", type=int, metavar="N", help="Run N random city pairs")
    parser.add_argument("--seed", type=int, default=42, help="Repeatable random selection")
    parser.add_argument("--save-maps", action="store_true", help="Save PNG route plots")
    args = parser.parse_args()

    graph = HighwayGraph.from_csv(BASE / "data/cities.csv", BASE / "data/roads.csv")

    if args.random is not None:
        if args.random < 1:
            parser.error("--random must be greater than zero")
        generator = random.Random(args.seed)
        for number in range(args.random):
            start, goal = generator.sample(graph.city_names(), 2)
            print(f"\nRandom pair {number + 1} of {args.random}")
            run_route(graph, start, goal, args.algorithm, args.save_maps)
    else:
        if not args.start or not args.goal:
            parser.error("Use both --start and --goal, or specify --random N")
        graph.city_index(args.start)
        graph.city_index(args.goal)
        run_route(graph, args.start, args.goal, args.algorithm, args.save_maps)


if __name__ == "__main__":
    main()
