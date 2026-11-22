---
name: esp32-desk-robot
description: "Build a tiny desk robot with an ESP32 and a 1.3 inch OLED face, then add features one prompt at a time: blinking eyes, a 25-minute focus timer, a to-do list you edit from your phone, a drink-water reminder. Ships tested starter firmware, the 4-wire wiring, flashing and troubleshooting. Triggers: 'ESP32 desk robot', 'OLED face robot', 'build a desk robot', 'Tabbie', 'make my ESP32 show eyes', 'ESP32 focus timer'."
version: "1.0.0"
category: build
platforms:
  - CLAUDE_CODE
tags: [esp32, oled, arduino, platformio, hardware, maker, embedded]
---

# ESP32 Desk Robot

Help the user build a small desk robot: an ESP32 board and a 1.3" I2C OLED
screen showing a face, in a printed case. You set up the project, flash a
working face first, then add one feature per request so they always have
something that works.

Inspired by Tabbie, the open-source desk robot by Lloyd December
(github.com/lloyd-december/tabbie). This skill's firmware is an independent
starter written for it; credit his project if the user shares their build.

## Parts (about $18)

- ESP32 dev board with USB-C (ESP32-WROOM-32 "DevKit", usually with a CP2102 or CH340 USB chip)
- 1.3" I2C OLED, 128x64, 4 pins (almost always the SH1106 controller)
- 4 female-female jumper wires
- Optional: a 3D-printed case

A 0.96" OLED works too, but it uses the SSD1306 controller (see Step 3).

## Step 1: Confirm the hardware

Ask the user (or read from photos / `pio device list`) and record:

1. Board: plain ESP32 (WROOM-32), ESP32-S3 or ESP32-C3? The starter targets `esp32dev`.
   For S3/C3 change `board` in platformio.ini and pick pins that board supports for I2C.
2. Screen size and the labels printed on its 4 pins (VDD/VCC, GND, SCK/SCL, SDA).
   Pin ORDER differs between brands: always wire by label, never by position.
3. USB driver: on macOS/Windows a CP2102 board needs the Silicon Labs CP210x driver,
   a CH340 board needs the WCH driver. `pio device list` should show the port once it is installed.

## Step 2: Wire it (4 wires, no soldering if the OLED has pins)

| OLED pin  | ESP32 pin | Why                                                    |
| --------- | --------- | ------------------------------------------------------ |
| VDD / VCC | 3V3       | power (3.3 V keeps the I2C logic at the ESP32's level) |
| GND       | GND       | ground                                                 |
| SDA       | GPIO21    | I2C data                                               |
| SCK / SCL | GPIO22    | I2C clock                                              |

GPIO21/22 are the default I2C pins on ESP32-WROOM-32 DevKits. Never connect VDD to 5V
unless the module's listing says it is 5V-tolerant; 3V3 is always safe.

## Step 3: Create the project from the starter

Copy `references/firmware/` (next to this file) into the user's project folder:

```
platformio.ini            esp32dev + U8g2
src/main.cpp              face, blink, glance, focus timer, to-do web page, water reminder
src/secrets.h.example     Wi-Fi name/password template (copy to secrets.h, gitignored)
.gitignore
```

- If the screen is a 0.96" SSD1306, swap the constructor at the top of main.cpp
  (the alternative line is in the comment above it).
- If they want the to-do page on their home Wi-Fi, create `src/secrets.h` from the
  example. Without it the robot opens its own Wi-Fi network called `desk-robot`.

The starter compiles for `esp32dev` (U8g2 2.35+, Arduino framework): about 15% RAM, 73% flash.

## Step 4: Flash and check

```bash
pio run -t upload && pio device monitor
```

(If PlatformIO isn't installed: `pipx install platformio` or `python3 -m pip install --user platformio`,
or use the PlatformIO IDE extension in VS Code.)

The serial monitor prints the to-do page address. The eyes should appear within
a second and blink every 3 to 5 seconds.

## Step 5: Add features one at a time

The starter already has all four; if the user wants to build up gradually (or
customize), strip main.cpp to just the face and add these in order, flashing after
each. Keep everything non-blocking: `millis()` timers, never `delay()` in `loop()`,
so the eyes keep blinking while Wi-Fi works.

1. **Blink and glance**: random blink every 3 to 5 s (close 60 ms, hold 30, open 60),
   glance left/right every 4 to 8 s by easing an x offset.
2. **Focus timer**: the BOOT button (GPIO0, INPUT_PULLUP, active low, debounced)
   starts/cancels 25:00; show squinting eyes, an MM:SS countdown and a progress bar.
3. **To-do list**: a small web page on the robot (WebServer) to add and complete
   items, stored in Preferences so they survive power cuts; show the next item under the eyes.
4. **Water reminder**: every 30 minutes show a droplet until the button is pressed.

Good follow-ups users ask for: different expressions (happy, sleepy, love), a
"focus streak" counter, showing the time from NTP, a sound with a passive buzzer,
or a servo to nod (add a 5V servo on a PWM pin with its own power).

## Troubleshooting

| Symptom                                          | Fix                                                                                 |
| ------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Screen stays black                               | Swap SDA/SCL; check VDD on 3V3 and GND; run an I2C scan (address is usually 0x3C)   |
| Garbage column on the right / image shifted 2 px | It's an SH1106 driven as SSD1306: use the SH1106 constructor                        |
| Upload fails "Failed to connect"                 | Hold BOOT while the upload starts; try another USB cable (charge-only cables fail)  |
| No serial port appears                           | Install the CP210x or CH340 driver; try a different USB port                        |
| Eyes freeze during Wi-Fi                         | Something blocks `loop()`: remove `delay()`, keep handlers short                    |
| Board resets when the screen flashes             | Power from a better USB port/cable; add a 10 µF capacitor across the OLED's VDD/GND |

## Rules

- Wire by pin labels; never assume a pin order or GPIO numbers for boards other than WROOM-32 DevKits.
- Keep the user's Wi-Fi password in `src/secrets.h` only, never in main.cpp or a commit.
- Flash after every feature so a working state always exists.
- When the user shares the project publicly, suggest crediting Tabbie (Lloyd December) as the inspiration.

More: the full build story and parts list at https://skills-hub.ai/blog/esp32-desk-robot-claude-code-skills-2026
