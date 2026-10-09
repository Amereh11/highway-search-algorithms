"""Regression tests for the highway search report (October 8, 2026)."""

import heapq
import random
import unittest
from math import inf

from city_data import CITIES, GRAPH, HEURISTIC_PAIRS, ROAD_EDGES, heuristic
from highway_search import ALGORITHMS, path_distance


class HighwaySearchTests(unittest.TestCase):
    def test_data_counts(self):
        self.assertEqual(len(CITIES), 11)
        self.assertEqual(len(ROAD_EDGES), 17)
        self.assertEqual(len(HEURISTIC_PAIRS), 55)
        self.assertEqual(sum(len(neighbors) for neighbors in GRAPH.values()), 34)

    def test_road_weights_bidirectional(self):
        for city, neighbors in GRAPH.items():
            for neighbor, distance in neighbors.items():
                self.assertGreater(distance, 0)
                self.assertEqual(GRAPH[neighbor][city], distance)

    def test_heuristic_table(self):
        for start in CITIES:
            self.assertEqual(heuristic(start, start), 0)
            for goal in CITIES:
                self.assertIsNotNone(heuristic(start, goal))
                self.assertEqual(heuristic(start, goal), heuristic(goal, start))

    def test_chicago_atlanta_matches_report(self):
        expected = {
            "BFS": (823, 10),
            "DFS": (3046, 10),
            "UCS": (719, 7),
            "A*": (719, 5),
        }
        for name, search in ALGORITHMS.items():
            with self.subTest(algorithm=name):
                path, expanded = search("Chicago", "Atlanta")
                self.assertEqual((path_distance(path), len(expanded)), expected[name])
        for name in ("UCS", "A*"):
            path, _ = ALGORITHMS[name]("Chicago", "Atlanta")
            self.assertEqual(path, ["Chicago", "Indianapolis", "Nashville", "Atlanta"])

    def test_random_seed_42(self):
        expected = [
            ("Nashville", "Chicago"),
            ("Saint Paul", "Columbus"),
            ("Indianapolis", "Nashville"),
            ("Springfield", "Chicago"),
            ("Nashville", "Columbia"),
        ]
        picker = random.Random(42)
        self.assertEqual([tuple(picker.sample(CITIES, 2)) for _ in range(5)], expected)

    def test_random_results_match_report(self):
        cases = [
            ("Nashville", "Chicago", (575, 1287, 471, 471)),
            ("Saint Paul", "Columbus", (723, 1435, 723, 723)),
            ("Indianapolis", "Nashville", (288, 2994, 288, 288)),
            ("Springfield", "Chicago", (201, 913, 201, 201)),
            ("Nashville", "Columbia", (462, 2727, 462, 462)),
        ]
        for start, goal, costs in cases:
            for (name, search), cost in zip(ALGORITHMS.items(), costs):
                with self.subTest(pair=(start, goal), algorithm=name):
                    path, _ = search(start, goal)
                    self.assertEqual(path_distance(path), cost)

    def test_every_algorithm_finds_a_valid_path(self):
        for start in CITIES:
            for goal in CITIES:
                for name, search in ALGORITHMS.items():
                    with self.subTest(start=start, goal=goal, algorithm=name):
                        path, expanded = search(start, goal)
                        self.assertEqual(path[0], start)
                        self.assertEqual(path[-1], goal)
                        self.assertGreaterEqual(len(expanded), 1)
                        for a, b in zip(path, path[1:]):
                            self.assertIn(b, GRAPH[a])

    def test_all_pairs_ucs_astar_optimal(self):
        # Dijkstra's distance table is calculated independently of the searches.
        for start in CITIES:
            distance = {city: inf for city in CITIES}
            distance[start] = 0
            frontier = [(0, start)]
            while frontier:
                current_distance, city = heapq.heappop(frontier)
                if current_distance != distance[city]:
                    continue
                for neighbor, weight in GRAPH[city].items():
                    new_distance = current_distance + weight
                    if new_distance < distance[neighbor]:
                        distance[neighbor] = new_distance
                        heapq.heappush(frontier, (new_distance, neighbor))
            for goal in CITIES:
                for name in ("UCS", "A*"):
                    with self.subTest(start=start, goal=goal, algorithm=name):
                        path, _ = ALGORITHMS[name](start, goal)
                        self.assertEqual(path_distance(path), distance[goal])

    def test_bfs_fewest_road_connections(self):
        for start in CITIES:
            hops = {start: 0}
            pending = [start]
            for city in pending:
                for neighbor in GRAPH[city]:
                    if neighbor not in hops:
                        hops[neighbor] = hops[city] + 1
                        pending.append(neighbor)
            for goal in CITIES:
                path, _ = ALGORITHMS["BFS"](start, goal)
                self.assertEqual(len(path) - 1, hops[goal])


if __name__ == "__main__":
    unittest.main()
