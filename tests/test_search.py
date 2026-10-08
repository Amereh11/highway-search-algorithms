# Project: Highway Search Algorithms - Intro to Artificial Intelligence
# Project team: Motasem Amereh, Tamanna Devi, Manjot Singh,
#               Thomas Zangrilli, Parv Alphonso Bhatia
# Version: 3.0 (matrix-based review draft)
# Updated: 2026-10-08
# Purpose: Check the 2D graph, algorithms, and saved result figures.

import heapq
import tempfile
import unittest
from math import inf
from pathlib import Path

from src.graph import HighwayGraph
from src.search import bfs, dfs, ucs, astar
from src.visualization import plot_route

ROOT = Path(__file__).resolve().parents[1]


class HighwayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = HighwayGraph.from_csv(ROOT / "data/cities.csv", ROOT / "data/roads.csv")

    def test_city_count(self):
        self.assertEqual(len(self.graph.names), 11)

    def test_two_dimensional_array(self):
        # The road matrix contains 11 rows, each with 11 columns.
        self.assertEqual(len(self.graph.roads), 11)
        for row in self.graph.roads:
            self.assertEqual(len(row), 11)

    def test_undirected_roads(self):
        # Every road weight must be the same in both directions.
        edges = 0
        for i in range(11):
            for j in range(11):
                self.assertEqual(self.graph.roads[i][j], self.graph.roads[j][i])
                if j > i and self.graph.roads[i][j] > 0:
                    edges += 1
        self.assertEqual(edges, 17)

    def test_all_searches_reach_the_goal(self):
        for algorithm in (bfs, dfs, ucs, astar):
            answer = algorithm(self.graph, "Saint Paul", "New York")
            self.assertEqual(answer.path[0], "Saint Paul")
            self.assertEqual(answer.path[-1], "New York")
            self.assertEqual(answer.distance, self.graph.path_distance(answer.path))

    def test_costs_for_main_route(self):
        for algorithm in (bfs, ucs, astar):
            self.assertEqual(algorithm(self.graph, "Saint Paul", "New York").distance, 1287)

    def test_start_equals_goal(self):
        for algorithm in (bfs, dfs, ucs, astar):
            answer = algorithm(self.graph, "Atlanta", "Atlanta")
            self.assertEqual(answer.path, ["Atlanta"])
            self.assertEqual(answer.distance, 0)

    def test_all_pairs_shortest_cost(self):
        # Independent Dijkstra calculation validates UCS and A* for 121 pairs.
        for start in range(11):
            distances = [inf] * 11
            distances[start] = 0
            frontier = [(0, start)]
            while frontier:
                cost, city = heapq.heappop(frontier)
                if cost != distances[city]:
                    continue
                for neighbor, miles in self.graph.neighbors(city):
                    if cost + miles < distances[neighbor]:
                        distances[neighbor] = cost + miles
                        heapq.heappush(frontier, (cost + miles, neighbor))
            for goal in range(11):
                for algorithm in (ucs, astar):
                    answer = algorithm(self.graph, self.graph.names[start],
                                       self.graph.names[goal])
                    self.assertAlmostEqual(answer.distance, distances[goal])

    def test_bfs_uses_fewest_connections(self):
        # No returned BFS route can have more connections than the shortest
        # number of connections in this simple unweighted reference search.
        for start in range(11):
            hops = [-1] * 11
            hops[start] = 0
            pending = [start]
            for city in pending:
                for neighbor, miles in self.graph.neighbors(city):
                    if hops[neighbor] == -1:
                        hops[neighbor] = hops[city] + 1
                        pending.append(neighbor)
            for goal in range(11):
                path = bfs(self.graph, self.graph.names[start],
                           self.graph.names[goal]).path
                self.assertEqual(len(path) - 1, hops[goal])

    def test_collected_plane_distance(self):
        self.assertAlmostEqual(self.graph.heuristic_miles("Saint Paul", "Chicago"), 346.44)

    def test_flight_time(self):
        self.assertAlmostEqual(self.graph.flight_hours("Saint Paul", "Chicago"), 346.44 / 250)

    def test_heuristic_zero_at_goal(self):
        self.assertEqual(self.graph.heuristic_miles("Chicago", "Chicago"), 0)

    def test_duplicate_road_fails(self):
        with self.assertRaises(ValueError):
            self.graph.add_road("Saint Paul", "Chicago", 398)

    def test_invalid_city_fails(self):
        with self.assertRaises(ValueError):
            bfs(self.graph, "Atlantis", "Chicago")

    def test_path_missing_edge_fails(self):
        with self.assertRaises(ValueError):
            self.graph.path_distance(["Saint Paul", "New York"])

    def test_map_saves_png(self):
        route = astar(self.graph, "Saint Paul", "New York")
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "route.png"
            plot_route(self.graph, route.path, route.expanded, "Test", output)
            self.assertTrue(output.exists())
            self.assertGreater(output.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
