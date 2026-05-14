# Dynamic Feature Example

Demonstrates dynamic feature modules with Play Store on-demand delivery.

## Structure

```
dynamic-feature/
├── app/                    # Base app module
├── feature/
│   └── advanced/           # Dynamic feature module
└── build-logic/            # Convention plugins
```

## Dynamic Features

Features can be delivered on-demand:
- Smaller initial APK size
- Conditional feature availability
- Faster initial installation

## Build Commands

```bash
./gradlew bundleDebug           # Build app bundle
./gradlew bundleRelease         # Build release bundle
```

## Key Configuration

In `settings.gradle.kts`:
```kotlin
include(":app", ":feature:advanced")
```

In `build.gradle.kts`:
```kotlin
android {
    dynamicFeatures += ":feature:advanced"
}
```