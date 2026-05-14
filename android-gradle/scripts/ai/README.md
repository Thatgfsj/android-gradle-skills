# AI-Callable Scripts

Scripts for AI agents to interact with the Gradle build system.

## Available Scripts

### add-dependency.py

Add a dependency to `gradle/libs.versions.toml`.

```bash
python add-dependency.py androidx.core core-ktx 1.13.1
```

### create-module.py

Create a new Android library module skeleton.

```bash
python create-module.py :core:network
```

### run-gradle-task.py

Safely execute a Gradle task.

```bash
python run-gradle-task.py assembleDebug
python run-gradle-task.py testDebugUnitTest
```