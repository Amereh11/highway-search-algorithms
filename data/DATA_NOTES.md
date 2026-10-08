# Data notes

The team-collected road and straight-line distances are retained unchanged. The runtime reads `cities.csv` and `roads.csv`, and the collected source snapshot remains `google_maps_collected.csv`. Every connection is treated as undirected and stored in both directions in an 11 × 11 matrix. A zero matrix entry means no direct connection. If a straight-line value is not provided for a city-goal pair, A* uses a Haversine calculation from coordinates.
