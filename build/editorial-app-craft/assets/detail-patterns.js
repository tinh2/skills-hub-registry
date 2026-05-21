/* ============================================================
 * EDITORIAL APP CRAFT — Detail Patterns (drop-in JS)
 * ============================================================
 * Each block is a self-contained, copy-paste recipe.
 * Include the design tokens CSS first.
 * ============================================================ */

// --------------------------------------------------------------
// 1) DAILY ORNAMENT + PALETTE + QUOTE
// Cycle a typographic fleuron, a brand gradient, and a curated
// quote based on the local calendar day. Same for everyone using
// the app today; fresh tomorrow.
// --------------------------------------------------------------
const DAILY_GLYPHS = [
  "✦",
  "❀",
  "✺",
  "❁",
  "✷",
  "✾",
  "✼",
  "❋",
  "❦",
  "✸",
  "✹",
  "❉",
  "❊",
  "✻",
  "❂",
  "✴",
];
const DAILY_PALETTES = [
  ["#B4C9A0", "#5D7355"], // sage
  ["#D4B68C", "#6B4E3D"], // clay
  ["#D89BB0", "#7A3E54"], // dusty rose
  ["#9AB5CC", "#4B6A8A"], // dusty blue
  ["#E5C078", "#9B6B1A"], // honey gold
  ["#E29C7E", "#A05A3F"], // terracotta
  ["#A2BFA8", "#4D6D54"], // moss
  ["#C5C58A", "#7A7A40"], // olive
];
const DAILY_QUOTES = [
  {
    text: "Family isn't an important thing. It's everything.",
    by: "Michael J. Fox",
  },
  {
    text: "The little things, the little moments. They are not little.",
    by: "Jon Kabat-Zinn",
  },
  { text: "Home is where the heart is.", by: "Pliny the Elder" },
  { text: "Notice the moments worth noticing.", by: "" },
  { text: "Where there is love, there is life.", by: "Mahatma Gandhi" },
  {
    text: "Happiness held is the seed. Happiness shared is the flower.",
    by: "John Harrigan",
  },
  {
    text: "We do not remember days, we remember moments.",
    by: "Cesare Pavese",
  },
  {
    text: "Today is a gift. That is why it is called the present.",
    by: "Bil Keane",
  },
  {
    text: "Small daily improvements over time create stunning results.",
    by: "Robin Sharma",
  },
  { text: "Gratitude turns what we have into enough.", by: "Aesop" },
  { text: "Take time to do what makes your soul happy.", by: "" },
  {
    text: "Almost everything will work again if you unplug it for a few minutes. Including you.",
    by: "Anne Lamott",
  },
  // Extend this list — 25 to 40 is a good size.
];

function dayIndex() {
  // Days since 2020-01-01 in LOCAL time.
  const start = new Date(2020, 0, 1);
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  return Math.floor((now - start) / 86400000);
}
function todaysGlyph() {
  return DAILY_GLYPHS[dayIndex() % DAILY_GLYPHS.length];
}
function todaysPalette() {
  return DAILY_PALETTES[dayIndex() % DAILY_PALETTES.length];
}
function todaysQuote() {
  return DAILY_QUOTES[dayIndex() % DAILY_QUOTES.length];
}

function applyDailyOrnament() {
  const glyph = todaysGlyph();
  const [from, to] = todaysPalette();
  const gradient = `linear-gradient(135deg, ${from} 0%, ${to} 100%)`;
  document.querySelectorAll(".brand-mark, .modal .mark").forEach((el) => {
    el.textContent = glyph;
    el.style.background = gradient;
    el.style.fontStyle = "normal"; // fleurons render best upright
  });
  const qEl = document.getElementById("daily-quote");
  if (qEl) {
    const q = todaysQuote();
    qEl.innerHTML = `
      <div class="dq-text">${q.text.replace(/</g, "&lt;")}</div>
      ${q.by ? `<div class="dq-by">${q.by.replace(/</g, "&lt;")}</div>` : ""}
    `;
  }
}
// Boot:  applyDailyOrnament(); setInterval(applyDailyOrnament, 60_000);

// --------------------------------------------------------------
// 2) TIME-OF-DAY GREETING
// Returns a friendly greeting based on the hour. Drop into your
// welcome / sign-in modal as italic Playfair above the headline.
// --------------------------------------------------------------
function timeOfDayGreeting() {
  const h = new Date().getHours();
  if (h >= 5 && h < 11) return "Good morning, friend.";
  if (h >= 11 && h < 14) return "Hello, friend.";
  if (h >= 14 && h < 18) return "Good afternoon, friend.";
  if (h >= 18 && h < 22) return "Good evening, friend.";
  return "Burning the midnight oil.";
}

// --------------------------------------------------------------
// 3) DAY-VARYING EMPTY STATES
// Map each empty zone in your app to a few lines; pick by day
// index so the same family sees the same line all day, fresh
// tomorrow. Empty states are character moments — not voids.
// --------------------------------------------------------------
const EMPTY_STATES = {
  todo: [
    "Nothing queued. Quiet morning ☕",
    "Clear deck. What's next?",
    "Open canvas. Add the first thing.",
    "A fresh page.",
  ],
  doing: [
    "Nothing in motion.",
    "All quiet on this front.",
    "Pause before momentum.",
    "Resting between rounds.",
  ],
  done: [
    "Wrapped up. Nice work.",
    "A good day. Closed out.",
    "All sorted. Well done.",
    "Quiet pride. Carry it.",
  ],
};
function emptyStateFor(zoneKey) {
  const lines = EMPTY_STATES[zoneKey] || [""];
  return lines[dayIndex() % lines.length];
}

// --------------------------------------------------------------
// 4) TOAST PERSONALITY VARIANTS
// Instead of one generic "+1 pt" toast, vary copy by context.
// First win of the day, big point value, meaningful task → all
// get a small editorial flourish.
// --------------------------------------------------------------
function celebrationLine({
  points = 1,
  meaningful = false,
  recipientName = "you",
  feed = [],
} = {}) {
  const ptsLabel = `+${points} pt${points === 1 ? "" : "s"}`;
  const todayKey = new Date().toISOString().slice(0, 10);
  const firstToday = !feed.some(
    (f) =>
      f.kind === "complete" &&
      f.at &&
      new Date(f.at).toISOString().slice(0, 10) === todayKey,
  );
  if (meaningful)
    return `Beautifully done. ❤︎ ${ptsLabel} for ${recipientName}.`;
  if (points >= 5) return `Big one. ★ ${ptsLabel} for ${recipientName}.`;
  if (firstToday)
    return `First win of the day. ${ptsLabel} for ${recipientName}.`;
  return `${ptsLabel} for ${recipientName}`;
}

// --------------------------------------------------------------
// 5) STREAK MILESTONE ORNAMENT
// Upgrade the streak's leading character as the streak grows.
// Pair with a CSS class .streak.milestone for a soft shimmer at
// the exact milestone day.
// --------------------------------------------------------------
function streakOrnament(s) {
  if (s >= 100) return "🏆";
  if (s >= 30) return "✦";
  if (s >= 14) return "❀";
  if (s >= 7) return "✨";
  return "🔥";
}
function isStreakMilestone(s) {
  return s === 7 || s === 14 || s === 30 || s === 100;
}

// --------------------------------------------------------------
// 6) iOS-AWARE VOICE INPUT
// iOS Safari + iOS Chrome both fail webkitSpeechRecognition with
// service-not-allowed. The iPhone keyboard has its own dictation
// mic, so hide ours on iOS and point users to it.
// --------------------------------------------------------------
function setupVoiceInput({ micBtn, textInput, voiceStatusEl }) {
  const isIOS =
    /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (isIOS) {
    micBtn.style.display = "none";
    textInput.placeholder = "Add a task. Tap 🎤 on your keyboard to dictate.";
    return null;
  }
  if (!SR) {
    micBtn.style.display = "none";
    return null;
  }

  const rec = new SR();
  rec.continuous = false;
  rec.interimResults = true;
  rec.lang = "en-US";

  let isListening = false;
  rec.onstart = () => {
    isListening = true;
    micBtn.classList.add("listening");
    voiceStatusEl.textContent = "Listening…";
  };
  rec.onresult = (e) => {
    let final = "",
      interim = "";
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const t = e.results[i][0].transcript;
      if (e.results[i].isFinal) final += t;
      else interim += t;
    }
    textInput.value = (final || interim).trim();
  };
  rec.onerror = (e) => {
    const errors = {
      "not-allowed": "Microphone blocked. Allow it in browser settings.",
      "service-not-allowed":
        "Voice service blocked. Allow this site in your browser's mic settings.",
      "no-speech": "Didn't hear anything. Try again.",
      "audio-capture": "No microphone found.",
    };
    voiceStatusEl.textContent = errors[e.error] || `Voice error: ${e.error}`;
    isListening = false;
    micBtn.classList.remove("listening");
  };
  rec.onend = () => {
    isListening = false;
    micBtn.classList.remove("listening");
  };

  micBtn.addEventListener("click", async () => {
    if (isListening) {
      rec.stop();
      return;
    }
    // Pre-grant mic permission so the speech service has an explicit
    // user gesture (avoids cold-start service-not-allowed in Chrome).
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach((t) => t.stop());
    } catch (e) {
      voiceStatusEl.textContent =
        "Microphone access denied. Allow it in the address bar.";
      return;
    }
    try {
      rec.start();
    } catch (_) {}
  });
  return rec;
}

// --------------------------------------------------------------
// 7) PAGE-LOAD ORCHESTRATION
// On first paint, cascade columns + cards with a brief stagger,
// then remove the class so future re-renders are instant. CSS
// counterpart in patterns.css under .board.first-paint.
// --------------------------------------------------------------
let __firstBoardRender = true;
function applyFirstPaint(boardEl) {
  if (!__firstBoardRender) return;
  __firstBoardRender = false;
  boardEl.classList.add("first-paint");
  setTimeout(() => boardEl.classList.remove("first-paint"), 900);
}
