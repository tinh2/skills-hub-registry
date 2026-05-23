---
name: iiot-bridge
description: Generate a production-grade Industrial IoT protocol bridge — OPC UA ↔ MQTT Sparkplug B, Modbus → MQTT, or direct PLC (Rockwell/Siemens/Beckhoff) → cloud (AWS IoT Core / Azure IoT Hub / GCP IoT / self-hosted HiveMQ). Output is real code with TLS / X.509 mutual auth, Sparkplug B lifecycle (NBIRTH/DBIRTH/DDATA/DDEATH), canonical topic schema, store-and-forward buffering for network drops, and a docker-compose test rig that runs end-to-end locally. TRIGGER on phrases like "OPC UA to MQTT", "Sparkplug B", "Modbus bridge", "industrial protocol bridge", "PLC to cloud", "IIoT gateway", "edge gateway", "device twin", "unified namespace", "UNS broker", "Ignition tag bridge", or any user describing a need to get plant-floor data into a cloud platform or unified namespace. Also trigger for OT/IT data convergence projects. The bridge is the single highest-friction integration in industrial software — this skill collapses 4-8 weeks of bespoke work into a generated scaffold.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

# Industrial IoT Bridge Generator

You generate a production-grade protocol bridge that moves plant-floor data into a modern broker / cloud platform with industrial standards (Sparkplug B, OPC UA, MQTT 5.0) and security (TLS, X.509 mutual auth, RBAC) built in from the start.

OT/IT integration is the #1 friction point in Industry 4.0 deployments — multiple SCADA hosts each requiring request/response gateways, manual config that grows linearly with device count. This skill outputs a publish-subscribe bridge that breaks that pattern.

============================================================
=== PRE-FLIGHT ===
============================================================

Gather and verify before generating:

- [ ] **Source protocol identified.**
  - OPC UA (modern PLCs: Siemens S7-1500, Beckhoff TwinCAT, Rockwell ControlLogix via Kepware)
  - Modbus TCP / Modbus RTU (legacy or simple devices)
  - Direct PLC: Rockwell EtherNet/IP (`pylogix` / `pycomm3`), Siemens S7 (`snap7`), Beckhoff ADS (`pyads`)
  - Ignition Tag Provider (use Ignition's MQTT Transmission module — usually a config job, not code)
- [ ] **Destination broker / cloud identified.**
  - HiveMQ (self-hosted, best Sparkplug B support)
  - AWS IoT Core (CloudFormation/CDK generation possible)
  - Azure IoT Hub (Device Provisioning Service patterns)
  - GCP IoT Core (deprecated as of 2023 — warn user; suggest HiveMQ on GKE)
  - Bare Mosquitto / EMQX (low-cost dev/test only — call out lack of Sparkplug B native support if used in prod)
- [ ] **Network topology known.** Is the bridge running ON the edge gateway (preferred), in a DMZ, or in the cloud? This drives TLS/cert strategy.
- [ ] **Tag/point count.** Under 100 = pure publish on change. Over 10,000 = batching + compression matter.
- [ ] **Security posture.** Production MUST use TLS + X.509 mutual auth. Dev/test can use username/password but the generated code MUST default to mTLS with a `--insecure` flag for explicit opt-out.

Recovery:

- If destination is undecided, generate for HiveMQ self-hosted (best Sparkplug B, easiest to migrate later).
- If protocols are mixed, scaffold a multi-source adapter pattern (each source = a separate driver module, common output schema).
- Never generate without TLS scaffolding — the cost of retrofitting security is the worst kind of tech debt.

============================================================
=== PHASE 1: TOPIC SCHEMA & NAMESPACE DESIGN ===
============================================================

Generate the topic schema based on **Sparkplug B** (the only widely-accepted industrial MQTT topic standard) OR the **ISA-95 / Unified Namespace** pattern if the user is going broader than Sparkplug.

**Sparkplug B topic format** (Eclipse Tahu spec):

```
spBv1.0/{group_id}/{message_type}/{edge_node_id}/{device_id}

Message types:
  NBIRTH — Edge node online (publishes ALL metric definitions)
  NDATA  — Edge node metric value update
  NDEATH — Edge node going offline (sent as LWT)
  DBIRTH — Device online (under an edge node)
  DDATA  — Device metric value update
  DDEATH — Device offline
  NCMD   — Inbound command to edge node
  DCMD   — Inbound command to device
```

**ISA-95 / Unified Namespace pattern** (for non-Sparkplug deployments):

```
{enterprise}/{site}/{area}/{line}/{cell}/{asset}/{metric}
e.g., acme/austin-plant/packaging/line-3/filler-2/torque

Reserve subtrees:
  .../events    — discrete state changes (Start, Stop, Alarm)
  .../alarms    — ISA-18.2 alarms
  .../commands  — write-back operations
```

Generate `topics.yaml` documenting the chosen schema. The schema is the contract for everything downstream — get it right at the start.

VALIDATION: All generated topics validate against the Sparkplug B spec OR the ISA-95 pattern, no special characters, no wildcards in publishers, ≤ 5 levels deep.

FALLBACK: If the user has an existing topic schema (legacy MQTT deployment), generate a translator layer rather than forcing migration.

============================================================
=== PHASE 2: BRIDGE CORE WITH SPARKPLUG LIFECYCLE ===
============================================================

Generate the bridge code. Default to Python (best industrial library support). Use Node only if user requests it.

Required dependencies:

- `paho-mqtt` (MQTT 5.0 client)
- `tahu-python` or hand-rolled Sparkplug B protobuf (vendor sparkplug_b.proto)
- `asyncua` for OPC UA
- `pymodbus` for Modbus
- `pylogix` / `pycomm3` / `snap7` / `pyads` for direct PLC

**Sparkplug B lifecycle implementation is non-negotiable**:

```python
# On startup:
1. Connect to broker with LWT = NDEATH topic (so broker auto-publishes our death)
2. Publish NBIRTH with ALL metric definitions and current values + bdSeq counter
3. For each device: publish DBIRTH with that device's metrics
4. Then start publishing DDATA on change

# On metric value change:
1. Increment seq number (0-255, wraps)
2. Publish DDATA with only the changed metrics (publish-on-change, NOT poll)

# On graceful shutdown:
1. Publish DDEATH for each device
2. Publish NDEATH for the edge node
3. Disconnect cleanly

# On broker reconnect:
1. Repeat NBIRTH/DBIRTH (consumers need fresh schema after death/birth)
2. Reset seq counter
3. Increment bdSeq (birth/death sequence — top-level continuity)
```

Common bugs to PREVENT by construction:

- Missing NBIRTH after reconnect → consumer treats edge node as stale forever.
- Seq counter not wrapping at 256 → spec violation, some consumers drop messages.
- Forgetting LWT → ungraceful network drop leaves devices appearing alive.
- bdSeq not in NDEATH payload → consumer can't correlate death to specific birth.

VALIDATION: Run the bridge against a local HiveMQ + Sparkplug B Inspector (or Chariot Edge); confirm NBIRTH appears, DDATA flows, and DDEATH publishes on graceful shutdown. Pull the network cable and verify NDEATH appears via LWT.

FALLBACK: If Sparkplug B is overkill for the use case, generate plain MQTT with the ISA-95 topic schema — but emit a warning that interop with industrial consumers (Ignition, HiveMQ Distributed Tracing) will be limited.

============================================================
=== PHASE 3: SECURITY & CERTIFICATE PROVISIONING ===
============================================================

Generate the security stack. Defaults that ship to production:

- **TLS 1.2+** on all broker connections (port 8883, not 1883).
- **X.509 mutual auth** — client cert per edge node, signed by an issuing CA.
- **Certificate rotation** scaffold using a 90-day validity and 30-day-before-expiry rotation hook.
- **RBAC at the broker** — generate HiveMQ / EMQX ACL config with least-privilege publish/subscribe per edge node.
- **Secrets** — never in code. Use env vars or, for AWS, the cert is fetched from IoT Core's provisioning flow.

Generate `security/`:

```
security/
├── ca/
│   ├── generate_ca.sh           # one-time root CA generation
│   └── sign_client.sh           # per-edge-node cert signing
├── certs/
│   └── .gitignore               # certs NEVER committed
├── broker_acl.yaml              # HiveMQ/EMQX ACL
└── README.md                    # rotation runbook
```

VALIDATION: Bridge fails closed if cert is missing or expired (does NOT silently fall back to plaintext). ACL prevents an edge node from publishing under another node's topic prefix.

FALLBACK: For air-gapped OT networks with no PKI, generate a PSK-based config — but mark explicitly as "lab/PoC only".

============================================================
=== PHASE 4: STORE-AND-FORWARD BUFFERING ===
============================================================

OT networks drop. Bridges that don't buffer lose data. Generate a persistent queue (SQLite or RocksDB) that:

1. Writes every outbound message to disk before publishing.
2. On broker disconnect, accumulates messages.
3. On reconnect, drains the queue in order, respecting the original timestamps (not the replay time).
4. Has a configurable retention cap (default 7 days) and overflow policy (drop-oldest with a logged warning).

This is the difference between a hobby script and a production bridge.

VALIDATION: Test by killing the broker for 60 seconds and confirming all messages arrive in order after reconnect with original timestamps preserved.

============================================================
=== PHASE 5: DOCKER-COMPOSE TEST RIG ===
============================================================

Generate `docker-compose.yml` so the entire stack runs locally for testing:

```yaml
services:
  hivemq:
    image: hivemq/hivemq4:latest
    ports: ["1883:1883", "8883:8883", "8080:8080"]
    volumes: [./security/certs:/opt/hivemq/conf/certs:ro]

  modbus-sim: # mock PLC for testing
    image: oitc/modbus-server:latest

  opcua-sim:
    image: opensimroot/opcua-server:latest

  sparkplug-inspector:
    image: cirruslink/sparkplug-inspector:latest
    ports: ["3000:3000"]

  bridge:
    build: .
    environment:
      - MQTT_HOST=hivemq
      - SOURCE_TYPE=opcua
      - SOURCE_ENDPOINT=opc.tcp://opcua-sim:4840
```

VALIDATION: `docker-compose up` brings up the full stack; Sparkplug Inspector at localhost:3000 shows the bridge's NBIRTH/DDATA flow within 30 seconds.

============================================================
=== PHASE 6: OBSERVABILITY ===
============================================================

Generate basic observability so failures don't hide:

- **Metrics endpoint** (Prometheus `/metrics`): messages_published_total, broker_reconnects_total, queue_depth, cert_expiry_days_remaining.
- **Structured logging** (JSON) with consistent fields: ts, level, asset_id, event_type, msg_id.
- **Healthcheck endpoint** (`/healthz`) returning 200 only if broker is connected AND source protocol session is active.

VALIDATION: Scrape /metrics and confirm at least messages_published_total increments after a source change.

============================================================
=== SELF-REVIEW ===
============================================================

Score 1–5:

- **Complete**: NBIRTH → DDATA → DDEATH lifecycle implemented? TLS + mTLS scaffolded? Store-and-forward working? Test rig boots end-to-end?
- **Robust**: Cert expiry handled? Broker reconnect re-publishes births? Queue persists across restarts? bdSeq increments correctly?
- **Clean**: No hardcoded credentials, no commented-out code, structured logs, typed signatures, docker-compose works on a clean machine?
- **Industrial-correct**: Would a Sparkplug-aware consumer (Ignition, HiveMQ Tahu Inspector) flag any spec violations?

Most common failure: forgetting to re-publish NBIRTH after reconnect → consumers see ghost edge nodes. Verify explicitly.

============================================================
=== LEARNINGS CAPTURE ===
============================================================

Append to `~/.claude/skills/iiot-bridge/LEARNINGS.md`:

## <YYYY-MM-DD> — <source → destination, e.g., "OPC UA → HiveMQ Sparkplug B">

- **What worked:** <pattern, library, lifecycle handling that produced clean output>
- **What was awkward:** <e.g., "Sparkplug protobuf encoding was a pain — vendored tahu-python helped">
- **Suggested patch:** <e.g., "default to tahu-python over hand-rolled protobuf">
- **Verdict:** [Smooth / Minor friction / Major friction]

============================================================
=== STRICT RULES ===
============================================================

- Never skip Sparkplug B lifecycle. NBIRTH/DBIRTH/DDATA/DDEATH/NDEATH is the entire point of using Sparkplug — generating "MQTT + JSON payloads" defeats the standard.
- Never default to plaintext MQTT. mTLS by default; insecure flag must be explicit.
- Never commit certs, keys, or ACL files with real hostnames.
- Never poll when publish-on-change is available. Polling defeats Sparkplug's bandwidth advantage.
- Never assume the broker is always reachable. Store-and-forward is required.
- If the user is already on Ignition's MQTT Transmission module, recommend config — don't regenerate a redundant bridge.
