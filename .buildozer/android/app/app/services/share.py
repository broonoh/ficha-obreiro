# app/services/share.py
"""Compartilhamento de arquivos (PDF gerado / dados exportados) com outra
pessoa (ex.: obreiro envia para o pastor completar a parte dele).

No Android, abre a folha de compartilhamento nativa (WhatsApp, E-mail,
Drive etc.) via androidstorage4kivy. Em desktop (ambiente de
desenvolvimento/testes), não existe uma folha de compartilhamento nativa
fora do Android, então revelamos o arquivo no gerenciador de arquivos do
sistema para o usuário anexar manualmente onde quiser.
"""
import shutil
import subprocess
import sys
from pathlib import Path

from kivy.utils import platform


def compartilhar_arquivo(caminho: str):
    if not Path(caminho).exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    if platform == "android":
        _compartilhar_android(caminho)
    else:
        _revelar_no_gerenciador(caminho)


def visualizar_arquivo(caminho: str):
    """Abre o próprio arquivo (não a pasta) no visualizador padrão do
    sistema — usado para a pré-visualização antes de enviar."""
    if not Path(caminho).exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    if platform == "android":
        _visualizar_android(caminho)
    else:
        _abrir_arquivo_desktop(caminho)


def _compartilhar_android(caminho: str):
    from androidstorage4kivy import SharedStorage, ShareSheet

    shared_file = SharedStorage().copy_to_shared(caminho)
    if shared_file is None:
        raise RuntimeError("Não foi possível preparar o arquivo para compartilhamento.")
    ShareSheet().share_file(shared_file)


def _visualizar_android(caminho: str):
    from androidstorage4kivy import SharedStorage, ShareSheet

    shared_file = SharedStorage().copy_to_shared(caminho)
    if shared_file is None:
        raise RuntimeError("Não foi possível preparar o arquivo para visualização.")
    ShareSheet().view_file(shared_file)


def _abrir_arquivo_desktop(caminho: str):
    if sys.platform.startswith("linux"):
        subprocess.Popen(["xdg-open", caminho])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", caminho])
    elif sys.platform.startswith("win"):
        import os
        os.startfile(caminho)  # noqa: S606 (abertura local do próprio PDF gerado)


def _revelar_no_gerenciador(caminho: str):
    """Abre o gerenciador de arquivos já apontando/selecionando o arquivo.

    `xdg-open <pasta>` sozinho às vezes reaproveita uma janela do
    gerenciador já aberta (ex.: Dolphin em KDE roda como processo único) e
    não traz essa janela para frente — parece que "não fez nada". Damos
    preferência a comandos que sabidamente selecionam o arquivo e pedimos
    explicitamente para ativar a janela."""
    pasta = str(Path(caminho).parent)
    if sys.platform.startswith("linux"):
        comandos = [
            ["dolphin", "--select", caminho],  # KDE
            ["nautilus", "--select", caminho],  # GNOME
            ["nemo", caminho],  # Cinnamon
            ["xdg-open", pasta],  # genérico, último recurso
        ]
        for cmd in comandos:
            if shutil.which(cmd[0]):
                subprocess.Popen(cmd)
                return
    elif sys.platform == "darwin":
        subprocess.Popen(["open", "-R", caminho])
    elif sys.platform.startswith("win"):
        subprocess.Popen(["explorer", f"/select,{caminho}"])
