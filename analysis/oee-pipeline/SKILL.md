---
name: oee-pipeline
description: "Generate a production-grade OEE (Overall Equipment Effectiveness) measurement pipeline for a manufacturing line — data ingestion from MQTT/OPC-UA/Modbus/CSV, A×P×Q calculation engine, Six Big Losses categorizer, MTBF/MTTR/TEEP metrics, Grafana or Streamlit dashboard."
version: "1.0.1"
category: analysis
platforms:
  - CLAUDE_CODE
---

# OEE Pipeline Generator

You generate a complete, production-grade Overall Equipment Effectiveness measurement pipeline for a manufacturing line. The output is real code (Python or Node + Grafana/Streamlit), not pseudocode or chat advice.

OEE = Availability × Performance × Quality. World-class is ~85%. Most plants run 40-60%. The gap is almost always invisible because nobody is measuring correctly. Your job is to make it measurable in a few hours of work.

============================================================
=== PRE-FLIGHT ===
============================================================

Before generating any code, gather and verify:

- [ ] **Data source identified.** What is the source of truth for production counts and machine state?
  - MQTT broker (most common in Industry 4.0 deployments — Sparkplug B preferred)
  - OPC UA endpoint (typical for greenfield brownfield with newer PLCs)
  - Modbus TCP/RTU (legacy PLCs — Allen-Bradley, Siemens S7, Mitsubishi)
  - Direct PLC tag read (Rockwell pylogix, Siemens snap7, Beckhoff ADS)
  - CSV / SQL export from existing MES (Ignition, Wonderware, Rockwell FactoryTalk)
  - Manual entry (last resort — generate web form scaffold)
- [ ] **Cycle time / planned production rate known.** OEE Performance = (Total Count × Ideal Cycle Time) / Run Time. Without ideal cycle time, you cannot compute Performance. If unknown, prompt the user or assume the published rate from the OEM datasheet.
- [ ] **Shift schedule defined.** Planned production time vs scheduled downtime (lunch, meetings, planned PM) must be distinguishable.
- [ ] **Reject/scrap counting available.** Quality = Good Count / Total Count. If only Total is available, generate a stub that flags this as a known limitation.
- [ ] **Output language chosen.** Default Python (best ecosystem for industrial data — pandas, numpy_financial, pymodbus, asyncua, paho-mqtt). Use Node if the user has a Node-first stack.

Recovery if anything is missing:

- Generate a stub data source adapter with mock data so the rest of the pipeline can be tested in isolation.
- Mark the stub clearly: `# TODO: replace with real <protocol> connection — see references/connectors.md`.
- Do NOT halt the entire skill — output a working scaffold with a known gap, not nothing.

============================================================
=== PHASE 1: SCAFFOLD THE PROJECT ===
============================================================

Generate this layout in the current working directory (or a subfolder if the user specifies one):

```
oee/
├── README.md                    # Quickstart, formulas, deployment notes
├── pyproject.toml               # or package.json if Node
├── docker-compose.yml           # Local stack: broker + Grafana + InfluxDB
├── src/
│   ├── ingest/
│   │   ├── mqtt_source.py       # paho-mqtt + Sparkplug B decoder
│   │   ├── opcua_source.py      # asyncua subscription
│   │   ├── modbus_source.py     # pymodbus TCP/RTU
│   │   └── mock_source.py       # for testing without hardware
│   ├── oee/
│   │   ├── calc.py              # core A×P×Q formulas
│   │   ├── six_big_losses.py    # downtime categorizer
│   │   └── metrics.py           # MTBF, MTTR, TEEP, NEE
│   ├── storage/
│   │   └── influx_writer.py     # InfluxDB or TimescaleDB writer
│   └── dashboard/
│       └── grafana_dashboard.json
└── tests/
    └── test_oee_calc.py         # validates formulas against published examples
```

VALIDATION: Every directory exists. Every file has at least a docstring and one runnable function. Tests pass against the published OEE example: A=0.80, P=0.85, Q=0.95 → OEE=0.6460.

FALLBACK: If the user's existing project structure is incompatible (Django app, Flask, etc.), embed the OEE module as a single package without forcing the folder layout.

============================================================
=== PHASE 2: OEE CALCULATION ENGINE ===
============================================================

Generate `src/oee/calc.py` with the exact formulas:

```python
# Availability = Run Time / Planned Production Time
# Planned Production Time = Shift Length - Planned Stops
# Run Time = Planned Production Time - Unplanned Stops

# Performance = (Ideal Cycle Time × Total Count) / Run Time
# Equivalent: Performance = (Total Count / Run Time) / Ideal Run Rate

# Quality = Good Count / Total Count

# OEE = Availability × Performance × Quality
# TEEP = OEE × Utilization (Utilization = Planned Production Time / All Time)
# NEE  = Availability_uptime × Performance × Quality (excludes planned downtime)
```

Edge cases the engine MUST handle:

- **Microstops** (< 5 min) → classified as Performance loss, NOT Availability loss (industry convention).
- **Speed loss** → Performance < 1.0 even with no stops; surface as separate metric.
- **Startup/changeover rejects** → categorized separately in Quality (Six Big Losses #5).
- **Performance > 100%** → clamp to 1.0 AND emit warning (ideal cycle time may be set too conservatively).
- **Zero planned production time** → return None, do NOT divide-by-zero.

Cite the formulas inline using a reference comment so future maintainers can audit:

```python
# Source: ISO 22400-2:2014 Key Performance Indicators for Manufacturing Operations Management
```

VALIDATION: Unit tests in `tests/test_oee_calc.py` cover: known-good values, divide-by-zero, P>1.0 clamp, partial shift, all-scrap output. All tests must pass.

FALLBACK: If a formula edge case is ambiguous (e.g., how to handle a machine running during a planned stop), default to the ISO 22400-2 interpretation and add a TODO comment explaining the assumption.

============================================================
=== PHASE 3: SIX BIG LOSSES CATEGORIZER ===
============================================================

Generate `src/oee/six_big_losses.py` that classifies downtime events into the canonical six categories:

| #   | Loss Category                  | OEE Bucket   | Detection Rule (default)                         |
| --- | ------------------------------ | ------------ | ------------------------------------------------ |
| 1   | Breakdowns / Equipment failure | Availability | unplanned stop > 5 min, fault code present       |
| 2   | Setup & Adjustments            | Availability | stop tagged "changeover" or between product runs |
| 3   | Small Stops / Idling           | Performance  | stop 0–5 min, no operator intervention           |
| 4   | Reduced Speed                  | Performance  | running but actual_rate < ideal_rate             |
| 5   | Startup Rejects                | Quality      | scrap within first N units after run start       |
| 6   | Production Rejects             | Quality      | scrap during steady-state production             |

The categorizer takes a stream of state events `(timestamp, state, duration, fault_code, product)` and emits classified loss events. Output schema must be JSON-serializable so it flows into the dashboard without ETL.

VALIDATION: Run the categorizer against a synthetic 8-hour shift in tests; verify that the six categories sum to the total loss within rounding.

FALLBACK: If fault codes are not available, classify all unplanned stops > 5 min as Breakdowns and emit a "fault_code_missing" warning so the user knows the granularity gap.

============================================================
=== PHASE 4: DATA INGESTION ADAPTER ===
============================================================

Generate the ingestion adapter matching the user's data source. Each adapter MUST:

1. Externalize credentials via environment variables — never hardcode.
2. Use TLS / mutual auth where the protocol supports it (Sparkplug B + TLS, OPC UA with X.509).
3. Handle reconnect with exponential backoff (start 1s, cap 60s).
4. Emit a canonical event schema regardless of source protocol:
   ```json
   {
     "ts": "ISO8601",
     "asset_id": "line-1",
     "metric": "good_count",
     "value": 1247,
     "quality": "GOOD"
   }
   ```

**MQTT Sparkplug B specifics**:

- Subscribe to `spBv1.0/{group}/DDATA/{edge_node}/{device}`.
- Decode protobuf payload (sparkplug_b.proto — include a copy in `vendor/`).
- Handle NBIRTH/DBIRTH to learn the metric schema before processing DDATA.

**OPC UA specifics**:

- Use `asyncua` (Python) — modern, asyncio-native, maintained.
- Subscribe to changes (not poll). Set publishing interval to match the desired sample rate.
- Browse the address space at startup, persist the discovered NodeIds to `config/opcua_nodes.yaml`.

**Modbus specifics**:

- Use `pymodbus`. Register maps live in `config/modbus_map.yaml`.
- Convert raw 16-bit registers to engineering units via the configured scale/offset.

VALIDATION: Adapter connects to a local broker (run via docker-compose) and emits at least 10 sample events in `python -m src.ingest.<adapter> --test` mode.

FALLBACK: If the protocol-specific library is unavailable in the user's environment, generate `mock_source.py` that replays a recorded CSV — pipeline still demonstrable end-to-end.

============================================================
=== PHASE 5: DASHBOARD ===
============================================================

Generate `src/dashboard/grafana_dashboard.json` (preferred) OR a Streamlit app at `src/dashboard/app.py`.

The dashboard MUST include:

1. **Big-number OEE** for the current shift (large, color-coded: red < 60%, yellow 60-85%, green > 85%).
2. **A / P / Q breakdown** (three stacked single-stats — shows WHERE the loss is).
3. **Six Big Losses Pareto chart** (descending bar — shows WHY).
4. **Hourly OEE trend** (last 24h line chart).
5. **Top 10 downtime events** (table — duration, reason, asset).
6. **MTBF / MTTR / TEEP** trio (secondary metrics).

Grafana panel queries must use the canonical event schema from Phase 4 so the dashboard works without per-deployment query editing.

VALIDATION: Import the JSON into a fresh Grafana instance (Grafana ≥ 10) and confirm all 6 panels render without errors against the mock data source.

FALLBACK: If Grafana setup is too heavy for the user, generate Streamlit (single `streamlit run app.py`).

============================================================
=== PHASE 6: README & DEPLOYMENT NOTES ===
============================================================

Write `README.md` with:

- One-paragraph summary of what the pipeline does.
- Quickstart: `docker-compose up && python -m src.ingest.mock_source && open http://localhost:3000`.
- Formula reference table (so non-engineers can audit calculations).
- How to swap the mock source for the real PLC/MQTT/OPC-UA source.
- Industry context: "Deploy OEE first as foundation. Layer predictive maintenance as a 12-24 month follow-on. ROI for OEE alone is typically 9-18 months." [cite: 2026 TeepTrak deployment guide]
- Known limitations (if any from PRE-FLIGHT gaps).

VALIDATION: README quickstart actually works on a fresh machine.

============================================================
=== SELF-REVIEW ===
============================================================

Score each dimension 1–5:

- **Complete**: Does the pipeline ingest real or simulated data, compute OEE correctly per ISO 22400-2, categorize the Six Big Losses, and render a usable dashboard?
- **Robust**: Does the calc handle microstops, divide-by-zero, P>1.0 clamp, partial shifts? Does the ingestion reconnect on failure?
- **Clean**: Is the code formatted (black/ruff for Python), typed (mypy/pyright clean), and free of unused stubs?
- **Industry-credible**: Would a controls engineer / continuous improvement engineer recognize the terminology and formulas as correct? (This is the killer dimension — wrong formulas destroy trust instantly.)

If any < 4:

- Identify the specific gap. Most common gap: Performance formula uses average cycle time instead of ideal cycle time → silently inflates OEE. Fix and re-test.
- If a gap is genuinely unfixable in this run (e.g., the user can't provide ideal cycle time), note it in the README under "Known Limitations" with a clear remediation path.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

After completing, append to `~/.claude/skills/oee-pipeline/LEARNINGS.md`:

## <YYYY-MM-DD> — <site/line/protocol context, e.g., "CNC mill, Sparkplug B">

- **What worked:** <specific approach — formula reference, dashboard layout, adapter pattern>
- **What was awkward:** <step that needed retry — e.g., "user couldn't provide ideal cycle time, defaulted to OEM spec">
- **Suggested patch:** <concrete improvement — e.g., "add pre-flight question for whether MES data already exists">
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never invent formula variants. Use ISO 22400-2 conventions or cite an explicit alternative.
- Never hardcode credentials or broker URLs. Externalize via env vars.
- Never claim a number you didn't calculate from real or mock data. The dashboard MUST be backed by the calc engine, not by static placeholders.
- Never skip the Six Big Losses categorizer. Total OEE without the loss breakdown is the most common failure mode — it tells management things are bad without telling engineers what to fix.
- If the user has an existing OEE platform, do NOT regenerate the pipeline — recommend a connector instead.
