# app/services/android_share_intent.py
"""Faz o app receber arquivos .json compartilhados por outros apps no
Android (WhatsApp, Drive, gerenciador de arquivos etc.) — tanto pela
folha de compartilhamento nativa ("Compartilhar" -> escolher este app,
ACTION_SEND) quanto abrindo o arquivo direto (ACTION_VIEW). Os
intent-filters que fazem o app aparecer nesses menus estão em
android_intent_filters.xml (ver buildozer.spec: android.manifest.intent_filters).
"""
from kivy.utils import platform


def processar_intent_recebido(ao_receber_arquivo):
    """Verifica se o app foi aberto por um arquivo compartilhado (checagem
    inicial) e passa a escutar por novos compartilhamentos recebidos
    enquanto o app já está aberto (android.manifest.launch_mode =
    singleTask garante que o Android reaproveita a mesma instância em vez
    de abrir uma nova). Chama `ao_receber_arquivo(caminho_local)` com um
    caminho de arquivo comum (já copiado para o armazenamento do app)."""
    if platform != "android":
        return

    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    activity = PythonActivity.mActivity

    def _tratar(intent):
        if intent is None:
            return
        try:
            acao = intent.getAction()
            uri = None
            if acao == Intent.ACTION_SEND:
                uri = intent.getParcelableExtra(Intent.EXTRA_STREAM)
            elif acao == Intent.ACTION_VIEW:
                uri = intent.getData()
            if uri is None:
                return

            from androidstorage4kivy import SharedStorage
            caminho_local = SharedStorage().copy_from_shared(uri)
            if caminho_local:
                ao_receber_arquivo(caminho_local)
        except Exception:
            import traceback
            traceback.print_exc()

    # Checagem do intent que abriu/trouxe o app para frente desta vez.
    _tratar(activity.getIntent())

    from android import activity as android_activity_signals

    def _ao_novo_intent(intent):
        # Chamado pela thread de UI do Android (fora da thread do Kivy);
        # tanto `ao_receber_arquivo` (populate_screen cria widgets, abre
        # Snackbar) quanto o resto do fluxo precisam voltar pra thread do
        # Kivy antes de tocar em qualquer widget — mesma pegadinha do
        # fluxo de impressão em app/services/android_print.py.
        activity.setIntent(intent)
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: _tratar(intent), 0)

    android_activity_signals.bind(on_new_intent=_ao_novo_intent)
