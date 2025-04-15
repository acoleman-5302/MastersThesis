# hex_knot_mosaic.py

from typing import Tuple, Dict, List

# ---------------------
# 1. Define tile types
# ---------------------

# Hex tile edge labeling: 0 = top, then clockwise to 5
Tile = Dict[str, any]

tile_set: Dict[int, Tile] = {
    1:  {"name": "empty", "paths": []},
    2:  {"name": "cap_EW", "paths": [(1, 4)]},
    3:  {"name": "cap_NESW", "paths": [(0, 3)]},
    4:  {"name": "cap_NWSE", "paths": [(5, 2)]},
    5:  {"name": "elbow_NE", "paths": [(0, 1)]},
    6:  {"name": "elbow_EN", "paths": [(1, 0)]},
    7:  {"name": "elbow_ES", "paths": [(1, 2)]},
    8:  {"name": "elbow_SE", "paths": [(2, 1)]},
    9:  {"name": "elbow_SW", "paths": [(3, 2)]},
    10: {"name": "elbow_WS", "paths": [(2, 3)]},
    11: {"name": "elbow_WN", "paths": [(3, 4)]},
    12: {"name": "elbow_NW", "paths": [(4, 3)]},
    13: {"name": "line_H", "paths": [(1, 4)]},
    14: {"name": "line_diag", "paths": [(0, 3)]},
    15: {"name": "line_diag2", "paths": [(5, 2)]},
    16: {"name": "cross_1", "paths": [(0, 3), (1, 4)]},
    17: {"name": "cross_2", "paths": [(2, 5), (0, 3)]},
    18: {"name": "cross_3", "paths": [(1, 4), (2, 5)]},
    19: {"name": "Y_split", "paths": [(0, 2), (0, 4), (2, 4)]},
    20: {"name": "Y_merge", "paths": [(1, 3), (1, 5), (3, 5)]},
    21: {"name": "T_conn", "paths": [(0, 3), (1, 4), (2, 5)]},
    22: {"name": "T_conn_alt", "paths": [(0, 2), (1, 5), (3, 4)]},
    23: {"name": "loop", "paths": [(1, 2), (4, 5)]},
    24: {"name": "big_curve", "paths": [(0, 5), (2, 3)]},
    25: {"name": "three_way", "paths": [(0, 2), (2, 4), (4, 0)]},
    26: {"name": "triple_knot", "paths": [(0, 3), (1, 4), (2, 5)]},
    27: {"name": "junction", "paths": [(0, 2), (2, 4), (0, 4)]},
}


# ---------------------
# 2. Grid Setup
# ---------------------

# Axial coordinate system (q, r)
Grid = Dict[Tuple[int, int], Dict]

# Example knot grid (a tiny sample)
grid: Grid = {
    (0, 0): {"tile": 16, "rotation": 0, "component": "A"},
    (1, 0): {"tile": 13, "rotation": 0, "component": "A"},
    (2, 0): {"tile": 4, "rotation": 1, "component": "A"},
}


# ---------------------
# 3. Helpers
# ---------------------

# Neighbor directions (0 to 5), axial deltas
HEX_DIRECTIONS = [
    (0, -1),  # 0 - top
    (1, -1),  # 1 - top-right
    (1, 0),   # 2 - bottom-right
    (0, 1),   # 3 - bottom
    (-1, 1),  # 4 - bottom-left
    (-1, 0),  # 5 - top-left
]

# Computes the neighbor hexagon given a direction
def neighbor(coord: Tuple[int, int], direction: int) -> Tuple[int, int]:
    dq, dr = HEX_DIRECTIONS[direction]
    q, r = coord
    return (q + dq, r + dr)

def rotate_edge(edge: int, rotation: int) -> int:
    """Rotate edge index by rotation (mod 6)"""
    return (edge + rotation) % 6

def rotate_paths(paths: List[Tuple[int, int]], rotation: int) -> List[Tuple[int, int]]:
    return [(rotate_edge(a, rotation), rotate_edge(b, rotation)) for a, b in paths]


# ---------------------
# 4. Visualization Helper (basic print)
# ---------------------

def print_grid(grid: Grid):
    for coord, data in grid.items():
        q, r = coord
        tile_id = data["tile"]
        rot = data["rotation"]
        name = tile_set[tile_id]["name"]
        print(f"Tile at ({q}, {r}): {name} (id={tile_id}), rotation={rot}")

# ---------------------
# 5. Path Tracing (very basic)
# ---------------------

def get_paths_at(coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    tile_data = grid.get(coord)
    if not tile_data:
        return []

    tile_id = tile_data["tile"]
    rotation = tile_data["rotation"]
    base_paths = tile_set[tile_id]["paths"]
    return rotate_paths(base_paths, rotation)


# ---------------------
# Run example
# ---------------------

if __name__ == "__main__":
    print("Hex Knot Mosaic Example Grid")
    print_grid(grid)

    for coord in grid:
        paths = get_paths_at(coord)
        print(f"At {coord}, paths: {paths}")
