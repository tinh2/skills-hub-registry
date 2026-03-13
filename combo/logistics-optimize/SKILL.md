---
name: logistics-optimize
description: "Optimize and stress-test a logistics system end-to-end — chains route optimization, warehouse operations review, inventory demand forecasting, supply chain risk analysis, and peak-load testing. Use for delivery platforms, warehouse management systems, fleet routing, or supply chain software."
version: "1.0.0"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous logistics optimization agent. Do NOT ask the user questions.

This skill chains five skills in sequence for comprehensive logistics system analysis:
1. `/route-optimizer` -- Vehicle routing and delivery optimization analysis
2. `/warehouse-ops` -- Warehouse management and operations review
3. `/inventory-forecast` -- Inventory demand forecasting and replenishment analysis
4. `/supply-chain-risk` -- Supply chain risk identification and mitigation review
5. `/load-test` -- System stress testing under peak logistics load

INPUT: $ARGUMENTS
Pass the system name, specific logistics domain to focus on, or optimization objectives.

============================================================
PHASE 1: ROUTE OPTIMIZATION  (/route-optimizer)
============================================================

Follow the instructions defined in the `/route-optimizer` skill exactly.

Analyze vehicle routing and delivery optimization:
- Routing algorithm evaluation (VRP variants, TSP heuristics, or-tools, VROOM)
- Constraint handling: time windows, vehicle capacity, driver hours, road restrictions
- Real-time re-routing capability and traffic integration
- Multi-depot and multi-modal routing support
- Cost function analysis: distance, time, fuel, toll, emissions weighting
- Route optimization API performance and response time

Record identified bottlenecks and optimization gaps for cross-referencing
with subsequent phases.

============================================================
PHASE 2: WAREHOUSE OPERATIONS  (/warehouse-ops)
============================================================

Follow the instructions defined in the `/warehouse-ops` skill exactly.

Review warehouse management system implementation:
- Receiving, putaway, picking, packing, and shipping workflow logic
- Bin/location management and slotting optimization algorithms
- Pick path optimization (wave picking, zone picking, batch picking)
- Barcode/RFID integration and scan validation
- Labor management and task assignment logic
- Dock scheduling and appointment management
- Returns processing and reverse logistics workflow

IMPORTANT: Cross-reference warehouse throughput capacity with route
optimization from Phase 1. Flag mismatches where routing assumes
warehouse processing speed that the WMS cannot sustain.

============================================================
PHASE 3: INVENTORY FORECASTING  (/inventory-forecast)
============================================================

Follow the instructions defined in the `/inventory-forecast` skill exactly.

Analyze inventory demand forecasting and replenishment:
- Demand forecasting models (time-series, ML, causal models)
- Safety stock calculation methodology
- Reorder point and economic order quantity logic
- ABC/XYZ classification implementation
- Seasonal and promotional demand handling
- Multi-echelon inventory optimization (if applicable)
- Forecast accuracy metrics and monitoring

IMPORTANT: Verify inventory forecasts align with warehouse capacity
from Phase 2 and delivery schedules from Phase 1. Flag any forecasting
assumptions that conflict with operational constraints.

============================================================
PHASE 4: SUPPLY CHAIN RISK  (/supply-chain-risk)
============================================================

Follow the instructions defined in the `/supply-chain-risk` skill exactly.

Identify and evaluate supply chain risk management:
- Supplier concentration and single-source dependency analysis
- Lead time variability modeling and buffer strategies
- Disruption scenario planning (natural disaster, geopolitical, pandemic)
- Alternate supplier and routing contingency logic
- Demand surge handling and allocation algorithms
- Supply chain visibility and tracking integration
- Risk scoring and early warning system evaluation

IMPORTANT: Cross-reference risk scenarios with routing alternatives
from Phase 1, warehouse overflow handling from Phase 2, and safety
stock adequacy from Phase 3.

============================================================
PHASE 5: LOAD TESTING  (/load-test)
============================================================

Follow the instructions defined in the `/load-test` skill exactly.

Stress test the logistics system under peak conditions:
- Peak season load simulation (holiday, promotional periods)
- Order volume ramp-up: 10x, 50x, 100x normal throughput
- Concurrent routing optimization requests under high load
- Inventory update throughput during bulk receiving
- API response times for order tracking and status queries
- Database query performance for reporting and analytics

IMPORTANT: Target the specific APIs and services identified in Phases 1-4.
Use realistic payload sizes based on actual order and shipment data models.
Identify which logistics subsystem becomes the bottleneck under peak load.

============================================================
OUTPUT
============================================================

## Logistics System Optimization Complete

| Phase | Skill | Status | Details |
|-------|-------|--------|---------|
| 1 | /route-optimizer | PASS/FAIL | {N} routing gaps, {optimization potential} |
| 2 | /warehouse-ops | PASS/FAIL | {N} workflow issues, {throughput assessment} |
| 3 | /inventory-forecast | PASS/FAIL | {N} forecasting gaps, {accuracy assessment} |
| 4 | /supply-chain-risk | PASS/FAIL | {N} risk factors, {N} unmitigated risks |
| 5 | /load-test | PASS/FAIL | p95={N}ms, error rate={N}%, bottleneck={subsystem} |

**System health:** {OPTIMIZED / NEEDS IMPROVEMENT / CRITICAL GAPS}
**Peak readiness:** {READY / AT RISK / NOT READY}
**Top bottleneck:** {identified subsystem and constraint}

### Cross-Phase Findings
[Misalignments between logistics subsystems -- highest optimization impact]

### Optimization Priority
1. [Highest-impact improvements ordered by cost savings potential]
2. [...]

NEXT STEPS:
- Address cross-phase misalignments first (highest ROI)
- Run `/security-review` to audit logistics platform APIs and access controls
- Run `/monitoring` to set up alerting for logistics KPIs
- Run `/arch-review` to evaluate microservice architecture for logistics scale
- Implement load test fixes and re-run `/load-test` to verify improvements

DO NOT:
- Do NOT modify any routing algorithms, inventory parameters, or warehouse configurations -- this is an analysis pipeline.
- Do NOT access or display actual customer order data, shipping addresses, or supplier contracts.
- Do NOT execute load tests against production systems without explicit confirmation.
- Do NOT skip the load testing phase -- operational correctness without scalability verification is incomplete.
- Do NOT assume subsystem independence -- cross-phase findings are often the most impactful.
