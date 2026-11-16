# AresPath

An interactive Mars terrain explorer and risk-aware route planner built with Python.

## Description

AresPath explores how terrain information can be turned into useful route-planning decisions. The prototype generates a reproducible synthetic landscape, estimates its slope, and compares a shortest route with a route that penalizes steep terrain.

The project is inspired by NASA Space Apps' **Interplanetary Survival Guide: Martian Map** challenge. It is an independent personal project. The current prototype uses synthetic terrain; it does not yet load NASA Mars datasets or control a rover.

## Features

- Generate a deterministic, crater-like demo terrain.
- Estimate terrain slope from an elevation grid.
- Mark cells above a configurable slope threshold as blocked.
- Compare shortest-distance and slope-aware routes.
- Visualize both paths and inspect route distance and accumulated cost.
- Run the path planner tests locally.

## Instructions

Python 3.11 or newer is recommended.

### Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
make install
```

On Windows, activate the environment with `.venv\\Scripts\\activate`.

### Run the app

```sh
make run
```

Streamlit will print a local URL to open in your browser.

### Run tests

```sh
make test
```

## Planning model

The terrain is represented as a regular grid. Each cell has an elevation and a derived slope. A cell above the selected slope limit is treated as blocked. A* searches the grid using either uniform cost (shortest route) or a slope-weighted traversal cost (terrain-aware route).

The terrain-aware cost is a heuristic for demonstration. It is not an official hazard map or a safety assessment for a real rover.

## Project structure

```text
src/arespath/
  app.py       # Streamlit interface and route comparison
  planner.py   # A* search on a weighted grid
  terrain.py   # Synthetic terrain, slope, and traversal costs
tests/
  test_planner.py
docs/
  PROJECT_PLAN.md
```

## Data sources and next step

The current demo does not download or redistribute external terrain data. The next milestone is to select a small, documented Mars elevation product and verify its format, spatial reference, resolution, attribution, and reuse conditions before adding a loader.

- [NASA Mars Trek](https://trek.nasa.gov/mars/) provides Mars imagery and terrain analysis tools.
- [Mars Trek tile API](https://trek.nasa.gov/tiles/apidoc/trekAPI.html?body=mars) documents its map services.
- [Perseverance rover location map](https://science.nasa.gov/mission/mars-2020-perseverance/location-map/) describes high-resolution elevation models used to help plan rover routes.
- [NASA Space Apps challenge reference](https://www.spaceappschallenge.org/2026/challenges/interplanetary-survival-guide-martian-map/).

## Roadmap

- [x] Create a reproducible synthetic terrain demo.
- [x] Implement A* and route comparison.
- [x] Add tests for paths, blocked cells, and invalid endpoints.
- [ ] Select and document a real Mars elevation dataset.
- [ ] Add geospatial loading and coordinate-aware map display.
- [ ] Add an elevation profile and exportable route metrics.

## Author

**mvasquez**
