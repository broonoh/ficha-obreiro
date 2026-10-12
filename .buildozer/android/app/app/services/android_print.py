# app/services/android_print.py
"""Gera PDF de verdade no Android usando o WebView nativo (mesmo motor de
renderização usado pelo Chrome) — o WeasyPrint não funciona no Android
porque ainda depende de Pango/GObject/HarfBuzz/Fontconfig (bibliotecas C
do sistema Linux desktop, sem equivalente/receita no python-for-android).

Como o HTML já gerado usa CSS moderno (flexbox, @page), o WebView do
Android — que é baseado no Chromium — reproduz o layout corretamente,
diferente de bibliotecas Python puras (xhtml2pdf etc.) que só suportam
CSS antigo.

Em vez de abrir a UI de impressão do sistema (`PrintManager.print()`) —
que gera confusão sobre "onde foi salvo o arquivo", já que quem escolhe o
destino é um picker do próprio Android fora do controle do app — usamos a
classe auxiliar Java `org.icm.ficha.util.PdfPrinter` (android_java_src/)
para escrever o PDF diretamente num arquivo nosso, usando o mesmo
adaptador de impressão do WebView por baixo dos panos. Com o arquivo
pronto em mãos, abrimos o compartilhamento nativo do Android (ShareSheet)
na sequência, deixando claro pra onde o PDF vai (WhatsApp, Drive, Arquivos
etc.) em vez de um "salvo em algum lugar" sem retorno visual.
"""
from jnius import autoclass, cast, PythonJavaClass, java_method

# Mantém referências vivas até o callback assíncrono do WebView disparar —
# caso contrário o Python coletaria esses objetos (GC) antes da impressão.
_referencias_vivas = []


class _Runnable(PythonJavaClass):
    __javainterfaces__ = ['java/lang/Runnable']
    __javacontext__ = 'app'

    def __init__(self, func):
        super().__init__()
        self._func = func

    @java_method('()V')
    def run(self):
        # Roda na UI thread do Android, fora do fluxo normal do Kivy — sem
        # isso, uma exceção aqui não aparece em lugar nenhum do log.
        try:
            self._func()
        except Exception:
            import traceback
            traceback.print_exc()


class _PdfCallback(PythonJavaClass):
    __javainterfaces__ = ['org/icm/ficha/util/PdfPrinter$Callback']
    __javacontext__ = 'app'

    def __init__(self, on_success, on_error):
        super().__init__()
        self._on_success = on_success
        self._on_error = on_error

    @java_method('()V')
    def onSuccess(self):
        try:
            self._on_success()
        except Exception:
            import traceback
            traceback.print_exc()

    @java_method('(Ljava/lang/String;)V')
    def onError(self, message):
        try:
            self._on_error(message)
        except Exception:
            import traceback
            traceback.print_exc()


def gerar_pdf_android(html: str, output_path: str, ao_concluir=None, ao_falhar=None):
    """Gera um PDF de verdade a partir do HTML (via WebView) escrevendo
    direto em `output_path`. `html` é o conteúdo (string), não um caminho
    de arquivo — evita qualquer problema de permissão de leitura de
    arquivo pelo WebView.

    Ao terminar, chama `ao_concluir(output_path)` (na UI thread do
    Android) ou `ao_falhar(mensagem)` em caso de erro."""
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WebView = autoclass('android.webkit.WebView')
    View = autoclass('android.view.View')
    ViewGroup = autoclass('android.view.ViewGroup')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    Handler = autoclass('android.os.Handler')
    Looper = autoclass('android.os.Looper')
    PdfPrinter = autoclass('org.icm.ficha.util.PdfPrinter')

    activity = PythonActivity.mActivity

    def _criar_e_imprimir():
        webview = WebView(activity)
        _referencias_vivas.append(webview)

        # O WebView PRECISA estar anexado à hierarquia de views da janela
        # com o tamanho final já correto: anexar com 1x1 (como antes) faz
        # o Chromium renderizar/paginar o conteúdo nesse espaço minúsculo
        # logo no load, e um redimensionamento manual depois (measure()/
        # layout() direto no Java) não força o reflow a tempo — o bitmap
        # final saía em branco. Em vez de 1x1, anexamos já na largura de
        # página usada pelo PdfPrinter (ver PdfPrinter.PAGE_WIDTH_PT *
        # SCALE) com uma altura de sobra, e escondemos via visibility (não
        # via tamanho) — View.draw() ignora visibility quando chamado
        # diretamente, mas o Chromium já terá feito layout no tamanho
        # certo desde o início.
        PAGE_WIDTH_PT = 595
        SCALE = 2
        largura_px = PAGE_WIDTH_PT * SCALE
        webview.setVisibility(View.INVISIBLE)

        decor_view = activity.getWindow().getDecorView()
        root = cast('android.view.ViewGroup', decor_view)
        root.addView(webview, LayoutParams(largura_px, 20000))

        webview.loadDataWithBaseURL(None, html, "text/html", "UTF-8", None)

        def _limpar():
            try:
                root.removeView(webview)
            except Exception:
                pass
            _referencias_vivas.clear()

        def _sucesso():
            _limpar()
            if ao_concluir:
                # O callback chega aqui pela thread de UI do Android (via
                # runOnUiThread), que não é a mesma thread em que o Kivy
                # roda seu loop gráfico — criar qualquer widget (Snackbar,
                # dialog etc.) direto daqui derruba o app com
                # "Cannot create graphics instruction outside the main
                # Kivy thread". Precisa voltar pra thread do Kivy.
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: ao_concluir(output_path), 0)

        def _erro(mensagem):
            _limpar()
            if ao_falhar:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: ao_falhar(mensagem), 0)

        def _gerar():
            PdfPrinter.printToFile(webview, output_path, _PdfCallback(_sucesso, _erro))

        # Handler preso ao Looper principal, independente do estado de
        # anexação da View — diferente de `webview.postDelayed`, que exige
        # a View já anexada para processar sua fila interna. O HTML é
        # local, sem imagens externas por URL (a foto já vem embutida em
        # base64), então carrega quase instantaneamente — 1.5s é folga.
        Handler(Looper.getMainLooper()).postDelayed(_Runnable(_gerar), 1500)

    activity.runOnUiThread(_Runnable(_criar_e_imprimir))
