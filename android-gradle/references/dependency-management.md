# Dependency Management

## Version Catalogs

Version catalogs (`gradle/libs.versions.toml`) provide centralized dependency management:

```toml
[versions]
agp = "8.7.0"
kotlin = "2.0.20"
compose-bom = "2024.11.00"
core-ktx = "1.13.1"

[libraries]
androidx-core = { group = "androidx.core", name = "core-ktx", version.ref = "core-ktx" }
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
```

## Dependency Configurations

### implementation vs api

- **`implementation`** - Only visible within the module (faster builds)
- **`api`** - Visible to consumers (like `compile` in old Groovy)

```kotlin
// In library module
dependencies {
    // Only visible within this module
    implementation("androidx.core:core-ktx:1.13.1")
    
    // Also visible to modules that depend on this library
    api("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
}
```

## Dynamic Versions

Avoid using `+` for production - use fixed versions:

```kotlin
// Avoid (can cause inconsistent builds)
implementation("androidx.core:core-ktx:1.+")

// Use fixed version
implementation("androidx.core:core-ktx:1.13.1")
```

For automatic updates, use `./gradlew useLatestVersions` with refreshVersions plugin.

## Module Dependencies

```kotlin
// Single module
implementation(project(":app"))

// Multi-module
implementation(project(":core:network"))
implementation(project(":core:ui"))
```

## Transitive Dependencies

View dependency tree:
```bash
./gradlew app:dependencies
./gradlew app:dependencies --configuration releaseRuntimeClasspath
```

Exclude transitive dependencies:
```kotlin
implementation("com.example:lib:1.0.0") {
    exclude(group = "org.unwanted", module = "unwanted-lib")
}
```

## Build Variant Dependencies

```kotlin
dependencies {
    // Debug only
    debugImplementation("com.facebook.stetho:stetho:1.6.0")
    
    // Test only
    testImplementation("junit:junit:4.13.2")
    
    // Android test only
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
}
```

## gradle.lockfile

The `gradle.lockfile` records resolved versions. Commit this file to ensure consistent builds across machines.

## Best Practices

1. Use Version Catalogs for centralized version management
2. Avoid dynamic versions in production
3. Use `implementation` to reduce compilation time
4. Commit `gradle.lockfile` for reproducible builds
5. Use `platform()` for Compose BOM to manage transitive versions