# app/services/paths.py
"""Caminhos de armazenamento do app — resolvidos corretamente em cada
plataforma.

No Android, `Path.home()` não aponta para a pasta do app: a variável de
ambiente HOME não é definida pelo runtime, e o fallback do Python cai para
"/data" (raiz da partição de dados do sistema, sem permissão de escrita para
o app), quebrando geração de PDF, exportação e o seletor de arquivos. O
caminho correto no Android é o "app storage" fornecido pelo próprio sistema.
"""
from pathlib import Path

from kivy.utils import platform


def pasta_privada_app() -> Path:
    """Diretório base gravável do app (equivalente ao Path.home() correto)."""
    if platform == "android":
        from android.storage import app_storage_path
        return Path(app_storage_path())
    return Path.home()


def pasta_fichas() -> Path:
    """Pasta onde PDFs/HTMLs gerados e dados exportados são salvos."""
    pasta = pasta_privada_app() / "FichaObreiro"
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta
