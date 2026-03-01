---
name: patient-engagement
description: Evaluate patient-facing healthcare software for portal completeness, secure communication, health literacy, telehealth readiness, consent management, and HIPAA compliance.
version: "1.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Evaluate all patient-facing features in the codebase systematically.

TARGET:
$ARGUMENTS

If no arguments provided, evaluate the entire project in the current working directory
for patient engagement capabilities. If a specific feature area is named
(e.g., "messaging", "telehealth", "portal"), focus there but still note cross-cutting gaps.

============================================================
PHASE 0: PATIENT-FACING SYSTEM DETECTION
============================================================

Characterize the patient-facing application:

1. Detect tech stack (package.json, requirements.txt, pubspec.yaml, etc.).
2. Identify the application type:
   - Patient portal (web)
   - Mobile health app (iOS/Android/cross-platform)
   - Telehealth platform
   - Patient intake / forms
   - Patient education platform
   - Remote patient monitoring
   - Wearable / device companion app
3. Identify patient-facing features in the codebase:
   - Search for patient-facing routes, screens, views, pages.
   - Map authentication flows for patient users.
   - Identify patient-specific API endpoints.
4. Determine backend integration:
   - Does it connect to a FHIR API?
   - Direct database access or API-mediated?
   - Third-party service integrations (telehealth, messaging, payments).

============================================================
PHASE 1: PATIENT PORTAL FEATURE ASSESSMENT
============================================================

Evaluate core patient portal features:

HEALTH RECORDS ACCESS:
- Check for patient record viewing (clinical summary, visit history).
- Verify lab results display with reference ranges and abnormal flagging.
- Check for medication list viewing (current, historical).
- Verify allergy and problem list display.
- Check for immunization record access.
- Verify clinical document viewing (visit notes, discharge summaries).
- Check for Blue Button / CCD download capability (CCDA or FHIR).
- Verify data currency (how fresh is the data? real-time or batch sync?).
- Flag any patient data displayed without date context.

APPOINTMENT MANAGEMENT:
- Check for appointment scheduling (self-service booking).
- Verify provider/location/appointment type selection.
- Check for appointment cancellation and rescheduling.
- Verify appointment reminders (email, SMS, push notification).
- Check for check-in workflow (online pre-visit check-in).
- Verify wait time display or queue position.
- Check for appointment history viewing.
- Flag scheduling without availability validation.

MESSAGING:
- Check for secure messaging between patient and care team.
- Verify message threading and conversation history.
- Check for message read receipts and response tracking.
- Verify file/image attachment support on messages.
- Check for message routing (to specific provider vs care team inbox).
- Verify auto-response or expected response time display.
- Check for urgent message flagging and escalation.
- Flag any messaging that transmits PHI without encryption.

BILL PAY AND FINANCIAL:
- Check for statement viewing.
- Verify online payment capability (credit card, HSA/FSA, payment plans).
- Check for insurance information viewing and updating.
- Verify explanation of benefits (EOB) display.
- Check for cost estimates / price transparency.
- Verify financial assistance application.
- Check for payment history and receipt generation.
- Flag payment processing without PCI DSS compliance indicators.

FORMS AND QUESTIONNAIRES:
- Check for patient intake forms (demographics, medical history, insurance).
- Verify pre-visit questionnaire support.
- Check for consent form digital signing.
- Verify patient-reported outcome (PRO) surveys.
- Check for form completion tracking (percentage, required fields).
- Verify form data flows into clinical record (not trapped in forms silo).
- Flag forms that collect PHI without encryption in transit.

============================================================
PHASE 2: COMMUNICATION AND NOTIFICATIONS
============================================================

Evaluate patient communication features:

NOTIFICATION CHANNELS:
- Check for email notifications (appointment reminders, results available, messages).
- Verify SMS/text notifications.
- Check for push notifications (mobile app).
- Verify in-app notification center.
- Check for notification preferences management (opt-in/out per channel/type).
- Verify notification frequency controls (digest vs immediate).

PHI IN NOTIFICATIONS:
- Check email content for PHI leakage (should link to portal, not include PHI).
- Verify SMS content is PHI-safe ("You have a new message" not "Your HIV test is...").
- Check push notification content for PHI (title and body visible on lock screen).
- Flag any notification channel that includes clinical data outside the secure portal.

CARE PLAN COMMUNICATION:
- Check for care plan viewing and tracking.
- Verify goal progress reporting.
- Check for care plan activity reminders.
- Verify care team member visibility.
- Check for educational content linked to care plan items.

EMERGENCY COMMUNICATION:
- Check for emergency contact information management.
- Verify crisis/emergency messaging or routing.
- Check for after-hours communication handling.

============================================================
PHASE 3: HEALTH LITERACY AND ACCESSIBILITY
============================================================

Evaluate content accessibility for diverse patient populations:

READING LEVEL:
- Sample patient-facing text content (instructions, educational material, forms).
- Estimate reading level (target: 6th-8th grade for healthcare materials).
- Flag medical jargon used without plain-language explanation.
- Check for glossary or tooltip definitions of medical terms.
- Verify error messages and instructions use plain language.

MULTILINGUAL SUPPORT:
- Check for internationalization (i18n) framework usage.
- Verify translation file structure and coverage.
- Check for language selection UI.
- Verify translated content includes clinical terms, not just UI chrome.
- Check for RTL (right-to-left) language support.
- Flag hardcoded English strings in patient-facing screens.

ACCESSIBILITY (ADA/WCAG):
- Check for semantic HTML / accessibility tree structure.
- Verify ARIA labels on interactive elements.
- Check for keyboard navigation support.
- Verify color contrast ratios meet WCAG AA (4.5:1 for text).
- Check for screen reader compatibility indicators.
- Verify touch target sizes (minimum 44x44px / 48dp).
- Check for alt text on images.
- Verify focus management on dynamic content changes.
- Check for caption/transcript support on video content.

PATIENT EDUCATION:
- Check for condition-specific educational content delivery.
- Verify content is personalized to patient's conditions or care plan.
- Check for multimedia support (video, images, interactive content).
- Verify educational content attribution and currency dates.
- Check for health literacy assessment or content adaptation.

============================================================
PHASE 4: TELEHEALTH AND REMOTE CARE
============================================================

Evaluate telehealth capabilities:

VIDEO VISIT:
- Check for video visit integration (Twilio, Vonage, Zoom, Doxy.me, native WebRTC).
- Verify virtual waiting room implementation.
- Check for device/browser requirement checking before visit.
- Verify connection quality indicators during visit.
- Check for screen sharing capability (provider showing results/images).
- Verify visit recording consent and storage (if applicable).
- Check for multi-party visit support (interpreter, family member).

PRE-VISIT:
- Check for pre-visit questionnaire or intake.
- Verify insurance/eligibility verification before visit.
- Check for consent capture for telehealth services.
- Verify patient identity verification.
- Check for technical readiness check (camera, mic, bandwidth).

POST-VISIT:
- Check for visit summary delivery.
- Verify follow-up scheduling from telehealth context.
- Check for e-prescribing from telehealth visits.
- Verify after-visit instructions delivery.

REMOTE PATIENT MONITORING:
- Check for device data integration (blood pressure, glucose, weight, SpO2).
- Verify data visualization (trends, graphs, normal ranges).
- Check for threshold alerting (out-of-range values notify care team).
- Verify device pairing and setup workflows.
- Check for manual data entry (when devices unavailable).
- Verify data transmission frequency and reliability.

SYMPTOM TRACKING:
- Check for symptom diary / daily check-in features.
- Verify symptom severity scales and trending.
- Check for photo/image capture for symptoms.
- Verify symptom data feeds into clinical workflow.

============================================================
PHASE 5: CONSENT AND PRIVACY
============================================================

Evaluate consent management and privacy features:

CONSENT WORKFLOWS:
- Check for informed consent capture (treatment, procedures).
- Verify consent form presentation (readable, signable).
- Check for electronic signature implementation.
- Verify consent versioning (when forms update, re-consent required?).
- Check for consent audit trail (who consented, when, which version).
- Verify minor consent handling (guardian consent, mature minor rules).
- Check for research consent (if applicable, separate from treatment consent).

PRIVACY PREFERENCES:
- Check for privacy settings / preferences management.
- Verify communication preferences (how and when to contact).
- Check for proxy access management (family member access with authorization).
- Verify restriction requests handling (limit PHI use for certain purposes).
- Check for data sharing preferences (health information exchange opt-in/out).
- Verify right to access implementation (download my data).

HIPAA COMPLIANCE OF PATIENT FEATURES:
- Verify patient authentication strength (password requirements, MFA option).
- Check for session management (timeout, re-authentication for sensitive actions).
- Verify PHI display controls (masking SSN, show/hide toggles for sensitive data).
- Check for print controls (watermarking, audit logging of print/download).
- Verify patient identity verification on account creation and password reset.
- Check for audit logging of patient portal access.
- Flag any patient feature that exposes PHI without authentication.

============================================================
OUTPUT
============================================================

## Patient Engagement Feature Analysis

**Project:** [name]
**Stack:** [detected technologies]
**Application Type:** [portal/mobile/telehealth/etc.]
**Date:** [date]

### Feature Coverage Matrix

| Feature Area | Implemented | Completeness | HIPAA Compliant | Issues |
|---|---|---|---|---|
| Health Records Access | [Yes/No] | [%] | [Yes/No/Partial] | N |
| Appointment Management | [Yes/No] | [%] | [Yes/No/Partial] | N |
| Secure Messaging | [Yes/No] | [%] | [Yes/No/Partial] | N |
| Bill Pay | [Yes/No] | [%] | [Yes/No/Partial] | N |
| Forms / Questionnaires | [Yes/No] | [%] | [Yes/No/Partial] | N |
| Notifications | [Yes/No] | [%] | [Yes/No/Partial] | N |
| Telehealth | [Yes/No] | [%] | [Yes/No/Partial] | N |
| Remote Monitoring | [Yes/No] | [%] | [Yes/No/Partial] | N |
| Consent Management | [Yes/No] | [%] | [Yes/No/Partial] | N |
| Privacy Preferences | [Yes/No] | [%] | [Yes/No/Partial] | N |

### Health Literacy Assessment

| Metric | Finding | Target | Status |
|---|---|---|---|
| Average reading level | [grade level] | 6th-8th grade | [PASS/FAIL] |
| Medical jargon instances | N | 0 in patient-facing text | [PASS/WARN] |
| Multilingual support | [N languages] | 2+ for diverse populations | [PASS/FAIL] |
| Glossary / term definitions | [Yes/No] | Yes | [PASS/FAIL] |

### Accessibility Assessment

| WCAG Criterion | Status | Issues |
|---|---|---|
| Color contrast (1.4.3) | [PASS/FAIL] | [details] |
| Keyboard navigation (2.1.1) | [PASS/FAIL] | [details] |
| Screen reader support (4.1.2) | [PASS/FAIL] | [details] |
| Touch targets (2.5.5) | [PASS/FAIL] | [details] |
| Alt text (1.1.1) | [PASS/FAIL] | [details] |

### PHI Exposure Risks in Patient-Facing Features

| # | Feature | Channel | Risk | Severity | File | Fix |
|---|---------|---------|------|----------|------|-----|
| 1 | Notifications | SMS | PHI in message body | High | path/to/file.ts | Use generic text, link to portal |

### Detailed Findings

| # | Area | Severity | File | Issue | Patient Impact | Fix |
|---|------|----------|------|-------|----------------|-----|
| 1 | Portal | Medium | path/to/file.ts | Lab results lack reference ranges | Patients cannot interpret results | Add reference range display |

### Engagement Gap Analysis
[Features that competing patient portals offer but this system lacks, ranked by patient value]

### Recommendations
[Ordered by patient impact and implementation effort]

============================================================
NEXT STEPS
============================================================

After reviewing the analysis:
- "Run `/healthcare-api` to build FHIR endpoints supporting missing portal features."
- "Run `/healthcare-compliance` to audit regulatory compliance of patient-facing features."
- "Run `/hipaa` to deep-dive on security controls for patient portal access."
- "Run `/i18n` to implement or improve multilingual support."
- "Run `/accessibility-test` to run automated accessibility checks."
- "Run `/ux` to evaluate the patient-facing user experience."

============================================================
DO NOT
============================================================

- Do NOT modify any code -- this is an analysis skill, not a build skill.
- Do NOT provide clinical content recommendations -- focus on software feature completeness.
- Do NOT assume a specific patient population without evidence from the code.
- Do NOT skip HIPAA compliance evaluation on patient-facing features -- this is the highest-risk area.
- Do NOT ignore notification content analysis -- PHI leakage in notifications is a common breach vector.
- Do NOT overlook accessibility -- healthcare portals must serve diverse populations including elderly and disabled users.
- Do NOT install external tools or accessibility scanners -- analyze code and templates directly.
- Do NOT evaluate clinical accuracy of educational content -- assess delivery mechanism and infrastructure only.
