---
name: android-gradle
description: Android app development with Gradle build system. Use when user wants to develop Android apps, create new projects, configure Gradle/AGP, build APKs, or troubleshoot build issues. Also covers uni-app + HBuilderX + Gradle hybrid packaging workflow. Triggers: "开发安卓", "Android项目", "Gradle构建", "AGP", "Android Studio", "打包APK", "build.gradle", "kotlin-dsl", "HBuilderX", "uni-app", "云打包", "本地打包".
---

# Android Gradle Skill

## 快速开始

用户要开发 Android 软件时，使用本 skill。

### 版本兼容性（背下来）

| AGP 版本 | Gradle 版本 | JDK 要求 | 最低 Android SDK |
|----------|------------|---------|----------------|
| 8.2.x | 8.2 | JDK 17+ | API 21 |
| 8.3.x | 8.4+ | JDK 17+ | API 24 |
| 8.4.x | 8.6+ | JDK 17+ | API 24 |
| 8.5.x | 8.7+ | JDK 17+ | API 24 |
| 8.6.x | 8.7+ | JDK 17+ | API 24 |

**AGP 8.0+ 必须用 JDK 17+。JDK 8 会报错。**

Gradle 和 AGP 的对应关系: `AGP 最小支持 Gradle 版本 = AGP version / 2.5` (大致)。

### 标准项目结构

```
project/
├── app/
│   ├── build.gradle.kts
│   └── src/main/
│       ├── java/
│       ├── res/
│       └── AndroidManifest.xml
├── build.gradle.kts          # root
├── settings.gradle.kts
├── gradle.properties
├── gradlew
├── gradlew.bat
└── gradle/wrapper/
    └── gradle-wrapper.properties
```

### 创建新项目

推荐用 `scripts/init_android_project.py`，会自动生成完整项目结构 + Gradle Wrapper + 正确版本配置。

```bash
python scripts/init_android_project.py <项目名> <保存路径> [AGP版本] [Gradle版本]
```

示例:
```bash
python scripts/init_android_project.py MyApp H:\Android_projects 8.2.0 8.2
```

### Gradle 构建命令

在项目目录下用 Gradle Wrapper:

```bash
# Windows
.\gradlew.bat assembleDebug
.\gradlew.bat assembleRelease

# 或用 run-gradle.bat（如果配置了 JAVA_HOME）
H:\Android_work\Gradle\run-gradle.bat assembleDebug
```

跳过测试快速构建:
```bash
.\gradlew.bat assembleDebug -x test -x lint
```

### 常见问题

**Q: 报错 "Could not resolve all files for configuration :classpath"**
A: AGP 8.2.0 需要 JDK 17+，当前 JDK 版本不够。加 `--stacktrace` 看详情。

**Q: 报错 "SDK location not found"**
A: 缺少 `local.properties` 或 `ANDROID_HOME` 环境变量。在 `local.properties` 加:
```
sdk.dir=H\:\\Android_work\\Android\\new\\sdk
```

**Q: Gradle 下载慢/失败**
A: 挂代理，或在 `gradle.properties` 加镜像:
```
org.gradle.jvmargs=-Dfile.encoding=UTF-8
```

**Q: 内存溢出 "OutOfMemoryError"**
A: 在 `gradle.properties` 加:
```
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m
```

### Gradle 版本升级

1. 修改 `gradle/wrapper/gradle-wrapper.properties` 中的 `distributionUrl`
2. 运行 `./gradlew wrapper --gradle-version=X.X` 更新 wrapper 脚本
3. 确保 AGP 版本支持新 Gradle 版本

### 关键文件内容参考

详细配置示例见:
- `references/agp-kts-templates.md` - build.gradle.kts 模板
- `references/version-compat.md` - 版本兼容性详细表
