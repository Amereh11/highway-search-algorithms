"""Draw the measured road connections and a highlighted search path."""

import matplotlib
matplotlib.use("Agg")  # Save images even when no screen is available.
import matplotlib.pyplot as plt


def plot_route(graph, path, expanded, title, save_path):
    fig, ax = plt.subplots(figsize=(11, 6))
    seen = set()
    for city in graph.city_names():
        x1, y1 = graph.locations[city][1], graph.locations[city][0]
        for neighbor, miles in graph.neighbors(city):
            road = frozenset((city, neighbor))
            if road in seen:
                continue
            seen.add(road)
            x2, y2 = graph.locations[neighbor][1], graph.locations[neighbor][0]
            ax.plot([x1, x2], [y1, y2], color="#aab7c5", linewidth=1.3, zorder=1)
            ax.text((x1+x2)/2, (y1+y2)/2, str(int(miles)), fontsize=7,
                    color="#586474")

    for index, city in enumerate(expanded, start=1):
        latitude, longitude = graph.locations[city]
        ax.annotate(str(index), (longitude, latitude), xytext=(-7, -12),
                    textcoords="offset points", fontsize=7, color="#5c6470")

    for city_a, city_b in zip(path, path[1:]):
        lat1, lon1 = graph.locations[city_a]
        lat2, lon2 = graph.locations[city_b]
        ax.plot([lon1, lon2], [lat1, lat2], color="#1766a6", linewidth=3.5,
                zorder=3)

    for city in graph.city_names():
        latitude, longitude = graph.locations[city]
        ax.scatter(longitude, latitude, s=35, color="#143c5c", zorder=4)
        ax.annotate(city, (longitude, latitude), xytext=(4, 5),
                    textcoords="offset points", fontsize=8)

    ax.set(title=title, xlabel="Longitude", ylabel="Latitude")
    ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(save_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
