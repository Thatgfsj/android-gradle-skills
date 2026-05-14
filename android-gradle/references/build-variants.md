# Build Variants

## Build Types

Two default build types: `debug` and `release`.

```kotlin
android {
    buildTypes {
        debug {
            isMinifyEnabled = false
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

## Product Flavors

Define dimensions and flavors:

```kotlin
android {
    flavorDimensions += "environment"
    
    productFlavors {
        create("dev") {
            dimension = "environment"
            applicationIdSuffix = ".dev"
            versionNameSuffix = "-dev"
            buildConfigField("String", "API_BASE_URL", "\"https://dev.api.example.com\"")
        }
        create("staging") {
            dimension = "environment"
            applicationIdSuffix = ".staging"
            versionNameSuffix = "-staging"
            buildConfigField("String", "API_BASE_URL", "\"https://staging.api.example.com\"")
        }
        create("prod") {
            dimension = "environment"
            buildConfigField("String", "API_BASE_URL", "\"https://api.example.com\"")
        }
    }
}
```

## Build Variant Matrix

| Dimension | Flavor | Type | Result |
|-----------|--------|------|--------|
| environment | dev | debug | com.example.app.dev.debug |
| environment | dev | release | com.example.app.dev.release |
| environment | prod | debug | com.example.app.prod.debug |
| environment | prod | release | com.example.app.prod.release |

## Variant Filtering

```kotlin
android {
    applicationVariants.all {
        if (buildType.name == "debug" && flavor.name == "prod") {
            packageApplicationProvider.set(
                prebuildOutputDir.map { dir ->
                    File(dir, "prod-debug.apk")
                }
            )
        }
    }
}
```

## Custom Application Variants

```kotlin
android {
    applicationVariants.create("benchmark") {
        dimension = "version"
        applicationIdSuffix = ".benchmark"
        versionNameSuffix = "-benchmark"
        matchingFallbacks += listOf("release")
    }
}
```

## Source Sets per Variant

```
src/
├── main/           # Shared
├── debug/          # Debug only
├── release/        # Release only
├── devDebug/       # Dev + Debug combined
├── prodRelease/    # Prod + Release combined
```

## Signing

### Debug Signing (automatic)

Debug builds use a generated debug keystore automatically.

### Release Signing

```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file("keystore/release.jks")
            storePassword = System.getenv("KEY_STORE_PASSWORD") ?: "default"
            keyAlias = System.getenv("KEY_ALIAS") ?: "release"
            keyPassword = System.getenv("KEY_PASSWORD") ?: "default"
        }
    }
    
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

**Best Practice**: Use environment variables or Gradle properties, never hardcode passwords.