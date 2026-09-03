[app]
title = SEOR Recoil Lab
package.name = seorrecoillab
package.domain = org.seor
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 35
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
