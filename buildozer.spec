[app]
title = Ficha Obreiro ICM
package.name = fichaobreiro
package.domain = org.icm.ficha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,ttf
version = 1.0.0

requirements = python3,kivy==2.3.0,kivymd==1.1.1,sqlalchemy,jinja2,pillow

# Permissões Android
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
android.api = 33
android.minapi = 24
android.ndk_api = 24
arch = arm64-v8a

# Orientação responsiva
orientation = user
fullscreen = 0

# Ícone e splash
#icon.filename = assets/icon.png
#presplash.filename = assets/splash.png

# Assinatura release
#android.release_artifact = aab
#android.keystore = ./release.keystore
#android.keyalias = ficha
#android.keyalias_password = ****

[buildozer]
log_level = 2
warn_on_root = 0