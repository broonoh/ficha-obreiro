[app]
title = Ficha do Obreiro
package.name = fichaobreiro
package.domain = org.icm.ficha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,ttf
source.exclude_dirs = venv,.buildozer,.git,bin
source.exclude_patterns = ficha_obreiro.db
version = 1.0.0

# WeasyPrint não roda no Android (depende de Pango/GObject/HarfBuzz/
# Fontconfig, bibliotecas C sem receita no p4a) — removido daqui; o PDF
# nativo no Android é gerado via WebView (app/services/android_print.py).
# markupsafe continua pois é dependência direta do jinja2 (usado para
# montar o HTML em ambas as plataformas).
requirements = python3,kivy==2.3.0,kivymd==1.1.1,sqlalchemy,typing_extensions,jinja2,markupsafe,pillow,androidstorage4kivy

# Permissões Android (inclui as exigidas pelo androidstorage4kivy para
# compartilhar o PDF/dados exportados via "Enviar PDF"/"Enviar Dados")
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO,INTERNET
android.api = 34
android.minapi = 24
android.ndk_api = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
android.sdk_path = /home/broonoh/Android/Sdk
# O sdkmanager novo do SDK já instalado aqui (cmdline-tools 23.0) trocou o
# formato de saída do '--list' por um CLI incompatível com o parser do
# buildozer 1.6.0 ("Did not find any build tools available to download").
# Como build-tools e a platform já estão instalados localmente, pulamos essa
# checagem online em vez de depender do parsing quebrado.
android.skip_update = True
# O python-for-android "master" (o default do buildozer) empacota Python
# 3.14, cujos arquivos .c pré-cythonizados do Kivy 2.3.0 são incompatíveis
# (API interna do CPython mudou: _PyInterpreterState_GetConfig etc. não
# existem mais). A tag v2024.01.21 empacota Python 3.11.5, compatível.
p4a.branch = v2024.01.21

# Classe Java auxiliar (android_java_src/.../PdfPrinter.java): gera o PDF
# de verdade a partir do WebView escrevendo direto num arquivo nosso, sem
# passar pela UI/spooler de impressão do sistema — permite abrir o
# compartilhamento nativo (ShareSheet) assim que o PDF estiver pronto, em
# vez do fluxo confuso de "Salvar" do diálogo de impressão do Android.
android.add_src = android_java_src

# Faz o app aparecer na folha de compartilhamento nativa do Android (ex.:
# "Compartilhar" num .json no WhatsApp/Drive/gerenciador de arquivos) e
# permite abrir esses arquivos direto nele — ver android_intent_filters.xml
# e app/services/android_share_intent.py.
android.manifest.intent_filters = android_intent_filters.xml
# singleTask: reaproveita a mesma instância do app (em vez de abrir uma
# nova) quando ele já está aberto e recebe um novo arquivo compartilhado,
# permitindo tratar isso via onNewIntent.
android.manifest.launch_mode = singleTask

# Orientação responsiva
orientation = all
fullscreen = 0

# Ícone e splash
icon.filename = assets/icon.png
presplash.filename = assets/splash.png
android.presplash_color = #03223F

# Assinatura release
#android.release_artifact = aab
#android.keystore = ./release.keystore
#android.keyalias = ficha
#android.keyalias_password = ****

[buildozer]
log_level = 2
warn_on_root = 0