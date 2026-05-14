#!/usr/bin/env python3
"""
run-gradle-task.sh <task>
Safely executes a Gradle task with error handling

Usage:
    python run-gradle-task.py assembleDebug
    python run-gradle-task.py testDebugUnitTest
"""

import sys
import subprocess
import os
from pathlib import Path

def run_gradle_task(task):
    project_root = Path(__file__).parent.parent.parent.parent
    gradlew = project_root / "gradlew"

    if not gradlew.exists():
        gradlew = project_root / "gradlew.bat"
        if not gradlew.exists():
            print(f"[ERROR] gradlew not found in {project_root}")
            return False

    print(f"[INFO] Running ./gradlew {task}...")

    cmd = [str(gradlew), task] if os.name != 'nt' else [str(gradlew), task]

    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            env={**os.environ, "TERM": "dumb"},
            timeout=600
        )

        if result.returncode == 0:
            print(f"[OK] Task '{task}' completed successfully")
            return True
        else:
            print(f"[ERROR] Task '{task}' failed with exit code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print(f"[ERROR] Task '{task}' timed out after 600 seconds")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to run task '{task}': {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run-gradle-task.py <task>")
        print("Example: python run-gradle-task.py assembleDebug")
        sys.exit(1)

    task = sys.argv[1]
    success = run_gradle_task(task)
    sys.exit(0 if success else 1)