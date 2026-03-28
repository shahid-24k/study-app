[app]
title = StudyApp
package.name = studyapp
package.domain = com.shahidkhan

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.include_patterns = assets/*,data/*

version = 1.0

# kivy==2.2.1 is stable for API 21 old phones
requirements = python3==3.11.6,kivy==2.2.1,pillow

# Orientation
orientation = portrait

# android.minapi=21 = Android 5.0 Lollipop and above (very old phone support)
# android.api=33    = target modern Android (required for most app stores)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.ndk_api = 21

# armeabi-v7a = old 32-bit phones | arm64-v8a = modern 64-bit phones
android.archs = arm64-v8a, armeabi-v7a

# SECURITY: No internet permission = zero network attack surface
android.permissions =

# Prevent ADB data extraction
android.allow_backup = False

android.manifest.intent_filters =
android.add_aars =

# Performance tuning for old/low-end GPUs
android.env_vars = KIVY_GL_BACKEND=sdl2,KIVY_WINDOW=sdl2

fullscreen = 0

# Uncomment to set app icon (place 512x512 icon.png in assets/)
# icon.filename = assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
