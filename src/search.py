"""Four ways to search the same highway graph."""

from collections import deque
from dataclasses import dataclass
import heapq
from math import inf


@dataclass
class SearchResult:
    path: list | None
    distance: float
    expanded: list


def build_path(parents, goal):
    """Follow the parent links backward from the goal to the start."""
    path = []
    city = goal
    while city is not None:
        path.append(city)
        city = parents[city]
    return list(reversed(path))


def bfs(graph, start, goal):
    graph.validate_city(start)
    graph.validate_city(goal)
    queue = deque([start])
    parents = {start: None}
    expanded = []

    while queue:
        city = queue.popleft()
        expanded.append(city)
        if city == goal:
            path = build_path(parents, goal)
            return SearchResult(path, graph.path_distance(path), expanded)
        for neighbor, miles in graph.neighbors(city):
            if neighbor not in parents:
                parents[neighbor] = city
                queue.append(neighbor)
    return SearchResult(None, inf, expanded)


def dfs(graph, start, goal):
    graph.validate_city(start)
    graph.validate_city(goal)
    # Keep the parent with each stack entry; a parent is finalized on visiting.
    stack = [(start, None)]
    visited = set()
    parents = {}
    expanded = []

    while stack:
        city, previous = stack.pop()
        if city in visited:
            continue
        visited.add(city)
        parents[city] = previous
        expanded.append(city)
        if city == goal:
            path = build_path(parents, goal)
            return SearchResult(path, graph.path_distance(path), expanded)
        # A stack reverses insertion order; reverse here to visit A before Z.
        for neighbor, miles in reversed(graph.neighbors(city)):
            if neighbor not in visited:
                stack.append((neighbor, city))
    return SearchResult(None, inf, expanded)


def ucs(graph, start, goal):
    graph.validate_city(start)
    graph.validate_city(goal)
    queue = [(0, start)]
    best_cost = {start: 0}
    parents = {start: None}
    expanded = []

    while queue:
        miles_so_far, city = heapq.heappop(queue)
        # Ignore an outdated queue entry after discovering a shorter route.
        if miles_so_far != best_cost[city]:
            continue
        expanded.append(city)
        if city == goal:
            return SearchResult(build_path(parents, goal), miles_so_far, expanded)
        for neighbor, road_miles in graph.neighbors(city):
            new_cost = miles_so_far + road_miles
            if new_cost < best_cost.get(neighbor, inf):
                best_cost[neighbor] = new_cost
                parents[neighbor] = city
                heapq.heappush(queue, (new_cost, neighbor))
    return SearchResult(None, inf, expanded)


def astar(graph, start, goal):
    graph.validate_city(start)
    graph.validate_city(goal)
    queue = [(graph.heuristic_miles(start, goal), 0, start)]
    best_cost = {start: 0}
    parents = {start: None}
    expanded = []

    while queue:
        priority, miles_so_far, city = heapq.heappop(queue)
        if miles_so_far != best_cost[city]:
            continue
        expanded.append(city)
        if city == goal:
            return SearchResult(build_path(parents, goal), miles_so_far, expanded)
        for neighbor, road_miles in graph.neighbors(city):
            new_cost = miles_so_far + road_miles
            if new_cost < best_cost.get(neighbor, inf):
                best_cost[neighbor] = new_cost
                parents[neighbor] = city
                estimate = graph.heuristic_miles(neighbor, goal)
                heapq.heappush(queue, (new_cost + estimate, new_cost, neighbor))
    return SearchResult(None, inf, expanded)
