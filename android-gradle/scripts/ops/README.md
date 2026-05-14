# Force Reload

Refresh version catalogs and update dependencies.

## Usage

```bash
./gradlew useLatestVersions --write
```

This requires the refreshVersions plugin configured in `settings.gradle.kts`:

```kotlin
pluginManagement {
    plugins {
        id("de.fayro.refreshVersions") version "0.60.0"
    }
}
```

## What it does

1. Scans all dependencies
2. Checks for newer versions
3. Updates `gradle/libs.versions.toml`
4. Creates git diff for review