# Gradle Build Basics

## Gradle Lifecycle

Gradle builds go through three phases:

1. **Initialization** - Determines which projects are in the build
2. **Configuration** - Executes build scripts for each project
3. **Execution** - Runs the tasks determined by the command line

## Common build.gradle.kts Configuration

### Root Project

```kotlin
plugins {
    id("com.android.application") version "8.7.0" apply false
    id("org.jetbrains.kotlin.android") version "2.0.20" apply false
}

android {
    namespace = "com.example.myapp"
    compileSdk = 34
}
```

### App Module

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
        debug {
            isMinifyEnabled = false
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
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-compose:1.9.3")
    implementation(platform("androidx.compose:compose-bom:2024.11.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
}
```

### Library Module

```kotlin
plugins {
    id("com.android.library")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.mylib"
    compileSdk = 34

    defaultConfig {
        minSdk = 24
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}
```

## Task Graph

Common tasks:
- `assembleDebug` - Build debug APK
- `assembleRelease` - Build release APK
- `clean` - Clean build directory
- `build` - Full build (debug + release)
- `testDebugUnitTest` - Run unit tests
- `lintDebug` - Run lint analysis

## Gradle Properties

Key properties in `gradle.properties`:

```properties
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.daemon=true

android.useAndroidX=true
android.enableJetifier=true

kotlin.code.style=official
```

## Version Catalogs (libs.versions.toml)

```toml
[versions]
agp = "8.7.0"
kotlin = "2.0.20"
compose-bom = "2024.11.00"

[libraries]
androidx-core = { group = "androidx.core", name = "core-ktx", version.ref = "core-ktx" }
compose-ui = { group = "androidx.compose.ui", name = "ui", version.ref = "compose-bom" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
```

Usage in build.gradle.kts:
```kotlin
plugins {
    alias(libs.plugins.android.application)
}

dependencies {
    implementation(libs.androidx.core)
    implementation(libs.compose.ui)
}
```