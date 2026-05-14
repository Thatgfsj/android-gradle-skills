# Troubleshooting

## "Could not resolve all files for configuration :classpath"

**Cause**: JDK version too low for AGP version.

**Solution**:
- AGP 8.x requires JDK 17+
- Check `java -version`
- Set `JAVA_HOME` to JDK 17+

```bash
# Check Java version
java -version

# On Windows
set JAVA_HOME=C:\Program Files\Java\jdk-17

# On Mac/Linux
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home
```

## "SDK location not found"

**Cause**: Android SDK path not configured.

**Solution**:
Create `local.properties` in project root:
```properties
sdk.dir=/path/to/android/sdk
```

Or set environment variable:
```bash
export ANDROID_HOME=/path/to/android/sdk
export ANDROID_SDK_ROOT=/path/to/android/sdk
```

## "Unsupported class file major version"

**Cause**: AGP version incompatible with JDK version.

**Solution**:
| AGP Version | Min JDK |
|-------------|---------|
| 8.2.x | JDK 17 |
| 8.3.x+ | JDK 17 |
| 8.7.x+ | JDK 17 |

Upgrade JDK or downgrade AGP.

## "OutOfMemoryError" during build

**Solution**: Add to `gradle.properties`:

```properties
org.gradle.jvmargs=-Xmx4096m -XX:MaxMetaspaceSize=1024m \
    -XX:+HeapDumpOnOutOfMemoryError
```

Also consider:
```kotlin
android {
    compileOptions {
        isIncremental = true
    }
}
```

## Configuration Cache Issues

**Cause**: Plugin doesn't support configuration cache.

**Solution**:
```properties
org.gradle.configuration-cache=false
```

Or identify problematic plugin and report issue.

## Dependency Conflicts

**Cause**: Transitive dependency version mismatch.

**Solution**:
```kotlin
dependencies {
    constraints {
        implementation("androidx.core:core-ktx:1.13.1") {
            because("version X has a bug")
        }
    }
}
```

Or force resolution:
```kotlin
configurations.all {
    resolutionStrategy {
        force("androidx.core:core-ktx:1.13.1")
    }
}
```

## Kotlin Version Mismatch

**Cause**: Kotlin version in build.gradle.kts doesn't match AGP's embedded version.

**Solution**: Use consistent Kotlin version across plugins:

```kotlin
plugins {
    id("com.android.application") version "8.7.0"
    id("org.jetbrains.kotlin.android") version "2.0.20"
}
```

## "Plugin [id] was not found"

**Cause**: Plugin not in repository or version mismatch.

**Solution**:
- Check `pluginManagement` in `settings.gradle.kts`
- Ensure Google and Maven Central repositories are configured
- Verify plugin ID and version exist

## Build Slow After Clean

This is normal for first build. For subsequent builds:
- Use `--parallel` for parallel execution
- Use `--build-cache` for caching
- Keep Gradle daemon running

## Daemon Crashed

```bash
./gradlew --stop
rm -rf ~/.gradle/daemon
./gradlew assembleDebug
```