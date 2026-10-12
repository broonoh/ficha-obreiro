# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# Define o caminho do banco de dados NA RAIZ DO PROJETO
DB_PATH = Path(__file__).parent.parent.parent / "ficha_obreiro.db"
print(f"📂 Banco de dados será criado em: {DB_PATH}")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def init_db():
    """Cria as tabelas no banco de dados se não existirem."""
    # Importamos os modelos explicitamente para registrar as tabelas no Base
    from app.db import models

    print("🔄 Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")


def get_session():
    init_db()
    return SessionLocal()