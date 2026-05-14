#!/usr/bin/env python3
"""
update-dependencies.py
Updates dependencies to latest versions using refreshVersions

This script requires the refreshVersions plugin to be configured.
Add to settings.gradle.kts:
    pluginManagement {
        plugins {
            id("de.fayro.refreshVersions") version "0.60.0"
        }
    }
"""

import sys
import subprocess
from pathlib import Path

def update_dependencies():
    script_dir = Path(__file__).parent.parent.parent.parent
    gradlew = script_dir / "gradlew"

    if not gradlew.exists():
        gradlew = script_dir / "gradlew.bat"

    print("[INFO] Checking for refreshVersions plugin...")

    settings_path = script_dir / "settings.gradle.kts"
    if settings_path.exists():
        content = settings_path.read_text(encoding='utf-8')
        if "refreshVersions" not in content:
            print("[INFO] Adding refreshVersions plugin to settings.gradle.kts...")
            new_content = content.replace(
                'dependencyResolutionManagement {',
                'plugins {\n    id("de.fayro.refreshVersions") version "0.60.0"\n}\n\ndependencyResolutionManagement {'
            )
            settings_path.write_text(new_content, encoding='utf-8')

    print("[INFO] Running ./gradlew useLatestVersions...")
    print("[INFO] This may take a few minutes...")

    result = subprocess.run(
        [str(gradlew), "useLatestVersions", "--write"],
        cwd=script_dir,
        capture_output=False
    )

    if result == 0:
        print("[OK] Dependencies updated successfully")
        print("[INFO] Review changes and commit:")
        print("  git diff")
    else:
        print("[ERROR] Failed to update dependencies")
        return False

    return result == 0

if __name__ == "__main__":
    success = update_dependencies()
    sys.exit(0 if success else 1)