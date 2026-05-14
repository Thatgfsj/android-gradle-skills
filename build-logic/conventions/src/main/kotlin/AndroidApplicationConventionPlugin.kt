package com.thatgfsj.plugins

import com.android.build.api.dsl.ApplicationExtension
import org.gradle.api.Plugin
import org.gradle.api.plugins.PluginManager

class AndroidApplicationConventionPlugin : Plugin<Any> {
    override fun apply(target: Any) {
        val pluginManager: PluginManager = target as? PluginManager
            ?: (target as? org.gradle.api.Project)?.plugins
            ?: throw IllegalArgumentException("Plugin must be applied to a Project or PluginManager")

        val project = if (target is org.gradle.api.Project) target else null

        pluginManager.apply("com.android.application")
        pluginManager.apply("org.jetbrains.kotlin.android")
        pluginManager.apply("org.jetbrains.kotlin.plugin.compose")

        project?.let { p ->
            p.extensions.configure<ApplicationExtension> {
                compileSdk = 34
                defaultConfig {
                    minSdk = 26
                    targetSdk = 34
                    versionCode = 1
                    versionName = "1.0.0"
                    testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
                    vectorDrawables {
                        useSupportLibrary = true
                    }
                }

                buildFeatures {
                    compose = true
                }

                compileOptions {
                    sourceCompatibility = JavaVersion.VERSION_17
                    targetCompatibility = JavaVersion.VERSION_17
                }

                kotlinOptions {
                    jvmTarget = "17"
                }

                packaging {
                    resources {
                        excludes += listOf("/META-INF/{AL2.0,LGPL2.1}")
                    }
                }
            }

            p.dependencies {
                "implementation"(p.dependencies.platform("androidx.compose:compose-bom:2024.11.00"))
                "implementation"("androidx.core:core-ktx:1.13.1")
                "implementation"("androidx.activity:activity-compose:1.9.3")
                "implementation"("androidx.compose.ui:ui")
                "implementation"("androidx.compose.ui:ui-graphics")
                "implementation"("androidx.compose.ui:ui-tooling-preview")
                "implementation"("androidx.compose.material3:material3")
                "testImplementation"("junit:junit:4.13.2")
                "androidTestImplementation"("androidx.test.ext:junit:1.2.1")
                "androidTestImplementation"("androidx.test.espresso:espresso-core:3.6.1")
            }
        }
    }
}