---
name: secrets
description: "Audit secret handling, set up secrets management with rotation, and configure CI/CD secrets integration"
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
- A secrets provider: `vault`, `aws-sm` (Secrets Manager), `aws-ssm` (Parameter Store), `gcp-sm`, `doppler`, `infisical`
- `--audit` — only audit current secret handling, do not generate config
- `--rotate` — set up secret rotation for database and API credentials
- `--ci` — configure CI/CD pipeline to pull secrets from provider
- `--env-template` — generate `.env.example` from detected env vars
- If no arguments, perform audit and recommend a provider based on existing infrastructure

============================================================
PHASE 1 — SECRET AUDIT
============================================================

Perform a comprehensive scan for secret exposure:

**1. Hardcoded secrets in source code**:
Search all source files (not node_modules, vendor, .git) for patterns:
- API keys: `(api[_-]?key|apikey)\s*[:=]\s*['"][A-Za-z0-9]{16,}['"]`
- AWS keys: `AKIA[0-9A-Z]{16}`
- Private keys: `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----`
- Tokens: `(token|secret|password)\s*[:=]\s*['"][^'"]{8,}['"]`
- Connection strings: `(postgres|mysql|mongodb|redis)://[^@]+@`
- JWT secrets: `(jwt[_-]?secret|signing[_-]?key)\s*[:=]\s*['"]`
- Generic high-entropy strings in assignment context (16+ chars, mixed case + digits)

**2. Environment files**:
- Check for `.env` files (`.env`, `.env.local`, `.env.production`, `.env.development`)
- Check if `.env` is in `.gitignore`
- Check if `.env` files are tracked by git: `git ls-files .env*`
- Read `.env` files and categorize values as: secret vs configuration

**3. Git history**:
- Check recent commits for accidentally committed secrets: scan diff of last 50 commits
- Check if any `.env` files were ever committed then removed
- Flag any file in history matching secret patterns

**4. Configuration files**:
- `docker-compose.yml` — passwords in environment blocks
- `application.yml` / `application.properties` — embedded credentials
- Terraform files — hardcoded provider credentials or database passwords
- Kubernetes secrets — base64-encoded values in committed YAML

**5. CI/CD configuration**:
- `.github/workflows/*.yml` — check for inline secrets (should use ${{ secrets.NAME }})
- `.gitlab-ci.yml` — check for variables with exposed values

Generate an audit report with severity levels:
- **CRITICAL**: Secrets in source code or git history
- **HIGH**: .env files tracked by git, secrets in docker-compose
- **MEDIUM**: .env not in .gitignore, missing .env.example
- **LOW**: No secrets manager configured, no rotation policy

============================================================
PHASE 2 — ENVIRONMENT TEMPLATE
============================================================

Generate `.env.example` from all detected environment variable references:

Scan for env var patterns:
- Node.js: `process.env.VARNAME`
- Python: `os.environ["VARNAME"]`, `os.getenv("VARNAME")`
- Go: `os.Getenv("VARNAME")`
- Generic: `${VARNAME}` in config files

Create `.env.example`:
```bash
# Application
NODE_ENV=development
PORT=3000
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Cache
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=REPLACE_ME_WITH_SECURE_RANDOM_VALUE
SESSION_SECRET=REPLACE_ME_WITH_SECURE_RANDOM_VALUE

# External APIs
# API_KEY=your_api_key_here

# Cloud Provider
# AWS_ACCESS_KEY_ID=your_access_key
# AWS_SECRET_ACCESS_KEY=your_secret_key
# AWS_REGION=us-east-1
```

Categorize each variable:
- Comment prefix `# SECRET:` for values that must come from secrets manager
- Comment prefix `# CONFIG:` for non-sensitive configuration

============================================================
PHASE 3 — SECRETS PROVIDER SETUP
============================================================

Based on detected infrastructure or $ARGUMENTS, set up the appropriate provider:

**AWS Secrets Manager**:
- Generate Terraform for `aws_secretsmanager_secret` resources
- Generate application helper to read secrets at startup:
  ```javascript
  // secrets.js
  const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');
  ```
- Configure IAM policy for ECS task role / Lambda execution role
- Set up secret versioning and stage labels

**AWS Systems Manager Parameter Store**:
- Generate Terraform for `aws_ssm_parameter` resources (SecureString type)
- Cheaper alternative for smaller number of secrets
- Hierarchical naming: `/{project}/{env}/{secret_name}`

**GCP Secret Manager**:
- Generate Terraform for `google_secret_manager_secret` resources
- Configure IAM bindings for service account access
- Application helper using `@google-cloud/secret-manager`

**HashiCorp Vault**:
- Generate Vault policy file
- Generate AppRole auth method config
- Application helper for Vault API integration
- Docker Compose service for local Vault dev server

**Doppler**:
- Generate `doppler.yaml` project config
- Set up environment configs (dev, staging, prod)
- CI/CD integration instructions

**For all providers**, generate a secrets loading wrapper:
```javascript
// load-secrets.js — unified secrets loader
async function loadSecrets() {
  if (process.env.NODE_ENV === 'production') {
    // Load from secrets manager
  } else {
    // Load from .env file
    require('dotenv').config();
  }
}
```

============================================================
PHASE 4 — SECRET ROTATION (if --rotate)
============================================================

Set up automatic rotation:

**Database credentials**:
- AWS: Lambda rotation function with `aws_secretsmanager_secret_rotation`
- Configure dual-user rotation strategy (alternating credentials)
- Rotation schedule: every 30 days

**API keys**:
- Generate key rotation script that:
  1. Creates new key in provider
  2. Updates secrets manager
  3. Waits for propagation
  4. Revokes old key
- Document manual rotation steps for third-party APIs

**TLS certificates**:
- Reference cert-manager or ACM for auto-renewal
- Alert 30 days before expiration

============================================================
PHASE 5 — CI/CD INTEGRATION (if --ci)
============================================================

**GitHub Actions**:
```yaml
# In workflow file, add step:
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-arn: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: us-east-1

- name: Load secrets
  uses: aws-actions/aws-secretsmanager-get-secrets@v2
  with:
    secret-ids: |
      ${{ vars.PROJECT_NAME }}/${{ vars.ENVIRONMENT }}
```

**Doppler**:
```yaml
- name: Load secrets from Doppler
  uses: dopplerhq/secrets-fetch-action@v1
  with:
    doppler-token: ${{ secrets.DOPPLER_TOKEN }}
```

Also configure:
- OIDC federation for GitHub -> AWS (no long-lived credentials)
- Environment protection rules for production secrets
- Secrets scanning: enable GitHub secret scanning and push protection

============================================================
PHASE 6 — REMEDIATION
============================================================

For each CRITICAL and HIGH finding from the audit:

1. **Hardcoded secrets**: Replace with environment variable references
2. **Committed .env files**: Add to `.gitignore`, remove from git tracking (warn about history)
3. **Docker compose passwords**: Replace with variable references `${DB_PASSWORD}`
4. **Missing .gitignore entries**: Add `.env*`, `*.pem`, `*.key` patterns

If secrets were found in git history, recommend:
- `git-filter-repo` to remove from history (document command but do not execute)
- Rotate ALL exposed credentials immediately

============================================================
OUTPUT
============================================================

```
## Secrets Audit & Configuration

### Audit Results
| Severity | Finding | Location | Status |
|----------|---------|----------|--------|
| CRITICAL | {finding} | {file:line} | {fixed/needs-action} |
| HIGH | {finding} | {file} | {fixed/needs-action} |

### Files Created/Modified
- .env.example — Environment variable template ({N} variables)
- .gitignore — Added secret file patterns
- {provider config files}
- {application secret loader}

### Secrets Inventory
| Secret | Provider | Rotation | CI/CD |
|--------|----------|----------|-------|
| DATABASE_URL | {provider} | 30 days | configured |
| JWT_SECRET | {provider} | 90 days | configured |

### Immediate Actions Required
{list of manual actions needed}
```

============================================================
NEXT STEPS
============================================================

1. Rotate any credentials that were exposed in source or git history
2. Set up the secrets provider account/project if not already done
3. Migrate existing .env values to the secrets provider
4. Update deployment scripts to pull secrets from provider at runtime
5. Enable GitHub secret scanning and push protection on the repository
6. Schedule quarterly secret rotation reviews

============================================================
DO NOT
============================================================

- Do NOT print, log, or display actual secret values in any output
- Do NOT commit real secrets to any file, even temporarily
- Do NOT delete `.env` files without warning — they may be the only copy of secrets
- Do NOT run `git filter-repo` or `git filter-branch` without explicit user confirmation
- Do NOT disable git history scanning — secrets in history are a real risk
- Do NOT use symmetric encryption for secrets at rest — use provider-managed encryption
- Do NOT create IAM users with long-lived credentials — prefer roles and OIDC federation
- Do NOT store secrets in Terraform state without encrypting the state backend
- Do NOT skip the audit phase — always scan before configuring
