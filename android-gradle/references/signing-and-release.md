# Signing and Release

## Signing Configuration

### Basic Release Config

```kotlin
android {
    signingConfigs {
        create("release") {
            // Load from environment variables
            storeFile = file(System.getenv("KEYSTORE_PATH") ?: "keystore/release.jks")
            storePassword = System.getenv("KEY_STORE_PASSWORD") ?: ""
            keyAlias = System.getenv("KEY_ALIAS") ?: ""
            keyPassword = System.getenv("KEY_PASSWORD") ?: ""
        }
    }
    
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
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

### gradle.properties approach

```properties
# gradle.properties (DO NOT commit to git)
KEYSTORE_PATH=/path/to/keystore.jks
KEY_STORE_PASSWORD=yourpassword
KEY_ALIAS=releasekey
KEY_PASSWORD=yourpassword
```

```kotlin
// build.gradle.kts
android {
    signingConfigs {
        create("release") {
            storeFile = file(project.property("KEYSTORE_PATH").toString())
            storePassword = project.property("KEY_STORE_PASSWORD").toString()
            keyAlias = project.property("KEY_ALIAS").toString()
            keyPassword = project.property("KEY_PASSWORD").toString()
        }
    }
}
```

## Generating a Keystore

```bash
keytool -genkey -v -keystore release.jks \
    -alias releasekey -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass yourpassword -keypass yourpassword \
    -dname "CN=Your Name, O=Your Organization, C=US"
```

## V1 and V2 Signing

- **V1** (Jar Signature) - Legacy, required for older devices
- **V2** (APK Signature) - Faster, recommended

```kotlin
android {
    buildTypes {
        release {
            // Enable both (default since AGP 3.0)
            isV1SigningEnabled = true
            isV2SigningEnabled = true
        }
    }
}
```

## Building for Release

```bash
# Clean build
./gradlew clean assembleRelease

# With specific signing config
./gradlew assembleRelease -Psigning.config=myconfig
```

## Uploading to Play Store

### Using bundletool

```bash
# Build bundle
./gradlew bundleRelease

# Convert to APK set
java -jar bundletool.jar build-apks \
    --bundle=app/build/outputs/bundle/release/app-release.aab \
    --output=app-release.apks \
    --ks=keystore/release.jks \
    --ks-pass=pass:password \
    --ks-key-alias=releasekey \
    --key-pass=pass:password
```

## CI/CD Secrets

Never commit keystores or passwords to git. In GitHub Actions:

```yaml
- name: Build Release APK
  env:
    KEYSTORE_PATH: ${{ secrets.KEYSTORE_PATH }}
    KEY_STORE_PASSWORD: ${{ secrets.KEY_STORE_PASSWORD }}
    KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
    KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
  run: ./gradlew assembleRelease
```

Store keystore as a secret file or use a secure vault.