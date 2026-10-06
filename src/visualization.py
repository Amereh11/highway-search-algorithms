from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from .graph import HighwayGraph


def plot_route(
    graph: HighwayGraph,
    path: list[str],
    expanded: list[str],
    title: str,
    save_path: Path | None = None,
) -> None:
    """Plot the full graph and highlight one search result."""

    fig, ax = plt.subplots(figsize=(12, 7))

    # Draw all road connections.
    drawn_edges: set[tuple[str, str]] = set()
    for city, neighbors in graph.adjacency.items():
        for neighbor, distance in neighbors:
            edge_key = tuple(sorted((city, neighbor)))
            if edge_key in drawn_edges:
                continue
            drawn_edges.add(edge_key)

            a = graph.cities[city]
            b = graph.cities[neighbor]
            ax.plot(
                [a.longitude, b.longitude],
                [a.latitude, b.latitude],
                linewidth=1,
                alpha=0.35,
            )

            mid_x = (a.longitude + b.longitude) / 2
            mid_y = (a.latitude + b.latitude) / 2
            ax.text(mid_x, mid_y, f"{distance:.0f}", fontsize=7, alpha=0.65)

    # Draw all city nodes.
    for city in graph.city_names():
        point = graph.cities[city]
        ax.scatter(point.longitude, point.latitude, s=45)
        ax.annotate(
            city,
            (point.longitude, point.latitude),
            xytext=(4, 5),
            textcoords="offset points",
            fontsize=8,
        )

    # Lightly show expansion order as numbered markers.
    for index, city in enumerate(expanded, start=1):
        point = graph.cities[city]
        ax.annotate(
            str(index),
            (point.longitude, point.latitude),
            xytext=(-8, -12),
            textcoords="offset points",
            fontsize=7,
        )

    # Highlight the selected path.
    for city_a, city_b in zip(path, path[1:]):
        a = graph.cities[city_a]
        b = graph.cities[city_b]
        ax.plot(
            [a.longitude, b.longitude],
            [a.latitude, b.latitude],
            linewidth=4,
        )

    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.2)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()
