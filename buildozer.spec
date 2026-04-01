[app]
title = StudyApp
package.name = studyapp
package.domain = com.shahidkhan

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.include_patterns = assets/*,data/*

version = 1.0

# Stable requirements that work on Android
requirements = python3,kivy==2.3.0,pillow,android

orientation = portrait

# Android 5.0+ support
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# Build for both old and new phones
android.archs = arm64-v8a, armeabi-v7a

# Permissions — none needed (fully offline app)
android.permissions =

# Security
android.allow_backup = False

# Fixes black screen on many Android devices
android.meta_data = android.max_aspect=2.1

android.manifest.intent_filters =

fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
