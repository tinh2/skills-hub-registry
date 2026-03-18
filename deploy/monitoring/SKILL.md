---
name: monitoring
description: "Set up application observability with Prometheus, Grafana, Datadog, or CloudWatch — instrument metrics endpoints, configure Golden Signal dashboards, define alert rules with burn-rate SLOs, and add structured logging"
version: "2.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- A monitoring stack: `prometheus`, `datadog`, `cloudwatch`, `newrelic`, `grafana`
- `--instrument` — add application-level metrics instrumentation to source code
- `--alerts-only` — generate alerting rules without full dashboard setup
- `--slo` — define and configure SLO/SLI targets with burn-rate alerts
- A specific focus: `latency`, `errors`, `traffic`, `saturation`
- If no arguments, auto-detect existing monitoring and extend it, or default to Prometheus + Grafana

============================================================
PHASE 1 — INFRASTRUCTURE DETECTION
============================================================

Scan for existing monitoring setup:

**Prometheus ecosystem**:
- `prometheus.yml`, `prometheus/` directory
- `alertmanager.yml`, `alertmanager/` directory
- Grafana dashboards: `grafana/`, `dashboards/`, `*.json` with `"panels"` key
- Docker compose services named `prometheus`, `grafana`, `alertmanager`

**Cloud-native**:
- AWS: CloudWatch references in Terraform, `aws_cloudwatch_*` resources
- GCP: Cloud Monitoring, `google_monitoring_*` resources
- Azure: Application Insights, `azurerm_monitor_*` resources

**Third-party**:
- Datadog: `datadog.yaml`, `DD_*` environment variables, `datadog-agent` in compose
- New Relic: `.newrelic.yml`, `NEW_RELIC_*` env vars, `newrelic` in dependencies
- Sentry: `sentry.properties`, `SENTRY_DSN` in env, `@sentry/*` in deps

**Application stack**:
- Node.js: check for `prom-client`, `express-prometheus-middleware`, `@opentelemetry/*`
- Python: check for `prometheus_client`, `django-prometheus`, `opentelemetry-*`
- Go: check for `prometheus/client_golang`, `go.opentelemetry.io`
- Java: check for Micrometer, Spring Actuator

**Infrastructure**:
- Kubernetes: check for ServiceMonitor CRDs, Prometheus Operator
- Docker: check compose services for metrics endpoints
- Serverless: check for X-Ray, CloudWatch Logs

============================================================
PHASE 2 — METRICS DESIGN (Golden Signals)
============================================================

Design metrics based on the Four Golden Signals:

**1. Latency** — time to service a request
- `http_request_duration_seconds` (histogram)
- Buckets: 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10
- Track by: method, route, status_code
- Report P50, P90, P95, P99 percentiles

**2. Traffic** — demand on the system
- `http_requests_total` (counter)
- Track by: method, route, status_code
- Report requests per second

**3. Errors** — rate of failed requests
- `http_errors_total` (counter) — 5xx responses
- `http_client_errors_total` (counter) — 4xx responses
- Error rate = errors / total requests

**4. Saturation** — how full the service is
- CPU utilization, memory usage
- Connection pool usage (database, Redis)
- Queue depth (if applicable)
- Event loop lag (Node.js)
- GC pause time (Java, Go)

============================================================
PHASE 3 — APPLICATION INSTRUMENTATION (if --instrument)
============================================================

Add metrics middleware to the application:

**Node.js (Express/Fastify)**:
- Install `prom-client` dependency
- Create metrics middleware tracking `http_request_duration_seconds` and `http_requests_total`
- Add `/metrics` endpoint exposing Prometheus format
- Add default Node.js process metrics (memory, CPU, event loop)

**Python (FastAPI/Django)**:
- Install `prometheus_client` or `prometheus-fastapi-instrumentator`
- Expose `/metrics` endpoint
- Add middleware for request duration tracking

**Go**:
- Add `promhttp.Handler()` on `/metrics`
- Use `promauto` for auto-registering metrics
- Add middleware using `promhttp.InstrumentHandlerDuration`

Also add to the application:
- **Health endpoints**: `/health` (liveness), `/ready` (readiness)
- **Version endpoint**: `/version` returning app version and build info
- **Structured logging**: ensure logs are JSON-formatted with correlation IDs

============================================================
PHASE 4 — PROMETHEUS + GRAFANA SETUP
============================================================

If using Prometheus stack, generate:

**`monitoring/prometheus/prometheus.yml`**:
- Global scrape interval: 15s, evaluation interval: 15s
- Rule files referencing `alerts/*.yml`
- Scrape config targeting `app:{port}` on `/metrics` with 10s interval

**`monitoring/prometheus/alerts/app.yml`**:
Alert rules (all with `for` duration to prevent flapping):
- `HighErrorRate`: `rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.01` for 5m (critical)
- `HighLatency`: P99 > 2s for 5m (warning)
- `HighMemoryUsage`: > 512MB for 10m (warning)
- `HighCPU`: > 80% for 10m (warning)
- `DiskUsageHigh`: > 80% for 5m (warning)
- `ServiceDown`: `up == 0` for 1m (critical)

**`monitoring/grafana/dashboards/app.json`**:
Grafana dashboard JSON with panels:
1. Request Rate (by status code)
2. Error Rate (percentage over time)
3. Latency Distribution (heatmap)
4. P50/P90/P99 Latency (time series)
5. Active Connections (gauge)
6. Memory Usage (time series)
7. CPU Usage (time series)
8. Saturation (connection pool, queue depth)

**`monitoring/grafana/provisioning/dashboards.yml`**: File-based dashboard provisioning.

**Docker Compose** (`monitoring/docker-compose.monitoring.yml`):
- Prometheus v2.51+ with 30d retention
- Grafana 10.4+ with provisioned dashboards and datasources
- Alertmanager v0.27+ for notification routing
- All with proper volume mounts and health checks

============================================================
PHASE 5 — CLOUD MONITORING (if Datadog/CloudWatch/New Relic)
============================================================

**Datadog**:
- Generate `datadog.yaml` agent config
- Add `dd-trace` to application dependencies
- Configure APM, log collection, custom metrics
- Generate monitor definitions in JSON

**CloudWatch**:
- Generate Terraform for CloudWatch alarms, dashboards, log groups
- Configure metric filters on log groups
- Set up SNS topics for alarm notifications

**New Relic**:
- Generate `newrelic.yml` configuration
- Add agent to application dependencies
- Configure custom dashboards via NR API (NRQL queries)

============================================================
PHASE 6 — SLO CONFIGURATION (if --slo)
============================================================

Define SLOs based on service type:

- **Availability SLO**: 99.9% uptime (43.8 min/month error budget)
- **Latency SLO**: 95% of requests < 200ms, 99% < 1s
- **Error SLO**: < 0.1% error rate

Generate burn rate alerts:
- Fast burn (2%/hour): page immediately — requires human attention within minutes
- Slow burn (5%/day): ticket within 1 hour — investigate during business hours


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available

============================================================
OUTPUT
============================================================

```
## Monitoring Setup Complete

### Stack: {Prometheus + Grafana / Datadog / CloudWatch / New Relic}

### Files Created
{list of all generated files with one-line descriptions}

### Metrics Endpoints
- Application: http://localhost:{port}/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)
- Alertmanager: http://localhost:9093

### Alert Rules
| Alert | Condition | Severity |
|-------|-----------|----------|
| HighErrorRate | >1% for 5m | critical |
| HighLatency | P99 >2s for 5m | warning |
| HighMemory | >512MB for 10m | warning |
| DiskUsageHigh | >80% for 5m | warning |
| ServiceDown | down for 1m | critical |

### Dashboard Panels
{list of dashboard panels with their metric queries}
```

============================================================
NEXT STEPS
============================================================

1. Start monitoring stack: `docker compose -f monitoring/docker-compose.monitoring.yml up -d`
2. Verify metrics are being scraped: check Prometheus targets page at :9090/targets
3. Configure alerting notification channels (Slack, PagerDuty, email) in Alertmanager
4. Add application-specific custom metrics for business KPIs
5. Set up log aggregation if not already configured (Loki, ELK)
6. Review alert thresholds after 1 week of baseline data


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /monitoring — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT set alert thresholds too aggressively — avoid alert fatigue
- Do NOT expose Prometheus/Grafana ports publicly without authentication
- Do NOT store Grafana admin passwords in plain text in committed files
- Do NOT use `rate()` on gauges — use `rate()` only on counters and histograms
- Do NOT create alerts without `for` duration — always require sustained condition
- Do NOT use high-cardinality labels (user IDs, request IDs) in Prometheus metrics
- Do NOT scrape more frequently than every 10s without good reason
- Do NOT overwrite existing monitoring configs — extend them
- Do NOT add instrumentation that significantly impacts application performance
