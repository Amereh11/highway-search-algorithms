11-CITY HIGHWAY SEARCH PROJECT
==============================
Intro to Artificial Intelligence - CS (NW) 36210 002, Fall 2026
Purdue University Northwest

Team: Motasem Amereh, Tamanna Devi, Manjot Singh, Thomas Zangrilli,
      Parv Alphonso Bhatia

Files
-----
highway_search.py  - Main program: BFS, DFS, UCS and A*, a text menu, and the
                     travel maps.
city_data.py       - All 11 cities, 17 g(n) highway edges, and 55 h(n)
                     straight-line distances.
usa-city-map.png   - Reference map of the 11 selected cities. Not required to
                     run the program.

How to run
----------
1. Install Python 3.8 or newer.
2. Install Matplotlib (used to draw the travel maps):

   pip install matplotlib

3. Keep highway_search.py and city_data.py in the same folder.
4. Run:

   python highway_search.py

Program features
----------------
Menu option 1 - Pick a start and target city
- Choose any two of the 11 cities by number.
- All four algorithms (BFS, DFS, UCS, A*) run on the same pair.
- For each algorithm the program prints the total driving distance, the
  number of cities expanded, and the final route.
- It also prints h(start, target) and the 250 mph airplane-time estimate.
- A map window shows all four results side by side: the final route in blue,
  expanded cities in orange numbered in expansion order, and cities never
  expanded in red.

Menu option 2 - Run 5 random tests
- Picks five random start/target pairs and runs all four algorithms on each.
- Prints the results and opens a map window for each test. Close a window to
  see the next test.
- The random seed is fixed (42), so the same five tests appear every time.

Menu option 3 - Quit

Algorithm costs
---------------
BFS and DFS use graph connectivity/order.
UCS uses accumulated driving distance g(n).
A* uses f(n) = g(n) + h(n), where both g and h are in miles.
The 250 mph airplane value is displayed as an additional estimate; it is not
mixed into f(n), because g(n) is measured in miles.

Data note
---------
The numerical g(n) and h(n) values in city_data.py were transcribed from the
handwritten data collected for this project from Google Maps.
