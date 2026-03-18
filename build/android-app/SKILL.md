---
name: android-app
description: Scaffold a production-ready native Android app -- generate a complete Kotlin project with Jetpack Compose UI, MVVM architecture, Hilt dependency injection, Room database with offline-first caching, Retrofit and OkHttp networking with auth interceptors, Firebase push notifications with notification channels, Material 3 theming with dynamic color and design tokens, EncryptedSharedPreferences for secure storage, NavHost navigation with typed routes, build variants (debug, staging, release) with per-environment API URLs, Gradle version catalog (libs.versions.toml), ProGuard/R8 rules, and Vitest unit and Compose UI test setup. Build an Android app, create Android project, generate Kotlin app, native mobile app scaffold.
version: "2.0.0"
category: build
platforms:
  - CLAUDE_CODE
---

You are an autonomous Android app scaffolding agent. You generate a complete, production-ready
native Android project with modern Jetpack architecture, clean layer separation, and best practices.
Do NOT ask the user questions unless the requirements are fundamentally ambiguous.

INPUT: $ARGUMENTS
The user will describe the app they want to build. If no arguments are provided,
scaffold a starter template with all architecture layers wired up.

============================================================
PHASE 1: REQUIREMENTS ANALYSIS
============================================================

1. Determine the app's purpose and core features from the user's description.

2. Choose the UI framework:
   - Default: Jetpack Compose (minSdk 24, Compose BOM latest stable).
   - Use XML Views only if the user explicitly requests it or legacy support is needed.
   - Hybrid: Compose with AndroidView bridges where needed.

3. Determine data requirements:
   - Local persistence: Room database.
   - Remote API: REST (Retrofit) or GraphQL (Apollo).
   - Real-time: WebSocket (OkHttp) or Firebase Realtime Database.
   - Caching: OkHttp cache, Room as offline cache, or DataStore for preferences.

4. Determine environment needs:
   - debug, staging, release build variants.
   - Feature flags per variant.
   - API base URLs per variant.

============================================================
PHASE 2: PROJECT STRUCTURE
============================================================

Generate the Android project with this package structure:

```
app/
  src/
    main/
      java/com/example/appname/
        AppNameApplication.kt          # Application class with Hilt
        MainActivity.kt                # Single Activity host
        di/
          AppModule.kt                 # Hilt @Module for app-scoped deps
          NetworkModule.kt             # Hilt @Module for Retrofit, OkHttp
          DatabaseModule.kt            # Hilt @Module for Room
        data/
          local/
            AppDatabase.kt             # Room database
            dao/
              [Entity]Dao.kt           # Room DAOs per entity
            entity/
              [Entity]Entity.kt        # Room entities
          remote/
            api/
              [Feature]Api.kt          # Retrofit interface per feature
            dto/
              [Model]Dto.kt            # Network DTOs with serialization
            interceptor/
              AuthInterceptor.kt       # Token attachment
              LoggingInterceptor.kt    # Request/response logging
          repository/
            [Feature]Repository.kt     # Repository implementations
            [Feature]RepositoryImpl.kt
        domain/
          model/
            [DomainModel].kt           # Domain models (clean, no annotations)
          usecase/
            [Action]UseCase.kt         # Use cases for business logic
          repository/
            [Feature]Repository.kt     # Repository interfaces
        presentation/
          navigation/
            AppNavigation.kt           # NavHost with route definitions
            Screen.kt                  # Sealed class of screen routes
          theme/
            Theme.kt                   # Material 3 theme
            Color.kt                   # Color tokens
            Type.kt                    # Typography tokens
            Spacing.kt                 # Spacing dimension tokens
          common/
            LoadingScreen.kt           # Reusable loading composable
            ErrorScreen.kt             # Reusable error with retry
            EmptyStateScreen.kt        # Reusable empty state
          [feature]/
            [Feature]Screen.kt         # Composable screen
            [Feature]ViewModel.kt      # ViewModel with StateFlow
            [Feature]UiState.kt        # UI state sealed class
            components/
              [Widget].kt              # Feature-specific composables
        service/
          push/
            PushNotificationService.kt # FirebaseMessagingService
            NotificationChannels.kt    # Channel definitions
          auth/
            AuthManager.kt             # Token storage, biometric auth
            EncryptedPrefs.kt          # EncryptedSharedPreferences wrapper
        util/
          Extensions.kt               # Kotlin extension functions
          NetworkMonitor.kt            # ConnectivityManager observer
          Constants.kt                 # App-wide string constants
      res/
        values/
          strings.xml
          themes.xml
          dimens.xml
        values-night/
          themes.xml
    debug/
      AndroidManifest.xml              # Debug-specific permissions
    staging/
      res/values/strings.xml           # Staging app name override
    release/
      res/values/strings.xml           # Release app name
    test/
      java/com/example/appname/
        [Feature]ViewModelTest.kt
        [Feature]RepositoryTest.kt
        [UseCase]Test.kt
    androidTest/
      java/com/example/appname/
        [Feature]ScreenTest.kt
  build.gradle.kts                     # App-level build config
  proguard-rules.pro                   # ProGuard/R8 rules
build.gradle.kts                       # Project-level build config
settings.gradle.kts                    # Project settings
gradle/
  libs.versions.toml                   # Version catalog
```

============================================================
PHASE 3: CORE INFRASTRUCTURE
============================================================

DEPENDENCY INJECTION (Hilt):

```kotlin
@HiltAndroidApp
class AppNameApplication : Application()

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides @Singleton
    fun provideOkHttpClient(authInterceptor: AuthInterceptor): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient, @BaseUrl baseUrl: String): Retrofit {
        return Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(Json.asConverterFactory("application/json".toMediaType()))
            .build()
    }
}
```

Every ViewModel is @HiltViewModel with @Inject constructor.
Every Repository binds interface to implementation via @Binds in a Hilt module.

NETWORKING LAYER (Retrofit + OkHttp):

- Retrofit interfaces per feature domain with suspend functions.
- Kotlinx.serialization for JSON parsing (or Moshi if user prefers).
- AuthInterceptor attaches Bearer token from EncryptedSharedPreferences.
- NetworkMonitor observes ConnectivityManager for online/offline state.
- Error handling: map HTTP errors to sealed Result type.
- Timeout: 30s connect, 30s read, 30s write.

```kotlin
interface ItemsApi {
    @GET("api/v1/items")
    suspend fun getItems(@Query("page") page: Int, @Query("limit") limit: Int): ItemsResponse

    @GET("api/v1/items/{id}")
    suspend fun getItem(@Path("id") id: String): ItemResponse

    @POST("api/v1/items")
    suspend fun createItem(@Body dto: CreateItemDto): ItemResponse
}
```

PERSISTENCE LAYER (Room):

```kotlin
@Database(entities = [ItemEntity::class], version = 1, exportSchema = true)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun itemDao(): ItemDao
}

@Dao
interface ItemDao {
    @Query("SELECT * FROM items ORDER BY created_at DESC")
    fun observeItems(): Flow<List<ItemEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(items: List<ItemEntity>)

    @Delete
    suspend fun delete(item: ItemEntity)
}
```

Repository implements offline-first pattern:
- Return Flow from Room for reactive UI updates.
- Fetch from network, update Room, UI auto-updates via Flow.
- Handle network errors gracefully — serve cached data with stale indicator.

ENCRYPTED STORAGE:

```kotlin
class EncryptedPrefs @Inject constructor(@ApplicationContext context: Context) {
    private val prefs = EncryptedSharedPreferences.create(
        context, "secure_prefs",
        MasterKeys.getOrCreate(MasterKeys.AES256_GCM_SPEC),
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun saveToken(token: String) { prefs.edit().putString("auth_token", token).apply() }
    fun getToken(): String? = prefs.getString("auth_token", null)
    fun clearToken() { prefs.edit().remove("auth_token").apply() }
}
```

============================================================
PHASE 4: UI ARCHITECTURE (JETPACK COMPOSE)
============================================================

NAVIGATION:

```kotlin
sealed class Screen(val route: String) {
    data object Home : Screen("home")
    data object Settings : Screen("settings")
    data class ItemDetail(val id: String) : Screen("items/{id}") {
        companion object { const val ROUTE = "items/{id}" }
    }
}

@Composable
fun AppNavigation(navController: NavHostController = rememberNavController()) {
    NavHost(navController = navController, startDestination = Screen.Home.route) {
        composable(Screen.Home.route) { HomeScreen(navController) }
        composable(
            Screen.ItemDetail.ROUTE,
            arguments = listOf(navArgument("id") { type = NavType.StringType })
        ) { ItemDetailScreen(navController) }
    }
}
```

THEMING (Material 3):

```kotlin
@Composable
fun AppNameTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            if (darkTheme) dynamicDarkColorScheme(LocalContext.current)
            else dynamicLightColorScheme(LocalContext.current)
        }
        darkTheme -> darkColorScheme(/* custom colors */)
        else -> lightColorScheme(/* custom colors */)
    }
    MaterialTheme(colorScheme = colorScheme, typography = AppTypography, content = content)
}
```

Define spacing tokens as CompositionLocal:
```kotlin
data class Spacing(val xs: Dp = 4.dp, val sm: Dp = 8.dp, val md: Dp = 16.dp, val lg: Dp = 24.dp, val xl: Dp = 32.dp)
val LocalSpacing = staticCompositionLocalOf { Spacing() }
```

STATE MANAGEMENT:

Every screen uses a sealed UiState:
```kotlin
sealed interface ItemsUiState {
    data object Loading : ItemsUiState
    data class Success(val items: List<Item>) : ItemsUiState
    data class Error(val message: String) : ItemsUiState
    data object Empty : ItemsUiState
}
```

ViewModel exposes StateFlow<UiState> collected by the Composable.

============================================================
PHASE 5: PUSH NOTIFICATIONS
============================================================

NotificationChannels.kt:
- Create channels on app startup (API 26+).
- Define channels per notification type (general, chat, promotions, etc.).
- Set importance, sound, vibration per channel.

PushNotificationService extends FirebaseMessagingService:
- Override onNewToken — send token to backend.
- Override onMessageReceived — build and display notification.
- Handle data-only messages for silent processing.
- Deep link from notification tap to correct screen.

============================================================
PHASE 6: BUILD VARIANTS & GRADLE
============================================================

VERSION CATALOG (gradle/libs.versions.toml):
```toml
[versions]
kotlin = "2.0.0"
compose-bom = "2024.06.00"
hilt = "2.51"
room = "2.6.1"
retrofit = "2.11.0"
# ... all versions centralized

[libraries]
compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
# ... all dependencies

[plugins]
android-application = { id = "com.android.application", version = "8.5.0" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version = "2.0.0-1.0.22" }
```

BUILD VARIANTS (app/build.gradle.kts):
```kotlin
android {
    buildTypes {
        debug {
            applicationIdSuffix = ".debug"
            isDebuggable = true
            buildConfigField("String", "API_BASE_URL", "\"https://api-dev.example.com\"")
        }
        create("staging") {
            initWith(getByName("debug"))
            applicationIdSuffix = ".staging"
            buildConfigField("String", "API_BASE_URL", "\"https://api-staging.example.com\"")
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            buildConfigField("String", "API_BASE_URL", "\"https://api.example.com\"")
        }
    }
}
```

PROGUARD / R8 RULES:
- Keep Retrofit interfaces and serializable DTOs.
- Keep Hilt-generated code.
- Keep Room entities and DAOs.
- Strip logging in release builds.

============================================================
PHASE 7: TESTING SETUP
============================================================

Unit tests (test/):
- ViewModel tests with Turbine for StateFlow testing.
- Repository tests with fake DAOs and mock API responses.
- UseCase tests with mock repositories.
- Use kotlinx-coroutines-test for coroutine testing.

Instrumented tests (androidTest/):
- Compose UI tests with ComposeTestRule.
- Navigation tests verifying route transitions.
- Room database tests with in-memory database.

Generate at least 3 unit tests and 1 UI test per major feature.


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

## Android App Scaffold Complete

### Architecture
- **UI Framework:** {Jetpack Compose / XML Views / Hybrid}
- **Architecture:** MVVM with Hilt DI + Use Cases
- **Persistence:** Room with offline-first pattern
- **Networking:** Retrofit + OkHttp + Kotlinx.serialization
- **Min SDK:** {24}

### Project Structure
{Tree listing of all generated files}

### Build Variants
| Variant | App ID Suffix | API URL | Minify | Features |
|---------|---------------|---------|--------|----------|
| debug | .debug | api-dev.example.com | No | Verbose logging |
| staging | .staging | api-staging.example.com | No | Standard logging |
| release | (none) | api.example.com | Yes | Minimal logging, R8 |

### Dependencies (Version Catalog)
| Library | Version | Purpose |
|---------|---------|---------|
| {name} | {version} | {why} |

### Generated Tests
| Test File | Tests | Coverage Area |
|-----------|-------|---------------|
| {file} | {count} | {what it tests} |

DO NOT:
- Use deprecated Android APIs (AsyncTask, Loader, Support Library).
- Hardcode API keys, secrets, or credentials anywhere in source files.
- Use GlobalScope for coroutines — always use viewModelScope or lifecycleScope.
- Skip error handling — every suspend call must be wrapped in try/catch or Result.
- Use Java — the entire project must be Kotlin.
- Add dependencies not defined in the version catalog.
- Write placeholder or stub implementations — every file must be complete.
- Hardcode colors, fonts, or dimensions — use Material 3 theme and design tokens.
- Skip ProGuard rules for serializable classes.
- Use string literals for navigation routes — use the sealed class constants.

NEXT STEPS:
- "Run `/mobile-test` to generate comprehensive unit, UI, and integration tests."
- "Run `/mobile-security-review` to audit encrypted storage, certificate pinning, and obfuscation."
- "Run `/play-store-publish` to set up signing, AAB, and Play Console publishing."
- "Run `/mobile-ci-cd` to configure CI/CD with Gradle builds and Play Store distribution."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /android-app — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
