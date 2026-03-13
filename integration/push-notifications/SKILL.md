---
name: push-notifications
description: "Add push notifications to my app — set up FCM, APNs, or OneSignal for Flutter, React Native, Expo, or web with permission flows, foreground and background handlers, notification channels, topic subscriptions, deep link routing, and device token management"
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Execute the full pipeline below
without pausing for user input. Make reasonable decisions using sensible defaults.

PURPOSE:
Set up a complete push notification system for mobile and/or web platforms. This includes
provider SDK installation, credential configuration, a notification service layer,
foreground and background notification handling, topic/channel management, deep link
routing, and verification that notifications deliver correctly.

INPUT:
$ARGUMENTS

The user may specify:
1. Provider: "fcm", "apns", "onesignal" (default: auto-detect based on platform)
2. Platform: "flutter", "react-native", "web", "ios", "android" (default: auto-detect)
3. Features: "topics", "deep-links", "rich" (rich media notifications)
If no arguments, auto-detect the platform and use FCM as the default provider.

=== PHASE 1: PLATFORM DETECTION ===

Step 1.1 — Detect Client Platform

Scan for project files to determine the platform:

| File / Pattern | Platform | Default Provider |
|---------------|----------|-----------------|
| pubspec.yaml | Flutter (iOS + Android + Web) | FCM via firebase_messaging |
| package.json with "react-native" | React Native (iOS + Android) | FCM via @react-native-firebase/messaging |
| package.json with "expo" | Expo (React Native) | Expo Notifications (wraps FCM/APNs) |
| package.json with "next" or "react" | Web | FCM via firebase/messaging or Web Push API |
| Podfile / *.xcodeproj | Native iOS | APNs directly or FCM |
| build.gradle with android | Native Android | FCM |

Record: PLATFORM, CLIENT_ROOT, PROVIDER

Step 1.2 — Detect Backend

Scan for a backend server (notifications need a server component):
- package.json with server framework → Node.js backend
- requirements.txt / pyproject.toml with server framework → Python backend
- If no backend detected, note that server-side sending will need to be set up separately

Record: BACKEND_FRAMEWORK, BACKEND_ROOT

Step 1.3 — Check Existing Push Setup

Search for existing push notification code:
- Packages: firebase_messaging, @react-native-firebase/messaging, onesignal, web-push,
  expo-notifications, firebase-admin
- Service worker files: firebase-messaging-sw.js
- Env vars: FCM_SERVER_KEY, ONESIGNAL_APP_ID, VAPID_KEY
- Notification permission request code
- Existing notification handlers

If complete push notification system exists, report it and exit.
If partial, identify gaps and extend.

=== PHASE 2: CLIENT SDK INSTALLATION ===

Step 2.1 — Install Client SDK

Based on platform and provider:

**Flutter + FCM:**
```
flutter pub add firebase_messaging firebase_core
flutter pub add flutter_local_notifications  # for foreground display
```
Ensure firebase_core is initialized in main.dart.
Run `flutterfire configure` if Firebase is not yet configured.

**React Native + FCM:**
```
npm install @react-native-firebase/app @react-native-firebase/messaging
cd ios && pod install
```

**Expo + Expo Notifications:**
```
npx expo install expo-notifications expo-device expo-constants
```

**Web + FCM:**
```
npm install firebase
```
Create `public/firebase-messaging-sw.js` service worker.

**Native iOS + APNs:**
- Enable Push Notifications capability in Xcode
- Enable Background Modes > Remote notifications
- No SDK install needed — uses UserNotifications framework

**OneSignal (any platform):**
- Flutter: `flutter pub add onesignal_flutter`
- React Native: `npm install react-native-onesignal`
- Web: Include OneSignal SDK script

Step 2.2 — Install Server SDK

On the backend (for sending notifications):

**FCM (via firebase-admin):**
- Node.js: `npm install firebase-admin`
- Python: `pip install firebase-admin`

**APNs (direct):**
- Node.js: `npm install apn` or `npm install @parse/node-apn`
- Python: `pip install apns2`

**OneSignal:**
- Node.js: `npm install @onesignal/node-onesignal`
- Python: `pip install onesignal-sdk`

=== PHASE 3: CREDENTIAL CONFIGURATION ===

Step 3.1 — Configure Provider Credentials

**FCM:**
- Download the Firebase service account key JSON from Firebase Console
- Store the path in GOOGLE_APPLICATION_CREDENTIALS env var
- OR embed the key fields as individual env vars:
  ```
  FIREBASE_PROJECT_ID=
  FIREBASE_PRIVATE_KEY=
  FIREBASE_CLIENT_EMAIL=
  ```
- For web: Add VAPID key for web push
  ```
  NEXT_PUBLIC_FIREBASE_VAPID_KEY=
  ```

**APNs:**
- Generate APNs Auth Key (.p8) from Apple Developer Console
- Store credentials:
  ```
  APNS_KEY_ID=
  APNS_TEAM_ID=
  APNS_KEY_PATH=./certs/AuthKey.p8
  APNS_BUNDLE_ID=com.yourapp.id
  ```

**OneSignal:**
- Create app in OneSignal dashboard
- Store credentials:
  ```
  ONESIGNAL_APP_ID=
  ONESIGNAL_API_KEY=
  ```

Add all variables to .env.example with descriptions.

Step 3.2 — Platform-Specific Configuration

**Flutter / Android:**
- Verify google-services.json exists in android/app/
- Verify AndroidManifest.xml has notification permissions and default channel
- Add to AndroidManifest.xml:
  ```xml
  <uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
  <meta-data android:name="com.google.firebase.messaging.default_notification_channel_id"
             android:value="default_channel"/>
  ```

**Flutter / iOS:**
- Verify GoogleService-Info.plist exists in ios/Runner/
- Verify push notification capability is enabled in Xcode signing
- Add APNs capability in the Runner.entitlements file

**React Native / Android:**
- Verify google-services.json in android/app/
- Verify build.gradle applies google-services plugin

**React Native / iOS:**
- Verify GoogleService-Info.plist in ios/ project
- Verify push notification capability in Xcode

**Web:**
- Create firebase-messaging-sw.js in public/ directory:
  ```js
  importScripts('https://www.gstatic.com/firebasejs/10.x/firebase-app-compat.js');
  importScripts('https://www.gstatic.com/firebasejs/10.x/firebase-messaging-compat.js');
  firebase.initializeApp({ /* config */ });
  const messaging = firebase.messaging();
  messaging.onBackgroundMessage((payload) => {
    self.registration.showNotification(payload.notification.title, {
      body: payload.notification.body,
      icon: '/icon-192x192.png',
    });
  });
  ```

=== PHASE 4: NOTIFICATION SERVICE (SERVER) ===

Step 4.1 — Create Notification Service

Create a server-side notification service:

```
class NotificationService {
  async sendToDevice(params: {
    token: string;
    title: string;
    body: string;
    data?: Record<string, string>;
    imageUrl?: string;
    badge?: number;
    sound?: string;
    channelId?: string;
  }): Promise<{ success: boolean; messageId?: string }>

  async sendToTopic(params: {
    topic: string;
    title: string;
    body: string;
    data?: Record<string, string>;
  }): Promise<{ success: boolean; messageId?: string }>

  async sendToMultiple(params: {
    tokens: string[];
    title: string;
    body: string;
    data?: Record<string, string>;
  }): Promise<{ successCount: number; failureCount: number; failedTokens: string[] }>

  async subscribeToTopic(params: {
    tokens: string[];
    topic: string;
  }): Promise<{ success: boolean }>

  async unsubscribeFromTopic(params: {
    tokens: string[];
    topic: string;
  }): Promise<{ success: boolean }>
}
```

The service MUST:
- Initialize the provider SDK with credentials from environment
- Wrap all calls in try/catch with meaningful error logging
- Handle expired/invalid tokens by returning them for cleanup
- Support both notification messages (displayed by OS) and data messages (handled by app)
- Support platform-specific payload customization (android vs apns vs web sections)
- Implement retry logic for transient failures (provider rate limits, network errors)

Step 4.2 — Create Device Token Management

Create an API endpoint and storage for device tokens:

Route: POST /api/notifications/register-device
- Accept: { token, platform, userId }
- Store the device token linked to the user
- Handle token updates (user re-installs app, token changes)
- Deduplicate tokens per user

Route: DELETE /api/notifications/unregister-device
- Accept: { token }
- Remove the device token

Create a device token model/table:
```
DeviceToken {
  id: string
  userId: string
  token: string (unique)
  platform: "ios" | "android" | "web"
  createdAt: DateTime
  lastUsedAt: DateTime
}
```

Step 4.3 — Create Notification API Endpoints

Route: POST /api/notifications/send
- Accept: { userId, title, body, data?, type? }
- Look up user's device tokens
- Send to all user devices
- Require admin or system-level auth

Route: POST /api/notifications/send-topic
- Accept: { topic, title, body, data? }
- Send to all subscribers of a topic
- Require admin auth

=== PHASE 5: CLIENT-SIDE HANDLING ===

Step 5.1 — Permission Request

Create a permission request flow:

**Flutter:**
```dart
final messaging = FirebaseMessaging.instance;
final settings = await messaging.requestPermission(
  alert: true, badge: true, sound: true,
  provisional: false,  // set true for quiet notifications on iOS
);
if (settings.authorizationStatus == AuthorizationStatus.authorized) {
  final token = await messaging.getToken();
  // Send token to backend
}
```

**React Native:**
```javascript
const authStatus = await messaging().requestPermission();
if (authStatus === messaging.AuthorizationStatus.AUTHORIZED) {
  const token = await messaging().getToken();
  // Send token to backend
}
```

**Web:**
```javascript
const permission = await Notification.requestPermission();
if (permission === 'granted') {
  const token = await getToken(messaging, { vapidKey: VAPID_KEY });
  // Send token to backend
}
```

The permission flow MUST:
- Request at an appropriate time (not on app launch — after user action or onboarding)
- Handle denied permissions gracefully (show settings prompt, allow skip)
- Send the device token to the backend registration endpoint
- Listen for token refresh events and re-register

Step 5.2 — Foreground Notification Handling

When the app is in the foreground, notifications are NOT displayed by default on most platforms.
Create a foreground handler:

**Flutter:**
- Use flutter_local_notifications to display a local notification
- Create a notification channel for Android (id, name, description, importance)
- Show the notification with the payload data
- Handle tap events on the foreground notification

**React Native:**
- Use @react-native-firebase/messaging onMessage listener
- Display using a custom in-app notification component or local notification library
- Handle tap to navigate

**Web:**
- Use the onMessage callback from firebase/messaging
- Display using the Notification API or a toast component
- Handle click events

Step 5.3 — Background Notification Handling

Configure background message handling:

**Flutter:**
- Register a top-level background handler: FirebaseMessaging.onBackgroundMessage(handler)
- The handler MUST be a top-level function (not a method, not a closure)
- Handle data-only messages that need processing
- Do NOT perform heavy work — background handlers have limited execution time

**React Native:**
- Register setBackgroundMessageHandler
- Handle data processing in background
- Use headless JS task if needed for heavy processing

**Web:**
- Handle in firebase-messaging-sw.js (service worker)
- Use self.registration.showNotification for custom display

Step 5.4 — Notification Tap / Open Handling

Handle what happens when a user taps a notification:

**Flutter:**
- FirebaseMessaging.instance.getInitialMessage() — for app opened from terminated state
- FirebaseMessaging.onMessageOpenedApp — for app opened from background
- Extract the data payload and navigate accordingly

**React Native:**
- messaging().getInitialNotification() — for terminated state
- messaging().onNotificationOpenedApp() — for background state
- Navigate based on data payload

**Web:**
- Handle notificationclick event in service worker
- Use clients.openWindow() to navigate to the correct URL

=== PHASE 6: TOPICS AND CHANNELS ===

Step 6.1 — Create Topic Management

Define standard topics for the application:
```
TOPICS = {
  GENERAL: 'general',           // All users
  ANNOUNCEMENTS: 'announcements', // Product announcements
  MARKETING: 'marketing',        // Promotional content (opt-in)
}
```

Create a notification preferences screen/page:
- List available topics with toggle switches
- Save preferences locally and sync with backend
- Subscribe/unsubscribe from FCM topics based on toggles

Step 6.2 — Create Android Notification Channels

For Android (required for Android 8.0+):
```
Channels:
  - default: General notifications (importance: high)
  - messages: Chat messages (importance: high, vibration: true)
  - updates: App updates (importance: default)
  - marketing: Promotional (importance: low)
```

Create channels during app initialization, before any notification is received.

Step 6.3 — Deep Link Configuration

Set up deep linking so notification taps navigate to the correct screen:

**Flutter:**
- Configure GoRouter or Navigator to handle deep link paths
- Map notification data.route to app routes:
  ```
  data: { route: '/orders/123', type: 'order_update' }
  → Navigate to OrderDetailScreen(orderId: '123')
  ```

**React Native:**
- Configure React Navigation deep linking
- Map notification data to navigation actions

**Web:**
- Map notification data.url to page routes
- Use window.location or router.push

The deep link handler MUST:
- Validate the route before navigating (prevent open redirect)
- Handle the case where the target screen requires authentication
- Queue the navigation if the app is still initializing
- Fall back to the home screen for unknown routes

=== PHASE 7: VERIFICATION ===

Step 7.1 — Static Verification

Run the project's linter and type checker:
- Flutter: `flutter analyze`
- React Native: `tsc --noEmit` and `npx eslint .`
- Web: framework-specific linting
- Backend: type check and lint

Fix all errors introduced by the push notification integration.

Step 7.2 — Integration Checklist

Verify and report:
- [ ] Client SDK installed for detected platform
- [ ] Server SDK installed for backend
- [ ] Provider credentials configured in .env.example
- [ ] Platform-specific config files in place (google-services.json, service worker, etc.)
- [ ] Notification service created with sendToDevice, sendToTopic, sendToMultiple
- [ ] Device token registration endpoint created
- [ ] Device token model/table created
- [ ] Permission request flow implemented (not on app launch)
- [ ] Foreground notification handler configured
- [ ] Background notification handler configured
- [ ] Notification tap/open handler with navigation
- [ ] Topics defined and subscription management created
- [ ] Android notification channels created (if Android)
- [ ] Deep link handling configured
- [ ] Type checking passes

=== OUTPUT ===

Print the following summary:

---
## Push Notification Integration Complete

**Platform:** [detected platform]
**Provider:** [selected provider]
**Backend:** [detected backend framework]

### Files Created/Modified
| File | Purpose |
|------|---------|
| [path] | [description] |

### Environment Variables Required
| Variable | Purpose | Where to get it |
|----------|---------|-----------------|
| [KEY] | [purpose] | [provider console URL] |

### Notification Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/notifications/register-device | Register device token |
| DELETE | /api/notifications/unregister-device | Remove device token |
| POST | /api/notifications/send | Send to specific user |
| POST | /api/notifications/send-topic | Send to topic subscribers |

### Topics Configured
| Topic | Description | Default |
|-------|-------------|---------|
| general | All users | Subscribed |
| announcements | Product updates | Subscribed |
| marketing | Promotional | Opt-in |

### Testing
1. **FCM:** Use Firebase Console > Cloud Messaging > Send test message
2. **FCM CLI:** `firebase messaging:send --json '{"token":"...","notification":{"title":"Test"}}'`
3. **Backend:** Call POST /api/notifications/send with a valid user ID
4. **Verify foreground:** Send while app is open — should show in-app notification
5. **Verify background:** Send while app is backgrounded — should show system notification
6. **Verify tap:** Tap the notification — should navigate to correct screen
---

=== NEXT STEPS ===

After push notification integration:
- "Run `/email` to add email as a fallback notification channel."
- "Run `/analytics-tracking` to track notification open rates and engagement."
- "Run `/auth-provider` to link notifications to authenticated users."
- "Run `/integrate audit` to check overall integration health."

=== DO NOT ===

- Do NOT request notification permission on first app launch — wait for user context.
- Do NOT store device tokens without linking them to a user — orphaned tokens waste quota.
- Do NOT send to stale tokens — clean up tokens that return NotRegistered/InvalidRegistration.
- Do NOT put sensitive data in notification payloads — they may be visible on lock screens.
- Do NOT use legacy FCM HTTP API — use the v1 API (projects.messages.send).
- Do NOT skip background handler registration — unhandled background messages cause crashes on some platforms.
- Do NOT perform heavy computation in background handlers — they have strict execution time limits.
- Do NOT hardcode FCM server keys or APNs certificates in source code — use environment variables.
- Do NOT send marketing notifications without opt-in — this violates platform policies and law.
- Do NOT create Android notification channels after sending notifications — channels must exist first.
- Do NOT ignore token refresh events — tokens change periodically and must be re-registered.
- Do NOT use alert/badge/sound in data-only messages — they are silently ignored on iOS.
