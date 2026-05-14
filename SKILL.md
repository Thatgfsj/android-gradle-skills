---
name: android-gradle-skills
description: Android Gradle build system knowledge base. Use when creating Android projects, building APK, Gradle dependency management, AGP/Gradle version compatibility, build optimization, Convention Plugins, Version Catalogs, Jetpack Compose setup, or Android Studio troubleshooting. Triggers: "Android项目", "创建Android项目", "Gradle构建", "打包APK", "AGP版本", "Gradle版本", "build.gradle", "kotlin-dsl", "Jetpack Compose", "Android构建优化", "Gradle依赖管理", "Version Catalogs", "Convention Plugins".
---

# Android Gradle Skills

Android Gradle build system knowledge base with AGP/Gradle version compatibility, project templates, and build automation scripts.

## Version Compatibility

| AGP | Gradle | JDK | Min SDK |
|-----|--------|-----|---------|
| 8.2.x | 8.2 | JDK 17+ | API 21 |
| 8.3.x | 8.4+ | JDK 17+ | API 24 |
| 8.4.x | 8.6+ | JDK 17+ | API 24 |
| 8.5.x | 8.7+ | JDK 17+ | API 24 |
| 8.6.x | 8.7+ | JDK 17+ | API 24 |
| 8.7.x | 8.10+ | JDK 17+ | API 24 |

> **Important:** AGP 8.x requires JDK 17+. JDK 8 will not work.

## Scripts

| Script | Purpose |
|--------|---------|
| `android-gradle/scripts/init_android_project.py` | Generate Android project templates |
| `android-gradle/scripts/ai/add-dependency.py` | Add dependencies using Version Catalogs |
| `android-gradle/scripts/ai/create-module.py` | Create new Android library modules |
| `android-gradle/scripts/ai/run-gradle-task.py` | Execute Gradle tasks safely |
| `android-gradle/scripts/ops/gradle-optimize.ps1` | Optimize Gradle build settings |
| `android-gradle/scripts/ops/run-ci-locally.ps1` | Simulate CI build locally |
| `android-gradle/scripts/ops/update-dependencies.py` | Update dependencies to latest versions |

## References

- `android-gradle/references/build-basics.md` - Gradle build fundamentals
- `android-gradle/references/dependency-management.md` - Version catalogs, api/implementation
- `android-gradle/references/build-variants.md` - Build types, product flavors
- `android-gradle/references/signing-and-release.md` - Signing, release builds
- `android-gradle/references/performance-optimization.md` - Parallel builds, caching
- `android-gradle/references/troubleshooting.md` - Common AGP/Gradle errors
- `android-gradle/references/ci-cd-integration.md` - GitHub Actions examples

## Examples

- `examples/basic-compose-app` - Single module Compose app
- `examples/multi-module-clean` - Multi-module with Convention Plugins
- `examples/dynamic-feature` - Dynamic feature modules

## Standard Tech Stack

| Category | Tech |
|----------|------|
| **Language** | Kotlin |
| **UI Framework** | Jetpack Compose (Material 3) |
| **Min SDK** | API 26 (Android 6.0) |
| **Target SDK** | API 34 (Android 14) |
| **Architecture** | Single module + MVVM |
| **Navigation** | Navigation Compose |
| **State Management** | Kotlin StateFlow + MutableStateFlow |
| **Build Tools** | Gradle 8.10.2 + AGP 8.7.0 |

## Setup Requirements

1. **JDK 17+** - Set via `JAVA_HOME` environment variable
2. **Android SDK** - Set via `ANDROID_HOME` or `local.properties`: `sdk.dir=/path/to/sdk`
3. **Gradle** - Wrapper included, no separate install needed

---

Source: https://github.com/Thatgfsj/android-gradle-skills