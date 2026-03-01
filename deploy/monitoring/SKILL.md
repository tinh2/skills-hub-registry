---
name: monitoring
description: "Auto-detect infrastructure and set up observability with dashboards, alerting rules, and application instrumentation"
version: "1.0.0"
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
- `--slo` — define and configure SLO/SLI targets
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
- `http_request_duration_seconds` (histogram, buckets: 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10)
- Track by: method, route, status_code
- P50, P90, P95, P99 percentiles

**2. Traffic** — demand on the system
- `http_requests_total` (counter)
- Track by: method, route, status_code
- Requests per second, per minute

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
```javascript
// metrics.js — Prometheus metrics middleware
const client = require('prom-client');

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
});

const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});
```
- Add `/metrics` endpoint exposing Prometheus format
- Add `prom-client` to dependencies

**Python (FastAPI/Django)**:
- Add `prometheus_client` or `prometheus-fastapi-instrumentator`
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
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerts/*.yml"

scrape_configs:
  - job_name: '{app-name}'
    static_configs:
      - targets: ['app:{port}']
    metrics_path: /metrics
    scrape_interval: 10s
```

**`monitoring/prometheus/alerts/app.yml`**:
```yaml
groups:
  - name: app-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 1% for 5 minutes"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency above 2 seconds"

      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes / 1024 / 1024 > 512
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Memory usage above 512MB for 10 minutes"

      - alert: HighCPU
        expr: rate(process_cpu_seconds_total[5m]) > 0.8
        for: 10m
        labels:
          severity: warning

      - alert: DiskUsageHigh
        expr: (node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Disk usage above 80%"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} is down"
```

**`monitoring/grafana/dashboards/app.json`**:
Generate a Grafana dashboard JSON with panels for:
1. **Request Rate** — graph of requests/sec by status code
2. **Error Rate** — graph of error percentage over time
3. **Latency Distribution** — heatmap of request duration
4. **P50/P90/P99 Latency** — time series of percentiles
5. **Active Connections** — gauge of concurrent requests
6. **Memory Usage** — time series of process memory
7. **CPU Usage** — time series of process CPU
8. **Saturation** — connection pool, queue depth

**`monitoring/grafana/provisioning/dashboards.yml`**:
```yaml
apiVersion: 1
providers:
  - name: 'default'
    folder: ''
    type: file
    options:
      path: /var/lib/grafana/dashboards
```

**Docker Compose addition** (add to existing or create `monitoring/docker-compose.monitoring.yml`):
```yaml
services:
  prometheus:
    image: prom/prometheus:v2.51.0
    volumes:
      - ./monitoring/prometheus:/etc/prometheus
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'

  grafana:
    image: grafana/grafana:10.4.0
    volumes:
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
      - grafana-data:/var/lib/grafana
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin  # Change in production

  alertmanager:
    image: prom/alertmanager:v0.27.0
    volumes:
      - ./monitoring/alertmanager:/etc/alertmanager
    ports:
      - "9093:9093"
```

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
- Add CloudWatch agent config
- Configure metric filters on log groups

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
- Fast burn (2%/hour): page immediately
- Slow burn (5%/day): ticket within 1 hour

============================================================
OUTPUT
============================================================

```
## Monitoring Setup Complete

### Files Created
{list of all generated files}

### Metrics Endpoints
- Application: http://localhost:{port}/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)
- Alertmanager: http://localhost:9093

### Alert Rules Configured
| Alert | Condition | Severity |
|-------|-----------|----------|
| HighErrorRate | >1% for 5m | critical |
| HighLatency | P99 >2s for 5m | warning |
| HighMemory | >512MB for 10m | warning |
| DiskUsageHigh | >80% for 5m | warning |
| ServiceDown | down for 1m | critical |

### Dashboard Panels
{list of dashboard panels}
```

============================================================
NEXT STEPS
============================================================

1. Start monitoring stack: `docker compose -f monitoring/docker-compose.monitoring.yml up -d`
2. Verify metrics are being scraped: check Prometheus targets page
3. Import Grafana dashboards and customize thresholds
4. Configure alerting notification channels (Slack, PagerDuty, email)
5. Add application-specific custom metrics for business KPIs
6. Set up log aggregation if not already configured (Loki, ELK)

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
