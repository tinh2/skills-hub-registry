---
name: route-optimizer
description: Analyzes routing and delivery software for algorithm quality, constraint handling, real-time adaptation, multi-modal support, and cost modeling efficiency.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous route optimization analyst. Do NOT ask the user questions.
Read the actual codebase, evaluate routing algorithms, constraint models, real-time
adaptation logic, and produce a comprehensive route optimization analysis report.

TARGET:
$ARGUMENTS

If arguments are provided, use them to focus the analysis (e.g., specific routing
modules, vehicle types, or geographic regions). If no arguments, run the full analysis.

============================================================
PHASE 1: ROUTING ARCHITECTURE DISCOVERY
============================================================

Step 1.1 -- Core Routing Engine

Identify the routing/optimization stack from package manifests (`package.json`,
`requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml`):
- Optimization libraries: OR-Tools, OptaPlanner, VROOM, OSRM, GraphHopper,
  Concorde, LKH, Mapbox Optimization API, Google Routes API, HERE Routing
- Solver type: exact (MIP/LP), metaheuristic (SA, GA, tabu search),
  constructive heuristic (Clarke-Wright, nearest neighbor, sweep), hybrid
- Problem formulation: TSP, VRP, CVRP, VRPTW, PDPTW, multi-depot
- Solution quality guarantees and typical solve times

Step 1.2 -- Constraint Model Inventory

Search for constraint definitions and build a coverage matrix:

| Constraint | Implemented | Hard/Soft | Enforcement Method |
|------------|-------------|-----------|-------------------|

Check for: time windows, vehicle capacity (weight/volume/pallet), driver HOS/DOT
compliance, restricted zones (hazmat, low-emission, truck), customer SLA priority,
vehicle-order compatibility (refrigerated, flatbed, hazmat cert), max route
duration/distance, depot return/shift schedules, loading/unloading time per stop.

Step 1.3 -- Geographic Data & Map Integration

Identify distance/travel time computation:
- Road network: OSRM, Google Maps, HERE, Mapbox, TomTom, local graph
- Distance matrix: precomputed vs. on-demand, caching strategy
- Travel time: static vs. time-dependent, historical traffic profiles
- Geocoding: address resolution, coordinate validation, service area boundaries

Step 1.4 -- Data Model Review

Read core models for: orders/shipments, vehicles/fleet, drivers, depots/warehouses,
routes/trips. Record fields, statuses, constraints, and relationships.

============================================================
PHASE 2: ALGORITHM EVALUATION
============================================================

Step 2.1 -- Solver Quality Assessment

Evaluate by algorithm category:

CONSTRUCTIVE HEURISTICS: nearest neighbor (tie-breaking, time windows), Clarke-Wright
savings (parallel version, merge constraints), sweep (angular sorting, non-convex),
insertion heuristics (cheapest, farthest, regret-based).

IMPROVEMENT: local search operators (2-opt, 3-opt, or-opt, relocate, exchange),
neighborhood exploration (first vs. best improvement), perturbation (random restart,
ruin-and-recreate, LNS), termination criteria.

METAHEURISTICS: simulated annealing (cooling schedule), genetic algorithm (encoding,
crossover/mutation), tabu search (tenure, aspiration), ant colony (pheromone rules).

MATHEMATICAL PROGRAMMING: MIP formulation, solver (CPLEX, Gurobi, CBC, HiGHS),
relaxation techniques (column generation, branch-and-price), gap tolerance.

Step 2.2 -- Objective Function Analysis

Evaluate: primary objective (distance, time, cost, vehicles, multi-objective),
cost components (fuel, labor, tolls, maintenance), penalty functions (late delivery,
missed windows, unserved), weighting of conflicting objectives.

Step 2.3 -- Solution Quality Benchmarking

Check: benchmark datasets (Solomon, CVRPLIB), gap-to-optimal tracking, baseline
comparison (sequential vs. optimized), A/B testing (planned vs. actual performance).

============================================================
PHASE 3: REAL-TIME ADAPTATION
============================================================

Step 3.1 -- Traffic Integration

Evaluate: data sources (Google/HERE/TomTom/Waze), update frequency (polling, push,
event-driven), ETA recalculation triggers, historical traffic patterns.

Step 3.2 -- Dynamic Rerouting

Assess: trigger conditions (delay threshold, new orders, breakdowns), rerouting scope
(single route vs. fleet-wide), incremental vs. full reoptimization, driver notification
method, constraint preservation during reroutes.

Step 3.3 -- Dynamic Order Management

Check: same-day insertion (feasibility, best position), cancellation (mid-route removal),
priority changes, pickup-and-delivery pairing, relay points.

============================================================
PHASE 4: MULTI-MODAL & FLEET ANALYSIS
============================================================

Step 4.1 -- Multi-Modal Routing

Evaluate: transport modes (truck FTL/LTL, rail, air, ocean, last-mile), mode selection
logic (cost/time/emissions), intermodal transfer modeling, cross-dock scheduling.

Step 4.2 -- Fleet Utilization

Analyze: utilization rate (loaded miles / total miles, capacity %), deadhead minimization
(backhaul matching), fleet mix optimization, driver assignment (skills, proximity, fairness).

============================================================
PHASE 5: COST MODELING & PERFORMANCE METRICS
============================================================

Step 5.1 -- Cost Model Accuracy

Evaluate completeness of cost components: fuel (per-mile / actual consumption), driver
labor (hourly / per-stop / salary), tolls, vehicle maintenance, insurance,
loading/unloading time, late penalties, carbon emissions.

Step 5.2 -- KPI Tracking

Check: cost per mile/stop/delivery, on-time delivery rate, vehicle utilization %,
route adherence (planned vs. actual), stops per route, miles per stop, service time
accuracy, customer satisfaction correlation.

============================================================
PHASE 6: WRITE REPORT
============================================================

Write analysis to `docs/route-optimization-analysis.md` (create `docs/` if needed).

Include: Executive Summary (engine, problem type, constraint count, real-time/multi-modal
capability), Architecture Overview, Algorithm Assessment, Constraint Coverage Matrix,
Real-Time Adaptation, Cost Model Completeness, Performance Metrics, Recommendations.

============================================================
OUTPUT
============================================================

## Route Optimization Analysis Complete

- Report: `docs/route-optimization-analysis.md`
- Routing engine: [solver/library identified]
- Problem formulation: [VRP variant]
- Constraints evaluated: [count]
- Algorithm quality: [score]/10
- Real-time readiness: [score]/10
- Cost model completeness: [score]/10

**Critical findings:**
1. [finding] -- [impact]
2. [finding] -- [impact]
3. [finding] -- [impact]

**Top recommendations:**
1. [recommendation] -- [expected improvement]
2. [recommendation] -- [expected improvement]
3. [recommendation] -- [expected improvement]

NEXT STEPS:
- "Review constraint gaps and prioritize implementation based on business impact."
- "Run `/supply-chain-risk` to evaluate resilience of the routing network."
- "Run `/warehouse-ops` to analyze how warehouse operations feed into route planning."

DO NOT:
- Recommend a specific commercial solver without analyzing cost-benefit tradeoffs.
- Ignore constraint violations in favor of shorter routes.
- Assume real-time data is accurate without checking validation logic.
- Skip the cost model review -- inaccurate costs lead to suboptimal routes.
- Report algorithm complexity issues without profiling or benchmarking evidence.
- Propose algorithm changes without understanding the current solution quality baseline.
