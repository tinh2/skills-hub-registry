# Firebase end-to-end deploy (single-file HTML app)

Battle-tested commands for shipping a single-file app to Firebase Hosting + Firestore + Auth + custom subdomain.

## Prerequisites

```bash
firebase login            # opens browser, auths user
firebase --version        # 14+ recommended
```

## 1. Create the project

```bash
firebase projects:create <project-id> --display-name "<App Name>"
firebase apps:create WEB "<web-app-name>" --project <project-id>
# Then grab the SDK config (apiKey, authDomain, etc.):
firebase apps:sdkconfig WEB --project <project-id>
```

Paste the config into the HTML's Firebase init block.

## 2. Enable required APIs (server-side)

Firebase CLI cannot enable APIs directly, but you can refresh the CLI's OAuth
token to get one with `cloud-platform` scope, then call Service Usage REST:

```js
// Refresh access token from firebase-tools config
const c = require(
  `${process.env.HOME}/.config/configstore/firebase-tools.json`,
);
const params = new URLSearchParams({
  grant_type: "refresh_token",
  refresh_token: c.tokens.refresh_token,
  client_id:
    "YOUR_CLIENT_ID.apps.googleusercontent.com",
  client_secret: "j9iVZfS8kkCEFUPaAeJV0sAi", // public client secret for firebase-tools
});
const r = await fetch("https://oauth2.googleapis.com/token", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: params,
});
const { access_token } = await r.json();
// Then:
await fetch(
  `https://serviceusage.googleapis.com/v1/projects/<PROJECT>/services:batchEnable`,
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${access_token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      serviceIds: [
        "firestore.googleapis.com",
        "identitytoolkit.googleapis.com",
        "calendar-json.googleapis.com",
      ],
    }),
  },
);
```

## 3. Create the Firestore database

```bash
firebase firestore:databases:create "(default)" --location us-central1 --project <project-id>
```

## 4. Enable Google sign-in

This step REQUIRES the Firebase Console UI (Google's policy — no public API):

https://console.firebase.google.com/project/<project-id>/authentication/providers

Click Google → Enable → set support email → Save.

Add the production hostname to the authorized domains list via the Admin API:

```bash
curl -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://identitytoolkit.googleapis.com/admin/v2/projects/<project-id>/config?updateMask=authorizedDomains" \
  -d '{"authorizedDomains":["localhost","<project-id>.firebaseapp.com","<project-id>.web.app","<your-custom-domain>"]}'
```

## 5. Deploy

```bash
# firebase.json + .firebaserc + firestore.rules + index.html must exist
firebase deploy --only hosting,firestore:rules --project <project-id>
```

Default hosting URL: `https://<project-id>.web.app`

## 6. Custom domain

Add the custom domain via API:

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://firebasehosting.googleapis.com/v1beta1/projects/<project>/sites/<site>/customDomains?customDomainId=<custom.domain.com>" \
  -d '{}'
# Then poll the resource to read requiredDnsUpdates.desired[].records — these
# are the CNAME and ACME TXT records the user needs to add at their DNS host.
curl -H "Authorization: Bearer $TOKEN" \
  "https://firebasehosting.googleapis.com/v1beta1/projects/<project>/sites/<site>/customDomains/<custom.domain.com>"
```

If the user's DNS is AWS Route 53:

```bash
# With AWS_PROFILE pointing at credentials that can manage the zone:
aws route53 change-resource-record-sets --hosted-zone-id <Z...> \
  --change-batch '{
    "Changes": [
      {"Action":"UPSERT","ResourceRecordSet":{
        "Name":"<sub>.<domain>.","Type":"CNAME","TTL":300,
        "ResourceRecords":[{"Value":"<project>.web.app"}]}},
      {"Action":"UPSERT","ResourceRecordSet":{
        "Name":"_acme-challenge.<sub>.<domain>.","Type":"TXT","TTL":300,
        "ResourceRecords":[{"Value":"\"<acme-token>\""}]}}
    ]
  }'
```

Firebase usually issues the SSL cert within 5–20 minutes after DNS propagates.

## Common pitfalls

- **`Firebase: Error (auth/unauthorized-domain)`** → custom domain isn't in authorizedDomains. PATCH it (step 4).
- **Sign-in popup blocked / missing-initial-state** → Hosting needs `Cross-Origin-Opener-Policy: same-origin-allow-popups` in `firebase.json` headers if you ever set a strict COOP.
- **`Cloud Firestore API has not been used in project`** → step 2 wasn't run, or the user clicked through the Enable link in the console.
- **iOS Safari date input shows no mm/dd/yyyy placeholder** → use the visible `.due-text-label` overlay technique from patterns.css (hidden input absolutely positioned underneath).
