# app/services/storage.py
import json
import re
import unicodedata
from datetime import datetime
from app.db.database import get_session
from app.db.models import Rascunho
from app.services.paths import pasta_fichas


def _nome_arquivo_seguro(nome: str) -> str:
    """Remove acentos/caracteres especiais para um nome de arquivo seguro em qualquer SO."""
    nome = unicodedata.normalize("NFKD", nome or "").encode("ascii", "ignore").decode("ascii")
    nome = re.sub(r"[^\w\s-]", "", nome).strip().replace(" ", "_")
    return nome or "ficha"


def exportar_dados_para_arquivo(dados: dict, caminho: str | None = None) -> str:
    """Exporta todos os dados preenchidos em tela para um arquivo .json
    portátil (ex.: para enviar por e-mail/WhatsApp e importar em outro
    dispositivo rodando o mesmo app)."""
    if caminho is None:
        nome = _nome_arquivo_seguro(dados.get("nome", "ficha"))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = str(pasta_fichas() / f"Ficha_{nome}_{timestamp}.json")

    json_str = json.dumps(dados, ensure_ascii=False, indent=2, default=str)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(json_str)
    return caminho


def importar_dados_de_arquivo(caminho: str) -> dict:
    """Lê um arquivo .json exportado por este app e retorna o dicionário de dados."""
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

def salvar_rascunho_no_bd(dados: dict):
    """将表单数据序列化为 JSON 并保存到数据库（只保留最新一份）"""
    sess = get_session()
    try:
        # 删除旧草稿
        sess.query(Rascunho).delete()
        # 保存新草稿 (default=str 处理日期对象)
        json_str = json.dumps(dados, ensure_ascii=False, default=str)
        novo = Rascunho(data_json=json_str)
        sess.add(novo)
        sess.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar rascunho: {e}")
        sess.rollback()
        return False
    finally:
        sess.close()

def carregar_rascunho_do_bd() -> dict:
    """从数据库读取最新的草稿并解析为字典"""
    sess = get_session()
    try:
        rascunho = sess.query(Rascunho).order_by(Rascunho.updated_at.desc()).first()
        if rascunho:
            return json.loads(rascunho.data_json)
        return {}
    except Exception as e:
        print(f"Erro ao carregar rascunho: {e}")
        return {}
    finally:
        sess.close()