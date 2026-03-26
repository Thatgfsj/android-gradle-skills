# Android Gradle Skills

OpenClaw 技能 — Android 应用开发与 Gradle 构建系统。

## 这是什么？

[OpenClaw](https://github.com/openclaw/openclaw) 的技能插件，提供 Android 开发知识，包括 AGP/Gradle 版本兼容性、项目模板、构建脚本和故障排除指南。

## 目录结构

```
android-gradle/
├── SKILL.md                              # 主技能文件（触发词：开发安卓 / Gradle构建 / 打包APK 等）
├── scripts/
│   └── init_android_project.py           # 一键创建 Android 项目
└── references/
    ├── agp-kts-templates.md             # Kotlin DSL build 文件模板
    └── version-compat.md                 # AGP ↔ Gradle ↔ JDK 版本兼容性表
```

## 版本兼容性

| AGP 版本 | Gradle 版本 | JDK 要求 | 最低 Android SDK |
|----------|------------|---------|----------------|
| 8.2.x | 8.2 | JDK 17+ | API 21 |
| 8.3.x | 8.4+ | JDK 17+ | API 24 |
| 8.4.x | 8.6+ | JDK 17+ | API 24 |
| 8.5.x | 8.7+ | JDK 17+ | API 24 |
| 8.6.x | 8.7+ | JDK 17+ | API 24 |

> ⚠️ **AGP 8.x 必须使用 JDK 17+，JDK 8 无法运行。**

## 快速开始

### 创建新项目

```bash
python scripts/init_android_project.py MyApp /path/to/save 8.2.0 8.2
```

这会生成完整的 Android 项目，包含：
- Kotlin DSL 构建文件 (build.gradle.kts)
- 配置好的 Gradle Wrapper
- 最小化 MainActivity 和布局文件
- 正确的 AGP + Gradle 版本兼容性

### 构建 APK

```bash
cd /path/to/project
./gradlew assembleDebug    # Debug APK
./gradlew assembleRelease  # Release APK
```

## uni-app + HBuilderX + Gradle 打包流程

适用于使用 uni-app 开发的项目，用 HBuilderX 编译前端，Gradle 打包 APK。

### 流程概览

```
uni-app 源码 (Vue)
        ↓  [HBuilderX 编译]
dist/build/app/  (web 资源)
        ↓  [替换到 Android 项目]
Android Studio 项目 (HBuilder-Integrate-AS 模板)
        ↓  [Gradle 打包]
apk 文件
```

### 详细步骤

**第一步：HBuilderX 编译 uni-app**
```bash
cd 项目目录
npx uni build --platform app
# 输出: dist/build/app/  (web 资源)
```

**第二步：替换 web 资源到 Android 项目**
将编译输出复制到 `assets/apps/<appid>/www/` 目录。
appid 从 `manifest.json` 中的 `id` 字段获取（格式 `__UNI__XXXXXXX`）。

**第三步：Gradle 打包**
```cmd
set JAVA_HOME=<JDK17路径>
set ANDROID_HOME=<Android SDK路径>
gradle -p <Android项目目录> assembleDebug
```

### 触发词

以下词汇会触发此技能：
- "开发安卓" / "Android项目"
- "Gradle构建" / "打包APK"
- "Android Studio配置"
- "AGP版本" / "Gradle升级"
- "build.gradle" / "kotlin-dsl"
- "HBuilderX" / "uni-app"

## 常见问题

**Q: "Could not resolve all files for configuration :classpath"**
JDK 版本太低。AGP 8.2+ 需要 JDK 17+。使用 Android Studio 自带的 JBR 或安装 JDK 17+。

**Q: "SDK location not found"**
创建 `local.properties` 文件：
```properties
sdk.dir=/path/to/your/android/sdk
```

**Q: "OutOfMemoryError"**
在 `gradle.properties` 中添加：
```properties
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m
```

## License

MIT — 可自由使用、修改和分发。
