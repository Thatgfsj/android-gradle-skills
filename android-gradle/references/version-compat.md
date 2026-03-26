# Gradle & AGP 版本兼容性详解

## 官方兼容表

### Android Gradle Plugin (AGP) 8.x

| AGP 版本 | 最低 Gradle | 最高 Gradle | 最低 JDK | 最低 Android SDK |
|----------|-------------|-------------|---------|----------------|
| 8.0.0 | 8.0 | 8.1 | JDK 17 | API 21 |
| 8.0.1 | 8.0 | 8.1 | JDK 17 | API 21 |
| 8.0.2 | 8.0 | 8.2 | JDK 17 | API 21 |
| 8.1.0 | 8.0 | 8.2 | JDK 17 | API 21 |
| 8.1.1 | 8.0 | 8.2 | JDK 17 | API 21 |
| 8.1.2 | 8.0 | 8.2 | JDK 17 | API 21 |
| 8.1.3 | 8.0 | 8.2 | JDK 17 | API 21 |
| 8.1.4 | 8.0 | 8.2 | JDK 17 | API 21 |
| 8.2.0 | 8.2 | 8.3 | JDK 17 | API 21 |
| 8.2.1 | 8.2 | 8.3 | JDK 17 | API 21 |
| 8.2.2 | 8.2 | 8.4 | JDK 17 | API 21 |
| 8.3.0 | 8.4 | 8.5 | JDK 17 | API 24 |
| 8.3.1 | 8.4 | 8.5 | JDK 17 | API 24 |
| 8.3.2 | 8.4 | 8.6 | JDK 17 | API 24 |
| 8.4.0 | 8.6 | 8.7 | JDK 17 | API 24 |
| 8.4.1 | 8.6 | 8.8 | JDK 17 | API 24 |
| 8.4.2 | 8.6 | 8.9 | JDK 17 | API 24 |
| 8.5.0 | 8.7 | 8.9 | JDK 17 | API 24 |
| 8.5.1 | 8.7 | 8.9 | JDK 17 | API 24 |
| 8.5.2 | 8.7 | 8.10 | JDK 17 | API 24 |
| 8.6.0 | 8.7 | 8.10 | JDK 17 | API 24 |
| 8.6.1 | 8.7 | 8.11 | JDK 17 | API 24 |

### Android SDK & Build Tools

| Build Tools | 最低 AGP | 最低 Gradle |
|-------------|---------|------------|
| 34.0.0 | 8.2.0 | 8.2 |
| 35.0.0 | 8.5.0 | 8.7 |
| 36.0.0 | 8.6.0 | 8.7 |

## 常见问题

### AGP 8.x + JDK 8 错误
```
Could not resolve all files for configuration ':classpath'.
> No matching variant of com.android.tools.build:gradle:8.2.0 was found.
  The consumer was configured to find a library for use during runtime,
  compatible with Java 8, packaged as a jar, and its dependencies
  declared externally, as well as attribute 'org.gradle.plugin.api-version'
  but the provider needed Java 11.
```
**解法**: 使用 JDK 17+。在 Windows 上推荐用 Android Studio 自带的 JBR (JetBrains Runtime)。

### Windows Gradle 路径问题
Gradle Wrapper 在 Windows 上用 `.bat`，Linux/Mac 用 shell 脚本。确保 `gradlew.bat` 有执行权限。

### Kotlin DSL vs Groovy
推荐用 Kotlin DSL (`.kts`)，类型安全，现代 Android 项目标配。

## Gradle 版本升级建议路径
- 8.0 → 8.2 (稳定)
- 8.2 → 8.4 (Kotlin 1.9 支持)
- 8.4 → 8.6 (最新稳定)
