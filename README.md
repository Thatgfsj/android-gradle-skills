# android-gradle-skills

OpenClaw skill for Android app development with Gradle build system.

## What is this?

A skill for [OpenClaw](https://github.com/openclaw/openclaw) that provides Android development knowledge, including AGP/Gradle version compatibility, project templates, build automation scripts, and troubleshooting guides.

## Contents

```
android-gradle/
├── SKILL.md                              # Main skill file (triggers on Android development tasks)
├── scripts/
│   └── init_android_project.py           # One-command Android project generator
└── references/
    ├── agp-kts-templates.md             # Kotlin DSL build file templates
    └── version-compat.md                 # AGP ↔ Gradle ↔ JDK compatibility table
```

## Version Compatibility

| AGP | Gradle | JDK |
|-----|--------|-----|
| 8.2.x | 8.2 | JDK 17+ |
| 8.3.x | 8.4+ | JDK 17+ |
| 8.4.x | 8.6+ | JDK 17+ |
| 8.5.x | 8.7+ | JDK 17+ |
| 8.6.x | 8.7+ | JDK 17+ |

> **Important:** AGP 8.x requires JDK 17 or higher. JDK 8 will not work.

## Quick Start

### Build an existing project

```bash
# Navigate to your Android project
cd /path/to/project

# Build debug APK
./gradlew assembleDebug

# Build release APK
./gradlew assembleRelease
```

### Create a new project

```bash
python scripts/init_android_project.py MyApp /path/to/save 8.2.0 8.2
```

This generates a complete Android project with:
- Kotlin DSL build files (build.gradle.kts)
- Gradle wrapper configured
- Minimal `MainActivity` and layout
- Proper AGP + Gradle version compatibility

## Skill Triggers

This skill activates when you say things like:
- "开发安卓" / "Android项目"
- "Gradle构建" / "打包APK"
- "Android Studio配置"
- "AGP版本" / "Gradle升级"
- "build.gradle" / "kotlin-dsl"

## Setup Requirements

1. **JDK 17+** — AGP 8.x will not work with JDK 8
2. **Android SDK** — Set in `local.properties`:
   ```
   sdk.dir=/path/to/your/android/sdk
   ```
3. **Gradle** (optional, wrapper included):
   ```
   gradle-8.2-bin.zip
   ```

## Troubleshooting

### "Could not resolve all files for configuration :classpath"
Your JDK version is too low. AGP 8.2+ requires JDK 17+. Use Android Studio's built-in JBR or install JDK 17+.

### "SDK location not found"
Create or edit `local.properties` in the project root:
```properties
sdk.dir=/path/to/your/android/sdk
```

### "OutOfMemoryError" during build
Add to `gradle.properties`:
```properties
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m
```

## License

MIT — free to use, modify, and distribute.
