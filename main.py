from __future__ import annotations

import argparse
import random
from pathlib import Path

from src.graph import HighwayGraph
from src.search import bfs, dfs, ucs, astar
from src.visualization import plot_route


ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs,
    "ucs": ucs,
    "astar": astar,
}


def print_result(graph: HighwayGraph, algorithm_name: str, result, start: str, goal: str) -> None:
    print(f"\n{algorithm_name.upper()}")
    print("-" * 60)

    if result.path is None:
        print("No route found.")
        return

    print("Path:", " -> ".join(result.path))
    print(f"Driving distance: {result.distance:.1f} miles")
    print(f"Nodes expanded: {len(result.expanded)}")
    print("Expansion order:", " -> ".join(result.expanded))

    straight_line = graph.heuristic_miles(start, goal)
    flight_hours = graph.estimated_flight_time_hours(start, goal)
    print(f"Straight-line heuristic from start: {straight_line:.1f} miles")
    print(f"Estimated direct-flight time at 250 mph: {flight_hours:.2f} hours")


def run_one(
    graph: HighwayGraph,
    start: str,
    goal: str,
    algorithm: str,
    save_maps: bool,
    output_dir: Path,
) -> None:
    names = list(ALGORITHMS) if algorithm == "all" else [algorithm]

    print(f"\nRoute request: {start} -> {goal}")

    for name in names:
        if name == "astar":
            result = ALGORITHMS[name](graph, start, goal)
        else:
            result = ALGORITHMS[name](graph, start, goal)

        print_result(graph, name, result, start, goal)

        if save_maps and result.path:
            output_dir.mkdir(parents=True, exist_ok=True)
            safe_start = start.replace(", ", "_").replace(" ", "_")
            safe_goal = goal.replace(", ", "_").replace(" ", "_")
            file_path = output_dir / f"{name}_{safe_start}_to_{safe_goal}.png"
            plot_route(
                graph=graph,
                path=result.path,
                expanded=result.expanded,
                title=f"{name.upper()}: {start} to {goal}",
                save_path=file_path,
            )
            print(f"Saved map: {file_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare BFS, DFS, UCS, and A* on a U.S. highway graph."
    )
    parser.add_argument("--start", help='Start city, e.g. "Chicago, IL"')
    parser.add_argument("--goal", help='Target city, e.g. "New York, NY"')
    parser.add_argument(
        "--algorithm",
        choices=["bfs", "dfs", "ucs", "astar", "all"],
        default="all",
        help="Algorithm to run (default: all).",
    )
    parser.add_argument(
        "--random",
        type=int,
        metavar="N",
        help="Run N randomly selected start/target city pairs.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--save-maps",
        action="store_true",
        help="Save a PNG route visualization for each algorithm.",
    )

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    graph = HighwayGraph.from_csv(
        project_root / "data" / "cities.csv",
        project_root / "data" / "roads.csv",
    )

    if args.random:
        if args.random < 1:
            parser.error("--random must be at least 1")

        rng = random.Random(args.seed)
        cities = graph.city_names()

        print(f"Running {args.random} random city pairs with seed {args.seed}.")
        for i in range(args.random):
            start, goal = rng.sample(cities, 2)
            print(f"\n{'=' * 70}\nRandom pair {i + 1}/{args.random}")
            run_one(
                graph,
                start,
                goal,
                args.algorithm,
                args.save_maps,
                project_root / "outputs",
            )
        return

    if not args.start or not args.goal:
        parser.error("Provide both --start and --goal, or use --random N.")

    graph.validate_city(args.start)
    graph.validate_city(args.goal)

    run_one(
        graph,
        args.start,
        args.goal,
        args.algorithm,
        args.save_maps,
        project_root / "outputs",
    )


if __name__ == "__main__":
    main()
