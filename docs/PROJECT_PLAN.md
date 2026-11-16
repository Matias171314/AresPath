# AresPath project plan

## Goal

Build a small interactive Mars terrain explorer that compares the shortest route with a route that avoids steep terrain. The current application is a portfolio prototype using synthetic terrain. Integrating real Mars elevation data is a later milestone.

This is a personal project inspired by NASA Space Apps' [Interplanetary Survival Guide: Martian Map](https://www.spaceappschallenge.org/2026/challenges/interplanetary-survival-guide-martian-map/), not a submission to the event.

## 150-hour scope

| Work package | Hours | Result |
|---|---:|---|
| Scope and data review | 14 | Region, candidate sources, and acceptance criteria |
| Reproducible Python environment | 8 | Project config, Makefile, app entry point |
| Terrain ingestion and preprocessing | 24 | Small, documented elevation dataset |
| Slope and traversal-cost model | 18 | Slope layer and configurable cost surface |
| A* planner and metrics | 26 | Tested routes, distance, cost, and failure cases |
| Map interface and visualization | 24 | Selectable endpoints and route comparison |
| Validation and robustness | 16 | Tests for data, endpoints, obstacles, and route validity |
| Documentation and polish | 20 | README, demo, credits, and final review |
| **Total** | **150** | **Reproducible portfolio MVP** |

## MVP acceptance criteria

- The project installs from a clean Python 3.11 environment.
- The synthetic demo runs without downloading external data.
- The app compares a shortest path with a slope-weighted path.
- Routes do not cross blocked cells or cut diagonally across blocked corners.
- Tests verify path endpoints, continuity, blocked terrain, and invalid inputs.
- Every future external data layer includes a source and usage/attribution note.
- The UI states that the prototype is not an operational rover safety tool.

## Proposed milestones

1. **Prototype:** synthetic terrain, slope computation, A* and tests.
2. **Data selection:** select one small Jezero-area terrain product and verify its format, map projection, resolution, and reuse conditions.
3. **Data integration:** load and crop the selected DEM; keep the synthetic mode as a fallback.
4. **Interface:** add geospatial map layers, selectable waypoints, elevation profile, and route metrics.
5. **Portfolio release:** polish README, add a short demo, document limitations, and tag a release.

## Scope boundaries

ROS 2 control, physical rover simulation, global Mars coverage, multi-mission fusion, and claims of real-world safety are outside the 150-hour MVP. Potential later work includes energy budgets, turn constraints, uncertainty layers, and comparison of Dijkstra with A*.

## Data references

- [NASA Mars Trek](https://trek.nasa.gov/mars/)
- [Mars Trek tile API](https://trek.nasa.gov/tiles/apidoc/trekAPI.html?body=mars)
- [Perseverance rover location map](https://science.nasa.gov/mission/mars-2020-perseverance/location-map/)
- [NASA PDS Mars 2020 map-data collection](https://pds.nasa.gov/ds-view/pds/viewCollection.jsp?identifier=urn%3Anasa%3Apds%3Amars2020_rover_places%3Adata_maps)

A concrete dataset has not been selected yet. Verify format, projection, resolution, access, and attribution before integrating one.
