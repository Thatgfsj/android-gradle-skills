# Performance Optimization

## Parallel Builds

Enable in `gradle.properties`:

```properties
org.gradle.parallel=true
```

## Build Cache

```properties
org.gradle.caching=true
```

## Daemon

```properties
org.gradle.daemon=true
```

## JVM Memory

```properties
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m \
    -XX:+HeapDumpOnOutOfMemoryError \
    -XX:+UseG1GC
```

## Incremental Compilation

Kotlin incremental compilation is enabled by default. For large projects:

```properties
kotlin.incremental=true
kotlin.incremental.useClasspathSnapshot=true
```

## Configuration Cache

Reduce configuration time (AGP 8.7+):

```properties
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn
```

Note: Some plugins may not support configuration cache yet.

## Avoiding Non-Configurable Issues

Avoid calling `allprojects` or `subprojects` in configuration phase:

```kotlin
// Slow - evaluates all projects eagerly
allprojects {
    tasks.withType<JavaCompile> {
        options.encoding = "UTF-8"
    }
}

// Better - lazy evaluation
subprojects {
    tasks.withType<JavaCompile>().configureEach {
        options.encoding = "UTF-8"
    }
}
```

## Module Structure Impact

- Use `implementation` instead of `api` to reduce downstream compilation
- Consider splitting large modules into smaller ones
- Use `core:network`, `core:ui` structure for better parallelism

## Build Scans

Generate build scan for analysis:

```bash
./gradlew assembleDebug --build-scan
```

Accept terms at the prompt. View detailed analysis at scans.gradle.com.

## Common Bottlenecks

1. **Configuration phase** - Too many projects or expensive plugins
2. **Task execution** - Unnecessary dependencies between tasks
3. **Resource processing** - Large resources or inefficient resource handling

## Benchmarking

Compare build times:

```bash
./gradlew assembleDebug --dry-run  # Show task graph
./gradlew assembleDebug --info 2>&1 | grep "TOTAL"  # Timing
```

## Tips

- Keep AGP and Gradle updated
- Use `configureEach` instead of `all` for lazy configuration
- Avoid `project.afterEvaluate` when possible
- Use build scan to identify bottlenecks