from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import heapq
from itertools import count
from math import inf

from .graph import HighwayGraph


@dataclass
class SearchResult:
    path: list[str] | None
    distance: float
    expanded: list[str]


def _reconstruct_path(parent: dict[str, str | None], goal: str) -> list[str]:
    path = []
    current: str | None = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def bfs(graph: HighwayGraph, start: str, goal: str) -> SearchResult:
    graph.validate_city(start)
    graph.validate_city(goal)

    queue = deque([start])
    parent: dict[str, str | None] = {start: None}
    expanded: list[str] = []

    while queue:
        current = queue.popleft()
        expanded.append(current)

        if current == goal:
            path = _reconstruct_path(parent, goal)
            return SearchResult(path, graph.path_distance(path), expanded)

        for neighbor, _ in graph.neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    return SearchResult(None, inf, expanded)


def dfs(graph: HighwayGraph, start: str, goal: str) -> SearchResult:
    graph.validate_city(start)
    graph.validate_city(goal)

    stack = [start]
    parent: dict[str, str | None] = {start: None}
    visited: set[str] = set()
    expanded: list[str] = []

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        expanded.append(current)

        if current == goal:
            path = _reconstruct_path(parent, goal)
            return SearchResult(path, graph.path_distance(path), expanded)

        # Reverse sorted order so alphabetically earlier neighbors are
        # processed first when popped from the LIFO stack.
        for neighbor, _ in reversed(graph.neighbors(current)):
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current
                stack.append(neighbor)

    return SearchResult(None, inf, expanded)


def ucs(graph: HighwayGraph, start: str, goal: str) -> SearchResult:
    graph.validate_city(start)
    graph.validate_city(goal)

    tie_breaker = count()
    frontier = [(0.0, next(tie_breaker), start)]
    best_cost = {start: 0.0}
    parent: dict[str, str | None] = {start: None}
    expanded: list[str] = []
    closed: set[str] = set()

    while frontier:
        cost, _, current = heapq.heappop(frontier)

        if current in closed:
            continue

        closed.add(current)
        expanded.append(current)

        if current == goal:
            path = _reconstruct_path(parent, goal)
            return SearchResult(path, cost, expanded)

        for neighbor, edge_cost in graph.neighbors(current):
            new_cost = cost + edge_cost

            if new_cost < best_cost.get(neighbor, inf):
                best_cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(
                    frontier,
                    (new_cost, next(tie_breaker), neighbor),
                )

    return SearchResult(None, inf, expanded)


def astar(graph: HighwayGraph, start: str, goal: str) -> SearchResult:
    graph.validate_city(start)
    graph.validate_city(goal)

    tie_breaker = count()
    start_h = graph.heuristic_miles(start, goal)

    frontier = [(start_h, 0.0, next(tie_breaker), start)]
    best_g = {start: 0.0}
    parent: dict[str, str | None] = {start: None}
    expanded: list[str] = []
    closed: set[str] = set()

    while frontier:
        _, g_cost, _, current = heapq.heappop(frontier)

        if current in closed:
            continue

        closed.add(current)
        expanded.append(current)

        if current == goal:
            path = _reconstruct_path(parent, goal)
            return SearchResult(path, g_cost, expanded)

        for neighbor, edge_cost in graph.neighbors(current):
            new_g = g_cost + edge_cost

            if new_g < best_g.get(neighbor, inf):
                best_g[neighbor] = new_g
                parent[neighbor] = current
                h = graph.heuristic_miles(neighbor, goal)
                f = new_g + h
                heapq.heappush(
                    frontier,
                    (f, new_g, next(tie_breaker), neighbor),
                )

    return SearchResult(None, inf, expanded)
