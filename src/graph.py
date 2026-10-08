# Project: Highway Search Algorithms - Intro to Artificial Intelligence
# Project team: Motasem Amereh, Tamanna Devi, Manjot Singh,
#               Thomas Zangrilli, Parv Alphonso Bhatia
# Version: 3.0 (matrix-based review draft)
# Updated: 2026-10-08
# Purpose: Load highway information into a two-dimensional road matrix.

import csv
from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_MILES = 3958.8
AIRPLANE_SPEED_MPH = 250


class HighwayGraph:
    """A small weighted graph stored as two-dimensional Python lists."""

    def __init__(self):
        self.names = []           # Index -> city name; indices match matrix rows.
        self.coordinates = []     # Index -> (latitude, longitude).
        self.roads = []           # roads[i][j] is road miles; 0 means no road.
        self.plane = []           # plane[i][j] is a collected direct distance.

    @classmethod
    def from_csv(cls, city_file, road_file):
        """Read the two data files; keep city indices in alphabetical order."""
        graph = cls()
        with open(city_file, newline="", encoding="utf-8") as file:
            rows = sorted(csv.DictReader(file), key=lambda row: row["city"])
            for row in rows:
                graph.add_city(row["city"], float(row["latitude"]),
                               float(row["longitude"]))

        with open(road_file, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                plane = float(row["plane_miles"]) if row["plane_miles"] else 0
                graph.add_road(row["city_a"], row["city_b"],
                               float(row["driving_miles"]), plane)
        return graph

    def add_city(self, name, latitude, longitude):
        """Add a matrix row and column whenever a city is added."""
        if name in self.names:
            raise ValueError(f"Duplicate city: {name}")
        self.names.append(name)
        self.coordinates.append((latitude, longitude))

        # Old rows need one new column; new rows contain one slot per city.
        for row in self.roads:
            row.append(0)
        for row in self.plane:
            row.append(0)
        self.roads.append([0] * len(self.names))
        self.plane.append([0] * len(self.names))

    def city_index(self, name):
        """Find the matrix row for the requested city."""
        if name not in self.names:
            raise ValueError(f"Unknown city '{name}'. Choose: {', '.join(self.names)}")
        return self.names.index(name)

    def city_names(self):
        return self.names.copy()

    def add_road(self, first, second, miles, plane_miles=0):
        """Store each road in both directions because roads are undirected."""
        a = self.city_index(first)
        b = self.city_index(second)
        if a == b or miles <= 0 or plane_miles < 0:
            raise ValueError("Road endpoints must differ and distances must be valid")
        if self.roads[a][b] != 0:
            raise ValueError(f"Repeated road: {first} - {second}")
        self.roads[a][b] = self.roads[b][a] = miles
        self.plane[a][b] = self.plane[b][a] = plane_miles

    def neighbors(self, city_index):
        """Return (neighbor index, miles) for roads in a matrix row."""
        return [(j, miles) for j, miles in enumerate(self.roads[city_index])
                if miles > 0]

    def path_distance(self, path):
        """Add driving distances along a list of city names."""
        total = 0
        for first, second in zip(path, path[1:]):
            a = self.city_index(first)
            b = self.city_index(second)
            if self.roads[a][b] == 0:
                raise ValueError(f"No road between {first} and {second}")
            total += self.roads[a][b]
        return total

    def estimate(self, a, b):
        """Get collected straight-line miles or calculate a Haversine estimate."""
        if a == b:
            return 0
        if self.plane[a][b] > 0:
            return self.plane[a][b]

        # Haversine converts latitude and longitude into great-circle miles.
        lat1, lon1 = map(radians, self.coordinates[a])
        lat2, lon2 = map(radians, self.coordinates[b])
        value = sin((lat2 - lat1) / 2) ** 2
        value += cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
        return 2 * EARTH_RADIUS_MILES * asin(sqrt(min(1, value)))

    def heuristic_miles(self, start, goal):
        return self.estimate(self.city_index(start), self.city_index(goal))

    def flight_hours(self, start, goal):
        """The class assignment assumes a straight flight at 250 miles/hour."""
        return self.heuristic_miles(start, goal) / AIRPLANE_SPEED_MPH
