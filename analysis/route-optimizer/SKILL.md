---
name: route-optimizer
description: "Generate a production-grade Vehicle Routing Problem (VRP) solver using Google OR-Tools — supports CVRP (capacity), VRPTW (time windows), VRPPD (pickup + delivery), multi-depot, multi-trip, heterogeneous fleet, driver hours-of-service (HOS) compliance."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Route Optimizer (OR-Tools VRP)

You generate a working route optimization pipeline. Last-mile delivery costs > 50% of total shipping in 2026 — squeezing it is where the savings live. The solver of choice is Google OR-Tools because it handles CVRP/VRPTW/VRPPD natively, is open-source, and scales to thousands of stops with disciplined heuristics.

============================================================
=== PRE-FLIGHT ===
============================================================

Verify:

- [ ] **Problem variant**: Pure capacity (CVRP)? Time windows (VRPTW)? Pickup + delivery (VRPPD)? Multi-depot? Heterogeneous fleet?
- [ ] **Stop count**: < 100 — exact solver. 100-1000 — OR-Tools with metaheuristics (Guided Local Search, ~30s-2min). > 1000 — split into clusters first then solve per cluster.
- [ ] **Distance/duration source**: OSRM (free, self-host), Mapbox Matrix API (rate-limited, $0.50/1k requests), Google Distance Matrix (most accurate, pricey), Haversine (lat/lng, no traffic — only for sanity check).
- [ ] **Constraints**: vehicle capacity (weight, volume, count), time windows (hard or soft), driver shift length, HOS compliance (US: 11hr drive / 14hr on-duty / 10hr rest), customer service time per stop, lunch breaks.
- [ ] **Objective**: minimize total distance? Total duration? Vehicle count? Weighted blend? Default is duration-weighted.

Recovery:

- If distance matrix is unavailable, fall back to Haversine + average speed factor (city: 25mph, suburb: 35mph, rural: 45mph) — mark output as "estimate, validate against real road network before dispatch."
- If stop count > 1000, generate the cluster-first scaffold and warn user about runtime.

============================================================
=== PHASE 1: PROJECT SCAFFOLD ===
============================================================

```
route-opt/
├── README.md
├── pyproject.toml              # ortools, numpy, pandas, requests, geojson
├── data/
│   ├── stops.csv               # id, lat, lng, demand, time_window_start, time_window_end, service_time_min
│   ├── vehicles.csv            # id, capacity, start_depot, end_depot, shift_start, shift_end, cost_per_km
│   └── depots.csv              # id, lat, lng
├── src/
│   ├── matrix.py               # build distance/duration matrix (OSRM/Mapbox/Google)
│   ├── solver.py               # OR-Tools routing model
│   ├── constraints.py          # time windows, capacity, HOS
│   ├── output.py               # GeoJSON, KPI report, turn-by-turn
│   └── cli.py                  # python -m src.cli --stops data/stops.csv --vehicles ...
├── tests/
│   ├── test_cvrp.py            # textbook 16-stop example, known optimum
│   └── test_vrptw.py           # Solomon C101 benchmark
└── examples/
    ├── small_cvrp.ipynb        # 20 stops, single depot
    └── large_vrptw.ipynb       # 200 stops, 8 vehicles, time windows
```

VALIDATION: Test against the OR-Tools CVRP example (16 stops, capacity 15) → solution matches published optimum within 1%.

============================================================
=== PHASE 2: DISTANCE / DURATION MATRIX ===
============================================================

Generate `matrix.py` that supports:

**OSRM** (preferred for self-hosting):

- POST to `/table/v1/driving/{coordinates}` → returns distance + duration in seconds.
- Batch in chunks of ≤ 100 origins × 100 destinations to avoid memory blowup.
- Cache results to local SQLite (origin_id, dest_id, dist_m, dur_s, computed_at).

**Mapbox Matrix API**:

- Max 25×25 per request — chunk and stitch.
- Account for `traffic_profile` (real-time vs typical).

**Google Distance Matrix**:

- Max 25 origins × 25 destinations per request, 100 elements per second rate limit.
- Use `departure_time` for traffic-aware estimates.

**Haversine fallback**:

- `R = 6371 km`, standard great-circle formula. Multiply by 1.3 for road-network estimate. Use only for prototyping.

VALIDATION: Matrix cache populated and re-used on subsequent runs. Falls back gracefully if API quota exhausted.

============================================================
=== PHASE 3: OR-TOOLS SOLVER ===
============================================================

Generate `solver.py` using `ortools.constraint_solver.pywrapcp`:

```python
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

manager = pywrapcp.RoutingIndexManager(num_locations, num_vehicles, starts, ends)
routing = pywrapcp.RoutingModel(manager)

# Distance callback
def distance_callback(from_idx, to_idx):
    return distance_matrix[manager.IndexToNode(from_idx)][manager.IndexToNode(to_idx)]
transit_idx = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

# Capacity constraint
def demand_callback(idx):
    return demands[manager.IndexToNode(idx)]
demand_idx = routing.RegisterUnaryTransitCallback(demand_callback)
routing.AddDimensionWithVehicleCapacity(demand_idx, 0, vehicle_capacities, True, 'Capacity')

# Time window constraint
def time_callback(from_idx, to_idx):
    travel = duration_matrix[manager.IndexToNode(from_idx)][manager.IndexToNode(to_idx)]
    service = service_times[manager.IndexToNode(from_idx)]
    return travel + service
time_idx = routing.RegisterTransitCallback(time_callback)
routing.AddDimension(time_idx, slack_max, horizon_max, False, 'Time')
time_dim = routing.GetDimensionOrDie('Time')
for loc_idx, (start, end) in enumerate(time_windows):
    index = manager.NodeToIndex(loc_idx)
    time_dim.CumulVar(index).SetRange(start, end)

# Search
search_params = pywrapcp.DefaultRoutingSearchParameters()
search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
search_params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
search_params.time_limit.FromSeconds(60)
search_params.log_search = False

solution = routing.SolveWithParameters(search_params)
```

VALIDATION: Solver returns a feasible solution OR a clear "infeasible: {reason}" diagnostic, never an empty result.

============================================================
=== PHASE 4: HOS COMPLIANCE & SOFT WINDOWS ===
============================================================

US DOT FMCSA rules for property-carrying drivers (49 CFR § 395.3):

- 11 hours max driving after 10 consecutive hours off-duty
- 14-hour on-duty window (driving + other on-duty)
- 30-min break required after 8 cumulative hours of driving
- 60 hours / 7 days OR 70 hours / 8 days
- 34-hour restart available

Model HOS as additional Time-dimension constraints with break activities. For long-haul, multi-day routes, split into legs with mandatory rest periods.

**Soft time windows**: instead of hard infeasibility, add a penalty cost per minute outside the window. Useful for VRPTW where some lateness is acceptable at a cost. Implement via `Dimension.SetSoftUpperBound(index, soft_max, penalty_per_unit)`.

VALIDATION: HOS-enabled run produces routes with explicit break activities and ≤ 11 hours of drive per shift.

============================================================
=== PHASE 5: OUTPUT (GeoJSON, KPIs, TBT) ===
============================================================

Generate `output.py` producing three artifacts:

**1. routes.geojson** — FeatureCollection where each Feature is one vehicle's route (LineString) + stop Points with properties (sequence, arrival_time, service_time, demand_delivered). Renderable in Mapbox GL JS, Leaflet, kepler.gl.

**2. kpi_report.md**:

```
Total routes:           N
Total stops:            M
Total distance:         X km (avg per route: Y km)
Total duration:         X hr (avg per route: Y hr)
Vehicle utilization:    (sum of capacity used) / (sum of capacity available) = X%
On-time stops:          N/M = X%
Avg stops per route:    X
Cost estimate:          $X (at $Y/km)
```

**3. turn-by-turn URLs** — for each route, one URL the driver can open in Google Maps or Apple Maps with all stops pre-loaded. Mapbox Directions API for production navigation.

VALIDATION: GeoJSON validates against geojson.io. KPI numbers reconcile (sum of route distances = total).

============================================================
=== PHASE 6: DISPATCH LOOP ===
============================================================

For ops teams running this daily, generate a `dispatch.py` CLI:

```
python -m src.dispatch \
  --stops today.csv \
  --vehicles fleet.csv \
  --depots depots.csv \
  --time-limit 120 \
  --output runs/$(date +%F)/
```

Pipeline:

1. Pull stops from order DB (or accept CSV).
2. Build distance matrix (use cache).
3. Solve VRP.
4. Output routes.
5. Notify drivers (SMS / Slack / Mobile app push).
6. Track in-progress vs solved on dashboard.

VALIDATION: Full pipeline runs end-to-end in < 5 minutes for 200 stops × 10 vehicles.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: Matrix + solver + HOS + GeoJSON + KPI all delivered?
- **Robust**: Handles infeasibility cleanly? Falls back to Haversine if API fails? Soft windows working?
- **Clean**: Tested against OR-Tools example + Solomon benchmark?
- **Ops-credible**: Would a fleet ops manager accept the GeoJSON + KPI report as a usable daily plan?

Common gap: ignoring service time at each stop → routes time out 30 min late. Verify service_time is in the time callback.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/route-optimizer/LEARNINGS.md`:

## <YYYY-MM-DD> — <variant, stop count, fleet size>

- **What worked:**
- **What was awkward:**
- **Suggested patch:**
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never silently solve with Haversine and ship to dispatch. Real road networks are 20-50% longer.
- Never ignore HOS for routes > 8 hours. FMCSA violations are $2-16k per occurrence.
- Never return empty / no solution without a reason. Surface "infeasible: capacity exceeded by N" so the user can fix inputs.
- Never solve with time_limit < 10s for > 100 stops. The first-solution heuristic alone produces 20%+ worse routes than guided local search at 30-60s.
- Always validate against a known benchmark before declaring the model correct.
