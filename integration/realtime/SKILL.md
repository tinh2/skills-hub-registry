---
name: realtime
description: Sets up WebSocket or SSE-based realtime communication with channels, presence, reconnection, and offline handling — supports Socket.io, Pusher, Ably, and more.
version: "1.0.0"
category: integration
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Detect everything from the codebase and proceed.

PURPOSE:
Set up production-ready realtime communication. Auto-detect the project's framework and the
requested realtime provider. Install the SDK, create a realtime service with subscribe/publish/
presence methods, implement robust connection management, handle authentication for private
channels, and manage offline/online state transitions.

TASK:
$ARGUMENTS

============================================================ PHASE 0: DETECTION ============================================================

1. FRAMEWORK DETECTION — scan the project root to identify the tech stack:
   - package.json with "react" or "next" → React / Next.js
   - package.json with "vue" → Vue
   - package.json with "angular" → Angular
   - pubspec.yaml → Flutter / Dart
   - package.json with "react-native" → React Native
   - package.json with "svelte" → SvelteKit
   - requirements.txt / pyproject.toml with "django" / "flask" / "fastapi" → Python backend
   - go.mod → Go backend
   - Gemfile with "rails" → Ruby on Rails
   - Detect backend framework for server-side event publishing.

2. PROVIDER DETECTION — determine realtime provider from $ARGUMENTS or existing config:
   - If $ARGUMENTS names a provider, use it.
   - If socket.io is installed → Socket.io.
   - If pusher-js or @pusher/pusher-js is installed → Pusher.
   - If ably is installed → Ably.
   - If supabase-js is installed → Supabase Realtime.
   - If firebase is installed → Firebase Realtime Database or Firestore listeners.
   - If no provider specified and project has a Node.js backend → Socket.io (self-hosted).
   - If no provider specified and project is serverless → Pusher or Ably (managed).
   - Supported: Socket.io, Pusher, Supabase Realtime, Ably, Firebase Realtime.

3. EXISTING REALTIME CHECK — search for existing realtime implementations:
   - Grep for "socket", "websocket", "ws", "pusher", "ably", "realtime", "subscribe" in src/.
   - If a realtime service exists, extend it rather than creating a duplicate.

4. AUTH DETECTION — identify the project's authentication system:
   - Grep for auth middleware, JWT, session, Firebase Auth, Supabase Auth.
   - Private channels require auth — the realtime service must integrate with it.

============================================================ PHASE 1: SDK INSTALLATION ============================================================

Install the correct SDK for the detected provider and framework:

SOCKET.IO:
  - Server: `socket.io` (Node.js)
  - Client JS/TS: `socket.io-client`
  - Flutter: `socket_io_client`
  - React Native: `socket.io-client` (same as web)
  - Python server: `python-socketio`

PUSHER:
  - Server JS/TS: `pusher`
  - Client JS/TS: `pusher-js`
  - Flutter: `pusher_channels_flutter`
  - Python server: `pusher`
  - Go server: `github.com/pusher/pusher-http-go/v5`

ABLY:
  - JS/TS: `ably`
  - Flutter: `ably_flutter`
  - Python: `ably`
  - Go: `github.com/ably/ably-go`

SUPABASE REALTIME:
  - JS/TS: included in `@supabase/supabase-js`
  - Flutter: included in `supabase_flutter`

FIREBASE REALTIME:
  - JS/TS: `firebase` (Firestore onSnapshot / RTDB onValue)
  - Flutter: `cloud_firestore` or `firebase_database`
  - React Native: `@react-native-firebase/firestore`

After installing:
- Add connection config to .env: `REALTIME_URL`, `REALTIME_APP_KEY`, `REALTIME_SECRET`.
- For Pusher: `PUSHER_APP_ID`, `PUSHER_KEY`, `PUSHER_SECRET`, `PUSHER_CLUSTER`.
- For Ably: `ABLY_API_KEY` (server), `ABLY_CLIENT_KEY` (frontend — subscribe only).
- Add all env vars to .env.example with placeholder values.
- NEVER expose server secrets to the client.

============================================================ PHASE 2: REALTIME SERVICE ============================================================

Create a realtime service that abstracts the provider.

FILE LOCATION:
  - JS/TS: `src/lib/realtime.ts` or `src/services/realtime.ts`
  - Flutter: `lib/services/realtime_service.dart`
  - Python: `app/services/realtime.py`
  - Go: `internal/realtime/realtime.go`

THE SERVICE MUST EXPOSE:

  init(config)
    Initialize the realtime client. Set up connection with auth token.

  connect()
    Establish the WebSocket/SSE connection. Returns a promise that resolves when connected.

  disconnect()
    Gracefully close the connection. Clean up all subscriptions.

  subscribe(channel, event, callback)
    Subscribe to an event on a channel. Returns an unsubscribe function.
    Callback receives: { data, channel, event, timestamp }.

  unsubscribe(channel, event?)
    Unsubscribe from a specific event on a channel, or all events on that channel.

  publish(channel, event, data)
    Publish an event to a channel (server-side, or client-side if provider allows).

  subscribeToChannel(channel, handlers)
    Subscribe to all events on a channel with a handler map: { [event]: callback }.
    Returns an unsubscribe function for the entire channel.

  presence(channel)
    Returns a presence object for the channel with:
    - getMembers() → current list of members.
    - onJoin(callback) → fires when a member joins.
    - onLeave(callback) → fires when a member leaves.
    - onUpdate(callback) → fires when a member updates their state.

  setPresenceState(channel, state)
    Update the current user's presence state (e.g., { status: "typing" }).

  getConnectionState()
    Returns: "connected" | "connecting" | "disconnected" | "reconnecting".

  onConnectionChange(callback)
    Subscribe to connection state changes. Fires on connect, disconnect, reconnect.

IMPLEMENTATION REQUIREMENTS:
  - Wrap all SDK calls in try/catch. Normalize errors into a RealtimeError type.
  - Make init and connect idempotent — calling them twice must not create duplicate connections.
  - Support lazy connection — do not connect until the first subscribe() call (configurable).
  - Track active subscriptions internally for cleanup on disconnect.
  - Add TypeScript types / Dart types for all event data and callback signatures.

============================================================ PHASE 3: CONNECTION MANAGEMENT ============================================================

Implement robust connection handling. This is the most critical part of any realtime system.

1. RECONNECTION:
   - Auto-reconnect on unexpected disconnect.
   - Use exponential backoff: 1s, 2s, 4s, 8s, 16s, max 30s.
   - Add jitter (random 0-1s) to prevent thundering herd on server restart.
   - Max reconnection attempts: 20 (then fire a "permanently_disconnected" event).
   - On reconnect, re-subscribe to all active channels automatically.

2. HEARTBEAT:
   - For Socket.io: configure pingInterval (25s) and pingTimeout (20s).
   - For custom WebSocket: implement client-side ping every 30s.
   - Detect stale connections — if no pong within timeout, trigger reconnect.

3. CONNECTION QUALITY:
   - Track round-trip latency on heartbeat responses.
   - Expose `getLatency()` method.
   - Fire "connection_degraded" event if latency exceeds 2000ms.

4. GRACEFUL DEGRADATION:
   - If WebSocket is blocked (corporate firewalls), fall back to long-polling (Socket.io).
   - If SSE is available but WebSocket is not, use SSE for server-to-client + REST for client-to-server.
   - Log the transport type being used.

============================================================ PHASE 4: CHANNEL ARCHITECTURE ============================================================

Define a channel naming convention and access control model:

1. CHANNEL TYPES:

   PUBLIC CHANNELS — anyone can subscribe:
     Pattern: `public:{resource}` (e.g., `public:feed`, `public:announcements`)
     No authentication required.

   PRIVATE CHANNELS — authenticated users only:
     Pattern: `private:{resource}:{id}` (e.g., `private:user:123`, `private:team:abc`)
     Requires auth token validation before subscribing.

   PRESENCE CHANNELS — private + who's online:
     Pattern: `presence:{resource}:{id}` (e.g., `presence:room:456`)
     Requires auth. Provides member list and join/leave events.

2. AUTH ENDPOINT (for Pusher/Ably/managed providers):
   - Create a server-side auth endpoint: `POST /api/realtime/auth`
   - Accepts: { socket_id, channel_name }
   - Validates: user is authenticated, user has access to the requested channel.
   - Returns: signed auth token for the channel.
   - For Socket.io: use middleware to validate the auth token on connection.

3. CHANNEL PERMISSIONS:
   - Create a permissions check function: `canAccessChannel(userId, channelName) → boolean`
   - Parse the channel pattern to determine the resource and ID.
   - Check the user's role/permissions against the resource.
   - Reject unauthorized subscriptions with a clear error.

============================================================ PHASE 5: PRESENCE ============================================================

Implement presence (who's online) functionality:

1. PRESENCE DATA STRUCTURE:
   ```typescript
   interface PresenceMember {
     userId: string;
     name: string;
     avatar?: string;
     status: "online" | "away" | "busy";
     joinedAt: Date;
     customState?: Record<string, unknown>;
   }
   ```

2. PRESENCE EVENTS:
   - member_joined — new member subscribes to the channel.
   - member_left — member unsubscribes or disconnects.
   - member_updated — member changes their presence state.

3. PRESENCE UI HELPER (framework-specific):

   REACT:
     Create `src/hooks/usePresence.ts`:
     - `usePresence(channel)` → returns `{ members, myState, setMyState }`.
     - Re-renders on member join/leave/update.
     - Cleans up subscription on unmount.

   FLUTTER:
     Create `lib/widgets/presence_indicator.dart`:
     - Shows online status dot (green/yellow/red).
     - Shows avatar stack of online members.

   VUE:
     Create `src/composables/usePresence.ts` with equivalent functionality.

4. TYPING INDICATORS:
   - `startTyping(channel)` — broadcast typing state to other members.
   - `stopTyping(channel)` — clear typing state.
   - Auto-stop after 5 seconds of inactivity.
   - Show "User is typing..." in the UI.

============================================================ PHASE 6: OFFLINE HANDLING ============================================================

Handle the transition between online and offline states:

1. OFFLINE DETECTION:
   - Web: listen for `navigator.onLine`, `online`/`offline` events.
   - Flutter: use `connectivity_plus` to detect network state.
   - React Native: use `@react-native-community/netinfo`.

2. MESSAGE QUEUING:
   - When offline, queue outgoing messages in memory (or localStorage for persistence).
   - On reconnect, flush the queue in order (FIFO).
   - Set a max queue size (100 messages) — drop oldest if exceeded.

3. MISSED EVENT RECOVERY:
   - On reconnect, request missed events since last received timestamp.
   - For Pusher/Ably: use the provider's message history API.
   - For Socket.io: implement a server-side buffer that stores last N events per channel.
   - For Supabase: Realtime broadcasts are fire-and-forget — use database changes for durability.

4. STATE SYNC:
   - After reconnect, emit a "sync_requested" event to get current state.
   - The server responds with the full current state of relevant channels.
   - The client merges the state, resolving conflicts with server-wins strategy.

5. UI INDICATORS:
   - Show a "Reconnecting..." banner when the connection is lost.
   - Show "You are offline. Changes will sync when you reconnect." in offline mode.
   - Hide the banner after successful reconnect.

============================================================ PHASE 7: RATE LIMITING & SAFETY ============================================================

1. CLIENT-SIDE RATE LIMITING:
   - Throttle outgoing messages: max 10 per second per channel.
   - Debounce typing indicators: max 1 per second.
   - Queue excess messages and drain at the rate limit.

2. SERVER-SIDE RATE LIMITING (if Socket.io or custom server):
   - Limit messages per connection: 100/minute.
   - Limit channel subscriptions per connection: 50.
   - Limit message payload size: 64KB.
   - Disconnect clients that exceed limits with a clear error code.

3. MESSAGE VALIDATION:
   - Server: validate all incoming message payloads against a schema.
   - Reject messages with unexpected fields, oversized payloads, or invalid types.
   - Never trust client-sent timestamps — use server time.

4. SECURITY:
   - Sanitize all message content before broadcasting (prevent XSS).
   - Do NOT include sensitive data (tokens, passwords) in messages.
   - Use TLS for all WebSocket connections (wss://, not ws://).

============================================================ PHASE 8: VALIDATION ============================================================

1. Run the project's build/compile step — fix any errors.
2. Run existing tests — fix any failures caused by the realtime integration.
3. Write at least 4 unit tests:
   - Test connection lifecycle (connect, disconnect, reconnect).
   - Test subscribe/unsubscribe (mock the SDK).
   - Test presence join/leave (mock the SDK).
   - Test offline queue — messages queue when disconnected and flush on reconnect.
4. Verify no memory leaks: subscriptions are cleaned up on unsubscribe and disconnect.
5. Commit all changes with descriptive messages:
   - "feat: add realtime service with [Provider] SDK"
   - "feat: add channel auth and presence support"
   - "feat: add connection management with reconnection and backoff"
   - "feat: add offline handling and message queuing"

============================================================ DO NOT ============================================================

- Do NOT expose server secrets or admin keys to the client.
- Do NOT allow unauthenticated access to private or presence channels.
- Do NOT broadcast messages without server-side validation.
- Do NOT trust client-sent timestamps or user IDs in messages.
- Do NOT create unbounded subscriptions — always clean up on unmount/dispose.
- Do NOT skip reconnection logic — connections WILL drop in production.
- Do NOT store sensitive data in presence state (tokens, emails, PII).
- Do NOT create a second realtime service if one already exists — extend it.
- Do NOT use ws:// in production — always use wss:// (TLS).
- Do NOT poll as a substitute for realtime unless explicitly requested.
- Do NOT allow unlimited message size — enforce payload limits.

============================================================ OUTPUT ============================================================

## Realtime Setup

- **Framework**: [detected framework and version]
- **Provider**: [realtime provider configured]
- **Transport**: [WebSocket / SSE / long-polling / provider-specific]
- **SDK**: [package name and version installed]
- **Service**: [path to realtime service file]
- **Methods**: [list of implemented methods]
- **Channels**: [channel types configured — public / private / presence]
- **Auth**: [auth endpoint path, integration with existing auth]
- **Presence**: [implemented yes/no, presence hook/widget path]
- **Reconnection**: [strategy — exponential backoff, max attempts, jitter]
- **Offline**: [queue size, recovery method, UI indicator]
- **Rate limits**: [client-side and server-side limits]
- **Tests**: [count, path to test file]
- **Build status**: [passing/failing]
- **Caveats**: [any known issues or manual steps remaining]

NEXT STEPS:

After realtime is set up:
- "Run `/ship` to build features that use live updates (chat, notifications, collaboration)."
- "Run `/analytics-tracking` to track realtime engagement metrics."
- "Run `/search` to add live search results that update in realtime."
- "Run `/perf` to load-test WebSocket connections and measure message latency."
- "Run `/check-vanta` to verify realtime auth and data handling meet compliance requirements."
