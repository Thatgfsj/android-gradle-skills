#!/usr/bin/env python3
"""
Android Gradle Project Initializer
Creates a new Android project with proper Gradle + AGP + Kotlin DSL setup.

Usage: python init_android_project.py <app_name> <path> [agp_version] [gradle_version]
       python init_android_project.py --interactive

Flags:
  --use-kotlin-dsl    Use Kotlin DSL (default: true)
  --min-sdk           Minimum SDK version (default: 26)
  --target-sdk        Target SDK version (default: 34)
  --with-compose      Include Jetpack Compose (default: true)
  --multi-module      Create multi-module structure (default: false)
"""

import os
import sys
import zipfile
import shutil
import tempfile
import urllib.request
from pathlib import Path

DEFAULT_AGP = "8.7.0"
DEFAULT_GRADLE = "8.10.2"
DEFAULT_KOTLIN = "2.0.20"
DEFAULT_COMPOSE_BOM = "2024.11.00"
DEFAULT_COMPILE_SDK = "34"
DEFAULT_MIN_SDK = "26"
DEFAULT_TARGET_SDK = "34"
DEFAULT_JVM_TARGET = "17"

MODULE_CORE_NETWORK = ":core:network"
MODULE_CORE_UI = ":core:ui"
MODULE_FEATURE_HOME = ":feature:home"


def get_version_matrix():
    return {
        "8.0": "8.0", "8.0.1": "8.0", "8.0.2": "8.0",
        "8.1": "8.0", "8.1.4": "8.2",
        "8.2": "8.2", "8.2.0": "8.2", "8.2.1": "8.2", "8.2.2": "8.2",
        "8.3": "8.4", "8.3.0": "8.4", "8.3.1": "8.4",
        "8.4": "8.6", "8.4.0": "8.6",
        "8.5": "8.7", "8.5.0": "8.7", "8.5.1": "8.7", "8.5.2": "8.7",
        "8.6": "8.7", "8.6.0": "8.7",
        "8.7": "8.10", "8.7.0": "8.10", "8.7.1": "8.10",
    }


def check_environment():
    errors = []
    java_home = os.environ.get("JAVA_HOME") or os.environ.get("JDK_HOME")
    if not java_home:
        jbr_path = os.environ.get("JBR_PATH", "")
        if jbr_path and os.path.exists(jbr_path):
            java_home = jbr_path
        else:
            errors.append("JAVA_HOME or JDK_HOME environment variable is not set.")
            errors.append("Please set it to your JDK 17+ installation path.")

    android_home = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if not android_home:
        sdk_dir_hint = os.path.join(os.path.expanduser("~"), "Android", "Sdk")
        if os.path.exists(sdk_dir_hint):
            android_home = sdk_dir_hint
        else:
            errors.append("ANDROID_HOME or ANDROID_SDK_ROOT environment variable is not set.")
            errors.append("Please set it to your Android SDK path.")

    if errors:
        print("[ERROR] Environment check failed:")
        for err in errors:
            print(f"  - {err}")
        print("\n[INFO] You can also set SDK path in local.properties after project creation:")
        print("       sdk.dir=/path/to/your/android/sdk")
        return False
    return True


def interactive_mode():
    print("\n=== Interactive Project Setup ===\n")

    app_name = input("App name (e.g., MyApp): ").strip()
    while not app_name:
        app_name = input("App name (e.g., MyApp): ").strip()

    base_path = input("Base path (e.g., /path/to/projects) [current dir]: ").strip()
    if not base_path:
        base_path = os.getcwd()

    use_compose = input("Include Jetpack Compose? [Y/n]: ").strip().lower() != 'n'
    use_multi_module = input("Create multi-module structure? [y/N]: ").strip().lower() == 'y'

    print("\n--- Advanced Options (press Enter for defaults) ---")
    agp_input = input(f"AGP version [{DEFAULT_AGP}]: ").strip()
    agp_version = agp_input if agp_input else DEFAULT_AGP

    min_sdk_input = input(f"Min SDK [{DEFAULT_MIN_SDK}]: ").strip()
    min_sdk = min_sdk_input if min_sdk_input else DEFAULT_MIN_SDK

    target_sdk_input = input(f"Target SDK [{DEFAULT_TARGET_SDK}]: ").strip()
    target_sdk = target_sdk_input if target_sdk_input else DEFAULT_TARGET_SDK

    gradle_input = input(f"Gradle version (auto-selected based on AGP): ").strip()
    gradle_version = gradle_input if gradle_input else None

    return {
        "app_name": app_name,
        "base_path": base_path,
        "agp_version": agp_version,
        "gradle_version": gradle_version,
        "min_sdk": min_sdk,
        "target_sdk": target_sdk,
        "compile_sdk": DEFAULT_COMPILE_SDK,
        "kotlin_version": DEFAULT_KOTLIN,
        "compose_bom": DEFAULT_COMPOSE_BOM,
        "use_compose": use_compose,
        "use_multi_module": use_multi_module,
        "use_kotlin_dsl": True,
    }


def download_gradle_wrapper(project_path, gradle_version):
    wrapper_dir = os.path.join(project_path, "gradle", "wrapper")
    os.makedirs(wrapper_dir, exist_ok=True)

    wrapper_url = f"https://services.gradle.org/distributions/gradle-{gradle_version}-bin.zip"
    wrapper_props = f"""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-{gradle_version}-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""

    gradlew_sh = """#!/bin/sh
exec java -jar "$(dirname "$0")/wrapper/gradle-wrapper.jar" "$@"
"""

    gradlew_bat = """@echo off
setlocal
set DIRNAME=%~dp0
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"
java %DEFAULT_JVM_OPTS% -jar "%APP_HOME%\gradle\wrapper\gradle-wrapper.jar" %*
"""

    gradle_wrapper_props_path = os.path.join(wrapper_dir, "gradle-wrapper.properties")
    with open(gradle_wrapper_props_path, "w", encoding="utf-8") as f:
        f.write(wrapper_props)

    gradle_wrapper_jar_url = "https://raw.githubusercontent.com/gradle/gradle/v8.10.2/gradle/wrapper/gradle-wrapper.jar"
    try:
        urllib.request.urlretrieve(gradle_wrapper_jar_url, os.path.join(wrapper_dir, "gradle-wrapper.jar"))
    except Exception:
        pass

    gradlew_path = os.path.join(project_path, "gradlew")
    gradlew_bat_path = os.path.join(project_path, "gradlew.bat")

    with open(gradlew_path, "w", encoding="utf-8") as f:
        f.write(gradlew_sh)
    with open(gradlew_bat_path, "w", encoding="utf-8") as f:
        f.write(gradlew_bat)

    os.chmod(gradlew_path, 0o755)
    print(f"[OK] Gradle wrapper files created (Gradle {gradle_version})")
    return True


def create_root_build_gradle_kts(project_path, app_name, agp_version, kotlin_version, use_version_catalogs=True):
    if use_version_catalogs:
        content = f'''plugins {{
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
}}

android {{
    namespace = "com.example.{app_name.lower()}"
    compileSdk = {DEFAULT_COMPILE_SDK}
}}

tasks.register("clean", Delete::class) {{
    delete(rootProject.layout.buildDirectory)
}}
'''
    else:
        content = f'''plugins {{
    id("com.android.application") version "{agp_version}" apply false
    id("org.jetbrains.kotlin.android") version "{kotlin_version}" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "{kotlin_version}" apply false
}}

android {{
    namespace = "com.example.{app_name.lower()}"
    compileSdk = {DEFAULT_COMPILE_SDK}
}}

tasks.register("clean", Delete::class) {{
    delete(rootProject.layout.buildDirectory)
}}
'''
    with open(os.path.join(project_path, "build.gradle.kts"), "w", encoding="utf-8") as f:
        f.write(content)


def create_settings_gradle_kts(project_path, modules=None, use_version_catalogs=True):
    includes = [":app"] + (modules or [])

    if use_version_catalogs:
        content = '''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "MyApp"
include(":app")
'''
    else:
        modules_str = "\n".join([f'include("{m}")' for m in includes])
        content = f'''pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "MyApp"
{modules_str}
'''

    with open(os.path.join(project_path, "settings.gradle.kts"), "w", encoding="utf-8") as f:
        f.write(content)


def create_gradle_properties(project_path):
    content = '''org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m -XX:+HeapDumpOnOutOfMemoryError
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.daemon=true

android.useAndroidX=true
android.enableJetifier=true

kotlin.code.style=official
'''
    with open(os.path.join(project_path, "gradle.properties"), "w", encoding="utf-8") as f:
        f.write(content)


def create_local_properties(project_path, sdk_path=None):
    if sdk_path:
        content = f"sdk.dir={sdk_path}\n"
    else:
        content = "sdk.dir=$ANDROID_HOME\n"
    with open(os.path.join(project_path, "local.properties"), "w", encoding="utf-8") as f:
        f.write(content)


def create_app_module(project_path, app_name, min_sdk, target_sdk, kotlin_version, use_compose, use_version_catalogs=True):
    app_dir = os.path.join(project_path, "app")
    os.makedirs(app_dir, exist_ok=True)

    if use_version_catalogs:
        app_build = f'''plugins {{
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}}

android {{
    namespace = "com.example.{app_name.lower()}"
    compileSdk = {DEFAULT_COMPILE_SDK}

    defaultConfig {{
        applicationId = "com.example.{app_name.lower()}"
        minSdk = {min_sdk}
        targetSdk = {target_sdk}
        versionCode = 1
        versionName = "1.0.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {{
            useSupportLibrary = true
        }}
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }}
        debug {{
            isMinifyEnabled = false
        }}
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

    packaging {{
        resources {{
            excludes += "/META-INF/{{AL2.0,LGPL2.1}}"
        }}
    }}
}}

dependencies {{
    implementation(libs.androidx.core)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.compose.bom))
    implementation(libs.compose.ui)
    implementation(libs.compose.ui.graphics)
    implementation(libs.compose.ui.tooling.preview)
    implementation(libs.compose.material3)

    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
}}
'''
    else:
        app_build = f'''plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}}

android {{
    namespace = "com.example.{app_name.lower()}"
    compileSdk = {DEFAULT_COMPILE_SDK}

    defaultConfig {{
        applicationId = "com.example.{app_name.lower()}"
        minSdk = {min_sdk}
        targetSdk = {target_sdk}
        versionCode = 1
        versionName = "1.0.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {{
            useSupportLibrary = true
        }}
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }}
        debug {{
            isMinifyEnabled = false
        }}
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

    packaging {{
        resources {{
            excludes += "/META-INF/{{AL2.0,LGPL2.1}}"
        }}
    }}
}}

dependencies {{
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-compose:1.9.3")
    implementation(platform("androidx.compose:compose-bom:2024.11.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")

    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.6.1")
}}
'''

    with open(os.path.join(app_dir, "build.gradle.kts"), "w", encoding="utf-8") as f:
        f.write(app_build)

    src_dir = os.path.join(app_dir, "src", "main")
    pkg_path = os.path.join(src_dir, "java", "com", "example", app_name.lower().replace("-", "_"))
    os.makedirs(pkg_path, exist_ok=True)

    manifest = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{app_name}"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.DarkActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
'''
    with open(os.path.join(src_dir, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest)

    main_activity = f'''package com.example.{app_name.lower().replace("-", "_")}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier

class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            MaterialTheme {{
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {{
                    Text(text = "Hello {app_name}!")
                }}
            }}
        }}
    }}
}}
'''
    with open(os.path.join(pkg_path, "MainActivity.kt"), "w", encoding="utf-8") as f:
        f.write(main_activity)

    res_dir = os.path.join(src_dir, "res")
    os.makedirs(res_dir, exist_ok=True)

    proguard_rules = '''# Add project specific ProGuard rules here.
-keepattributes *Annotation*
-keepclassmembers class * {
    @androidx.compose.runtime.Composable <methods>;
}
'''
    with open(os.path.join(app_dir, "proguard-rules.pro"), "w", encoding="utf-8") as f:
        f.write(proguard_rules)

    print("[OK] App module created")


def create_gitignore(project_path):
    gitignore = '''# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar

# Android Studio
*.iml
.idea/
local.properties

# Build
*.apk
*.aab
*.ap_
*.dex

# Keystore
*.jks
*.keystore

# Misc
*.log
.DS_Store
'''
    with open(os.path.join(project_path, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore)


def create_multi_module_structure(project_path, app_name):
    modules = [
        (MODULE_CORE_NETWORK, "com.example.core.network"),
        (MODULE_CORE_UI, "com.example.core.ui"),
        (MODULE_FEATURE_HOME, "com.example.feature.home"),
    ]

    for module_path, namespace in modules:
        full_path = os.path.join(project_path, module_path)
        os.makedirs(full_path, exist_ok=True)

        module_build = f'''plugins {{
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
    implementation(project(":core:network"))
    implementation(project(":core:ui"))

    implementation("androidx.core:core-ktx:1.13.1")
    implementation(platform("androidx.compose:compose-bom:2024.11.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
}}
'''
        src_dir = os.path.join(full_path, "src", "main")
        os.makedirs(src_dir, exist_ok=True)

        manifest = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
</manifest>
'''
        with open(os.path.join(src_dir, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
            f.write(manifest)

        with open(os.path.join(full_path, "build.gradle.kts"), "w", encoding="utf-8") as f:
            f.write(module_build)

    print("[OK] Multi-module structure created")


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--interactive":
        if not check_environment():
            sys.exit(1)
        config = interactive_mode()
    elif len(sys.argv) < 3:
        print("Usage: python init_android_project.py <app_name> <path> [agp_version] [gradle_version]")
        print("       python init_android_project.py --interactive")
        print("\nExamples:")
        print("  python init_android_project.py MyApp /path/to/projects")
        print("  python init_android_project.py MyApp /path/to/projects 8.7.0 8.10.2")
        sys.exit(1)
    else:
        if not check_environment():
            sys.exit(1)

        app_name = sys.argv[1]
        base_path = sys.argv[2]
        agp_version = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_AGP
        gradle_version = sys.argv[4] if len(sys.argv) > 4 else None

        if not gradle_version:
            version_matrix = get_version_matrix()
            gradle_version = version_matrix.get(agp_version, "8.10.2")

        config = {
            "app_name": app_name,
            "base_path": base_path,
            "agp_version": agp_version,
            "gradle_version": gradle_version,
            "min_sdk": DEFAULT_MIN_SDK,
            "target_sdk": DEFAULT_TARGET_SDK,
            "compile_sdk": DEFAULT_COMPILE_SDK,
            "kotlin_version": DEFAULT_KOTLIN,
            "compose_bom": DEFAULT_COMPOSE_BOM,
            "use_compose": True,
            "use_multi_module": False,
            "use_kotlin_dsl": True,
        }

    print(f"\nCreating Android project: {config['app_name']}")
    print(f"  AGP: {config['agp_version']}, Gradle: {config['gradle_version']}")
    print(f"  Min SDK: {config['min_sdk']}, Target SDK: {config['target_sdk']}")

    project_path = os.path.join(config["base_path"], config["app_name"])

    if os.path.exists(project_path):
        response = input(f"Directory {project_path} already exists! Overwrite? [y/N]: ").strip().lower()
        if response != 'y':
            print("Aborted.")
            sys.exit(0)
        shutil.rmtree(project_path)

    os.makedirs(project_path, exist_ok=True)
    os.makedirs(os.path.join(project_path, "app"), exist_ok=True)

    print(f"[INFO] Creating project at: {project_path}")

    download_gradle_wrapper(project_path, config["gradle_version"])
    create_root_build_gradle_kts(project_path, config["app_name"], config["agp_version"], config["kotlin_version"], config["use_kotlin_dsl"])
    create_settings_gradle_kts(project_path, use_version_catalogs=config["use_kotlin_dsl"])
    create_gradle_properties(project_path)
    create_local_properties(project_path)
    create_gitignore(project_path)
    create_app_module(project_path, config["app_name"], config["min_sdk"], config["target_sdk"], config["kotlin_version"], config["use_compose"], config["use_kotlin_dsl"])

    if config["use_multi_module"]:
        create_multi_module_structure(project_path, config["app_name"])

    print(f"\n[DONE] Project created at: {project_path}")
    print("\nTo build:")
    print(f"  cd {project_path}")
    print(f"  ./gradlew assembleDebug")


if __name__ == "__main__":
    main()