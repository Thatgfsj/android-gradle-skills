#!/usr/bin/env bash
# gradle-optimize.ps1
# Optimize Gradle build settings

$ErrorActionPreference = "Stop"

Write-Host "=== Gradle Optimization Script ===" -ForegroundColor Cyan

$gradlePropsPath = "$PSScriptRoot\..\..\..\gradle.properties"

if (-not (Test-Path $gradlePropsPath)) {
    Write-Host "[WARN] gradle.properties not found, creating new one" -ForegroundColor Yellow
    $content = @"
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m -XX:+HeapDumpOnOutOfMemoryError
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.daemon=true

android.useAndroidX=true
android.enableJetifier=true

kotlin.code.style=official
"@
    Set-Content -Path $gradlePropsPath -Value $content -Encoding UTF8
}

$optimizedContent = @"
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m -XX:+HeapDumpOnOutOfMemoryError
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.daemon=true

android.useAndroidX=true
android.enableJetifier=true

kotlin.code.style=official
"@

Set-Content -Path $gradlePropsPath -Value $optimizedContent -Encoding UTF8

Write-Host ""
Write-Host "[OK] Gradle settings optimized:" -ForegroundColor Green
Write-Host "  - org.gradle.parallel=true"
Write-Host "  - org.gradle.caching=true"
Write-Host "  - org.gradle.daemon=true"
Write-Host "  - JVM: -Xmx2048m -XX:MaxMetaspaceSize=512m"
Write-Host ""
Write-Host "Apply changes by restarting Gradle daemon:" -ForegroundColor Yellow
Write-Host "  ./gradlew --stop"