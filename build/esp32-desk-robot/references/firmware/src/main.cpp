// Desk robot starter firmware: ESP32 + 1.3" SH1106 OLED (I2C).
//
// Features, each self-contained so you (or your agent) can add them one at a
// time:  face with natural blinks and glances  ->  25-minute focus timer on
// the BOOT button  ->  a to-do list you edit from your phone over Wi-Fi  ->
// a drink-water reminder every 30 minutes.
//
// Everything is non-blocking (millis(), no delay()), so the eyes keep
// blinking while Wi-Fi connects or a web request is handled.
//
// Wiring (ESP32 DevKit default I2C):  OLED VDD -> 3V3, GND -> GND,
//                                     SDA -> GPIO21, SCK/SCL -> GPIO22

#include <Arduino.h>
#include <Wire.h>
#include <U8g2lib.h>
#include <WiFi.h>
#include <WebServer.h>
#include <Preferences.h>

#if __has_include("secrets.h")
#include "secrets.h"  // defines WIFI_SSID and WIFI_PASS (gitignored)
#else
#define WIFI_SSID ""
#define WIFI_PASS ""
#endif

// ---- hardware -----------------------------------------------------------------
constexpr int PIN_SDA = 21;
constexpr int PIN_SCL = 22;
constexpr int PIN_BUTTON = 0;  // the BOOT button: free to use once running

// 1.3" modules are almost always SH1106. If you have a 0.96" SSD1306 module,
// swap this for: U8G2_SSD1306_128X64_NONAME_F_HW_I2C oled(U8G2_R0, U8X8_PIN_NONE);
U8G2_SH1106_128X64_NONAME_F_HW_I2C oled(U8G2_R0, U8X8_PIN_NONE);

// ---- state --------------------------------------------------------------------
enum class Mode { Face, Focus, Water };
Mode mode = Mode::Face;

uint32_t nextBlink = 0, blinkStart = 0;
uint32_t nextGlance = 0;
int lookX = 0, lookTarget = 0;

constexpr uint32_t FOCUS_MS = 25UL * 60UL * 1000UL;
uint32_t focusStart = 0;

constexpr uint32_t WATER_EVERY_MS = 30UL * 60UL * 1000UL;
uint32_t lastWater = 0;

constexpr int MAX_TODOS = 8;
String todos[MAX_TODOS];
int todoCount = 0;

Preferences prefs;
WebServer server(80);

// ---- button: debounced press detection ------------------------------------------
bool buttonPressed() {
  static bool last = HIGH;
  static uint32_t changedAt = 0;
  bool now = digitalRead(PIN_BUTTON);
  if (now != last && millis() - changedAt > 30) {
    changedAt = millis();
    last = now;
    return now == LOW;  // pressed (active low)
  }
  return false;
}

// ---- to-do storage (survives power cycles) ----------------------------------------
void saveTodos() {
  prefs.putInt("n", todoCount);
  for (int i = 0; i < todoCount; i++) prefs.putString(("t" + String(i)).c_str(), todos[i]);
}

void loadTodos() {
  todoCount = constrain((int)prefs.getInt("n", 0), 0, MAX_TODOS);
  for (int i = 0; i < todoCount; i++) todos[i] = prefs.getString(("t" + String(i)).c_str(), "");
}

// ---- drawing ----------------------------------------------------------------------
// Eyes are rounded boxes; a blink shrinks their height for ~150 ms.
void drawEyes(int h, int y, int dx) {
  int w = 26;
  int r = min(8, h / 2);
  if (h < 3) {  // closed: a line
    oled.drawBox(40 - w / 2 + dx, y, w, 2);
    oled.drawBox(88 - w / 2 + dx, y, w, 2);
    return;
  }
  oled.drawRBox(40 - w / 2 + dx, y - h / 2, w, h, r);
  oled.drawRBox(88 - w / 2 + dx, y - h / 2, w, h, r);
}

int blinkHeight(int open) {
  uint32_t t = millis() - blinkStart;
  if (t > 150) return open;
  // close for 60 ms, hold 30 ms, open for 60 ms
  if (t < 60) return open - (open - 2) * t / 60;
  if (t < 90) return 2;
  return 2 + (open - 2) * (t - 90) / 60;
}

void drawFace() {
  drawEyes(blinkHeight(30), 31, lookX);
}

void drawFocus() {
  uint32_t left = FOCUS_MS - min(FOCUS_MS, millis() - focusStart);
  char buf[6];
  snprintf(buf, sizeof(buf), "%02lu:%02lu", (unsigned long)(left / 60000), (unsigned long)((left / 1000) % 60));
  // squinting, concentrating eyes above the countdown
  oled.drawRBox(43, 6, 14, 5, 2);
  oled.drawRBox(71, 6, 14, 5, 2);
  oled.setFont(u8g2_font_logisoso24_tn);
  int w = oled.getStrWidth(buf);
  oled.drawStr((128 - w) / 2, 46, buf);
  int bar = (int)(100UL * left / FOCUS_MS);
  oled.drawFrame(14, 55, 100, 4);
  oled.drawBox(14, 55, bar, 4);
}

void drawWater() {
  // a simple droplet and a nudge
  oled.drawDisc(64, 30, 11);
  oled.drawTriangle(53, 27, 75, 27, 64, 8);
  oled.setFont(u8g2_font_6x10_tf);
  const char *msg = "drink some water";
  oled.drawStr((128 - oled.getStrWidth(msg)) / 2, 58, msg);
}

void drawNextTodo() {
  // Shown under the eyes while idle, when there is something to do.
  if (todoCount == 0) return;
  oled.setFont(u8g2_font_6x10_tf);
  String t = todos[0];
  if (t.length() > 20) t = t.substring(0, 19) + ".";
  oled.drawStr((128 - oled.getStrWidth(t.c_str())) / 2, 62, t.c_str());
}

// ---- web page: edit the to-do list from a phone ----------------------------------------
String page() {
  String html = F("<!doctype html><meta name=viewport content='width=device-width'>"
                  "<title>Desk robot</title><body style='font:18px system-ui;max-width:28em;margin:2em auto;padding:0 1em'>"
                  "<h2>To-do</h2><ol>");
  for (int i = 0; i < todoCount; i++) {
    String safe = todos[i];
    safe.replace("&", "&amp;");
    safe.replace("<", "&lt;");
    html += "<li>" + safe + " <a href='/done?i=" + String(i) + "'>done</a></li>";
  }
  html += F("</ol><form action=/add><input name=t maxlength=60 autofocus> <button>Add</button></form>"
            "<p><a href=/focus>Start a 25 min focus timer</a></p></body>");
  return html;
}

void setupWeb() {
  server.on("/", [] { server.send(200, "text/html", page()); });
  server.on("/add", [] {
    String t = server.arg("t");
    t.trim();
    if (t.length() && todoCount < MAX_TODOS) {
      todos[todoCount++] = t;
      saveTodos();
    }
    server.sendHeader("Location", "/");
    server.send(303);
  });
  server.on("/done", [] {
    int i = server.arg("i").toInt();
    if (i >= 0 && i < todoCount) {
      for (int k = i; k < todoCount - 1; k++) todos[k] = todos[k + 1];
      todoCount--;
      saveTodos();
    }
    server.sendHeader("Location", "/");
    server.send(303);
  });
  server.on("/focus", [] {
    mode = Mode::Focus;
    focusStart = millis();
    server.sendHeader("Location", "/");
    server.send(303);
  });
  server.begin();
}

// Join your Wi-Fi if secrets.h is filled in; otherwise (or if it fails)
// open an access point called "desk-robot" so the page still works.
void setupWifi() {
  if (strlen(WIFI_SSID)) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    uint32_t t0 = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - t0 < 10000) {
      oled.clearBuffer();
      drawEyes(blinkHeight(30), 31, 0);
      oled.sendBuffer();
      delay(20);  // only during boot; the main loop never blocks
    }
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("To-do page: http://%s/\n", WiFi.localIP().toString().c_str());
  } else {
    WiFi.mode(WIFI_AP);
    WiFi.softAP("desk-robot");
    Serial.printf("To-do page: join Wi-Fi 'desk-robot', open http://%s/\n", WiFi.softAPIP().toString().c_str());
  }
}

// ---- main ---------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  Wire.begin(PIN_SDA, PIN_SCL);
  oled.begin();
  prefs.begin("robot", false);
  loadTodos();
  randomSeed(esp_random());
  nextBlink = millis() + 1500;
  setupWifi();
  setupWeb();
  lastWater = millis();
}

void loop() {
  server.handleClient();
  uint32_t now = millis();

  // BOOT button: start or cancel the focus timer; dismiss the water reminder.
  if (buttonPressed()) {
    if (mode == Mode::Water) {
      mode = Mode::Face;
      lastWater = now;
    } else if (mode == Mode::Focus) {
      mode = Mode::Face;
    } else {
      mode = Mode::Focus;
      focusStart = now;
    }
  }

  if (mode == Mode::Focus && now - focusStart >= FOCUS_MS) mode = Mode::Face;
  if (mode == Mode::Face && now - lastWater >= WATER_EVERY_MS) mode = Mode::Water;

  // Natural blinks every 3-5 s, glances every 4-8 s.
  if (now >= nextBlink) {
    blinkStart = now;
    nextBlink = now + random(3000, 5000);
  }
  if (now >= nextGlance) {
    lookTarget = random(0, 3) == 0 ? 0 : (random(0, 2) ? 10 : -10);
    nextGlance = now + random(4000, 8000);
  }
  if (lookX != lookTarget) lookX += (lookTarget > lookX) ? 2 : -2;

  oled.clearBuffer();
  switch (mode) {
    case Mode::Face:
      drawFace();
      drawNextTodo();
      break;
    case Mode::Focus:
      drawFocus();
      break;
    case Mode::Water:
      drawWater();
      break;
  }
  oled.sendBuffer();
}
