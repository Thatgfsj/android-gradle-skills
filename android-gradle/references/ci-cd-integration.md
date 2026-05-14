# CI/CD Integration

## GitHub Actions

### Basic Validation Workflow

```yaml
name: Android CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3
        with:
          gradle-home: ~/.gradle

      - name: Cache Gradle packages
        uses: actions/cache@v4
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/native
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.lockfile') }}
          restore-keys: ${{ runner.os }}-gradle-

      - name: Run lint
        run: ./gradlew lintDebug

      - name: Run unit tests
        run: ./gradlew testDebugUnitTest

      - name: Build debug APK
        run: ./gradlew assembleDebug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: debug-apk
          path: app/build/outputs/apk/debug/*.apk
```

### Release Workflow

```yaml
name: Release Build

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Release version'
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Decode keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > app/keystore.jks

      - name: Build release APK
        env:
          KEY_STORE_PASSWORD: ${{ secrets.KEY_STORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        run: |
          ./gradlew assembleRelease \
            -PKEYSTORE_PATH=app/keystore.jks \
            -PKEY_STORE_PASSWORD=$KEY_STORE_PASSWORD \
            -PKEY_ALIAS=$KEY_ALIAS \
            -PKEY_PASSWORD=$KEY_PASSWORD

      - name: Upload release APK
        uses: actions/upload-artifact@v4
        with:
          name: release-apk
          path: app/build/outputs/apk/release/*.apk
```

## GitLab CI

```yaml
image: openjdk:17

stages:
  - build
  - test

variables:
  GRADLE_OPTS: "-Dorg.gradle.daemon=true"

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .gradle/caches
    - .gradle/native

build:
  stage: build
  script:
    - ./gradlew assembleDebug
  artifacts:
    paths:
      - app/build/outputs/apk/debug/*.apk

test:
  stage: test
  script:
    - ./gradlew testDebugUnitTest
```

## Build Reports

Upload test and lint reports:

```yaml
- name: Upload test reports
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-reports
    path: |
      **/build/reports/tests/testDebugUnitTest/*
      **/build/outputs/lint-results*
```

## Gradle Enterprise

For self-hosted Gradle Enterprise:

```yaml
- name: Run build with scan
  run: ./gradlew assembleDebug --build-scan
  env:
    GRADLE_ENTERPRISE_URL: ${{ secrets.GE_URL }}
    GRADLE_ENTERPRISE_ACCESS_KEY: ${{ secrets.GE_ACCESS_KEY }}
```