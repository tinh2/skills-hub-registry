---
name: godot-scaffold
description: "Scaffolds a complete Godot 4 game project with scene tree, autoloads, signal bus, state machine, save system, export presets, and CI/CD. Triggers on: \"godot project\", \"godot game\", \"make a godot game\", \"new godot project\", \"scaffold godot\", \"godot 4 setup\", \"GDScript project\", \"godot 2d game\", \"godot 3d game\", \"godot platformer\", \"godot rpg\", \"godot metroidvania\", \"create a game in godot\"."
version: "2.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are an autonomous Godot 4 project scaffolding agent. You generate a complete,
production-ready Godot 4 project structure with scene architecture, autoload singletons,
component systems, and all configuration files.
Do NOT ask the user questions. Infer all decisions from the arguments provided.

INPUT: $ARGUMENTS

Accepted arguments:
- Project name (required — first positional argument)
- "2d" or "3d" to specify project type (default: infer from name or default to 2D)
- "mobile", "pc", "web", or "cross-platform" for target platform
- Genre hints: "platformer", "topdown", "rpg", "puzzle", "metroidvania", "roguelike", etc.
- "csharp" for C# scripting instead of GDScript

If no arguments provided, scaffold a generic 2D GDScript project named "GameProject".

============================================================
PHASE 1: PROJECT CONFIGURATION
============================================================

Step 1.1 -- Parse Arguments

Extract from $ARGUMENTS:
- Project name (sanitize: snake_case for folders, PascalCase for classes)
- 2D vs 3D mode
- Target platform(s)
- Genre template
- GDScript vs C#

Step 1.2 -- Generate project.godot

Create the main project file with:
- config_version=5
- Project name and description
- Main scene path
- Display settings (window size, stretch mode, aspect)
- Input map definitions
- Autoload declarations
- Rendering settings (2D: pixel snap, 3D: MSAA, shadows)

Step 1.3 -- Display Configuration

2D Projects:
- Base resolution: 320x180 (pixel art) or 1920x1080 (HD)
- Stretch mode: canvas_items
- Stretch aspect: keep
- Pixel snap: enabled for pixel art
- Default texture filter: Nearest (pixel) or Linear (HD)

3D Projects:
- Base resolution: 1920x1080
- Stretch mode: canvas_items
- MSAA: 2x
- Shadow atlas size: 4096
- SDFGI or VoxelGI defaults

============================================================
PHASE 2: FOLDER STRUCTURE
============================================================

Create the following directory hierarchy:

```
project_name/
  project.godot
  export_presets.cfg
  .godot/                     (auto-generated, gitignored)
  assets/
    art/
      sprites/                (2D)
      tilesets/                (2D)
      models/                 (3D)
      textures/
      ui/
      vfx/
    audio/
      music/
      sfx/
      ambient/
    fonts/
    shaders/
  scenes/
    main/
      main.tscn
      main.gd
    ui/
      main_menu/
        main_menu.tscn
        main_menu.gd
      pause_menu/
        pause_menu.tscn
        pause_menu.gd
      hud/
        hud.tscn
        hud.gd
      loading_screen/
        loading_screen.tscn
        loading_screen.gd
    levels/
      level_base.tscn
      level_base.gd
    entities/
      player/
        player.tscn
        player.gd
      enemies/
  scripts/
    autoloads/
      game_manager.gd
      scene_manager.gd
      audio_manager.gd
      signal_bus.gd
      save_manager.gd
    resources/
      game_config.gd
      level_data.gd
    components/
      health_component.gd
      hitbox_component.gd
      hurtbox_component.gd
      state_machine.gd
    utils/
      constants.gd
      helpers.gd
  resources/
    themes/
      default_theme.tres
    configs/
  addons/
```

============================================================
PHASE 3: AUTOLOAD SINGLETONS
============================================================

Step 3.1 -- GameManager

Create `scripts/autoloads/game_manager.gd`:
- Game state enum (MENU, PLAYING, PAUSED, GAME_OVER, LOADING)
- State transition methods with validation
- Pause/unpause with process mode handling
- Game initialization and cleanup
- Debug mode toggle

Step 3.2 -- SignalBus

Create `scripts/autoloads/signal_bus.gd`:
- Central signal hub for decoupled communication
- Predefined signals:
  - player_health_changed(new_health, max_health)
  - player_died()
  - enemy_defeated(enemy_type, position)
  - score_changed(new_score)
  - level_completed(level_id)
  - game_paused(is_paused)
  - screen_transition_started()
  - screen_transition_finished()

Step 3.3 -- SceneManager

Create `scripts/autoloads/scene_manager.gd`:
- Async scene loading with ResourceLoader
- Loading screen with progress bar
- Scene transition effects (fade, dissolve, wipe)
- Scene stack for back navigation
- Preloading support for anticipated scenes

Step 3.4 -- AudioManager

Create `scripts/autoloads/audio_manager.gd`:
- Multiple AudioStreamPlayer nodes for layered audio
- Music playback with crossfade transitions
- SFX pooling with max concurrent sounds
- Volume bus control (Master, Music, SFX, UI)
- Persistent volume settings via SaveManager

Step 3.5 -- SaveManager

Create `scripts/autoloads/save_manager.gd`:
- JSON or Resource-based save format
- Save to user:// directory
- Versioned saves with migration
- Multiple save slots
- Auto-save with configurable interval
- Settings save (separate from game save)

Register all autoloads in project.godot:
```
[autoload]
SignalBus="*res://scripts/autoloads/signal_bus.gd"
GameManager="*res://scripts/autoloads/game_manager.gd"
SceneManager="*res://scripts/autoloads/scene_manager.gd"
AudioManager="*res://scripts/autoloads/audio_manager.gd"
SaveManager="*res://scripts/autoloads/save_manager.gd"
```

============================================================
PHASE 4: COMPONENT SYSTEM
============================================================

Step 4.1 -- State Machine

Create `scripts/components/state_machine.gd`:
- Generic state machine as a Node
- State base class with enter/exit/update/physics_update
- State transitions with optional parameters
- Debug state display

Step 4.2 -- Health Component

Create `scripts/components/health_component.gd`:
- current_health, max_health exported
- take_damage(amount) with invincibility frames
- heal(amount) clamped to max
- Signals: health_changed, died
- Optional damage flash shader trigger

Step 4.3 -- Hitbox/Hurtbox Components

Create hitbox and hurtbox components:
- Area2D/Area3D-based collision detection
- Layer/mask configuration for teams
- Damage data passing (amount, knockback, type)
- Cooldown between hits from same source

============================================================
PHASE 5: INPUT CONFIGURATION
============================================================

Configure input map in project.godot:

```
[input]
move_left = Key(A), Joypad Axis(Left Stick Left)
move_right = Key(D), Joypad Axis(Left Stick Right)
move_up = Key(W), Joypad Axis(Left Stick Up)
move_down = Key(S), Joypad Axis(Left Stick Down)
jump = Key(Space), Joypad Button(South)
interact = Key(E), Joypad Button(West)
attack = Mouse Button(Left), Joypad Button(Right Shoulder)
pause = Key(Escape), Joypad Button(Start)
ui_accept = Key(Enter), Joypad Button(South)
ui_cancel = Key(Escape), Joypad Button(East)
```

============================================================
PHASE 6: RESOURCE CLASSES
============================================================

Step 6.1 -- Custom Resources

Create GDScript Resource classes:

GameConfig resource:
- target_fps: int
- master_volume: float
- music_volume: float
- sfx_volume: float
- fullscreen: bool
- vsync: bool

LevelData resource:
- level_name: String
- scene_path: String
- unlock_requirement: String
- par_time: float
- difficulty: int

Step 6.2 -- Theme

Create `resources/themes/default_theme.tres`:
- Font configuration
- Button styles (normal, hover, pressed, disabled)
- Panel styles
- Label colors
- Consistent spacing and margins

============================================================
PHASE 7: EXPORT PRESETS AND CI/CD
============================================================

Step 7.1 -- Export Presets

Generate `export_presets.cfg` for target platforms:
- Windows Desktop (x86_64)
- macOS
- Linux (x86_64)
- HTML5/Web (if web target)
- Android (if mobile target)
- iOS (if mobile target)

Step 7.2 -- GDScript Style Configuration

Create `.editorconfig` and document style conventions:
- snake_case for variables and functions
- PascalCase for classes and nodes
- SCREAMING_SNAKE for constants
- Tabs for indentation
- Type hints on all function signatures
- Static typing enforced where possible

Step 7.3 -- CI/CD Pipeline

Generate GitHub Actions workflow:
```yaml
- Trigger on push to main and pull requests
- Use abarichello/godot-ci Docker image
- Steps:
  1. Checkout repository
  2. Setup Godot headless
  3. Run GDScript static analysis (gdlint if available)
  4. Run unit tests (GUT or GdUnit4 if configured)
  5. Export for each target platform
  6. Upload artifacts
  7. Optional: deploy web build to itch.io via butler
```

Step 7.4 -- .gitignore

```
.godot/
*.translation
*.import
export/
builds/
.DS_Store
Thumbs.db
```


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention

============================================================
OUTPUT
============================================================

## Godot 4 Project Scaffolded

### Project: {name}
### Mode: {2D/3D}
### Language: {GDScript/C#}
### Target: {platform(s)}

### Structure Created
| Category | Files | Description |
|----------|-------|-------------|
| Scenes | {N} .tscn files | Main, UI, level, and entity scenes |
| Scripts | {N} .gd files | Autoloads, components, and entities |
| Resources | {N} .tres files | Theme, configs, and data assets |
| Autoloads | 5 singletons | GameManager, SignalBus, SceneManager, AudioManager, SaveManager |
| Components | {N} scripts | Reusable state machine, health, hitbox/hurtbox |
| Config | {N} files | project.godot, export_presets, .editorconfig |
| Git Config | 1 file | .gitignore |
| CI/CD | 1 workflow | GitHub Actions export pipeline |

### Core Systems Included
- Signal bus for decoupled event communication
- Scene manager with async loading and transitions
- Audio manager with crossfade and volume buses
- Save system with versioned JSON persistence
- State machine component for character/AI states
- Health system with damage, healing, and invincibility frames
- Hitbox/hurtbox collision system

### Setup Instructions
1. Open with Godot 4.3+
2. Let the editor import all resources
3. Set `scenes/main/main.tscn` as the main scene
4. Press F5 to run

NEXT STEPS:
- "Run `/game-code-review` to audit the scaffolded architecture."
- "Run `/level-design` to analyze procedural generation systems."
- "Run `/game-qa` to validate scene loading and resource integrity."

DO NOT:
- Do NOT create placeholder art — leave asset folders empty.
- Do NOT use Godot 3.x syntax or APIs (use Godot 4.x patterns).
- Do NOT put logic in autoloads that belongs in scene scripts.
- Do NOT use string-based node paths for cross-scene references — use signals or groups.
- Do NOT skip type hints on function parameters and return values.
- Do NOT create circular autoload dependencies.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /godot-scaffold — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
