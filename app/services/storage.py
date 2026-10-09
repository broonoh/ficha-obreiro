# app/services/storage.py
import json
from app.db.database import get_session
from app.db.models import Rascunho

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