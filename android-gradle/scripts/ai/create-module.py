#!/usr/bin/env python3
"""
create-module.sh <module-name>
Creates a new Android library module skeleton

Usage:
    python create-module.py :core:network
    python create-module.py :feature:home
"""

import sys
import os
from pathlib import Path

DEFAULT_COMPILE_SDK = "34"
DEFAULT_MIN_SDK = "26"
DEFAULT_JVM_TARGET = "17"
DEFAULT_KOTLIN = "2.0.20"

def create_module(module_name):
    if not module_name.startswith(":"):
        module_name = ":" + module_name

    script_dir = Path(__file__).parent.parent.parent.parent
    project_root = script_dir.parent

    module_path = project_root / module_name.lstrip(":")
    parts = module_name.lstrip(":").split(":")
    namespace = "com.example." + module_name.lstrip(":").replace("-", "").replace("/", ".")

    if module_path.exists():
        print(f"[WARN] Module {module_name} already exists at {module_path}")
        return False

    os.makedirs(module_path / "src" / "main", exist_ok=True)

    build_gradle = f'''plugins {{
    id("com.android.library")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}}

android {{
    namespace = "{namespace}"
    compileSdk = {DEFAULT_COMPILE_SDK}

    defaultConfig {{
        minSdk = {DEFAULT_MIN_SDK}
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}

    kotlinOptions {{
        jvmTarget = "{DEFAULT_JVM_TARGET}"
    }}

    buildFeatures {{
        compose = true
    }}
}}

dependencies {{
    implementation("androidx.core:core-ktx:1.13.1")
    implementation(platform("androidx.compose:compose-bom:2024.11.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
}}
'''

    with open(module_path / "build.gradle.kts", "w", encoding="utf-8") as f:
        f.write(build_gradle)

    manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
</manifest>
'''
    with open(module_path / "src" / "main" / "AndroidManifest.xml", "w", encoding="utf-8") as f:
        f.write(manifest)

    settings_path = project_root / "settings.gradle.kts"
    if settings_path.exists():
        content = settings_path.read_text(encoding='utf-8')
        if f'include("{module_name}")' not in content:
            content = content.rstrip() + f'\ninclude("{module_name}")\n'
            settings_path.write_text(content, encoding='utf-8')
            print(f"[OK] Added include(\"{module_name}\") to settings.gradle.kts")

    print(f"[OK] Created module {module_name} at {module_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create-module.py <module-name>")
        print("Example: python create-module.py :core:network")
        sys.exit(1)

    module_name = sys.argv[1]
    success = create_module(module_name)
    sys.exit(0 if success else 1)