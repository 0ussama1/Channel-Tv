[app]
title = Sat Channel Editor Pro
package.name = satchannelpro
package.domain = org.oussama.sat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,m3u,cfg
version = 1.0.1

requirements = python3==3.11.9,kivy==2.3.0,kivymd==1.2.0,plyer,pillow

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.private_storage = True
android.accept_sdk_license = True
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
