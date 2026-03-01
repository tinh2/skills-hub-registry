---
name: k8s
description: "Generate production-grade Kubernetes manifests with Deployments, Services, Ingress, HPA, and optional Helm charts"
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
- `--helm` — generate a Helm chart instead of plain manifests
- `--namespace <name>` — target namespace (default: app name)
- `--replicas <n>` — initial replica count (default: 2)
- `--ingress <domain>` — configure ingress with this domain
- `--istio` — include Istio service mesh annotations
- `--argocd` — generate ArgoCD Application manifest
- `--kustomize` — generate Kustomize overlays for dev/staging/prod
- A specific resource to generate: `deployment`, `service`, `ingress`, `hpa`, `configmap`, `secret`, `pdb`
- If no arguments, generate the full manifest set as plain YAML

============================================================
PHASE 1 — APPLICATION ANALYSIS
============================================================

Scan the project to determine Kubernetes requirements:

**Container image**:
- Check for existing Dockerfile — extract EXPOSE port, HEALTHCHECK, CMD
- If no Dockerfile, note that one is needed (reference `deploy/docker` skill)
- Determine image name from: git remote URL, package.json name, go.mod module

**Ports and protocols**:
- Read application config for listen port (default: 3000/8080)
- Check for gRPC (protobuf files), WebSocket endpoints, metrics endpoint

**Resource requirements**:
- Estimate based on stack:
  - Node.js: 128Mi-512Mi memory, 100m-500m CPU
  - Go: 64Mi-256Mi memory, 50m-250m CPU
  - Java/Spring: 512Mi-1Gi memory, 250m-1000m CPU
  - Python: 128Mi-512Mi memory, 100m-500m CPU
- Check for existing resource usage data or load test results

**Dependencies**:
- Database: detected from Prisma, SQLAlchemy, GORM, etc.
- Cache: Redis/Memcached references
- Message queues: RabbitMQ, Kafka, NATS
- External services: API calls, third-party integrations

**Health endpoints**:
- Check for `/health`, `/healthz`, `/ready`, `/readyz`, `/live`, `/livez`
- If none found, note to create them

**Environment variables**:
- Scan for `process.env.`, `os.Getenv`, `os.environ` references
- Categorize as: config (ConfigMap) vs secrets (Secret)

============================================================
PHASE 2 — GENERATE NAMESPACE AND RBAC
============================================================

Create `k8s/namespace.yml`:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: {app-name}
  labels:
    app.kubernetes.io/name: {app-name}
    app.kubernetes.io/managed-by: skill-deploy-k8s
```

Create `k8s/serviceaccount.yml`:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {app-name}
  namespace: {namespace}
  labels:
    app.kubernetes.io/name: {app-name}
```

============================================================
PHASE 3 — GENERATE CORE MANIFESTS
============================================================

Create all manifests in `k8s/` directory (or `helm/{app-name}/templates/` if `--helm`).

**Deployment** (`k8s/deployment.yml`):
- `apiVersion: apps/v1`
- Minimum 2 replicas for HA
- Rolling update strategy: `maxSurge: 1`, `maxUnavailable: 0`
- Pod anti-affinity: prefer spreading across nodes
- Resource requests AND limits (always set both)
- Liveness probe: HTTP GET on health endpoint, `initialDelaySeconds: 15`, `periodSeconds: 10`
- Readiness probe: HTTP GET on ready endpoint, `initialDelaySeconds: 5`, `periodSeconds: 5`
- Startup probe (for slow-starting apps like Java): `failureThreshold: 30`, `periodSeconds: 10`
- `terminationGracePeriodSeconds: 30`
- Security context:
  ```yaml
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault
  containerSecurityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    capabilities:
      drop: ["ALL"]
  ```
- Environment from ConfigMap and Secret refs
- Image pull policy: `IfNotPresent` for tagged, `Always` for `latest`

**Service** (`k8s/service.yml`):
- `type: ClusterIP` (default)
- Target port matching container port
- Named port for service mesh compatibility

**Ingress** (`k8s/ingress.yml`, if domain provided):
- `networking.k8s.io/v1`
- TLS configuration with cert-manager annotation:
  ```yaml
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  ```
- Path-based routing (`/` -> service)
- TLS section with secret reference

**HPA** (`k8s/hpa.yml`):
- `autoscaling/v2`
- Min replicas: 2, Max replicas: 10
- CPU target: 70%
- Memory target: 80%
- Scale-down stabilization: 300s (prevent flapping)
- Behavior:
  ```yaml
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 25
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
  ```

**PodDisruptionBudget** (`k8s/pdb.yml`):
- `minAvailable: 1` or `maxUnavailable: 1` (prefer minAvailable for small replica counts)

**ConfigMap** (`k8s/configmap.yml`):
- Non-sensitive configuration values extracted from env analysis
- `LOG_LEVEL`, `NODE_ENV`, `APP_PORT`, etc.

**Secret** (`k8s/secret.yml`):
- Placeholder secret with `stringData` (not base64 in source)
- Mark clearly as "REPLACE BEFORE APPLYING"
- Database URLs, API keys, tokens

**NetworkPolicy** (`k8s/networkpolicy.yml`):
- Default deny ingress
- Allow ingress only from ingress controller namespace
- Allow egress to database/cache services and DNS

============================================================
PHASE 4 — HELM CHART (if --helm)
============================================================

Generate Helm chart structure:
```
helm/{app-name}/
  Chart.yaml
  values.yaml
  values-dev.yaml
  values-staging.yaml
  values-prod.yaml
  templates/
    _helpers.tpl
    deployment.yaml
    service.yaml
    ingress.yaml
    hpa.yaml
    pdb.yaml
    configmap.yaml
    secret.yaml
    serviceaccount.yaml
    networkpolicy.yaml
    NOTES.txt
```

**values.yaml** — parameterize all environment-specific values:
- `image.repository`, `image.tag`, `image.pullPolicy`
- `replicaCount`, `resources.requests`, `resources.limits`
- `ingress.enabled`, `ingress.hosts`, `ingress.tls`
- `autoscaling.enabled`, `autoscaling.minReplicas`, `autoscaling.maxReplicas`
- `env` as key-value map

**_helpers.tpl** — standard helper templates:
- `fullname`, `name`, `chart`, `labels`, `selectorLabels`

============================================================
PHASE 5 — KUSTOMIZE (if --kustomize)
============================================================

Generate Kustomize structure:
```
k8s/
  base/
    kustomization.yaml
    deployment.yaml
    service.yaml
    ...
  overlays/
    dev/
      kustomization.yaml
      patches/
    staging/
      kustomization.yaml
      patches/
    prod/
      kustomization.yaml
      patches/
```

Environment differences:
- **dev**: 1 replica, lower resources, debug logging
- **staging**: 2 replicas, production-like resources, info logging
- **prod**: 3+ replicas, full resources, warn logging, PDB enabled

============================================================
PHASE 6 — ISTIO / SERVICE MESH (if --istio)
============================================================

Add Istio annotations and resources:

- Pod annotation: `sidecar.istio.io/inject: "true"`
- Namespace label: `istio-injection: enabled`
- Generate `VirtualService` for traffic routing
- Generate `DestinationRule` for connection pool settings
- Generate `PeerAuthentication` for mTLS (STRICT mode)

============================================================
PHASE 7 — ARGOCD (if --argocd)
============================================================

Generate `argocd/application.yml`:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {app-name}
  namespace: argocd
spec:
  project: default
  source:
    repoURL: {git remote}
    targetRevision: HEAD
    path: k8s/  # or helm/{app-name}
  destination:
    server: https://kubernetes.default.svc
    namespace: {namespace}
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

============================================================
OUTPUT
============================================================

Print a summary:

```
## Kubernetes Manifests Generated

### Files Created
{list all generated files with descriptions}

### Resource Summary
| Resource | Name | Key Settings |
|----------|------|--------------|
| Namespace | {ns} | — |
| Deployment | {name} | {replicas} replicas, {memory} memory |
| Service | {name} | ClusterIP, port {port} |
| Ingress | {name} | {domain}, TLS enabled |
| HPA | {name} | {min}-{max} replicas |
| PDB | {name} | minAvailable: 1 |

### Apply Commands
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/

### Checklist Before Applying
- [ ] Replace placeholder secrets in k8s/secret.yml
- [ ] Verify container image is pushed to registry
- [ ] Ensure namespace exists in target cluster
- [ ] Configure cert-manager ClusterIssuer if using TLS
- [ ] Review resource limits for your workload
```

============================================================
NEXT STEPS
============================================================

1. Build and push the container image to your registry
2. Replace placeholder secrets with real values (or use external secrets operator)
3. Apply manifests to a dev cluster first: `kubectl apply -f k8s/ -n {namespace}`
4. Verify pods are running: `kubectl get pods -n {namespace}`
5. Check health probes: `kubectl describe pod -n {namespace}`
6. Consider setting up GitOps with ArgoCD or Flux for automated deployments

============================================================
DO NOT
============================================================

- Do NOT use `apiVersion: extensions/v1beta1` — use current stable APIs
- Do NOT set resource limits without requests (always set both)
- Do NOT use `latest` tag in deployment manifests — use specific tags or SHA digests
- Do NOT store real secrets in YAML files committed to git
- Do NOT set `replicas` in Deployment when HPA is enabled (HPA manages replicas)
- Do NOT use `hostNetwork: true` or `hostPort` without explicit justification
- Do NOT use `privileged: true` in security context
- Do NOT skip liveness/readiness probes — they are required for production
- Do NOT use `LoadBalancer` service type without considering cost — prefer `ClusterIP` + Ingress
- Do NOT overwrite existing manifests without reading them first
- Do NOT generate manifests for services not detected in the project
