import math

import numpy as np
import pytest

from arespath.planner import astar
from arespath.terrain import slope_degrees, traversal_cost


def test_astar_finds_direct_path_on_uniform_grid():
    path, cost = astar(np.ones((5, 5)), (0, 0), (4, 4))

    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)
    assert len(path) == 5
    assert cost == pytest.approx(4 * math.sqrt(2))


def test_astar_routes_around_blocked_cells():
    grid = np.ones((5, 5))
    grid[1:4, 2] = np.inf

    path, _ = astar(grid, (2, 0), (2, 4))

    assert path
    assert all(np.isfinite(grid[point]) for point in path)
    assert (2, 2) not in path


def test_astar_returns_no_path_when_goal_is_blocked():
    grid = np.ones((3, 3))
    grid[2, 2] = np.inf

    path, cost = astar(grid, (0, 0), (2, 2))

    assert path == []
    assert math.isinf(cost)


def test_astar_rejects_out_of_bounds_endpoint():
    with pytest.raises(ValueError, match="outside the grid"):
        astar(np.ones((3, 3)), (0, 0), (3, 1))


def test_astar_does_not_cut_diagonal_corners():
    grid = np.array([[1.0, np.inf], [np.inf, 1.0]])

    path, cost = astar(grid, (0, 0), (1, 1))

    assert path == []
    assert math.isinf(cost)


def test_slope_cost_blocks_steep_cells():
    elevation = np.zeros((5, 5))
    elevation[:, 2:] = np.arange(3, dtype=float) * 100.0

    slopes = slope_degrees(elevation, 1.0)
    costs = traversal_cost(slopes, max_slope_degrees=20.0)

    assert np.isinf(costs[:, 2:]).any()
    assert np.isfinite(costs[:, :2]).all()


def test_slope_rejects_non_positive_resolution():
    with pytest.raises(ValueError, match="positive"):
        slope_degrees(np.zeros((3, 3)), 0.0)
