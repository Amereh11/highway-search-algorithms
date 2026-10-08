"""Run BFS, DFS, UCS, and A* on the highway dataset."""

import argparse
import random
from pathlib import Path

from src.graph import HighwayGraph
from src.search import astar, bfs, dfs, ucs
from src.visualization import plot_route

ROOT = Path(__file__).resolve().parent
SEARCHES = {"bfs": bfs, "dfs": dfs, "ucs": ucs, "astar": astar}


def run_route(graph, start, goal, selection, save_maps):
    print(f"\nRoute: {start} -> {goal}")
    names = list(SEARCHES) if selection == "all" else [selection]

    for name in names:
        result = SEARCHES[name](graph, start, goal)
        print(f"\n{name.upper()}")
        if result.path is None:
            print("No route found")
            continue
        print("Path:", " -> ".join(result.path))
        print(f"Driving distance: {result.distance:.0f} miles")
        print(f"Expanded: {len(result.expanded)} cities")
        print("Expansion order:", " -> ".join(result.expanded))
        print(f"Straight-line estimate: {graph.heuristic_miles(start, goal):.2f} miles")
        print(f"Flight estimate (250 mph): {graph.estimated_flight_time_hours(start, goal):.2f} hours")

        if save_maps:
            folder = ROOT / "outputs"
            folder.mkdir(exist_ok=True)
            filename = f"{name}_{start.replace(' ', '_')}_to_{goal.replace(' ', '_')}.png"
            plot_route(graph, result.path, result.expanded,
                       f"{name.upper()}: {start} to {goal} ({result.distance:.0f} miles)",
                       folder / filename)
            print("Saved:", folder / filename)


def main():
    parser = argparse.ArgumentParser(description="Highway graph search comparison")
    parser.add_argument("--start", help="Starting city")
    parser.add_argument("--goal", help="Destination city")
    parser.add_argument("--algorithm", choices=[*SEARCHES, "all"], default="all")
    parser.add_argument("--random", type=int, metavar="N", help="Run N random city pairs")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--save-maps", action="store_true")
    args = parser.parse_args()

    graph = HighwayGraph.from_csv(ROOT / "data/cities.csv", ROOT / "data/roads.csv")
    if args.random is not None:
        if args.random < 1:
            parser.error("--random must be 1 or greater")
        rng = random.Random(args.seed)
        for number in range(args.random):
            start, goal = rng.sample(graph.city_names(), 2)
            print(f"\nRandom pair {number + 1} of {args.random}")
            run_route(graph, start, goal, args.algorithm, args.save_maps)
    else:
        if not args.start or not args.goal:
            parser.error("Provide --start and --goal, or --random N")
        try:
            graph.validate_city(args.start)
            graph.validate_city(args.goal)
        except ValueError as error:
            parser.error(str(error))
        run_route(graph, args.start, args.goal, args.algorithm, args.save_maps)


if __name__ == "__main__":
    main()
