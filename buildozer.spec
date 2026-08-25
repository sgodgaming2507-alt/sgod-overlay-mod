[app]
title = SGOD Mod Panel
package.name = sgodmod
package.domain = org.sgod
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.2.1
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,SYSTEM_ALERT_WINDOW
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True

android.presplash_filename = presplash.png
android.presplash_color = #000000

[buildozer]
log_level = 1
warn_on_root = 1
