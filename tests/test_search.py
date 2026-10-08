"""Checks for the data, the search strategies, and their route costs."""

import heapq
import unittest
from math import inf
from pathlib import Path

from src.graph import HighwayGraph
from src.search import astar, bfs, dfs, ucs

ROOT = Path(__file__).resolve().parents[1]


class SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = HighwayGraph.from_csv(ROOT / "data/cities.csv", ROOT / "data/roads.csv")

    def test_dataset_size(self):
        self.assertEqual(len(self.graph.city_names()), 11)
        self.assertEqual(sum(len(v) for v in self.graph.roads.values()) // 2, 17)

    def test_edges_are_two_way(self):
        for city in self.graph.city_names():
            for neighbor, miles in self.graph.neighbors(city):
                self.assertIn((city, miles), self.graph.neighbors(neighbor))

    def test_four_searches_return_valid_paths(self):
        for method in (bfs, dfs, ucs, astar):
            result = method(self.graph, "Saint Paul", "New York")
            self.assertEqual(result.path[0], "Saint Paul")
            self.assertEqual(result.path[-1], "New York")
            self.assertEqual(self.graph.path_distance(result.path), result.distance)

    def test_main_shortest_route(self):
        expected = ["Saint Paul", "Chicago", "Columbus", "Philadelphia", "New York"]
        for method in (ucs, astar):
            result = method(self.graph, "Saint Paul", "New York")
            self.assertEqual(result.path, expected)
            self.assertEqual(result.distance, 1287)

    def test_all_pairs_optimal(self):
        # Independently compute shortest distances with a small Dijkstra loop.
        for start in self.graph.city_names():
            distances = {start: 0}
            frontier = [(0, start)]
            while frontier:
                cost, city = heapq.heappop(frontier)
                if cost != distances[city]:
                    continue
                for neighbor, miles in self.graph.neighbors(city):
                    if cost + miles < distances.get(neighbor, inf):
                        distances[neighbor] = cost + miles
                        heapq.heappush(frontier, (cost + miles, neighbor))
            for goal in self.graph.city_names():
                for method in (ucs, astar):
                    result = method(self.graph, start, goal)
                    self.assertAlmostEqual(result.distance, distances[goal], msg=f"{method.__name__}: {start} -> {goal}")

    def test_bfs_uses_fewest_edges(self):
        path = bfs(self.graph, "Saint Paul", "New York").path
        self.assertEqual(len(path) - 1, 4)

    def test_dfs_path_has_no_repeat_cities(self):
        path = dfs(self.graph, "Washington", "Chicago").path
        self.assertEqual(len(path), len(set(path)))

    def test_same_start_and_goal(self):
        for method in (bfs, dfs, ucs, astar):
            answer = method(self.graph, "Chicago", "Chicago")
            self.assertEqual(answer.path, ["Chicago"])
            self.assertEqual(answer.distance, 0)

    def test_unknown_city(self):
        with self.assertRaises(ValueError):
            bfs(self.graph, "Atlantis", "Chicago")

    def test_collected_heuristic(self):
        self.assertAlmostEqual(self.graph.heuristic_miles("Saint Paul", "Chicago"), 346.44)

    def test_heuristic_zero_at_goal(self):
        self.assertEqual(self.graph.heuristic_miles("Chicago", "Chicago"), 0)

    def test_flight_time(self):
        h = self.graph.heuristic_miles("Chicago", "Columbus")
        self.assertAlmostEqual(self.graph.estimated_flight_time_hours("Chicago", "Columbus"), h / 250)

    def test_invalid_road(self):
        graph = HighwayGraph()
        graph.add_city("A", 0, 0)
        graph.add_city("B", 0, 1)
        with self.assertRaises(ValueError):
            graph.add_road("A", "B", -1)

    def test_duplicate_road(self):
        graph = HighwayGraph()
        graph.add_city("A", 0, 0)
        graph.add_city("B", 0, 1)
        graph.add_road("A", "B", 100)
        with self.assertRaises(ValueError):
            graph.add_road("A", "B", 100)


if __name__ == "__main__":
    unittest.main()
