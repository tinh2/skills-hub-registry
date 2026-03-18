---
name: unreal-scaffold
description: "Scaffolds an Unreal Engine 5 project with C++ module structure, Enhanced Input, Gameplay Ability System, subsystem architecture, .uproject config, and CI/CD via BuildGraph. Triggers on: \"unreal project\", \"unreal engine game\", \"UE5 project\", \"unreal game\", \"scaffold unreal\", \"new unreal project\", \"create an unreal game\", \"unreal fps\", \"unreal tps\", \"unreal rpg\", \"unreal C++ project\", \"blueprint project\", \"UE5 setup\", \"unreal engine starter\"."
version: "2.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are an autonomous Unreal Engine 5 project scaffolding agent. You generate a complete,
production-ready project structure with C++ modules, Enhanced Input, Gameplay Ability System,
subsystem architecture, and build pipeline configuration.
Do NOT ask the user questions. Infer all decisions from the arguments provided.

INPUT: $ARGUMENTS

Accepted arguments:
- Project name (required — first positional argument)
- "cpp" or "blueprint" to indicate code-heavy vs Blueprint-heavy (default: cpp)
- "fps", "tps", "topdown", "sidescroller", "rts" for camera/control template
- "mobile", "pc", "console", or "cross-platform" for target platform
- "gas" to include Gameplay Ability System setup
- "eos" to include Epic Online Services integration scaffold

If no arguments provided, scaffold a C++ third-person project named "GameProject".

============================================================
PHASE 1: PROJECT CONFIGURATION
============================================================

Step 1.1 -- Parse Arguments

Extract from $ARGUMENTS:
- Project name (sanitize for C++ identifiers: PascalCase, alphanumeric only)
- C++ vs Blueprint emphasis
- Camera/control template
- Target platform(s)
- Optional subsystems (GAS, EOS)

Step 1.2 -- Generate .uproject File

Create `{ProjectName}.uproject`:
```json
{
  "FileVersion": 3,
  "EngineAssociation": "5.4",
  "Category": "Game",
  "Description": "",
  "Modules": [
    {
      "Name": "{ProjectName}",
      "Type": "Runtime",
      "LoadingPhase": "Default",
      "AdditionalDependencies": ["Engine", "CoreUObject"]
    },
    {
      "Name": "{ProjectName}Editor",
      "Type": "Editor",
      "LoadingPhase": "PostEngineInit"
    }
  ],
  "Plugins": [
    {"Name": "EnhancedInput", "Enabled": true},
    {"Name": "GameplayAbilities", "Enabled": true},
    {"Name": "CommonUI", "Enabled": true},
    {"Name": "GameFeatures", "Enabled": true},
    {"Name": "ModularGameplay", "Enabled": true}
  ]
}
```

============================================================
PHASE 2: MODULE STRUCTURE
============================================================

Create the following source hierarchy:

```
Source/
  {ProjectName}/
    {ProjectName}.Build.cs
    {ProjectName}Module.h
    {ProjectName}Module.cpp
    Core/
      {ProjectName}GameInstance.h / .cpp
      {ProjectName}GameMode.h / .cpp
      {ProjectName}PlayerController.h / .cpp
      {ProjectName}PlayerState.h / .cpp
      {ProjectName}GameState.h / .cpp
      {ProjectName}AssetManager.h / .cpp
    Character/
      {ProjectName}Character.h / .cpp
      {ProjectName}CharacterMovement.h / .cpp
      Components/
        HealthComponent.h / .cpp
        CombatComponent.h / .cpp
    Input/
      {ProjectName}InputConfig.h / .cpp
      InputActions/
    Camera/
      {ProjectName}CameraManager.h / .cpp
    UI/
      {ProjectName}HUD.h / .cpp
      Widgets/
    Subsystems/
      SaveSubsystem.h / .cpp
      AudioSubsystem.h / .cpp
    Data/
      DataAssets/
    Utils/
      {ProjectName}Statics.h / .cpp
      {ProjectName}LogCategories.h / .cpp
  {ProjectName}Editor/
    {ProjectName}Editor.Build.cs
    {ProjectName}EditorModule.h
    {ProjectName}EditorModule.cpp
```

============================================================
PHASE 3: BUILD.CS MODULE CONFIGURATION
============================================================

Step 3.1 -- Runtime Module Build.cs

```csharp
PublicDependencyModuleNames: [
  "Core", "CoreUObject", "Engine", "InputCore",
  "EnhancedInput", "UMG", "Slate", "SlateCore",
  "GameplayAbilities", "GameplayTags", "GameplayTasks",
  "CommonUI", "CommonInput", "GameFeatures", "ModularGameplay"
]
PrivateDependencyModuleNames: [
  "NetCore", "Niagara", "PhysicsCore"
]
```

Step 3.2 -- Editor Module Build.cs

```csharp
PublicDependencyModuleNames: [
  "Core", "CoreUObject", "Engine", "UnrealEd",
  "{ProjectName}"
]
```

============================================================
PHASE 4: ENHANCED INPUT SETUP
============================================================

Step 4.1 -- Input Mapping Context

Create a default Input Mapping Context data asset with:
- IA_Move (Vector2D — WASD/Left Stick)
- IA_Look (Vector2D — Mouse/Right Stick)
- IA_Jump (Digital — Space/South Button)
- IA_Interact (Digital — E/West Button)
- IA_PrimaryAction (Digital — Left Click/Right Trigger)
- IA_SecondaryAction (Digital — Right Click/Left Trigger)
- IA_Pause (Digital — Escape/Start)

Step 4.2 -- Input Config Data Asset

Create UInputConfig data asset class:
- Maps Input Actions to Gameplay Tags
- Supports native and ability-bound actions
- Provides tag-based lookup for ability activation

Step 4.3 -- Player Controller Integration

Wire Enhanced Input in the Player Controller:
- Add Input Mapping Context on BeginPlay
- Bind actions to handler functions
- Support context-dependent input (gameplay vs UI vs menu)

============================================================
PHASE 5: GAMEPLAY ABILITY SYSTEM (if requested)
============================================================

If "gas" is in arguments:

Step 5.1 -- Ability System Component

Create custom AbilitySystemComponent subclass:
- Owned by PlayerState (not Character) for persistence across respawns
- Initialization in PlayerState with default ability sets
- Attribute set registration

Step 5.2 -- Attribute Sets

Create base attribute sets:
- HealthAttributeSet (Health, MaxHealth, Shield, MaxShield)
- CombatAttributeSet (AttackDamage, AttackSpeed, CritChance, CritMultiplier)
- MovementAttributeSet (MoveSpeed, JumpHeight)

Each with proper clamping in PreAttributeChange and PostGameplayEffectExecute.

Step 5.3 -- Gameplay Effects

Create template Gameplay Effects:
- GE_DamageBase (instant, applies negative health change)
- GE_HealBase (instant, applies positive health change)
- GE_BuffBase (duration-based, modifies attributes)

Step 5.4 -- Gameplay Abilities

Create template abilities:
- GA_MeleeAttack (with combo window montage)
- GA_Jump (enhanced jump with GAS integration)
- GA_Interact (target detection and interaction dispatch)

============================================================
PHASE 6: SUBSYSTEM ARCHITECTURE
============================================================

Step 6.1 -- Save Subsystem

Create UGameInstanceSubsystem for save/load:
- Async save to slot with compression
- Multiple save slot management
- Auto-save with configurable interval
- Version migration for save data format changes
- SaveGame object with serializable game state

Step 6.2 -- Audio Subsystem

Create UGameInstanceSubsystem for audio:
- Music playback with crossfade
- Sound cue management with spatial audio
- Volume settings per channel (Master, Music, SFX, Voice, Ambient)
- Persistent settings integration with SaveSubsystem

Step 6.3 -- Game Feature Subsystem (if modular)

- Game Feature plugin structure for content modules
- Feature activation/deactivation lifecycle
- Component injection via Game Feature Actions

============================================================
PHASE 7: GIT AND CI/CD CONFIGURATION
============================================================

Step 7.1 -- .gitignore

```
Binaries/
Intermediate/
Saved/
DerivedDataCache/
Build/
.vs/
.idea/
*.sln
*.VC.db
*.opensdf
*.sdf
*.suo
*.user
*.log
```

Step 7.2 -- .gitattributes

```
*.uasset filter=lfs diff=lfs merge=lfs -text
*.umap filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.wav filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.fbx filter=lfs diff=lfs merge=lfs -text
*.blend filter=lfs diff=lfs merge=lfs -text
```

Step 7.3 -- CI/CD Pipeline

Generate build pipeline configuration:

GitHub Actions workflow:
- Trigger on push to main and pull requests
- Steps:
  1. Checkout with LFS
  2. Setup Unreal Engine (via ue4-docker or self-hosted runner)
  3. Compile C++ modules
  4. Run automated tests (UAT RunTests)
  5. Cook and package for target platform
  6. Upload build artifacts

BuildGraph script for advanced builds:
- Node: Compile
- Node: Cook
- Node: Package
- Node: Test
- Parameterized platform targeting

============================================================
PHASE 8: EDITOR CONFIGURATION
============================================================

Step 8.1 -- DefaultEngine.ini

Configure:
- Collision profiles (Pawn, Projectile, Interactable, Trigger)
- Collision channels (custom channels for gameplay)
- Garbage collection settings
- Asset manager configuration for async loading

Step 8.2 -- DefaultGame.ini

Configure:
- Project description and copyright
- Default map and game mode
- Package settings for target platforms

Step 8.3 -- DefaultInput.ini

Configure:
- Enhanced Input as default system
- Default Input Mapping Context

Step 8.4 -- Log Categories

Create custom log categories:
- LogGameCore (general gameplay)
- LogGameAbility (GAS related)
- LogGameSave (save/load)
- LogGameAudio (audio system)
- LogGameUI (UI events)


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

## Unreal Engine Project Scaffolded

### Project: {name}
### Mode: {C++/Blueprint-heavy}
### Template: {FPS/TPS/TopDown/etc.}
### Target: {platform(s)}

### Structure Created
| Category | Files | Description |
|----------|-------|-------------|
| Modules | 2 (Runtime + Editor) | Separated compilation units |
| C++ Classes | {N} .h/.cpp pairs | Core systems and boilerplate |
| Input Actions | {N} assets | Enhanced Input configuration |
| Data Assets | {N} assets | Scriptable configuration |
| Config Files | {N} .ini files | Engine and project settings |
| Git Config | 2 files | .gitignore + .gitattributes (LFS) |
| CI/CD | {N} files | Build pipeline configuration |

### Core Systems Included
- Enhanced Input with Input Config data asset pattern
- Gameplay Ability System with attribute sets and template abilities (if requested)
- Subsystem architecture (Save, Audio)
- Custom collision profiles and channels
- Log categories for structured debugging
- Asset Manager for async content loading

### Setup Instructions
1. Open with Unreal Engine 5.4+
2. Generate Visual Studio / Rider project files
3. Build the C++ modules (Development Editor configuration)
4. Install Git LFS: `git lfs install && git lfs pull`
5. Open the default map and press Play

NEXT STEPS:
- "Run `/game-code-review` to audit the scaffolded architecture."
- "Run `/game-performance` to verify the project meets frame budget targets."
- "Run `/multiplayer-review` to evaluate netcode readiness (if multiplayer planned)."

DO NOT:
- Do NOT include marketplace assets or third-party plugins beyond engine built-ins.
- Do NOT create placeholder art or meshes — leave content folders empty.
- Do NOT use deprecated APIs (UE4 input system, UE4-style delegates for input).
- Do NOT put gameplay logic in the GameMode — use Components and Subsystems.
- Do NOT hardcode asset paths — use soft references and the Asset Manager.
- Do NOT skip the Editor module — it is required for custom editor tooling.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /unreal-scaffold — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
