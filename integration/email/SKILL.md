---
name: email
description: "Add transactional email to my app — set up Resend, SendGrid, SES, Postmark, or Mailgun with HTML templates for welcome, password reset, and notification emails, delivery webhooks, bounce handling, and suppression lists"
version: "2.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Execute the full pipeline below
without pausing for user input. Make reasonable decisions using sensible defaults.

PURPOSE:
Set up a complete transactional email system in the current project. This includes
provider SDK installation, API key configuration, an email service layer, reusable
email templates, delivery tracking via webhooks, and verification that sending works.

INPUT:
$ARGUMENTS

The user may specify:
1. Provider: "sendgrid", "resend", "ses", "postmark", "mailgun" (default: "resend")
2. Templates to create: "welcome", "password-reset", "notification", "invoice", or "all"
3. Additional requirements: "tracking", "webhooks", "batch"
If no arguments, default to Resend with welcome + password-reset + notification templates.

=== PHASE 1: PROJECT DETECTION ===

Step 1.1 — Detect Framework

Scan for project files to determine the tech stack:

| File | Framework | Email Service Location |
|------|-----------|----------------------|
| package.json with "next" | Next.js | lib/email.ts or src/lib/email.ts |
| package.json with "fastify" | Fastify | src/services/email.service.ts |
| package.json with "express" | Express | src/services/email.service.ts |
| package.json with "nestjs" | NestJS | src/email/email.service.ts |
| requirements.txt with "django" | Django | apps/email/services.py |
| requirements.txt with "fastapi" | FastAPI | app/services/email.py |
| Gemfile with "rails" | Rails | app/mailers/ |

Record: FRAMEWORK, LANGUAGE, PROJECT_ROOT, SERVICE_DIR

Step 1.2 — Check Existing Email Setup

Search for any existing email integration:
- Packages: @sendgrid/mail, resend, nodemailer, @aws-sdk/client-ses, postmark
- Env vars: SENDGRID_API_KEY, RESEND_API_KEY, SMTP_HOST, SES_REGION
- Existing email service or mailer classes
- Email template files or directories

If a complete email integration exists, report it and exit.
If partial, identify gaps and fill them.

Step 1.3 — Select Provider

If the user specified a provider, use it. Otherwise, auto-select:
- If @sendgrid/mail is already installed → SendGrid
- If resend is already installed → Resend
- If @aws-sdk is already installed → SES
- If none detected → Default to Resend (best DX, generous free tier)

Record: PROVIDER

=== PHASE 2: SDK INSTALLATION ===

Step 2.1 — Install Provider SDK

Based on the selected provider:

**Resend:**
- Node.js: `npm install resend`
- Python: `pip install resend`

**SendGrid:**
- Node.js: `npm install @sendgrid/mail`
- Python: `pip install sendgrid`

**AWS SES:**
- Node.js: `npm install @aws-sdk/client-ses @aws-sdk/client-sesv2`
- Python: `pip install boto3`

**Postmark:**
- Node.js: `npm install postmark`
- Python: `pip install postmarker`

**Mailgun:**
- Node.js: `npm install mailgun.js form-data`
- Python: `pip install requests` (Mailgun uses REST API directly)

Step 2.2 — Install Template Engine (if needed)

If the project does not already have a template engine for email rendering:
- Node.js: `npm install @react-email/components react-email` (for Resend/React projects)
  OR `npm install handlebars` (for simpler template needs)
- Python: Use Jinja2 (usually already available in Django/FastAPI)
- Ruby: Use ERB (built into Rails)

Step 2.3 — Configure Environment Variables

Add to .env.example:

**Resend:**
```
RESEND_API_KEY=re_...
EMAIL_FROM=noreply@yourdomain.com
```

**SendGrid:**
```
SENDGRID_API_KEY=SG....
EMAIL_FROM=noreply@yourdomain.com
```

**AWS SES:**
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
EMAIL_FROM=noreply@yourdomain.com
```

**Postmark:**
```
POSTMARK_API_KEY=
EMAIL_FROM=noreply@yourdomain.com
```

Update config validation if the project uses one.

=== PHASE 3: EMAIL SERVICE ===

Step 3.1 — Create Email Client Module

Create a provider-specific client at the appropriate location:

The client module MUST:
- Import the provider SDK
- Initialize with API key from environment variables
- Export a singleton instance
- Handle initialization errors gracefully

Step 3.2 — Create Email Service Layer

Create the email service with a provider-agnostic interface:

```
class EmailService {
  async send(params: {
    to: string | string[];
    subject: string;
    html: string;
    text?: string;
    from?: string;
    replyTo?: string;
    tags?: Record<string, string>;
    attachments?: Array<{ filename: string; content: Buffer }>;
  }): Promise<{ id: string; success: boolean }>

  async sendTemplate(params: {
    to: string | string[];
    template: string;       // template name: "welcome", "password-reset", etc.
    data: Record<string, unknown>;  // template variables
    from?: string;
    replyTo?: string;
  }): Promise<{ id: string; success: boolean }>

  async sendBatch(params: {
    messages: Array<{
      to: string;
      subject: string;
      html: string;
      text?: string;
    }>;
  }): Promise<{ ids: string[]; success: boolean }>
}
```

The service MUST:
- Wrap all provider calls in try/catch
- Log errors with the project's logger (never swallow failures silently)
- Validate email addresses before sending (basic format check)
- Set a default "from" address from EMAIL_FROM env var
- Return a message ID on success for tracking
- Support both HTML and plain text versions
- Handle rate limiting gracefully (retry with backoff for 429 responses)

Step 3.3 — Create Provider Adapter

Implement the provider-specific adapter that EmailService delegates to:

**Resend adapter:**
- Use resend.emails.send() for single emails
- Use resend.batch.send() for batch
- Map response to { id, success }

**SendGrid adapter:**
- Use sgMail.send() for single emails
- Use sgMail.sendMultiple() for batch
- Map response to { id, success }

**SES adapter:**
- Use SendEmailCommand for single emails
- Use SendBulkEmailCommand for batch
- Map response to { id, success }

This adapter pattern allows swapping providers without changing calling code.

=== PHASE 4: EMAIL TEMPLATES ===

Step 4.1 — Create Template Directory

Create an email templates directory:
- Node.js: `src/emails/` or `emails/`
- Python: `templates/emails/`
- Ruby: `app/views/mailers/`

Step 4.2 — Create Welcome Template

Template name: "welcome"
Variables: { userName, appName, loginUrl }

Content structure:
- Header: App logo placeholder + "Welcome to [appName]"
- Body: Greeting with userName, brief onboarding message
- CTA button: "Get Started" linking to loginUrl
- Footer: Unsubscribe link placeholder, company info

Step 4.3 — Create Password Reset Template

Template name: "password-reset"
Variables: { userName, resetUrl, expiryMinutes }

Content structure:
- Header: "Reset Your Password"
- Body: "Hi [userName], we received a request to reset your password."
- CTA button: "Reset Password" linking to resetUrl
- Expiry notice: "This link expires in [expiryMinutes] minutes."
- Security notice: "If you didn't request this, you can safely ignore this email."
- Footer: Company info

Step 4.4 — Create Notification Template

Template name: "notification"
Variables: { userName, title, message, actionUrl, actionText }

Content structure:
- Header: [title]
- Body: "Hi [userName]," followed by [message]
- CTA button (optional): [actionText] linking to [actionUrl]
- Footer: Notification preferences link, company info

Step 4.5 — Create Base Layout

Create a shared base layout that all templates extend:
- Responsive HTML email wrapper (600px max-width, mobile-friendly)
- Inline CSS (email clients strip <style> tags)
- Preheader text support
- Light/readable color scheme (white background, dark text, branded accent)
- All images use absolute URLs
- Alt text on all images
- MSO conditionals for Outlook rendering

=== PHASE 5: DELIVERY TRACKING ===

Step 5.1 — Create Webhook Endpoint for Delivery Events

Route: POST /api/webhooks/email (or framework equivalent)

Handle provider-specific delivery events:

**Resend events:**
- email.sent, email.delivered, email.bounced, email.complained, email.opened, email.clicked

**SendGrid events:**
- processed, delivered, bounce, deferred, dropped, open, click, spam_report, unsubscribe

**SES events (via SNS):**
- Delivery, Bounce, Complaint, Open, Click

The webhook handler MUST:
- Verify the webhook signature (provider-specific verification)
- Parse the event type
- Log the event for debugging
- Update delivery status in database (if a delivery tracking table exists)
- Handle bounces: mark email address as invalid, stop future sends
- Handle complaints: add to suppression list

Step 5.2 — Create Delivery Status Types

Define delivery status enum:
```
enum EmailDeliveryStatus {
  QUEUED      // Accepted by provider, not yet sent
  SENT        // Sent to recipient's mail server
  DELIVERED   // Confirmed delivery to inbox
  OPENED      // Recipient opened the email (if tracking enabled)
  CLICKED     // Recipient clicked a link (if tracking enabled)
  BOUNCED     // Hard bounce — address invalid
  DEFERRED    // Soft bounce — temporary failure, will retry
  DROPPED     // Provider rejected (suppression list, invalid)
  COMPLAINED  // Recipient marked as spam
}
```

Step 5.3 — Create Suppression List Handler

Create a module that manages email suppression:
- Store bounced and complained addresses
- Check suppression list before sending
- Provide a method to remove addresses from suppression (manual override)
- Log all suppression events

=== PHASE 6: VERIFICATION ===

Step 6.1 — Static Verification

Run the project's type checker and linter:
- Fix all errors introduced by the email integration
- Ensure all imports resolve
- Verify templates render without errors

Step 6.2 — Integration Checklist

Verify and report:
- [ ] Email SDK installed for selected provider
- [ ] Environment variables documented in .env.example
- [ ] Email client singleton created
- [ ] Email service with send, sendTemplate, sendBatch methods
- [ ] Provider adapter implemented
- [ ] Welcome email template created
- [ ] Password reset email template created
- [ ] Notification email template created
- [ ] Base layout with responsive HTML
- [ ] Delivery webhook endpoint created
- [ ] Bounce handling implemented
- [ ] Suppression list handler created
- [ ] Type checking passes

=== OUTPUT ===

Print the following summary:

---
## Email Integration Complete

**Framework:** [detected framework]
**Provider:** [selected provider]
**Templates created:** [list]

### Files Created/Modified
| File | Purpose |
|------|---------|
| [path] | [description] |

### Environment Variables Required
| Variable | Purpose | Where to get it |
|----------|---------|-----------------|
| [KEY] | [purpose] | [provider dashboard URL] |
| EMAIL_FROM | Default sender address | Must match verified domain |

### Email Templates
| Template | Variables | Usage |
|----------|-----------|-------|
| welcome | userName, appName, loginUrl | After user registration |
| password-reset | userName, resetUrl, expiryMinutes | Password reset request |
| notification | userName, title, message, actionUrl | General notifications |

### Usage Example
```typescript
import { emailService } from './services/email.service';

await emailService.sendTemplate({
  to: user.email,
  template: 'welcome',
  data: { userName: user.name, appName: 'MyApp', loginUrl: 'https://myapp.com/login' },
});
```

### Domain Verification
To send from your own domain:
1. Add DNS records (SPF, DKIM, DMARC) as specified by [provider]
2. Verify domain in [provider] dashboard
3. Update EMAIL_FROM to use your verified domain

### Webhook Configuration
- Endpoint: POST /api/webhooks/email
- Configure in [provider] dashboard > Webhooks
- Events to subscribe: delivered, bounced, complained, opened
---

=== NEXT STEPS ===

After email integration:
- "Run `/auth-provider` to add authentication with email verification flows."
- "Run `/push-notifications` to add push as a complementary notification channel."
- "Run `/analytics-tracking` to track email open rates and engagement."
- "Run `/integrate audit` to check overall integration health."

=== DO NOT ===

- Do NOT send emails synchronously in request handlers — queue them or use async/await with timeouts.
- Do NOT include sensitive data (passwords, tokens, full URLs with secrets) in email bodies.
- Do NOT skip email address validation before sending — catch invalid addresses early.
- Do NOT ignore bounces — continued sending to bounced addresses harms sender reputation.
- Do NOT hardcode the "from" address in individual send calls — use the centralized EMAIL_FROM config.
- Do NOT use raw HTML strings for templates — use a template engine for maintainability.
- Do NOT skip plain text versions — some email clients and accessibility tools require them.
- Do NOT store API keys in template files or client-side code.
- Do NOT send emails without an unsubscribe mechanism — this violates CAN-SPAM/GDPR.
- Do NOT trust webhook payloads without signature verification — they can be spoofed.
- Do NOT batch more than the provider's per-request limit (varies by provider, typically 100-1000).


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the integration, validate:

1. Run the project's test suite to verify the integration works end-to-end.
2. Run build/compile to confirm no breakage.
3. Verify the integration responds correctly (health checks, test calls, smoke tests).
4. If failures occur, diagnose from error output and apply minimal fixes.
5. Repeat up to 3 iterations.

IF STILL FAILING after 3 iterations:
- Document the integration state and what's blocking
- Include error output and attempted fixes


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /email — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
