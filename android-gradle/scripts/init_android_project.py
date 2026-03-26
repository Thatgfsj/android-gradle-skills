#!/usr/bin/env python3
"""
Android Gradle Project Initializer
Creates a new Android project with proper Gradle + AGP + Kotlin DSL setup.
Usage: python init_android_project.py <app_name> <path> [agp_version] [gradle_version]
"""

import os
import sys
import urllib.request
import zipfile
import shutil

DEFAULT_AGP = "8.2.0"
DEFAULT_GRADLE = "8.2"
DEFAULT_KOTLIN = "1.9.20"
DEFAULT_COMPILE_SDK = 34
DEFAULT_MIN_SDK = 24
DEFAULT_TARGET_SDK = 34


def get_version_matrix():
    """Return a dict of AGP -> Gradle compatibility."""
    return {
        "8.0": "8.0", "8.0.1": "8.0", "8.0.2": "8.0",
        "8.1": "8.0", "8.1.4": "8.2",
        "8.2": "8.2", "8.2.0": "8.2", "8.2.1": "8.2", "8.2.2": "8.2",
        "8.3": "8.4", "8.3.0": "8.4", "8.3.1": "8.4", "8.3.2": "8.4",
        "8.4": "8.6", "8.4.0": "8.6", "8.4.1": "8.6", "8.4.2": "8.6",
        "8.5": "8.7", "8.5.0": "8.7", "8.5.1": "8.7", "8.5.2": "8.7",
        "8.6": "8.7", "8.6.0": "8.7", "8.6.1": "8.7",
    }


def create_gradle_wrapper(project_path, gradle_version):
    """Download Gradle and create wrapper."""
    wrapper_dir = os.path.join(project_path, "gradle", "wrapper")
    os.makedirs(wrapper_dir, exist_ok=True)

    wrapper_props = f"""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-{gradle_version}-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
    with open(os.path.join(wrapper_dir, "gradle-wrapper.properties"), "w", encoding="utf-8") as f:
        f.write(wrapper_props)

    # Copy gradlew scripts from this skill or create minimal ones
    gradlew_sh = """#!/bin/sh
# Gradle wrapper script
exec java -jar "$(dirname "$0")/gradle/wrapper/gradle-wrapper.jar" "$@"
"""
    gradlew_bat = """@echo off
setlocal
set DIRNAME=%~dp0
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%
java -jar "%APP_HOME%\\gradle\\wrapper\\gradle-wrapper.jar" %*
"""

    with open(os.path.join(project_path, "gradlew"), "w", encoding="utf-8") as f:
        f.write(gradlew_sh)
    with open(os.path.join(project_path, "gradlew.bat"), "w", encoding="utf-8") as f:
        f.write(gradlew_bat)

    print(f"[OK] Gradle Wrapper files created (Gradle {gradle_version})")
    return True


def create_build_files(project_path, app_name, agp_version, kotlin_version, compile_sdk, min_sdk, target_sdk):
    """Create all Gradle build files."""

    # Root build.gradle.kts
    root_build = f"""plugins {{
    id("com.android.application") version "{agp_version}" apply false
    id("org.jetbrains.kotlin.android") version "{kotlin_version}" apply false
}}

android {{
    namespace = "com.example.{app_name.lower()}"
    compileSdk = {compile_sdk}
}}

buildscript {{
    repositories {{
        google()
        mavenCentral()
    }}
}}

pluginManagement {{
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
"""
    with open(os.path.join(project_path, "build.gradle.kts"), "w", encoding="utf-8") as f:
        f.write(root_build)

    # settings.gradle.kts
    settings = f"""pluginManagement {{
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

rootProject.name = "{app_name}"
include(":app")
"""
    with open(os.path.join(project_path, "settings.gradle.kts"), "w", encoding="utf-8") as f:
        f.write(settings)

    # gradle.properties
    gradle_props = """# Project-wide Gradle settings
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m -XX:+HeapDumpOnOutOfMemoryError
org.gradle.parallel=true
org.gradle.caching=true

# AndroidX
android.useAndroidX=true
android.enableJetifier=true

# Kotlin
kotlin.code.style=official
"""
    with open(os.path.join(project_path, "gradle.properties"), "w", encoding="utf-8") as f:
        f.write(gradle_props)

    # local.properties
    local_props = """sdk.dir=/path/to/your/android/sdk
"""
    with open(os.path.join(project_path, "local.properties"), "w", encoding="utf-8") as f:
        f.write(local_props)

    # app/build.gradle.kts
    app_pkg = app_name.lower().replace("-", "_")
    app_build = f"""plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}}

android {{
    namespace = "com.example.{app_pkg}"
    compileSdk = {compile_sdk}

    defaultConfig {{
        applicationId = "com.example.{app_pkg}"
        minSdk = {min_sdk}
        targetSdk = {target_sdk}
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
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
        jvmTarget = "17"
    }}

    packaging {{
        resources {{
            excludes += "/META-INF/{{AL2.0,LGPL2.1}}"
        }}
    }}
}}

dependencies {{
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.activity:activity-ktx:1.8.2")
    implementation("androidx.fragment:fragment-ktx:1.6.2")

    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}}
"""
    with open(os.path.join(project_path, "app", "build.gradle.kts"), "w", encoding="utf-8") as f:
        f.write(app_build)

    print("[OK] All Gradle build files created")
    return True


def create_app_source(app_path, app_name):
    """Create minimal Android app source files."""
    pkg_dir = os.path.join(app_path, "src", "main", "java", "com", "example", app_name.lower().replace("-", "_"))
    res_dir = os.path.join(app_path, "src", "main", "res")

    os.makedirs(pkg_dir, exist_ok=True)

    # AndroidManifest.xml
    manifest = f"""<?xml version="1.0" encoding="utf-8"?>
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
"""
    with open(os.path.join(app_path, "src", "main", "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest)

    # MainActivity.kt
    main_activity = f"""package com.example.{app_name.lower().replace("-", "_")}

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }}
}}
"""
    with open(os.path.join(pkg_dir, "MainActivity.kt"), "w", encoding="utf-8") as f:
        f.write(main_activity)

    # activity_main.xml
    layout_dir = os.path.join(res_dir, "layout")
    os.makedirs(layout_dir, exist_ok=True)
    layout = f"""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:id="@+id/text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello {{app_name}}!" />

</LinearLayout>
"""
    with open(os.path.join(layout_dir, "activity_main.xml"), "w", encoding="utf-8") as f:
        f.write(layout)

    # proguard-rules.pro
    with open(os.path.join(app_path, "proguard-rules.pro"), "w", encoding="utf-8") as f:
        f.write("# Proguard rules for " + app_name + "\n")

    # .gitignore
    gitignore = """# Gradle
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
"""
    with open(os.path.join(app_path, "..", ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore)

    print("[OK] App source files created")
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python init_android_project.py <app_name> <path> [agp_version] [gradle_version]")
        print("Example: python init_android_project.py MyApp H:/Android_projects 8.2.0 8.2")
        sys.exit(1)

    app_name = sys.argv[1]
    base_path = sys.argv[2]
    agp_version = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_AGP
    gradle_version = sys.argv[4] if len(sys.argv) > 4 else get_version_matrix().get(agp_version, DEFAULT_GRADLE)

    project_path = os.path.join(base_path, app_name)

    if os.path.exists(project_path):
        print(f"[WARN] Directory {project_path} already exists!")
        response = input("Overwrite? [y/N]: ")
        if response.lower() != "y":
            sys.exit(0)
        shutil.rmtree(project_path)

    print(f"Creating Android project: {app_name}")
    print(f"  AGP: {agp_version}, Gradle: {gradle_version}")

    os.makedirs(project_path, exist_ok=True)
    os.makedirs(os.path.join(project_path, "app"), exist_ok=True)

    create_gradle_wrapper(project_path, gradle_version)
    create_build_files(project_path, app_name, agp_version, DEFAULT_KOTLIN,
                      DEFAULT_COMPILE_SDK, DEFAULT_MIN_SDK, DEFAULT_TARGET_SDK)
    create_app_source(os.path.join(project_path, "app"), app_name)

    print(f"\n[DONE] Project created at: {project_path}")
    print(f"\nTo build:")
    print(f"  cd {project_path}")
    print(f"  .\\gradlew.bat assembleDebug")


if __name__ == "__main__":
    main()
