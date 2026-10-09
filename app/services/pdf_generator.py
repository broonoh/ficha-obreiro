# app/services/pdf_generator.py
import os
import re
from datetime import datetime
from pathlib import Path
from jinja2 import Template

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "ficha.html"


def _check(v):
    """Retorna chip visual para booleanos no PDF."""
    if v is None or v == "" or v == "None":
        return '<span class="check check-empty">—</span>'
    if isinstance(v, bool):
        if v:
            return '<span class="check check-yes">✓ Sim</span>'
        return '<span class="check check-no">✗ Não</span>'
    # String "True"/"False"
    if str(v).lower() in ("true", "sim", "yes"):
        return '<span class="check check-yes">✓ Sim</span>'
    if str(v).lower() in ("false", "não", "nao", "no"):
        return '<span class="check check-no">✗ Não</span>'
    return str(v)


def _v(value):
    """Normaliza valor vazio/None/indefinido para um travessão — evita
    campos em branco no PDF (ex.: campos administrativos sem tela própria,
    como "Situação Final", que nunca chegam no dicionário de dados)."""
    from jinja2 import Undefined
    if isinstance(value, Undefined) or value is None or value == "" or value == "None":
        return "—"
    return value


def _sim_nao(sim, nao):
    """Chip Sim/Não a partir de um par de checkboxes mutuamente exclusivos."""
    if sim:
        return '<span class="check check-yes">✓ Sim</span>'
    if nao:
        return '<span class="check check-no">✗ Não</span>'
    return '<span class="check check-empty">—</span>'


def gerar_pdf(dados: dict) -> str:
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        tpl = Template(f.read())

    dados.setdefault("gerado_em", datetime.now().strftime("%d/%m/%Y %H:%M"))
    html = tpl.render(check=_check, v=_v, sim_nao=_sim_nao, **dados)

    # O WeasyPrint trata espaços em branco entre tags (indentação/quebras de
    # linha do template) como itens "fantasmas" dentro de containers flex,
    # o que força quebra de linha prematura nas grades de campos (3 colunas
    # viravam 2). Remover espaços puramente entre tags resolve isso sem
    # afetar texto real (campos multilinha do usuário não têm ">...<" puro).
    html = re.sub(r">\s+<", "><", html)

    out_dir = Path.home() / "FichaObreiro"
    out_dir.mkdir(parents=True, exist_ok=True)

    nome_seguro = (dados.get("nome") or "ficha").replace(" ", "_")[:40]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = out_dir / f"Ficha_{nome_seguro}_{ts}.pdf"

    try:
        from weasyprint import HTML
        HTML(string=html).write_pdf(str(path))
    except Exception as e:
        html_path = path.with_suffix(".html")
        html_path.write_text(html, encoding="utf-8")
        raise RuntimeError(
            f"WeasyPrint indisponível ({e}). HTML salvo em {html_path}."
        )

    return str(path)