"""Synthetic terrain generation and slope-aware traversal costs."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

FloatGrid = NDArray[np.float64]


def create_demo_terrain(size: int = 100) -> tuple[FloatGrid, float]:
    """Return a deterministic elevation grid and its cell spacing in metres."""
    if size < 10:
        raise ValueError("size must be at least 10")

    cell_size_m = 3000.0 / (size - 1)
    axis = np.linspace(-1500.0, 1500.0, size)
    x_grid, y_grid = np.meshgrid(axis, axis)

    crater = -90.0 * np.exp(
        -(((x_grid + 280.0) ** 2) + ((y_grid - 180.0) ** 2)) / (2.0 * 430.0**2)
    )
    ridge = 190.0 * np.exp(-((x_grid - 180.0) ** 2) / (2.0 * 155.0**2))
    ridge *= 0.72 + 0.28 * np.cos(y_grid / 380.0)
    hill = 95.0 * np.exp(
        -(((x_grid - 800.0) ** 2) + ((y_grid + 670.0) ** 2)) / (2.0 * 360.0**2)
    )
    gentle_variation = 12.0 * np.sin(x_grid / 260.0) * np.cos(y_grid / 310.0)

    elevation = crater + ridge + hill + gentle_variation
    return elevation.astype(np.float64), cell_size_m


def slope_degrees(elevation: FloatGrid, cell_size_m: float) -> FloatGrid:
    """Estimate slope angle in degrees using central finite differences."""
    grid = np.asarray(elevation, dtype=np.float64)
    if grid.ndim != 2 or min(grid.shape) < 2:
        raise ValueError("elevation must be a 2D grid with at least two cells per axis")
    if cell_size_m <= 0:
        raise ValueError("cell_size_m must be positive")

    gradient_y, gradient_x = np.gradient(grid, cell_size_m)
    slope = np.degrees(np.arctan(np.hypot(gradient_x, gradient_y)))
    return slope.astype(np.float64)


def traversal_cost(
    slope: FloatGrid,
    max_slope_degrees: float = 25.0,
    slope_weight: float = 4.0,
) -> FloatGrid:
    """Build a positive cost grid; cells steeper than the limit are blocked."""
    grid = np.asarray(slope, dtype=np.float64)
    if grid.ndim != 2:
        raise ValueError("slope must be a 2D grid")
    if max_slope_degrees <= 0:
        raise ValueError("max_slope_degrees must be positive")
    if slope_weight < 0:
        raise ValueError("slope_weight cannot be negative")

    costs = 1.0 + slope_weight * (grid / max_slope_degrees) ** 2
    costs = costs.astype(np.float64)
    costs[grid > max_slope_degrees] = np.inf
    return costs
