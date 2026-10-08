# Project: Highway Search Algorithms - Intro to Artificial Intelligence
# Project team: Motasem Amereh, Tamanna Devi, Manjot Singh,
#               Thomas Zangrilli, Parv Alphonso Bhatia
# Version: 3.0 (matrix-based review draft)
# Updated: 2026-10-08
# Purpose: Compare four searches using the graph's two-dimensional road array.

from collections import deque
from dataclasses import dataclass
import heapq
from math import inf


@dataclass
class SearchResult:
    path: list          # City names in the route, or None if unreachable.
    distance: float     # Total driving miles on the selected route.
    expanded: list      # Order in which cities were taken from the frontier.


def make_result(graph, parent, goal, expanded, distance=None):
    """Follow parent indices backward, then convert indices to city names."""
    indices = []
    current = goal
    while current != -1:
        indices.append(current)
        current = parent[current]
    path = [graph.names[index] for index in reversed(indices)]
    miles = graph.path_distance(path) if distance is None else distance
    return SearchResult(path, miles, [graph.names[i] for i in expanded])


def no_route(graph, expanded):
    return SearchResult(None, inf, [graph.names[i] for i in expanded])


def bfs(graph, start, goal):
    """BFS: explore cities level by level using a first-in, first-out queue."""
    first, target = graph.city_index(start), graph.city_index(goal)
    visited = [False] * len(graph.names)  # One boolean per matrix row.
    parent = [-1] * len(graph.names)
    queue = deque([first])
    expanded = []
    visited[first] = True

    while queue:
        city = queue.popleft()
        expanded.append(city)
        if city == target:
            return make_result(graph, parent, target, expanded)

        # Each matrix column is a possible neighbor.
        for next_city, miles in graph.neighbors(city):
            if not visited[next_city]:
                visited[next_city] = True
                parent[next_city] = city
                queue.append(next_city)
    return no_route(graph, expanded)


def dfs(graph, start, goal):
    """DFS: use a stack to explore one branch before backtracking."""
    first, target = graph.city_index(start), graph.city_index(goal)
    visited = [False] * len(graph.names)
    parent = [-1] * len(graph.names)
    stack = [(first, -1)]  # (city, parent); fix parent when visiting.
    expanded = []

    while stack:
        city, previous = stack.pop()
        if visited[city]:
            continue
        visited[city] = True
        parent[city] = previous
        expanded.append(city)
        if city == target:
            return make_result(graph, parent, target, expanded)

        # Reverse the neighbors because the last stack entry is visited first.
        for next_city, miles in reversed(graph.neighbors(city)):
            if not visited[next_city]:
                stack.append((next_city, city))
    return no_route(graph, expanded)


def ucs(graph, start, goal):
    """UCS: expand the city with the smallest driving cost so far."""
    first, target = graph.city_index(start), graph.city_index(goal)
    best = [inf] * len(graph.names)
    parent = [-1] * len(graph.names)
    queue = [(0, first)]  # (driving cost, city index).
    expanded = []
    best[first] = 0

    while queue:
        cost, city = heapq.heappop(queue)
        if cost != best[city]:  # Ignore a more expensive old entry.
            continue
        expanded.append(city)
        if city == target:
            return make_result(graph, parent, target, expanded, cost)

        for next_city, miles in graph.neighbors(city):
            new_cost = cost + miles
            if new_cost < best[next_city]:
                best[next_city] = new_cost
                parent[next_city] = city
                heapq.heappush(queue, (new_cost, next_city))
    return no_route(graph, expanded)


def astar(graph, start, goal):
    """A*: select the smallest f(n) = g(n) + h(n)."""
    first, target = graph.city_index(start), graph.city_index(goal)
    best = [inf] * len(graph.names)
    parent = [-1] * len(graph.names)
    expanded = []
    best[first] = 0
    # A queue entry stores (f, g, city). g is driving miles already traveled.
    queue = [(graph.estimate(first, target), 0, first)]

    while queue:
        priority, cost, city = heapq.heappop(queue)
        if cost != best[city]:
            continue
        expanded.append(city)
        if city == target:
            return make_result(graph, parent, target, expanded, cost)

        for next_city, miles in graph.neighbors(city):
            new_cost = cost + miles
            if new_cost < best[next_city]:
                best[next_city] = new_cost
                parent[next_city] = city
                heuristic = graph.estimate(next_city, target)
                heapq.heappush(queue, (new_cost + heuristic, new_cost, next_city))
    return no_route(graph, expanded)
