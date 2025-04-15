# hex_knot_mosaic_plot.py

import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, Dict, List

# --- 1. TILE DEFINITIONS ---
Tile = Dict[str, any]

tile_set: Dict[int, Tile] = {
    4:  {"name": "cap_NWSE", "paths": [(5, 2)]},
    13: {"name": "line_H", "paths": [(1, 4)]},
    16: {"name": "cross_1", "paths": [(0, 3), (1, 4)]},
}

# --- 2. GRID SETUP ---
Grid = Dict[Tuple[int, int], Dict]

grid: Grid = {
    (0, 0): {"tile": 16, "rotation": 0, "component": "A"},
    (1, 0): {"tile": 13, "rotation": 0, "component": "A"},
    (2, 0): {"tile": 4, "rotation": 1, "component": "A"},
}

# --- 3. HEX GEOMETRY ---
HEX_DIRECTIONS = [
    (0, -1),  # 0 - top
    (1, -1),  # 1 - top-right
    (1, 0),   # 2 - bottom-right
    (0, 1),   # 3 - bottom
    (-1, 1),  # 4 - bottom-left
    (-1, 0),  # 5 - top-left
]

def neighbor(coord: Tuple[int, int], direction: int) -> Tuple[int, int]:
    dq, dr = HEX_DIRECTIONS[direction]
    q, r = coord
    return (q + dq, r + dr)

def rotate_edge(edge: int, rotation: int) -> int:
    return (edge + rotation) % 6

def rotate_paths(paths: List[Tuple[int, int]], rotation: int) -> List[Tuple[int, int]]:
    return [(rotate_edge(a, rotation), rotate_edge(b, rotation)) for a, b in paths]

def edge_to_point(edge: int, center: Tuple[float, float], radius: float = 1.0) -> Tuple[float, float]:
    angle_deg = 60 * edge - 30
    angle_rad = np.radians(angle_deg)
    return (
        center[0] + radius * np.cos(angle_rad),
        center[1] + radius * np.sin(angle_rad),
    )

def axial_to_xy(q: int, r: int, size: float = 1.0) -> Tuple[float, float]:
    x = size * (3**0.5) * (q + r/2)
    y = size * 1.5 * r
    return (x, y)

# --- 4. PLOTTING ---
def plot_grid(grid: Grid, size: float = 1.0):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_aspect('equal')

    for (q, r), data in grid.items():
        tile_id = data["tile"]
        rotation = data["rotation"]
        center = axial_to_xy(q, r, size)
        hex_patch = hexagon_patch(center, size, edgecolor='black', facecolor='white')
        ax.add_patch(hex_patch)

        paths = rotate_paths(tile_set[tile_id]["paths"], rotation)
        for a, b in paths:
            p1 = edge_to_point(a, center, size * 0.95)
            p2 = edge_to_point(b, center, size * 0.95)
            plot_arc(ax, p1, p2, center)

        ax.text(center[0], center[1], str(tile_id), ha='center', va='center', fontsize=8)

    ax.set_xlim(-1, 8)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')
    plt.show()

def hexagon_patch(center: Tuple[float, float], size: float, **kwargs):
    cx, cy = center
    angles = np.linspace(0, 2*np.pi, 7)
    verts = [(cx + size * np.cos(a), cy + size * np.sin(a)) for a in angles]
    return plt.Polygon(verts, closed=True, **kwargs)

def plot_arc(ax, p1, p2, center, color='green'):
    """Draws a curved line from p1 to p2, roughly curving toward the center."""
    cx, cy = center
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    # Pull toward center for curve
    ctrl = ((mx + cx) / 2, (my + cy) / 2)

    path = np.array([p1, ctrl, p2])
    bez_x, bez_y = bezier(path)
    ax.plot(bez_x, bez_y, color=color, lw=2)

def bezier(points, steps=30):
    """Quadratic Bézier curve from 3 points"""
    t = np.linspace(0, 1, steps)
    p0, p1, p2 = np.array(points)
    curve = (1 - t)**2[:, None] * p0 + 2*(1 - t)[:, None]*t[:, None]*p1 + t**2[:, None]*p2
    return curve[:, 0], curve[:, 1]

# --- MAIN ---
if __name__ == "__main__":
    plot_grid(grid)
