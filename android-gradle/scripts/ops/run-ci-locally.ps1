#!/usr/bin/env bash
# run-ci-locally.ps1
# Simulate GitHub Actions CI environment locally

$ErrorActionPreference = "Stop"

Write-Host "=== Simulating CI Build ===" -ForegroundColor Cyan
Write-Host ""

$tasks = @(
    @{ Name = "spotlessCheck"; Desc = "Code formatting check" },
    @{ Name = "lintDebug"; Desc = "Lint analysis" },
    @{ Name = "testDebugUnitTest"; Desc = "Unit tests" },
    @{ Name = "assembleDebug"; Desc = "Build debug APK" }
)

$failed = $false

foreach ($task in $tasks) {
    Write-Host "[RUN] ./gradlew $($task.Name)" -ForegroundColor Yellow
    Write-Host "      → $($task.Desc)" -ForegroundColor Gray

    $start = Get-Date
    $result = & "$PSScriptRoot\..\..\..\gradlew.bat" $task.Name 2>&1
    $exitCode = $LASTEXITCODE
    $elapsed = (Get-Date) - $start

    if ($exitCode -eq 0) {
        Write-Host "[OK] $($task.Name) completed in $($elapsed.TotalSeconds)s" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $($task.Name) failed after $($elapsed.TotalSeconds)s" -ForegroundColor Red
        $failed = $true
    }
    Write-Host ""
}

if ($failed) {
    Write-Host "=== CI Simulation FAILED ===" -ForegroundColor Red
    exit 1
} else {
    Write-Host "=== CI Simulation PASSED ===" -ForegroundColor Green
    exit 0
}