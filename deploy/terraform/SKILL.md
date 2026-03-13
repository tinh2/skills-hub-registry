---
name: terraform
description: "Generate Terraform infrastructure-as-code for AWS, GCP, or Azure. Creates modular VPC, compute, database, cache, CDN, and monitoring configs with per-environment sizing, remote state, cost estimates, and security best practices. Use when you need to set up cloud infrastructure, provision servers, create IaC, deploy to AWS/GCP/Azure, or scaffold a Terraform project."
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
- A cloud provider: `aws`, `gcp`, `azure`
- A compute target: `ecs`, `ecs-fargate`, `gke`, `aks`, `cloud-run`, `lambda`, `app-engine`
- A database: `rds`, `cloudsql`, `azure-sql`, `aurora`, `dynamodb`
- `--env <name>` — generate for specific environment (default: generate dev/staging/prod)
- `--modules` — use Terraform modules for reusable components
- `--state <backend>` — state backend: `s3`, `gcs`, `azurerm`, `terraform-cloud`
- `--minimal` — generate only compute + database (skip CDN, DNS, monitoring)
- `--import` — generate import blocks for existing infrastructure
- If no cloud provider specified, detect from: existing `.tf` files, AWS credentials, `gcloud` config, `az` CLI

============================================================
PHASE 1 — PROJECT ANALYSIS
============================================================

Analyze the application to determine infrastructure requirements:

**Application type**:
- Web API: needs compute, load balancer, database, cache
- Static site: needs S3/GCS bucket, CDN, DNS
- Background worker: needs compute, queue, database
- Full-stack: needs all of the above

**Detect from project files**:
- `Dockerfile` — containerized app, prefer ECS/GKE/Cloud Run
- `next.config.*` — SSR app, consider Vercel or container
- `serverless.yml` — Lambda/Cloud Functions
- `prisma/schema.prisma` — read datasource provider for DB engine
- Database ORM config — determine DB engine (postgres, mysql, sqlite, mongodb)
- Redis/cache references — need ElastiCache/Memorystore/Azure Cache

**Existing Terraform**:
- Read any existing `.tf` files to understand current state
- Check for `terraform.tfstate` or remote backend config
- Identify provider and region already in use

============================================================
PHASE 2 — PROJECT STRUCTURE
============================================================

Generate modular Terraform structure:

```
terraform/
  modules/
    networking/
      main.tf
      variables.tf
      outputs.tf
    compute/
      main.tf
      variables.tf
      outputs.tf
    database/
      main.tf
      variables.tf
      outputs.tf
    cache/
      main.tf
      variables.tf
      outputs.tf
    cdn/
      main.tf
      variables.tf
      outputs.tf
    monitoring/
      main.tf
      variables.tf
      outputs.tf
  environments/
    dev/
      main.tf
      variables.tf
      terraform.tfvars
      backend.tf
    staging/
      main.tf
      variables.tf
      terraform.tfvars
      backend.tf
    prod/
      main.tf
      variables.tf
      terraform.tfvars
      backend.tf
  main.tf          # Root module (for simple setups)
  variables.tf
  outputs.tf
  providers.tf
  versions.tf
```

If `--modules` is not set and project is simple, use flat structure:
```
terraform/
  main.tf
  variables.tf
  outputs.tf
  providers.tf
  versions.tf
  terraform.tfvars.example
```

============================================================
PHASE 3 — PROVIDER AND STATE CONFIGURATION
============================================================

**`versions.tf`**:
```hcl
terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {  # or google, azurerm
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

**`providers.tf`**:
```hcl
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
```

**`backend.tf`** (per environment):
- **AWS S3**:
  ```hcl
  terraform {
    backend "s3" {
      bucket         = "{project}-terraform-state"
      key            = "{env}/terraform.tfstate"
      region         = "us-east-1"
      encrypt        = true
      dynamodb_table = "{project}-terraform-locks"
    }
  }
  ```
- **GCP GCS**:
  ```hcl
  terraform {
    backend "gcs" {
      bucket = "{project}-terraform-state"
      prefix = "{env}"
    }
  }
  ```
- **Azure**:
  ```hcl
  terraform {
    backend "azurerm" {
      resource_group_name  = "{project}-terraform-rg"
      storage_account_name = "{project}tfstate"
      container_name       = "tfstate"
      key                  = "{env}.terraform.tfstate"
    }
  }
  ```

============================================================
PHASE 4 — NETWORKING MODULE
============================================================

**AWS VPC**:
- VPC with /16 CIDR (e.g., 10.0.0.0/16)
- 3 public subnets across AZs (for ALB)
- 3 private subnets across AZs (for compute, DB)
- NAT Gateway (single for dev, per-AZ for prod)
- Internet Gateway
- Route tables (public and private)
- VPC Flow Logs (prod only)

**GCP**:
- VPC network with custom subnets
- Cloud Router + Cloud NAT
- Firewall rules (deny all ingress by default, allow from LB)

**Azure**:
- Virtual Network with subnets
- Network Security Groups
- NAT Gateway

Always output: `vpc_id`, `public_subnet_ids`, `private_subnet_ids`

============================================================
PHASE 5 — COMPUTE MODULE
============================================================

**AWS ECS Fargate** (default for containerized apps):
```hcl
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-${var.environment}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn
  # container_definitions from template
}

resource "aws_ecs_service" "app" {
  name            = "${var.project_name}-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [aws_security_group.ecs.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = var.project_name
    container_port   = var.container_port
  }
}
```

- Application Load Balancer with HTTPS listener
- Auto-scaling policies (CPU and memory targets)
- Security groups (ALB -> ECS only)
- IAM roles (execution role for ECR pull, task role for app permissions)

**GCP Cloud Run**:
- `google_cloud_run_v2_service` with auto-scaling
- IAM for public access or authenticated only
- Custom domain mapping

**Azure Container Apps / AKS**:
- Container App Environment or AKS cluster
- Managed identity for secrets access

Include environment-specific sizing:
- **dev**: minimal (256 CPU, 512 MB, 1 task)
- **staging**: moderate (512 CPU, 1 GB, 2 tasks)
- **prod**: production (1024 CPU, 2 GB, 3+ tasks, auto-scaling)

============================================================
PHASE 6 — DATABASE MODULE
============================================================

**AWS RDS**:
```hcl
resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-${var.environment}"
  engine         = var.db_engine  # "postgres" or "mysql"
  engine_version = var.db_engine_version
  instance_class = var.db_instance_class

  allocated_storage     = var.db_storage
  max_allocated_storage = var.db_max_storage  # auto-scaling

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password  # from secrets manager

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  multi_az               = var.environment == "prod"
  backup_retention_period = var.environment == "prod" ? 30 : 7
  deletion_protection    = var.environment == "prod"
  skip_final_snapshot    = var.environment != "prod"

  storage_encrypted = true

  performance_insights_enabled = var.environment == "prod"
}
```

- DB subnet group in private subnets
- Security group (allow from compute SG only)
- Parameter group with optimized settings
- Automated backups with retention policy

**GCP Cloud SQL**: equivalent with `google_sql_database_instance`
**Azure SQL**: equivalent with `azurerm_mssql_server`

Environment sizing:
- **dev**: `db.t4g.micro` / smallest tier, single-AZ
- **staging**: `db.t4g.small`, single-AZ
- **prod**: `db.r6g.large`, multi-AZ, performance insights, 30-day backups

============================================================
PHASE 7 — CACHE, CDN, DNS MODULES (if not --minimal)
============================================================

**Cache** (if Redis/cache detected):
- AWS ElastiCache Redis cluster
- Single node for dev, replication group for prod
- Security group (allow from compute only)

**CDN** (if web application):
- CloudFront distribution with S3 origin or ALB origin
- Cache behaviors (static assets: 1y, API: no-cache, HTML: 5m)
- Custom error responses (403 -> /index.html for SPAs)

**DNS** (if domain configured):
- Route53 hosted zone
- A record aliased to CloudFront or ALB
- ACM certificate with DNS validation

============================================================
PHASE 8 — MONITORING MODULE
============================================================

- CloudWatch alarms for: ECS CPU, ECS memory, RDS connections, ALB 5xx rate
- CloudWatch dashboard with key metrics
- SNS topic for alarm notifications
- Log groups with retention policies (dev: 7d, staging: 30d, prod: 90d)

============================================================
PHASE 9 — VARIABLES AND OUTPUTS
============================================================

**`variables.tf`** — define all inputs with descriptions, types, defaults, and validation:
```hcl
variable "project_name" {
  description = "Name of the project, used in resource naming"
  type        = string
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must be lowercase alphanumeric with hyphens."
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

**`outputs.tf`** — expose key values:
```hcl
output "app_url" {
  description = "Application URL"
  value       = "https://${var.domain}"
}

output "database_endpoint" {
  description = "Database connection endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}
```

**`terraform.tfvars.example`** — example values for each variable (never real secrets):
```hcl
project_name = "my-app"
environment  = "dev"
aws_region   = "us-east-1"
# db_password = "REPLACE_ME"  # Use secrets manager
```

============================================================
PHASE 10 — COST ANNOTATIONS
============================================================

Add cost estimate comments to each resource:
```hcl
# Cost estimate (us-east-1):
#   dev:     ~$15/mo (t4g.micro, single-AZ, 20GB)
#   staging: ~$35/mo (t4g.small, single-AZ, 50GB)
#   prod:    ~$200/mo (r6g.large, multi-AZ, 100GB, PIOPS)
resource "aws_db_instance" "main" { ... }
```

============================================================
OUTPUT
============================================================

```
## Terraform Configuration Generated

### Structure
{tree of generated files}

### Resources by Environment
| Resource | Dev | Staging | Prod |
|----------|-----|---------|------|
| Compute | {spec} | {spec} | {spec} |
| Database | {spec} | {spec} | {spec} |
| Cache | — | {spec} | {spec} |

### Estimated Monthly Cost
| Environment | Estimate |
|-------------|----------|
| Dev | ~${X}/mo |
| Staging | ~${X}/mo |
| Prod | ~${X}/mo |

### Commands
terraform init
terraform plan -var-file="environments/dev/terraform.tfvars"
terraform apply -var-file="environments/dev/terraform.tfvars"
```

============================================================
NEXT STEPS
============================================================

1. Create the state backend (S3 bucket + DynamoDB table) before running `terraform init`
2. Set sensitive variables via environment variables or Terraform Cloud
3. Start with dev environment, validate, then promote to staging and prod
4. Set up CI/CD to run `terraform plan` on PRs and `terraform apply` on merge
5. Enable Terraform Cloud or Spacelift for team collaboration and state locking

============================================================
DO NOT
============================================================

- Do NOT hardcode secrets, passwords, or API keys in `.tf` or `.tfvars` files
- Do NOT use `terraform apply -auto-approve` in documentation — always review plans
- Do NOT create resources without tags — use default_tags on the provider
- Do NOT use overly permissive IAM policies (`*` actions or resources)
- Do NOT skip `deletion_protection` on production databases
- Do NOT create public subnets for databases or caches
- Do NOT use `latest` AMI IDs — pin to specific versions or use data sources
- Do NOT generate resources for services not needed by the application
- Do NOT overwrite existing Terraform files — read and extend them
- Do NOT use deprecated resource types or provider syntax
- Do NOT create NAT Gateways per-AZ for dev environments (cost optimization)
- Do NOT skip remote state configuration — local state is not suitable for teams
