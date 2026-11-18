# Deploy

Infrastructure, CI/CD, containers, monitoring, DNS, CDN, secrets management, cloud deployment, and mobile app publishing.

## Main Skill

**[devops](devops/)** -- Scans infrastructure gaps and orchestrates deployment readiness across CI/CD, containers, monitoring, and IaC. Routes to the appropriate sub-skills based on what is missing.

## Skills (18)

| Skill | Version | Description |
|-------|---------|-------------|
| [devops](devops/) | 1.0.0 | Main orchestrator. Scans infrastructure gaps and orchestrates deployment readiness across CI/CD, containers, monitoring, and IaC |
| [docker](docker/) | 1.0.0 | Auto-detect stack and generate optimized multi-stage Dockerfiles with compose, health checks, and security hardening |
| [github-actions](github-actions/) | 1.0.0 | Auto-detect tech stack and generate production-grade GitHub Actions CI/CD workflows with caching and security scanning |
| [k8s](k8s/) | 1.0.0 | Generate production-grade Kubernetes manifests with Deployments, Services, Ingress, HPA, and optional Helm charts |
| [terraform](terraform/) | 1.0.0 | Generate modular multi-cloud Terraform configurations with VPC, compute, database, cache, CDN, and remote state |
| [aws](aws/) | 1.1.0 | Generates production-ready Terraform files for AWS infrastructure |
| [cdn](cdn/) | 1.0.0 | Auto-detect hosting and configure CDN with caching rules, SSL/TLS, edge functions, and performance optimization |
| [dns](dns/) | 1.0.0 | Configure DNS records, SSL/TLS certificates, subdomains, email authentication, and health check routing |
| [monitoring](monitoring/) | 1.0.0 | Auto-detect infrastructure and set up observability with dashboards, alerting rules, and application instrumentation |
| [secrets](secrets/) | 1.0.0 | Audit secret handling, set up secrets management with rotation, and configure CI/CD secrets integration |
| [app-icon](app-icon/) | 1.1.0 | Generates a polished app icon and applies it as the launcher icon for iOS and Android |
| [app-store-publish](app-store-publish/) | 1.0.0 | iOS App Store publishing -- Fastlane, provisioning, screenshots, metadata, TestFlight |
| [play-store-publish](play-store-publish/) | 1.0.0 | Google Play Store publishing -- AAB config, Fastlane supply, data safety, staged rollout |
| [mobile-ci-cd](mobile-ci-cd/) | 1.0.0 | Mobile CI/CD -- GitHub Actions / Bitrise / Codemagic for iOS+Android |
| [ota-updates](ota-updates/) | 1.0.0 | Over-the-air updates -- CodePush, Shorebird, Play In-App Updates, rollback |

## Usage

- Full infrastructure readiness scan: `/devops`
- Containerize an application: `/docker`
- Set up CI/CD pipelines: `/github-actions`
- Generate Kubernetes manifests: `/k8s`
- Generate Terraform infrastructure: `/terraform` or `/aws`
- Set up CDN and caching: `/cdn`
- Configure DNS and SSL: `/dns`
- Set up monitoring and alerting: `/monitoring`
- Audit and manage secrets: `/secrets`
- Generate and apply app icons: `/app-icon`
- Publish to iOS App Store: `/app-store-publish`
- Publish to Google Play Store: `/play-store-publish`
- Set up mobile CI/CD: `/mobile-ci-cd`
- Configure OTA updates: `/ota-updates`
- Full deploy pipeline (combo): `/full-deploy` chains docker, CI/CD, monitoring, and preflight
- Mobile publish pipeline (combo): `/mobile-publish` chains mobile CI/CD, App Store, Play Store, and analytics

## Recently Added

| Skill | Version | Description |
|-------|---------|-------------|
| [ci-fixer](ci-fixer/) | 1 | Scan all repos for failing or stuck GitHub Actions workflows, diagnose issues, and fix them. Use when: 'fix ci', 'ci is broken', 'github actions failing', 'unblock ci', 'clear... |
| [flutter-deploy](flutter-deploy/) | 1.0.0 | Build and deploy Flutter apps to App Store (TestFlight) and Google Play (internal/production). Auto-detects project structure, pulls signing secrets from AWS Secrets Manager,... |
| [free-keys](free-keys/) | 2.0.0 | Provision free LLM API keys from 20+ providers. Health-checks existing keys, opens signup pages, validates new keys, and saves them to your project. |
| [hotfix](hotfix/) | 2.1.0 | Emergency bug fix pipeline — diagnose, fix, test, commit, push, and PR in 2 iterations max. Speed over perfection. |

<!-- BEGIN GENERATED: skills-hub-index (scripts/gen-index.mjs, do not edit by hand) -->
## All Deploy skills on skills-hub.ai

Each skill page on skills-hub.ai shows ratings and reviews, install counts, a one-command install, and related skills. 18 of 18 skills in this folder have a page. You can also [browse the Deploy category on skills-hub.ai](https://skills-hub.ai/browse?category=deploy), which includes skills from other publishers.

| Skill | Description | Page |
|-------|-------------|------|
| [app-store-publish](app-store-publish/) | Configure a complete iOS App Store publishing pipeline — sets up Fastlane with code signing (match), App Store Connect API key,... | [View on skills-hub](https://skills-hub.ai/skills/app-store-publish) |
| [aws](aws/) | Generates production-ready Terraform files for AWS infrastructure. | [View on skills-hub](https://skills-hub.ai/skills/aws) |
| [cdn](cdn/) | Configure a CDN with optimized caching, SSL/TLS, security headers, and cache invalidation — auto-detects hosting provider and app type,... | [View on skills-hub](https://skills-hub.ai/skills/cdn) |
| [ci-fixer](ci-fixer/) | Scan all repos for failing or stuck GitHub Actions workflows, diagnose issues, and fix them. | [View on skills-hub](https://skills-hub.ai/skills/ci-fixer) |
| [devops](devops/) | Audit deployment readiness across CI/CD, containers, monitoring, IaC, secrets, CDN, and DNS — score each area 0-100, identify critical... | [View on skills-hub](https://skills-hub.ai/skills/devops) |
| [dns](dns/) | Set up DNS records, SSL/TLS certificates, subdomains, SPF/DKIM/DMARC email authentication, and health-check failover routing for... | [View on skills-hub](https://skills-hub.ai/skills/dns) |
| [docker](docker/) | Detect project stack and generate production-ready multi-stage Dockerfiles with compose services, .dockerignore, non-root users, health... | [View on skills-hub](https://skills-hub.ai/skills/docker) |
| [flutter-deploy](flutter-deploy/) | Build and deploy Flutter apps to App Store (TestFlight) and Google Play (internal/production). | [View on skills-hub](https://skills-hub.ai/skills/flutter-deploy) |
| [free-keys](free-keys/) | Provision free LLM API keys from 20+ providers. | [View on skills-hub](https://skills-hub.ai/skills/free-keys) |
| [github-actions](github-actions/) | Detect project stack and generate GitHub Actions CI/CD workflows — PR checks with lint/test/build/security, deploy pipelines for... | [View on skills-hub](https://skills-hub.ai/skills/github-actions) |
| [hotfix](hotfix/) | Emergency bug fix pipeline — diagnose, fix, test, commit, push, and PR in 2 iterations max. | [View on skills-hub](https://skills-hub.ai/skills/hotfix) |
| [k8s](k8s/) | Generate production-grade Kubernetes manifests — Deployments with probes and security contexts, Services, Ingress with TLS, HPA, PDB,... | [View on skills-hub](https://skills-hub.ai/skills/k8s) |
| [mobile-ci-cd](mobile-ci-cd/) | Set up mobile CI/CD pipelines for Flutter, React Native, or native iOS/Android — GitHub Actions workflows for testing, code signing,... | [View on skills-hub](https://skills-hub.ai/skills/mobile-ci-cd) |
| [monitoring](monitoring/) | Set up application observability with Prometheus, Grafana, Datadog, or CloudWatch — instrument metrics endpoints, configure Golden... | [View on skills-hub](https://skills-hub.ai/skills/monitoring) |
| [ota-updates](ota-updates/) | Configure over-the-air mobile updates — Shorebird for Flutter, CodePush or EAS Update for React Native — with update channels, staged... | [View on skills-hub](https://skills-hub.ai/skills/ota-updates) |
| [play-store-publish](play-store-publish/) | Configure the complete Google Play Store publishing pipeline — upload key generation, AAB bundle optimization, Fastlane supply lanes for... | [View on skills-hub](https://skills-hub.ai/skills/play-store-publish) |
| [secrets](secrets/) | Audit codebases for leaked secrets and hardcoded credentials, generate .env templates, configure secrets management with AWS Secrets... | [View on skills-hub](https://skills-hub.ai/skills/secrets) |
| [terraform](terraform/) | Generate Terraform infrastructure-as-code for AWS, GCP, or Azure. | [View on skills-hub](https://skills-hub.ai/skills/terraform) |
<!-- END GENERATED: skills-hub-index -->
