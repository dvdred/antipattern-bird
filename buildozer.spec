[app]
title = AntiPattern Bird Epic Game
package.name = antipatternbird
package.domain = com.dvdred

source.dir = .
source.include_exts = py,png,wav,ttf
source.include_patterns = assets/*,*.py,*.png,*.wav,*.ttf

version = 1.0.0

# IMPORTANTE: Solo pygame-ce, non pygame! E python3 con versione specifica
requirements = python3==3.10.14,kivy,pygame-ce

orientation = portrait
fullscreen = 1

# Icona e splash
icon.filename = icon32.png
presplash.filename = icon32.png

# Permessi Android (rimosso INTERNET se non serve)
android.permissions = VIBRATE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a

# Meta
author = dvdred@gmail.com

[buildozer]
log_level = 2
warn_on_root = 1
p4a.branch = develop
p4a.use_pip_install_args = --no-user
android.accept_sdk_license = True