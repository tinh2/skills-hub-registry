---
name: dns
description: "Configure DNS records, SSL/TLS certificates, subdomains, email authentication, and health check routing"
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
- A domain: `example.com` or `app.example.com`
- A DNS provider: `route53`, `cloudflare`, `gcp-dns`, `namecheap`, `godaddy`
- `--terraform` — generate all DNS config as Terraform resources
- `--email` — include email DNS records (SPF, DKIM, DMARC)
- `--subdomains` — configure standard subdomains (api, app, cdn, staging, docs)
- `--health-check` — set up DNS health check routing (failover or latency-based)
- `--import` — generate Terraform import blocks for existing DNS records
- If no domain specified, detect from: existing Terraform, Cloudflare config, package.json homepage, environment variables

============================================================
PHASE 1 — CURRENT STATE ANALYSIS
============================================================

Scan the project for existing DNS configuration:

**Terraform DNS resources**:
- `aws_route53_zone`, `aws_route53_record`
- `cloudflare_zone`, `cloudflare_record`
- `google_dns_managed_zone`, `google_dns_record_set`

**Application config**:
- Domain references in: `vercel.json`, `netlify.toml`, `wrangler.toml`
- `DOMAIN`, `BASE_URL`, `APP_URL` in environment variables
- `next.config.js` — `assetPrefix`, `images.domains`
- `CNAME` file (GitHub Pages)

**Infrastructure references**:
- CloudFront distribution domain names
- Load balancer DNS names (ALB, NLB)
- S3 website endpoints
- Cloud Run service URLs
- Kubernetes ingress hosts

**SSL/TLS certificates**:
- ACM certificates in Terraform (`aws_acm_certificate`)
- Let's Encrypt references (`certbot`, Caddy auto-TLS)
- Cloudflare SSL settings
- Self-signed certificates (flag for replacement)

Compile a list of:
- Current domain and all subdomains in use
- Where each domain/subdomain points (target/origin)
- Current SSL/TLS status per domain

============================================================
PHASE 2 — DNS RECORD GENERATION
============================================================

Generate DNS records for all required domains. Organize by record type:

**Root domain** (`example.com`):
```
A     example.com    →  {load balancer IP or CDN}
AAAA  example.com    →  {IPv6 address if available}
```
- For AWS: use ALIAS record to CloudFront or ALB
- For Cloudflare: use proxied A/CNAME record (orange cloud)
- For bare domain with CNAME target: use ALIAS/ANAME (provider-specific)

**Standard subdomains** (if `--subdomains`):

| Subdomain | Record | Target | Purpose |
|-----------|--------|--------|---------|
| `www` | CNAME | `example.com` | www redirect |
| `api` | CNAME | ALB/Cloud Run/API Gateway | API endpoint |
| `app` | CNAME | CDN/Vercel/Netlify | Frontend app |
| `cdn` | CNAME | CloudFront/Cloudflare | Static assets |
| `staging` | CNAME | Staging environment | Pre-production |
| `docs` | CNAME | GitHub Pages/Gitbook | Documentation |
| `status` | CNAME | Status page provider | Uptime monitoring |
| `mail` | MX/CNAME | Email provider | Mail routing |

**Terraform format** (if `--terraform`):
```hcl
resource "aws_route53_zone" "main" {
  name = var.domain
  tags = {
    Project     = var.project_name
    Environment = "shared"
    ManagedBy   = "terraform"
  }
}

resource "aws_route53_record" "root" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.${var.domain}"
  type    = "CNAME"
  ttl     = 300
  records = [var.domain]
}

resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain}"
  type    = "CNAME"
  ttl     = 300
  records = [aws_lb.api.dns_name]
}
```

**Cloudflare format**:
```hcl
resource "cloudflare_zone" "main" {
  account_id = var.cloudflare_account_id
  zone       = var.domain
  plan       = "free"
}

resource "cloudflare_record" "root" {
  zone_id = cloudflare_zone.main.id
  name    = "@"
  content = var.origin_ip
  type    = "A"
  proxied = true
  ttl     = 1  # Auto when proxied
}
```

**GCP Cloud DNS format**:
```hcl
resource "google_dns_managed_zone" "main" {
  name     = "${var.project_name}-zone"
  dns_name = "${var.domain}."

  dnssec_config {
    state = "on"
  }
}
```

============================================================
PHASE 3 — SSL/TLS CERTIFICATE SETUP
============================================================

Configure SSL certificates for all domains:

**AWS ACM** (for CloudFront and ALB):
```hcl
resource "aws_acm_certificate" "main" {
  domain_name               = var.domain
  subject_alternative_names = [
    "*.${var.domain}",  # Wildcard for all subdomains
  ]
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  zone_id = aws_route53_zone.main.zone_id
  name    = each.value.name
  type    = each.value.type
  ttl     = 60
  records = [each.value.record]
}

resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
```
- Note: CloudFront certificates MUST be in us-east-1
- Use wildcard certificate to cover all subdomains

**Cloudflare**:
- SSL mode: Full (strict) — origin must have valid certificate
- Enable Universal SSL (automatic, covers root + www)
- For origin certificates: generate Cloudflare Origin CA cert (15-year validity)

**Let's Encrypt** (self-hosted):
- Generate Certbot command for certificate acquisition
- Set up auto-renewal cron: `0 0 1 * * certbot renew --quiet`
- Or use Caddy/Traefik for automatic TLS

============================================================
PHASE 4 — EMAIL DNS (if --email)
============================================================

Configure email authentication records to prevent spoofing:

**SPF** (Sender Policy Framework):
```
TXT  example.com  "v=spf1 include:_spf.google.com include:amazonses.com ~all"
```
- Adjust `include:` based on detected email provider
- Common: Google Workspace, Microsoft 365, AWS SES, SendGrid, Postmark
- Always end with `~all` (soft fail) or `-all` (hard fail)

**DKIM** (DomainKeys Identified Mail):
```
CNAME  google._domainkey.example.com  →  google._domainkey.{value}.gappssmtp.com
```
- Provider-specific DKIM records
- Multiple DKIM records for multiple senders (transactional + marketing)

**DMARC** (Domain-based Message Authentication):
```
TXT  _dmarc.example.com  "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com; ruf=mailto:dmarc@example.com; pct=100"
```
- Start with `p=none` to monitor, then move to `p=quarantine`, then `p=reject`
- `rua` for aggregate reports, `ruf` for forensic reports

**MX records** (mail routing):
```
MX  example.com  10  aspmx.l.google.com      (Google Workspace)
MX  example.com  20  alt1.aspmx.l.google.com
```
or
```
MX  example.com  0   mail.example.com         (Self-hosted)
```

**Additional email records**:
- `TXT _domainkey.example.com` — DKIM policy
- `CNAME autodiscover.example.com` — Outlook auto-configuration
- `SRV _imaps._tcp.example.com` — IMAP service discovery

Terraform for email DNS:
```hcl
resource "aws_route53_record" "spf" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domain
  type    = "TXT"
  ttl     = 3600
  records = ["v=spf1 include:_spf.google.com ~all"]
}

resource "aws_route53_record" "dmarc" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "_dmarc.${var.domain}"
  type    = "TXT"
  ttl     = 3600
  records = ["v=DMARC1; p=quarantine; rua=mailto:dmarc@${var.domain}; pct=100"]
}
```

============================================================
PHASE 5 — HEALTH CHECK ROUTING (if --health-check)
============================================================

Set up DNS-level health checks for failover or latency-based routing:

**AWS Route53 health checks**:
```hcl
resource "aws_route53_health_check" "primary" {
  fqdn              = "api.${var.domain}"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30

  tags = {
    Name = "${var.project_name}-primary-health"
  }
}

resource "aws_route53_record" "api_failover_primary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain}"
  type    = "CNAME"
  ttl     = 60

  failover_routing_policy {
    type = "PRIMARY"
  }

  health_check_id = aws_route53_health_check.primary.id
  set_identifier  = "primary"
  records         = [var.primary_origin]
}

resource "aws_route53_record" "api_failover_secondary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain}"
  type    = "CNAME"
  ttl     = 60

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier = "secondary"
  records        = [var.secondary_origin]
}
```

**Cloudflare load balancing**:
- Configure origin pools (primary + fallback)
- Health check monitors (HTTP/HTTPS)
- Steering policy: failover, round-robin, or latency-based

**Latency-based routing** (multi-region):
```hcl
resource "aws_route53_record" "api_latency_us" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain}"
  type    = "CNAME"
  ttl     = 60

  latency_routing_policy {
    region = "us-east-1"
  }

  set_identifier = "us-east-1"
  records        = [var.us_east_origin]
}
```

============================================================
PHASE 6 — VALIDATION
============================================================

After generating configuration, verify:

1. **No conflicting records** — check for duplicate A/CNAME on same name
2. **CNAME restrictions** — CNAME cannot coexist with other record types on same name
3. **TTL values** — production records should use reasonable TTLs (300-3600s)
4. **Missing records** — warn if www redirect, SSL validation records, or MX records are absent
5. **DNSSEC** — recommend enabling if provider supports it

============================================================
OUTPUT
============================================================

```
## DNS Configuration Complete

### Domain: {domain}
### Provider: {provider}

### Records Generated
| Type | Name | Value | TTL | Notes |
|------|------|-------|-----|-------|
| A | {domain} | {target} | 300 | Root domain |
| CNAME | www | {domain} | 300 | www redirect |
| CNAME | api | {alb/origin} | 300 | API endpoint |
| TXT | {domain} | v=spf1... | 3600 | SPF |
| TXT | _dmarc | v=DMARC1... | 3600 | DMARC |

### SSL/TLS
- Certificate: {ACM/Cloudflare/Let's Encrypt}
- Coverage: {domain}, *.{domain}
- Auto-renewal: {yes/no}

### Files Created
{list of files}

### Nameservers (if new zone)
{ns1, ns2, ns3, ns4 — update at registrar}
```

============================================================
NEXT STEPS
============================================================

1. If new zone: update nameservers at your domain registrar
2. Wait for DNS propagation (up to 48 hours, usually minutes)
3. Verify records: `dig +short example.com A` and `dig +short example.com MX`
4. Verify SSL: `curl -vI https://example.com 2>&1 | grep 'SSL certificate'`
5. Test email authentication: send test email and check headers for SPF/DKIM/DMARC pass
6. Set up monitoring for DNS resolution and certificate expiration
7. If using DMARC with `p=none`, monitor reports for 2 weeks then tighten to `p=quarantine`

============================================================
DO NOT
============================================================

- Do NOT set TTL below 60 seconds without good reason (DDoS amplification risk)
- Do NOT use CNAME at zone apex — use ALIAS, ANAME, or A record instead
- Do NOT create MX records pointing to IP addresses — use hostnames
- Do NOT use `p=reject` DMARC policy without first monitoring with `p=none`
- Do NOT create DNS records for services that do not exist yet
- Do NOT delete existing DNS records — only add or modify
- Do NOT hardcode IP addresses that may change — use CNAME to stable DNS names
- Do NOT skip SSL/TLS setup — all domains must serve over HTTPS
- Do NOT create wildcard DNS records unless specifically needed (security risk)
- Do NOT overwrite existing Terraform DNS resources without reading them first
