[app]
title = AntiPattern Bird Epic Game
package.name = antipatternbird
package.domain = com.dvdred

source.dir = .
source.include_exts = py,png,wav,ttf
source.include_patterns = assets/*,*.py,*.png,*.wav,*.ttf

version = 1.0.0

# CAMBIA QUESTA RIGA - usa pygame dalla recipe p4a
requirements = python3,kivy,pygame==2.1.3.1

orientation = portrait
fullscreen = 1

icon.filename = icon32.png
presplash.filename = icon32.png

android.permissions = VIBRATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a

# IMPORTANTE: forza l'uso della recipe pygame di p4a
p4a.bootstrap = sdl2

author = dvdred@gmail.com

[buildozer]
log_level = 2
warn_on_root = 0
p4a.branch = develop
android.accept_sdk_license = True