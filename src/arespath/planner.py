"""A* path planning for two-dimensional traversal-cost grids."""

from __future__ import annotations

import heapq
import math
from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

Grid = NDArray[np.float64]
Point = tuple[int, int]


def astar(cost_grid: Grid, start: Point, goal: Point) -> tuple[list[Point], float]:
    """Find a least-cost path through a grid.

    Infinite-cost cells are blocked. The returned cost includes the geometric
    length of each step multiplied by the average cost of its two cells.
    Diagonal moves are allowed only when they do not cut across blocked cells.
    """
    grid = np.asarray(cost_grid, dtype=np.float64)
    if grid.ndim != 2 or grid.size == 0:
        raise ValueError("cost_grid must be a non-empty 2D array")

    _validate_point(start, grid.shape, "start")
    _validate_point(goal, grid.shape, "goal")
    if not np.isfinite(grid[start]) or not np.isfinite(grid[goal]):
        return [], math.inf
    if np.any(grid[np.isfinite(grid)] <= 0):
        raise ValueError("finite traversal costs must be positive")

    min_cost = float(np.min(grid[np.isfinite(grid)]))
    open_heap: list[tuple[float, float, Point]] = []
    start_h = _heuristic(start, goal) * min_cost
    heapq.heappush(open_heap, (start_h, 0.0, start))

    scores: dict[Point, float] = {start: 0.0}
    parents: dict[Point, Point] = {}
    moves: Sequence[tuple[int, int, float]] = (
        (-1, 0, 1.0),
        (1, 0, 1.0),
        (0, -1, 1.0),
        (0, 1, 1.0),
        (-1, -1, math.sqrt(2.0)),
        (-1, 1, math.sqrt(2.0)),
        (1, -1, math.sqrt(2.0)),
        (1, 1, math.sqrt(2.0)),
    )

    while open_heap:
        _, current_cost, current = heapq.heappop(open_heap)
        if current_cost > scores.get(current, math.inf):
            continue
        if current == goal:
            return _reconstruct(parents, start, goal), current_cost

        row, col = current
        for row_step, col_step, distance in moves:
            neighbor = (row + row_step, col + col_step)
            if not _inside(neighbor, grid.shape) or not np.isfinite(grid[neighbor]):
                continue
            if row_step and col_step:
                side_a = (row + row_step, col)
                side_b = (row, col + col_step)
                if not np.isfinite(grid[side_a]) or not np.isfinite(grid[side_b]):
                    continue

            step_cost = distance * (grid[current] + grid[neighbor]) / 2.0
            candidate = current_cost + float(step_cost)
            if candidate >= scores.get(neighbor, math.inf):
                continue

            scores[neighbor] = candidate
            parents[neighbor] = current
            estimate = candidate + _heuristic(neighbor, goal) * min_cost
            heapq.heappush(open_heap, (estimate, candidate, neighbor))

    return [], math.inf


def _validate_point(point: Point, shape: tuple[int, int], label: str) -> None:
    if (
        not isinstance(point, tuple)
        or len(point) != 2
        or not all(isinstance(value, int) for value in point)
    ):
        raise ValueError(f"{label} must be a tuple of two integers")
    if not _inside(point, shape):
        raise ValueError(f"{label} is outside the grid")


def _inside(point: Point, shape: tuple[int, int]) -> bool:
    return 0 <= point[0] < shape[0] and 0 <= point[1] < shape[1]


def _heuristic(point: Point, goal: Point) -> float:
    return math.hypot(goal[0] - point[0], goal[1] - point[1])


def _reconstruct(parents: dict[Point, Point], start: Point, goal: Point) -> list[Point]:
    path = [goal]
    while path[-1] != start:
        path.append(parents[path[-1]])
    path.reverse()
    return path
