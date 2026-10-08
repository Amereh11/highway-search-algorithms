"""Load the highway data and provide distances between cities."""

import csv
from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_MILES = 3958.8
PLANE_SPEED_MPH = 250


class HighwayGraph:
    def __init__(self):
        self.locations = {}  # city name -> (latitude, longitude)
        self.roads = {}      # city name -> list of (neighbor, driving miles)
        self.plane_miles = {}  # measured straight-line distance for listed edges

    @classmethod
    def from_csv(cls, city_file, road_file):
        graph = cls()
        with open(city_file, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                graph.add_city(row["city"], float(row["latitude"]),
                               float(row["longitude"]))

        with open(road_file, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                graph.add_road(row["city_a"], row["city_b"],
                               float(row["driving_miles"]),
                               float(row["plane_miles"]) if row.get("plane_miles") else None)
        return graph

    def add_city(self, name, latitude, longitude):
        if name in self.locations:
            raise ValueError(f"Duplicate city: {name}")
        self.locations[name] = (latitude, longitude)
        self.roads[name] = []

    def validate_city(self, name):
        if name not in self.locations:
            choices = ", ".join(self.city_names())
            raise ValueError(f"Unknown city: {name}. Choose from: {choices}")

    def add_road(self, city_a, city_b, driving_miles, plane_miles=None):
        self.validate_city(city_a)
        self.validate_city(city_b)
        if city_a == city_b or driving_miles <= 0:
            raise ValueError("Roads must connect different cities with positive mileage")
        if plane_miles is not None and (plane_miles < 0 or plane_miles > driving_miles):
            raise ValueError("Straight-line mileage must be between zero and road mileage")
        if any(name == city_b for name, _ in self.roads[city_a]):
            raise ValueError(f"Duplicate road: {city_a} - {city_b}")

        self.roads[city_a].append((city_b, driving_miles))
        self.roads[city_b].append((city_a, driving_miles))
        self.roads[city_a].sort()
        self.roads[city_b].sort()
        if plane_miles is not None:
            self.plane_miles[frozenset((city_a, city_b))] = plane_miles

    def city_names(self):
        return sorted(self.locations)

    def neighbors(self, city):
        self.validate_city(city)
        return self.roads[city]

    def path_distance(self, path):
        total = 0
        for city_a, city_b in zip(path, path[1:]):
            matches = [miles for neighbor, miles in self.roads[city_a]
                       if neighbor == city_b]
            if not matches:
                raise ValueError(f"No road between {city_a} and {city_b}")
            total += matches[0]
        return total

    def heuristic_miles(self, city, goal):
        """Use a collected straight-line distance, or estimate with Haversine."""
        self.validate_city(city)
        self.validate_city(goal)
        if city == goal:
            return 0.0
        measured = self.plane_miles.get(frozenset((city, goal)))
        if measured is not None:
            return measured

        lat1, lon1 = self.locations[city]
        lat2, lon2 = self.locations[goal]
        lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))
        part = sin((lat2 - lat1) / 2) ** 2
        part += cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
        return 2 * EARTH_RADIUS_MILES * asin(sqrt(min(1.0, part)))

    def estimated_flight_time_hours(self, city, goal):
        return self.heuristic_miles(city, goal) / PLANE_SPEED_MPH
