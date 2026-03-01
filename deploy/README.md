# Deploy

Infrastructure, CI/CD, containers, monitoring, DNS, CDN, secrets management, cloud deployment, and mobile app publishing.

## Main Skill

**[devops](devops/)** -- Scans infrastructure gaps and orchestrates deployment readiness across CI/CD, containers, monitoring, and IaC. Routes to the appropriate sub-skills based on what is missing.

## Skills (15)

| Skill | Version | Description |
|-------|---------|-------------|
| [devops](devops/) | 1.0.0 | Main orchestrator. Scans infrastructure gaps and orchestrates deployment readiness across CI/CD, containers, monitoring, and IaC |
| [docker](docker/) | 1.0.0 | Auto-detect stack and generate optimized multi-stage Dockerfiles with compose, health checks, and security hardening |
| [github-actions](github-actions/) | 1.0.0 | Auto-detect tech stack and generate production-grade GitHub Actions CI/CD workflows with caching and security scanning |
| [k8s](k8s/) | 1.0.0 | Generate production-grade Kubernetes manifests with Deployments, Services, Ingress, HPA, and optional Helm charts |
| [terraform](terraform/) | 1.0.0 | Generate modular multi-cloud Terraform configurations with VPC, compute, database, cache, CDN, and remote state |
| [aws](aws/) | 1.0.0 | Generates production-ready Terraform files for AWS infrastructure |
| [cdn](cdn/) | 1.0.0 | Auto-detect hosting and configure CDN with caching rules, SSL/TLS, edge functions, and performance optimization |
| [dns](dns/) | 1.0.0 | Configure DNS records, SSL/TLS certificates, subdomains, email authentication, and health check routing |
| [monitoring](monitoring/) | 1.0.0 | Auto-detect infrastructure and set up observability with dashboards, alerting rules, and application instrumentation |
| [secrets](secrets/) | 1.0.0 | Audit secret handling, set up secrets management with rotation, and configure CI/CD secrets integration |
| [app-icon](app-icon/) | 1.0.0 | Generates a polished app icon and applies it as the launcher icon for iOS and Android |
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
