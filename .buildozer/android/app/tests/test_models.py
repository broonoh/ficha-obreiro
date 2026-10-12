# tests/test_models.py
import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import (
    Base, FichaObreiro, FuncaoAtual, SituacaoFicha,
    ExperienciaGraca, TipoExperienciaGraca
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_criar_ficha_completa(session):
    ficha = FichaObreiro(
        nome="João da Silva",
        cpf="123.456.789-00",
        funcao_atual=FuncaoAtual.OBREIRO,
        tempo_icm_anos=10,
        dizimista_fiel=True,
        situacao=SituacaoFicha.APROVADO,
    )
    session.add(ficha)
    session.commit()

    assert ficha.id is not None
    assert ficha.funcao_atual == FuncaoAtual.OBREIRO
    assert ficha.situacao == SituacaoFicha.APROVADO


def test_experiencias_graca_cascade(session):
    ficha = FichaObreiro(nome="Maria")
    ficha.experiencias_graca.append(
        ExperienciaGraca(
            tipo=TipoExperienciaGraca.CLAMOR,
            descricao="Forte experiência de clamor"
        )
    )
    session.add(ficha)
    session.commit()
    assert len(ficha.experiencias_graca) == 1