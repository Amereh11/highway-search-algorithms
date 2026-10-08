# Project: Highway Search Algorithms - Intro to Artificial Intelligence
# Project team: Motasem Amereh, Tamanna Devi, Manjot Singh,
#               Thomas Zangrilli, Parv Alphonso Bhatia
# Version: 3.0 (matrix-based review draft)
# Updated: 2026-10-08
# Purpose: Draw the graph and highlight a searched route.

import matplotlib
matplotlib.use("Agg")  # This allows graph saving without opening a window.
import matplotlib.pyplot as plt


def plot_route(graph, path, expanded, title, save_path):
    """Plot all measured roads and highlight the selected route."""
    fig, ax = plt.subplots(figsize=(10.8, 6))
    n = len(graph.names)

    # Plot every undirected road exactly once, above the matrix diagonal.
    for i in range(n):
        for j in range(i + 1, n):
            miles = graph.roads[i][j]
            if miles == 0:
                continue
            y1, x1 = graph.coordinates[i]
            y2, x2 = graph.coordinates[j]
            ax.plot([x1, x2], [y1, y2], color="#c3ced7", linewidth=1.2)
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{miles:.0f}", fontsize=7)

    # The highlighted route is drawn over the background road connections.
    for first, second in zip(path, path[1:]):
        a, b = graph.city_index(first), graph.city_index(second)
        y1, x1 = graph.coordinates[a]
        y2, x2 = graph.coordinates[b]
        ax.plot([x1, x2], [y1, y2], color="#2069a2", linewidth=3.2)

    # Label each city and the order in which the search expanded it.
    for i, name in enumerate(graph.names):
        latitude, longitude = graph.coordinates[i]
        ax.scatter(longitude, latitude, s=38, color="#183a59", zorder=3)
        ax.annotate(name, (longitude, latitude), xytext=(4, 5),
                    textcoords="offset points", fontsize=8)
    for order, name in enumerate(expanded, 1):
        latitude, longitude = graph.coordinates[graph.city_index(name)]
        ax.annotate(str(order), (longitude, latitude), xytext=(-7, -12),
                    textcoords="offset points", fontsize=7, color="#4e6575")

    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=.18)
    fig.tight_layout()
    fig.savefig(save_path, dpi=170, bbox_inches="tight")
    plt.close(fig)
