---
name: android-gradle
description: Android app development with Gradle build system. Use when user wants to develop Android apps with Kotlin + Jetpack Compose, create new projects, configure Gradle/AGP, build APKs, or troubleshoot build issues. Triggers: "开发安卓", "Android项目", "Gradle构建", "AGP", "Android Studio", "打包APK", "build.gradle", "kotlin-dsl", "Jetpack Compose".
---

# Android Gradle Skill

## 快速开始

用户要开发 Android 软件时，使用本 skill。

### 标准技术栈

| 类别 | 技术 |
|------|------|
| **语言** | Kotlin |
| **UI框架** | Jetpack Compose (Material 3) |
| **最小SDK** | API 26 (Android 6.0) |
| **目标SDK** | API 34 (Android 14) |
| **架构** | 单模块 + Mock数据层（或 MVVM） |
| **导航** | Navigation Compose |
| **状态管理** | Kotlin StateFlow + MutableStateFlow |
| **编译工具** | Gradle 8.2 + AGP 8.2.2 |

### 版本兼容性（背下来）

| AGP 版本 | Gradle 版本 | JDK 要求 | 最低 Android SDK |
|----------|------------|---------|----------------|
| 8.2.x | 8.2 | JDK 17+ | API 21 |
| 8.3.x | 8.4+ | JDK 17+ | API 24 |
| 8.4.x | 8.6+ | JDK 17+ | API 24 |
| 8.5.x | 8.7+ | JDK 17+ | API 24 |
| 8.6.x | 8.7+ | JDK 17+ | API 24 |

**AGP 8.0+ 必须用 JDK 17+。JDK 8 会报错。**

本地 JDK 路径：`H:\Android_work\AS\jbr`（JDK 17）
本地 Android SDK：`H:\Android_work\Android\new`

### 标准项目结构

```
project/
├── app/
│   ├── build.gradle.kts
│   └── src/main/
│       ├── java/com/你的包名/
│       │   ├── data/          # 数据模型 + Repository
│       │   ├── ui/           # Compose 页面
│       │   │   ├── theme/    # 颜色 + 主题
│       │   │   └── screens/  # 各页面
│       │   └── MainActivity.kt
│       ├── res/
│       └── AndroidManifest.xml
├── build.gradle.kts          # root
├── settings.gradle.kts
├── gradle.properties
├── local.properties           # sdk.dir 配置
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
python scripts/init_android_project.py MyApp H:\Android_projects 8.2.2 8.2
```

### Gradle 构建命令

```cmd
set JAVA_HOME=H:\Android_work\AS\jbr
set ANDROID_HOME=H:\Android_work\Android\new
cd <项目路径>
.\gradlew.bat assembleDebug --no-daemon
```

跳过测试快速构建:
```cmd
.\gradlew.bat assembleDebug -x test -x lint --no-daemon
```

### 关键 build.gradle.kts 配置

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        vectorDrawables {
            useSupportLibrary = true
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.8"
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation("androidx.navigation:navigation-compose:2.7.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")

    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
```

### local.properties 配置

```properties
sdk.dir=H\:\\Android_work\\Android\\new
```

### gradle.properties 配置

```properties
android.useAndroidX=true
android.enableJetifier=true
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
kotlin.code.style=official
android.nonTransitiveRClass=true
```

### 常见问题

**Q: 报错 "Could not resolve all files for configuration :classpath"**
A: AGP 8.2.0 需要 JDK 17+，当前 JDK 版本不够。

**Q: 报错 "SDK location not found"**
A: 缺少 `local.properties`。在项目根目录创建：
```
sdk.dir=H\:\\Android_work\\Android\\new
```

**Q: 报错 "App has different base APK"**
A: 之前装过不同签名的 APK，先卸载再装。

**Q: 内存溢出 "OutOfMemoryError"**
A: 在 `gradle.properties` 加：
```
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m
```

**Q: Gradle 下载慢/失败**
A: 在 `gradle.properties` 加镜像或挂代理。

### Gradle 版本升级

1. 修改 `gradle/wrapper/gradle-wrapper.properties` 中的 `distributionUrl`
2. 确保 AGP 版本支持新 Gradle 版本

### Jetpack Compose 项目初始化文件清单

| 文件 | 作用 |
|------|------|
| `app/src/main/java/.../MainActivity.kt` | Compose 入口 |
| `app/src/main/java/.../ui/theme/Color.kt` | 颜色定义 |
| `app/src/main/java/.../ui/theme/Theme.kt` | Material3 主题 |
| `app/src/main/java/.../data/model.kt` | 数据模型 |
| `app/src/main/java/.../data/Repository.kt` | Mock 数据仓库 |
| `app/src/main/java/.../ui/XXXScreen.kt` | 各页面 |

详细配置示例见：
- `references/agp-kts-templates.md` - build.gradle.kts 模板
- `references/version-compat.md` - 版本兼容性详细表
