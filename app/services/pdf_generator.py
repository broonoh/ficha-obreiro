# app/services/pdf_generator.py
import base64
import os
import re
from pathlib import Path
from jinja2 import Template

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "ficha.html"
LOGO_PATH = Path(__file__).parent.parent.parent / "assets" / "logo_icm.png"

_logo_base64_cache = None


def _logo_base64() -> str:
    """Logo da ICM embutido como data URI — igual à foto do usuário, pra
    não depender de resolver caminho de arquivo relativo (WeasyPrint no
    desktop e WebView no Android resolvem isso de formas diferentes)."""
    global _logo_base64_cache
    if _logo_base64_cache is None:
        dados = LOGO_PATH.read_bytes()
        _logo_base64_cache = "data:image/png;base64," + base64.b64encode(dados).decode()
    return _logo_base64_cache


def _check(v):
    """Retorna chip visual para booleanos no PDF."""
    if v is None or v == "" or v == "None":
        return ""
    if isinstance(v, bool):
        if v:
            return '<span class="check check-yes">✓ Sim</span>'
        return '<span class="check check-no">✓ Não</span>'
    # String "True"/"False"
    if str(v).lower() in ("true", "sim", "yes"):
        return '<span class="check check-yes">✓ Sim</span>'
    if str(v).lower() in ("false", "não", "nao", "no"):
        return '<span class="check check-no">✓ Não</span>'
    return str(v)


def _v(value):
    """Normaliza valor vazio/None/indefinido para string vazia (campo em
    branco no PDF, sem travessão) — inclui campos administrativos sem tela
    própria (ex.: "Situação Final"), que nunca chegam no dicionário de dados."""
    from jinja2 import Undefined
    if isinstance(value, Undefined) or value is None or value == "" or value == "None":
        return ""
    return value


def _sim_nao(sim, nao):
    """Chip Sim/Não a partir de um par de checkboxes mutuamente exclusivos."""
    if sim:
        return '<span class="check check-yes">✓ Sim</span>'
    if nao:
        return '<span class="check check-no">✓ Não</span>'
    return ""


def gerar_pdf(dados: dict) -> str:
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        tpl = Template(f.read())

    html = tpl.render(check=_check, v=_v, sim_nao=_sim_nao, logo_base64=_logo_base64(), **dados)

    # O WeasyPrint trata espaços em branco entre tags (indentação/quebras de
    # linha do template) como itens "fantasmas" dentro de containers flex,
    # o que força quebra de linha prematura nas grades de campos (3 colunas
    # viravam 2). Remover espaços puramente entre tags resolve isso sem
    # afetar texto real (campos multilinha do usuário não têm ">...<" puro).
    html = re.sub(r">\s+<", "><", html)

    from app.services.paths import pasta_fichas
    out_dir = pasta_fichas()

    nome_seguro = (dados.get("nome") or "Obreiro").strip().replace(" ", "_")[:40]
    html_path = out_dir / f"Ficha_Obreiro_{nome_seguro}.html"
    html_path.write_text(html, encoding="utf-8")

    from kivy.utils import platform
    if platform == "android":
        # WeasyPrint ainda depende de Pango/GObject/HarfBuzz/Fontconfig
        # (bibliotecas C do desktop Linux) — sem receita no
        # python-for-android, não há como gerar PDF nativo no Android por
        # essa via. O HTML gerado aqui é usado pela tela de "Imprimir como
        # PDF" nativa do Android (app/services/android_print.py), que
        # produz o PDF de verdade usando o WebView do próprio sistema.
        return str(html_path)

    try:
        from weasyprint import HTML
        pdf_path = html_path.with_suffix(".pdf")
        HTML(string=html).write_pdf(str(pdf_path))
        html_path.unlink(missing_ok=True)
        return str(pdf_path)
    except Exception:
        import traceback
        traceback.print_exc()
        return str(html_path)