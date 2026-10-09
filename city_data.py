"""Data for the 11-city highway search project.

ROAD_EDGES are the team's Google Maps driving distances g(n).
HEURISTIC_PAIRS are the team's straight-line distances h(n), in miles.
"""

AIRPLANE_SPEED_MPH = 250.0

CITIES = [
    "Saint Paul", "Chicago", "Springfield", "Indianapolis", "Columbus",
    "Philadelphia", "New York", "Washington DC", "Columbia", "Atlanta", "Nashville"
]

# Approximate geographic coordinates used ONLY to place nodes on the program's map.
# Search costs use ROAD_EDGES and HEURISTIC_PAIRS below.
CITY_COORDS = {
    "Saint Paul": (44.9537, -93.0900),
    "Chicago": (41.8781, -87.6298),
    "Springfield": (39.7817, -89.6501),
    "Indianapolis": (39.7684, -86.1581),
    "Columbus": (39.9612, -82.9988),
    "Philadelphia": (39.9526, -75.1652),
    "New York": (40.7128, -74.0060),
    "Washington DC": (38.9072, -77.0369),
    "Columbia": (34.0007, -81.0348),
    "Atlanta": (33.7490, -84.3880),
    "Nashville": (36.1627, -86.7816),
}

# g(n): driving-distance edges from the first handwritten data sheet.
ROAD_EDGES = [
    ("Saint Paul", "Chicago", 398),
    ("Saint Paul", "Springfield", 515),
    ("Springfield", "Chicago", 201),
    ("Springfield", "Nashville", 374),
    ("Springfield", "Indianapolis", 211),
    ("Chicago", "Indianapolis", 183),
    ("Chicago", "Columbus", 325),
    ("Indianapolis", "Nashville", 288),
    ("Indianapolis", "Columbus", 174),
    ("Nashville", "Columbia", 462),
    ("Nashville", "Atlanta", 248),
    ("Columbus", "Philadelphia", 469),
    ("Columbus", "Washington DC", 398),
    ("Atlanta", "Columbia", 214),
    ("Columbia", "Washington DC", 478),
    ("Washington DC", "Philadelphia", 136),
    ("Philadelphia", "New York", 95),
]

# h(n): all 55 unique straight-line city-pair distances supplied by the team.
HEURISTIC_PAIRS = {
    ("Saint Paul", "Chicago"): 346.44,
    ("Saint Paul", "Springfield"): 397.21,
    ("Saint Paul", "Indianapolis"): 505.89,
    ("Saint Paul", "Columbus"): 619.46,
    ("Saint Paul", "Philadelphia"): 974.70,
    ("Saint Paul", "New York"): 1007.55,
    ("Saint Paul", "Washington DC"): 922.29,
    ("Saint Paul", "Columbia"): 991.33,
    ("Saint Paul", "Atlanta"): 901.326,
    ("Saint Paul", "Nashville"): 691.88,

    ("Chicago", "Springfield"): 179.51,
    ("Chicago", "Indianapolis"): 165.34,
    ("Chicago", "Columbus"): 291.66,
    ("Chicago", "Philadelphia"): 663.84,
    ("Chicago", "New York"): 711.148,
    ("Chicago", "Washington DC"): 594.225,
    ("Chicago", "Columbia"): 652.39,
    ("Chicago", "Atlanta"): 588.091,
    ("Chicago", "Nashville"): 397.628,

    ("Springfield", "Indianapolis"): 186.0,
    ("Springfield", "Columbus"): 352.246,
    ("Springfield", "Philadelphia"): 767.487,
    ("Springfield", "New York"): 824.93,
    ("Springfield", "Washington DC"): 675.288,
    ("Springfield", "Columbia"): 621.64,
    ("Springfield", "Atlanta"): 508.823,
    ("Springfield", "Nashville"): 296.54,

    ("Indianapolis", "Columbus"): 169.24,
    ("Indianapolis", "Philadelphia"): 583.29,
    ("Indianapolis", "New York"): 643.35,
    ("Indianapolis", "Washington DC"): 492.189,
    ("Indianapolis", "Columbia"): 488.603,
    ("Indianapolis", "Atlanta"): 426.476,
    ("Indianapolis", "Nashville"): 251.50,

    ("Columbus", "Philadelphia"): 414.98,
    ("Columbus", "New York"): 475.44,
    ("Columbus", "Washington DC"): 326.60,
    ("Columbus", "Columbia"): 426.119,
    ("Columbus", "Atlanta"): 435.507,
    ("Columbus", "Nashville"): 333.711,

    ("Philadelphia", "New York"): 80.62,
    ("Philadelphia", "Washington DC"): 123.41,
    ("Philadelphia", "Columbia"): 523.569,
    ("Philadelphia", "Atlanta"): 663.913,
    ("Philadelphia", "Nashville"): 683.559,

    ("New York", "Washington DC"): 202.26,
    ("New York", "Columbia"): 523.73,
    ("New York", "Atlanta"): 745.027,
    ("New York", "Nashville"): 682.955,

    ("Washington DC", "Columbia"): 405.32,
    ("Washington DC", "Atlanta"): 542.443,
    ("Washington DC", "Nashville"): 566.509,

    ("Columbia", "Atlanta"): 193.14,
    ("Columbia", "Nashville"): 357.54,

    ("Atlanta", "Nashville"): 214.81,
}

GRAPH = {city: {} for city in CITIES}
for a, b, miles in ROAD_EDGES:
    GRAPH[a][b] = miles
    GRAPH[b][a] = miles


def heuristic(city, goal):
    """Return h(city, goal) in straight-line miles."""
    if city == goal:
        return 0.0
    return HEURISTIC_PAIRS.get((city, goal), HEURISTIC_PAIRS.get((goal, city)))
