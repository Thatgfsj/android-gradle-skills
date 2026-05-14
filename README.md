# android-gradle-skills

![Build Status](https://img.shields.io/github/actions/workflow/status/Thatgfsj/android-gradle-skills/validate.yml?branch=master)
![License](https://img.shields.io/github/license/Thatgfsj/android-gradle-skills)
![AGP](https://img.shields.io/badge/AGP-8.7.0-blue)
![Gradle](https://img.shields.io/badge/Gradle-8.10.2-blue)

OpenClaw skill for Android app development with Gradle build system.

## What is this?

A skill for [OpenClaw](https://github.com/openclaw/openclaw) that provides Android development knowledge, including AGP/Gradle version compatibility, project templates, build automation scripts, and troubleshooting guides.

## Standard Tech Stack

| Category | Tech |
|----------|------|
| **Language** | Kotlin |
| **UI Framework** | Jetpack Compose (Material 3) |
| **Min SDK** | API 26 (Android 6.0) |
| **Target SDK** | API 34 (Android 14) |
| **Architecture** | Single module + Mock data (or MVVM) |
| **Navigation** | Navigation Compose |
| **State Management** | Kotlin StateFlow + MutableStateFlow |
| **Build Tools** | Gradle 8.10.2 + AGP 8.7.0 |

## Version Compatibility

| AGP | Gradle | JDK | Min Android SDK |
|-----|--------|-----|----------------|
| 8.2.x | 8.2 | JDK 17+ | API 21 |
| 8.3.x | 8.4+ | JDK 17+ | API 24 |
| 8.4.x | 8.6+ | JDK 17+ | API 24 |
| 8.5.x | 8.7+ | JDK 17+ | API 24 |
| 8.6.x | 8.7+ | JDK 17+ | API 24 |
| 8.7.x | 8.10+ | JDK 17+ | API 24 |

> **Important:** AGP 8.x requires JDK 17 or higher. JDK 8 will not work.

## Quick Start

### Create a new project

```bash
python scripts/init_android_project.py MyApp /path/to/projects
```

Or use interactive mode:

```bash
python scripts/init_android_project.py --interactive
```

This generates a complete Android project with:
- Kotlin DSL build files (build.gradle.kts)
- Gradle wrapper configured
- Jetpack Compose + Material 3 theme template
- Version Catalogs support (gradle/libs.versions.toml)
- Convention Plugins support

### Build APK

```bash
cd /path/to/project
./gradlew assembleDebug    # Debug APK
./gradlew assembleRelease  # Release APK
```

## Project Structure

```
android-gradle-skills/
├── gradle/
│   └── libs.versions.toml    # Version Catalogs
├── build-logic/
│   └── conventions/           # Convention Plugins
├── android-gradle/
│   ├── scripts/              # Automation scripts
│   │   ├── init_android_project.py
│   │   ├── ai/               # AI-callable scripts
│   │   └── ops/              # DevOps scripts
│   └── references/           # Knowledge base
├── examples/
│   ├── basic-compose-app/
│   ├── multi-module-clean/
│   └── dynamic-feature/
└── .github/
    ├── workflows/
    │   └── validate.yml
    └── dependabot.yml
```

## Skill Triggers

This skill activates when you say things like:
- "Android项目" / "创建Android项目"
- "Gradle构建" / "打包APK"
- "Android Studio问题"
- "AGP版本" / "Gradle版本"
- "build.gradle" / "kotlin-dsl"
- "Jetpack Compose"

## Setup Requirements

1. **JDK 17+** - AGP 8.x will not work with JDK 8
   
   Set via environment variable:
   ```
   export JAVA_HOME=/path/to/jdk-17
   ```

2. **Android SDK** - Set via environment variable or `local.properties`:
   ```
   export ANDROID_HOME=/path/to/android/sdk
   ```
   
   Or create `local.properties`:
   ```properties
   sdk.dir=/path/to/your/android/sdk
   ```

3. **Gradle** - Wrapper is included, no need to install separately

## Repository Structure

| Path | Description |
|------|-------------|
| `gradle/libs.versions.toml` | Centralized dependency version management |
| `build-logic/conventions/` | Reusable build convention plugins |
| `android-gradle/scripts/` | Automation scripts for AI and DevOps |
| `android-gradle/references/` | Gradle knowledge base docs |
| `examples/` | Sample projects demonstrating best practices |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute new Gradle knowledge or examples.

## License

MIT - free to use, modify, and distribute.