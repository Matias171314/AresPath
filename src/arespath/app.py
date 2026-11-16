"""Streamlit demo for comparing shortest and slope-aware Mars routes."""

from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from arespath.planner import astar
from arespath.terrain import create_demo_terrain, slope_degrees, traversal_cost


def _unblocked_grid(cost_grid: np.ndarray) -> np.ndarray:
    """Use uniform cost for the shortest-distance baseline."""
    return np.where(np.isfinite(cost_grid), 1.0, np.inf)


def _format_distance(path: list[tuple[int, int]], cell_size: float) -> str:
    if len(path) < 2:
        return "—"
    distance = sum(
        math.dist(first, second) * cell_size
        for first, second in zip(path, path[1:])
    )
    return f"{distance / 1000.0:.2f} km"


def _add_path(
    figure: go.Figure,
    path: list[tuple[int, int]],
    cell_size: float,
    name: str,
    color: str,
) -> None:
    if not path:
        return
    figure.add_trace(
        go.Scatter(
            x=[point[1] * cell_size for point in path],
            y=[point[0] * cell_size for point in path],
            mode="lines",
            line={"width": 3, "color": color},
            name=name,
            hoverinfo="skip",
        )
    )


st.set_page_config(page_title="AresPath", page_icon="🔴", layout="wide")
st.title("AresPath")
st.caption("Explore a Mars-inspired terrain and compare two route-planning objectives.")

elevation, cell_size_m = create_demo_terrain()
slopes = slope_degrees(elevation, cell_size_m)

with st.sidebar:
    st.header("Mission setup")
    max_slope = st.slider("Maximum traversable slope", 5.0, 40.0, 25.0, 1.0)
    slope_weight = st.slider("Slope penalty", 0.0, 10.0, 4.0, 0.5)
    st.caption("Coordinates are grid cells in this synthetic demo.")
    start_row = st.number_input("Start row", 0, elevation.shape[0] - 1, 8)
    start_col = st.number_input("Start column", 0, elevation.shape[1] - 1, 8)
    goal_row = st.number_input("Goal row", 0, elevation.shape[0] - 1, 91)
    goal_col = st.number_input("Goal column", 0, elevation.shape[1] - 1, 91)

start = (int(start_row), int(start_col))
goal = (int(goal_row), int(goal_col))
risk_cost = traversal_cost(slopes, max_slope, slope_weight)
shortest_path, shortest_cost = astar(_unblocked_grid(risk_cost), start, goal)
safe_path, safe_cost = astar(risk_cost, start, goal)

left, right = st.columns(2)
left.metric("Shortest route", _format_distance(shortest_path, cell_size_m))
right.metric("Slope-aware route", _format_distance(safe_path, cell_size_m))

axis_m = np.arange(elevation.shape[0]) * cell_size_m
fig = go.Figure()
fig.add_trace(
    go.Heatmap(
        x=axis_m,
        y=axis_m,
        z=slopes,
        colorscale="Turbo",
        colorbar={"title": "Slope (°)"},
        hovertemplate="east=%{x:.0f} m<br>north=%{y:.0f} m<br>slope=%{z:.1f}°<extra></extra>",
    )
)
_add_path(fig, shortest_path, cell_size_m, "Shortest", "#44d9e6")
_add_path(fig, safe_path, cell_size_m, "Slope-aware", "#ff4f81")
fig.add_trace(
    go.Scatter(
        x=[start[1] * cell_size_m, goal[1] * cell_size_m],
        y=[start[0] * cell_size_m, goal[0] * cell_size_m],
        mode="markers+text",
        text=["START", "GOAL"],
        textposition="top center",
        marker={
            "size": 12,
            "color": ["#ffffff", "#ffe66d"],
            "line": {"width": 2, "color": "#171923"},
        },
        name="Waypoints",
    )
)
fig.update_layout(
    height=650,
    template="plotly_dark",
    xaxis_title="East (m)",
    yaxis_title="North (m)",
    yaxis={"autorange": "reversed", "scaleanchor": "x", "scaleratio": 1},
    legend={"orientation": "h", "y": 1.02, "x": 0},
    margin={"l": 20, "r": 20, "t": 40, "b": 20},
)
st.plotly_chart(fig, use_container_width=True)

if not shortest_path or not safe_path:
    st.warning("No route exists for the selected endpoints and slope limit.")
else:
    details_left, details_right = st.columns(2)
    details_left.write(
        f"Shortest: {len(shortest_path)} cells · "
        f"{_format_distance(shortest_path, cell_size_m)} · cost {shortest_cost:.1f}"
    )
    details_right.write(
        f"Slope-aware: {len(safe_path)} cells · "
        f"{_format_distance(safe_path, cell_size_m)} · cost {safe_cost:.1f}"
    )

st.info(
    "Prototype note: this view uses a synthetic elevation grid. "
    "It is not a NASA hazard map and does not assess real rover safety."
)
