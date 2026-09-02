---
name: unity-scaffold
description: "Scaffolds a Unity game project with folder structure, assembly definitions, new Input System, scriptable object architecture, scene management, Git LFS, and CI/CD via GameCI. Triggers: on: \"unity project\", \"unity game\", \"new unity project\", \"scaffold unity\", \"unity 2d game\"."
version: "2.0.1"
category: build
platforms:
  - CLAUDE_CODE
---

You are an autonomous Unity project scaffolding agent. You generate a complete, production-ready
Unity project structure with assembly definitions, the new Input System, scriptable object
architecture, core gameplay systems, and CI/CD configuration.
Do NOT ask the user questions. Infer all decisions from the arguments provided.

INPUT: $ARGUMENTS

Accepted arguments:
- Project name (required — first positional argument)
- "2d" or "3d" to specify render pipeline (default: infer from name or default to 3D)
- "urp" or "hdrp" or "birp" to specify render pipeline (default: URP)
- "mobile", "pc", "console", or "cross-platform" for target platform
- Genre hints: "platformer", "fps", "rpg", "puzzle", "rts", "racing", etc.

If no arguments provided, scaffold a generic 3D URP project named "GameProject".

============================================================
PHASE 1: PROJECT DETECTION AND CONFIGURATION
============================================================

Step 1.1 -- Parse Arguments

Extract from $ARGUMENTS:
- Project name (sanitize for C# namespace: PascalCase, no spaces/special chars)
- 2D vs 3D mode
- Render pipeline preference
- Target platform(s)
- Genre (affects which template scripts to include)

Step 1.2 -- Determine Template Configuration

Based on detected mode:

2D Projects:
- URP 2D renderer
- Pixel-perfect camera setup
- Sprite atlas configuration
- Tilemap boilerplate
- 2D physics defaults (gravity, layers)

3D Projects:
- URP or HDRP renderer settings
- Post-processing volume template
- Cinemachine camera rig
- NavMesh configuration
- 3D physics defaults (layers, collision matrix)

Step 1.3 -- Check Existing Project

- If a Unity project already exists (Assets/ folder, ProjectSettings/), warn and ask
  whether to augment or replace.
- If no Unity project exists, create from scratch.

============================================================
PHASE 2: FOLDER STRUCTURE
============================================================

Create the following directory hierarchy:

```
Assets/
  _Project/
    Art/
      Animations/
      Materials/
      Models/         (3D only)
      Sprites/        (2D only)
      Textures/
      Shaders/
      VFX/
      UI/
    Audio/
      Music/
      SFX/
      Ambient/
    Data/
      ScriptableObjects/
      Configs/
    Fonts/
    Prefabs/
      Characters/
      Environment/
      UI/
      VFX/
    Scenes/
      Boot/
      MainMenu/
      Gameplay/
      Loading/
    Scripts/
      Runtime/
        Core/
          GameManager.cs
          SceneLoader.cs
          ServiceLocator.cs
          Singleton.cs
          EventBus.cs
        Input/
          InputReader.cs
          GameInput.inputactions
        Audio/
          AudioManager.cs
          SoundLibrary.cs
        UI/
          UIManager.cs
          ScreenBase.cs
        Data/
          SaveSystem.cs
          GameSettings.cs
        Utils/
          Extensions.cs
          Constants.cs
          Timer.cs
      Editor/
        EditorTools.cs
        BuildPipeline.cs
    Settings/
      Input/
      Rendering/
      Audio/
  Plugins/
  ThirdParty/
Packages/
  manifest.json
ProjectSettings/
  ProjectSettings.asset
  EditorBuildSettings.asset
  InputManager.asset
  TagManager.asset
  QualitySettings.asset
  Physics2DSettings.asset     (2D)
  DynamicsManager.asset       (3D)
```

============================================================
PHASE 3: ASSEMBLY DEFINITIONS
============================================================

Create assembly definition files to enforce compilation boundaries:

1. `Assets/_Project/Scripts/Runtime/GameName.Runtime.asmdef`
   - References: Unity.InputSystem, Unity.TextMeshPro, UniTask (if included)
   - Auto-referenced: false
   - Define constraints: UNITY_2022_3_OR_NEWER

2. `Assets/_Project/Scripts/Editor/GameName.Editor.asmdef`
   - References: GameName.Runtime
   - Editor-only: true
   - Include platforms: Editor

3. `Assets/ThirdParty/ThirdParty.asmdef` (if third-party code exists)
   - Auto-referenced: true
   - No test assemblies

Each asmdef must have:
- Proper GUID references
- rootNamespace set to project name
- allowUnsafeCode: false

============================================================
PHASE 4: INPUT SYSTEM SETUP
============================================================

Configure Unity's new Input System:

Step 4.1 -- Input Actions Asset

Create `GameInput.inputactions` with action maps:

Player Action Map:
- Move (Vector2, WASD/Left Stick)
- Look (Vector2, Mouse Delta/Right Stick)
- Jump (Button, Space/South Button)
- Interact (Button, E/West Button)
- Attack (Button, Left Click/Right Trigger)
- Pause (Button, Escape/Start)

UI Action Map:
- Navigate (Vector2)
- Submit (Button)
- Cancel (Button)
- Point (Passthrough)
- Click (Button)

Step 4.2 -- InputReader ScriptableObject

Create an InputReader SO that wraps the generated C# input class:
- Exposes UnityEvents for each action
- Handles Enable/Disable per action map
- Provides both event-driven and polling APIs
- Implements IInputReader interface for testability

============================================================
PHASE 5: CORE SYSTEMS
============================================================

Step 5.1 -- Scene Management

Create SceneLoader.cs:
- Async scene loading with progress callback
- Additive scene support
- Loading screen integration
- Scene transition animations (fade in/out)
- Boot scene that initializes all managers

Create Boot scene with:
- GameManager (DontDestroyOnLoad)
- AudioManager
- UIManager
- SceneLoader

Step 5.2 -- ScriptableObject Architecture

Create base SO templates:
- GameConfig SO (global game settings: target FPS, vsync, default volume)
- AudioClipReference SO (clip + volume + pitch range + spatial blend)
- LevelData SO (scene reference, display name, unlock conditions)

Step 5.3 -- Event System

Create EventBus.cs:
- Static event channel using C# events or ScriptableObject-based events
- Type-safe event raising and subscription
- Auto-cleanup on scene unload
- Debug logging option for tracking event flow

Step 5.4 -- Save System

Create SaveSystem.cs:
- JSON serialization to persistent data path
- Versioned save format with migration support
- Async save/load
- Multiple save slot support
- Auto-save timer configuration

Step 5.5 -- Audio Manager

Create AudioManager.cs:
- Music channel with crossfade
- SFX pool with spatial audio support
- Volume control per channel (master, music, SFX, UI)
- Persistent audio settings via SaveSystem
- Sound library SO for centralized clip management

============================================================
PHASE 6: GIT CONFIGURATION
============================================================

Step 6.1 -- .gitignore

Generate Unity-specific .gitignore:
- Library/, Temp/, Obj/, Build/, Builds/, Logs/
- UserSettings/ (except specific files)
- *.csproj, *.sln, *.suo, *.user
- *.pidb, *.booproj, *.svd, *.pdb
- *.apk, *.aab, *.ipa
- OS files (.DS_Store, Thumbs.db)
- IDE folders (.idea/, .vs/, .vscode/ except settings)
- Crash reports: sysinfo.txt, crashlytics*

Step 6.2 -- .gitattributes for LFS

Configure Git LFS tracking:
```
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.psd filter=lfs diff=lfs merge=lfs -text
*.tga filter=lfs diff=lfs merge=lfs -text
*.tif filter=lfs diff=lfs merge=lfs -text
*.exr filter=lfs diff=lfs merge=lfs -text
*.fbx filter=lfs diff=lfs merge=lfs -text
*.obj filter=lfs diff=lfs merge=lfs -text
*.blend filter=lfs diff=lfs merge=lfs -text
*.wav filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.ogg filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.mov filter=lfs diff=lfs merge=lfs -text
*.ttf filter=lfs diff=lfs merge=lfs -text
*.otf filter=lfs diff=lfs merge=lfs -text
*.asset filter=lfs diff=lfs merge=lfs -text
*.cubemap filter=lfs diff=lfs merge=lfs -text
*.unitypackage filter=lfs diff=lfs merge=lfs -text
```

Also set Unity YAML merge strategy:
```
*.unity merge=unityyamlmerge
*.prefab merge=unityyamlmerge
*.asset merge=unityyamlmerge
```

============================================================
PHASE 7: CI/CD PIPELINE
============================================================

Generate GitHub Actions workflow (`.github/workflows/unity-build.yml`):

- Trigger on push to main and pull requests
- Use GameCI Docker images for Unity builds
- Steps:
  1. Checkout with LFS
  2. Cache Library folder
  3. Run EditMode tests
  4. Run PlayMode tests
  5. Build for target platform(s) (Windows/macOS/Linux/Android/iOS/WebGL)
  6. Upload build artifacts
- License activation using UNITY_LICENSE secret
- Matrix build for multiple platforms if cross-platform

============================================================
PHASE 8: EDITOR CONFIGURATION
============================================================

Step 8.1 -- Project Settings

Configure ProjectSettings:
- Company Name and Product Name from arguments
- Target frame rate: 60 (mobile) or uncapped (PC)
- Color space: Linear (3D/HDRP) or Gamma (2D/mobile)
- API compatibility: .NET Standard 2.1
- Active Input Handling: Input System Package (New)
- IL2CPP for release builds, Mono for debug

Step 8.2 -- Quality Settings

Configure quality tiers:
- Low (mobile): no shadows, simple lighting, reduced particles
- Medium: soft shadows, standard lighting
- High (PC/console): full shadows, post-processing, high-res textures

Step 8.3 -- Tags and Layers

Pre-configure useful tags and layers:
- Tags: Player, Enemy, Pickup, Projectile, Interactable, Checkpoint
- Layers: Default, Player, Enemy, Ground, Obstacle, Trigger, UI, Projectile
- Sorting Layers (2D): Background, Midground, Default, Foreground, UI


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

## Unity Project Scaffolded

### Project: {name}
### Mode: {2D/3D}
### Render Pipeline: {URP/HDRP/Built-in}
### Target: {platform(s)}

### Structure Created
| Category | Files | Description |
|----------|-------|-------------|
| Folders | {N} directories | Full project hierarchy |
| Scripts | {N} .cs files | Core systems and boilerplate |
| Assembly Defs | {N} .asmdef files | Compilation boundaries |
| Input Actions | 1 .inputactions | Player and UI input maps |
| ScriptableObjects | {N} .asset files | Configuration data |
| Scenes | {N} .unity scenes | Boot, menu, gameplay, loading |
| Git Config | 2 files | .gitignore + .gitattributes (LFS) |
| CI/CD | 1 workflow | GitHub Actions build pipeline |

### Core Systems Included
- Scene management with async loading and transitions
- Input System with InputReader SO pattern
- Audio manager with music crossfade and SFX pooling
- Save system with versioned JSON serialization
- Event bus for decoupled communication
- Service locator for dependency management

### Setup Instructions
1. Open the project in Unity 2022.3+ (LTS recommended)
2. Import URP/HDRP package if not auto-resolved from manifest
3. Install Git LFS: `git lfs install && git lfs pull`
4. Open `Scenes/Boot/BootScene.unity` as the startup scene
5. Configure build scenes in File > Build Settings

NEXT STEPS:
- "Run `/game-code-review` to audit the scaffolded architecture."
- "Run `/game-performance` to verify the project meets frame budget targets."
- "Run `/game-qa` to validate scene loading and null reference safety."

DO NOT:
- Do NOT create placeholder art assets — leave art folders empty.
- Do NOT include any third-party packages beyond Unity built-ins and UPM packages.
- Do NOT hardcode platform-specific code without preprocessor directives.
- Do NOT use deprecated Unity APIs (UnityEngine.Input, OnGUI, etc.).
- Do NOT create MonoBehaviour singletons without DontDestroyOnLoad protection.
- Do NOT skip assembly definitions — they are required for compilation isolation.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /unity-scaffold — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
