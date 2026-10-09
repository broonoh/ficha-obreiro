# app/db/models.py
"""Modelo SQLAlchemy completo — mapeia 100% dos campos da ficha ICM."""
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Boolean, Date, Text,
    ForeignKey, Enum, Float
)
from sqlalchemy.orm import relationship
import enum

# ✅ CORREÇÃO: Importar o Base do database.py, NÃO criar um novo!
from .database import Base

# ─────────────────────────────────────────────────────────────
# ENUMS (valores permitidos conforme ficha)
# ─────────────────────────────────────────────────────────────
class FuncaoAtual(enum.Enum):
    EVANGELISTA = "Evangelista"
    OBREIRO = "Obreiro"
    DIACONO = "Diácono"
    UNGIDO = "Ungido"

class SituacaoFicha(enum.Enum):
    APROVADO = "Aprovado"
    NAO_APROVADO = "Não Aprovado"
    REVER = "Rever"
    AGUARDAR = "Aguardar"

# ... (mantenha todo o resto do seu código das classes FichaObreiro, ExperienciaGraca, etc.) ...

class TipoExperienciaGraca(enum.Enum):
    CLAMOR = "Clamor pelo Sangue de Jesus / Oração"
    JEJUM = "Jejum"
    MADRUGADA = "Madrugada"
    CONSULTA_PALAVRA = "Consulta à Palavra / A Palavra"
    LOUVOR = "Louvor"


class TipoExperienciaObreiro(enum.Enum):
    DONS_CUMPRIDOS = "Dons entregues pelo obreiro que se cumpriram"
    PROVAS = "Provas vividas pelo obreiro"
    EXPERIENCIAS = "Experiências vividas pelo obreiro"


# ─────────────────────────────────────────────────────────────
# FICHA PRINCIPAL
# ─────────────────────────────────────────────────────────────
class FichaObreiro(Base):
    __tablename__ = "fichas_obreiro"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(Date, default=date.today)
    updated_at = Column(Date, default=date.today, onupdate=date.today)

    # ── CABEÇALHO ────────────────────────────────────────────
    numero = Column(String(20))
    mes = Column(String(20))            # Mês(es)
    ano = Column(Integer)               # OE Ano(s)
    data_preenchimento = Column(Date)
    empresa = Column(String(120))
    foto_path = Column(String(255))     # 3x4 terno e gravata

    # ── DADOS PESSOAIS (22 campos) ───────────────────────────
    nome = Column(String(150), nullable=False)
    cpf = Column(String(14))
    rg = Column(String(20))             # Carteira de Identidade
    empregado = Column(String(120))
    arma = Column(String(80))
    data_nascimento = Column(Date)
    idade = Column(Integer)
    estado_civil = Column(String(30))
    profissao = Column(String(80))
    escolaridade = Column(String(60))
    endereco_rua = Column(String(200))
    endereco_bairro = Column(String(100))
    endereco_cidade = Column(String(100))
    endereco_uf = Column(String(2))
    endereco_cep = Column(String(9))
    telefone = Column(String(20))
    email = Column(String(120))
    militar_patente = Column(String(60))
    aposentado_motivo = Column(Text)

    # ── VIDA ESPIRITUAL (41 itens) ───────────────────────────
    # 01
    funcao_atual = Column(Enum(FuncaoAtual))
    # 02
    tempo_funcao_meses = Column(Integer)
    tempo_funcao_anos = Column(Integer)
    # 03
    grupo_intercessao = Column(Boolean, default=False)
    # 04
    responsavel_trabalho = Column(Boolean, default=False)
    responsavel_trabalho_qual = Column(String(120))
    # 05
    crescimento_grupo_pct = Column(Float)
    # 06
    visitas_mes = Column(Integer)
    # 07
    dizimista_fiel = Column(Boolean, default=False)
    # 08
    tempo_icm_meses = Column(Integer)
    tempo_icm_anos = Column(Integer)
    # 09
    afastou_igreja = Column(Boolean, default=False)
    afastou_igreja_motivo = Column(Text)
    afastou_data1 = Column(Date)
    afastou_data2 = Column(Date)
    afastou_data3 = Column(Date)
    # 10
    foi_provado = Column(Boolean, default=False)
    foi_provado_qual = Column(Text)
    # 11
    tem_experiencia = Column(Boolean, default=False)
    # 12
    tem_sequelas_passado = Column(Text)
    # 13
    ultimos_seminarios = Column(Text)
    # 14
    participa_maanaim_voluntario = Column(Boolean, default=False)
    participa_maanaim_meio_semana = Column(Boolean, default=False)
    participa_maanaim_final_semana = Column(Boolean, default=False)
    # 15
    participa_madrugada = Column(Boolean, default=False)
    # 16
    integrado_culto_profetico = Column(Boolean, default=False)
    # 17
    tem_governo_lar = Column(Boolean, default=False)
    # 18
    familia_integrada = Column(Boolean, default=False)
    # 19
    respeita_pastor_presbiterio = Column(Boolean, default=False)
    # 20
    zelo_bens_icm = Column(Boolean, default=False)
    # 21 — dons espirituais (múltiplos)
    dons_linguas = Column(Boolean, default=False)
    dons_interpretacao = Column(Boolean, default=False)
    dons_ciencia = Column(Boolean, default=False)
    dons_sonho = Column(Boolean, default=False)
    dons_visao = Column(Boolean, default=False)
    dons_revelacao = Column(Boolean, default=False)
    # 22
    veio_outra_igreja = Column(String(100))
    # 23
    cumpridor_obrigacoes = Column(Boolean, default=False)
    # 24
    divida_irmaos = Column(Boolean, default=False)
    # 25
    tempo_casado_candidato = Column(String(20))   # "X ano(s) Y mes(es)"
    tempo_casado_esposa = Column(String(20))
    # 26
    nome_esposa = Column(String(150))
    # 27
    funcao_esposa = Column(String(80))
    # 28
    profissao_esposa = Column(String(80))
    # 29
    estado_civil_antes_candidato = Column(String(30))
    # 30
    estado_civil_antes_esposa = Column(String(30))
    # 31
    quantos_filhos = Column(Integer)
    quantos_membros_igreja = Column(Integer)
    # 32
    filhos_motivo_sem = Column(Text)
    # 33
    disposto_ministerio_voluntario = Column(Boolean, default=False)
    # 34
    leu_toda_biblia = Column(Boolean, default=False)
    livros_lidos = Column(Integer)
    # 35
    pratica_ensinos_satelite = Column(Boolean, default=False)
    # 36
    aplica_satelite_igreja = Column(Boolean, default=False)
    # 37
    concluiu_instituto_biblico = Column(Boolean, default=False)
    curso_realizado = Column(String(120))
    # 38
    frequencia_media_igreja = Column(Integer)
    # 39
    estuda_noite = Column(Boolean, default=False)
    # 40
    disposto_viagem = Column(Boolean, default=False)
    # 41
    contribuicoes_ebd_mes = Column(Integer)

    assinatura_obreiro = Column(String(150))

    # ── ÁREA DO PASTOR (17 itens) ────────────────────────────
    pastor_igreja = Column(String(150))
    pastor_cidade = Column(String(100))
    pastor_uf = Column(String(2))
    # 01
    funcao_apresentada = Column(String(60))
    # 02
    caracteristica_ministerio = Column(Text)
    # 03
    tem_mensagem_revelada = Column(Boolean, default=False)
    # 04
    transmite_bem_mensagem = Column(Boolean, default=False)
    # 05
    defeito = Column(String(120))
    # 06
    tem_bom_testemunho = Column(Boolean, default=False)
    # 07
    maturidade_dons = Column(Boolean, default=False)
    # 08
    gosta_imitar_movimentos = Column(Boolean, default=False)
    # 09
    e_gastador = Column(Boolean, default=False)
    # 10
    dado_comentarios_depreciativos = Column(Boolean, default=False)
    comentarios_depreciativos_quais = Column(Text)
    # 11
    pontual = Column(Boolean, default=False)
    # 12
    sobrio_vestir = Column(Boolean, default=False)
    # 13
    numero_igrejas_bairro = Column(Integer)
    # 14
    numero_pastores_bairro = Column(Integer)
    # 15
    obediente_dons = Column(Boolean, default=False)
    obediente_dons_quais = Column(Text)
    # 16
    ja_apresentado_antes = Column(Boolean, default=False)
    quantas_vezes_apresentado = Column(Integer)
    ano_apresentacao = Column(Integer)
    motivo_nao_aprovado = Column(Text)
    # 17
    igreja_assumira = Column(String(200))
    observacao_pastor = Column(Text)
    assinatura_pastor = Column(String(150))

    # ── SITUAÇÃO FINAL ───────────────────────────────────────
    situacao = Column(Enum(SituacaoFicha))
    dom_comissao_area = Column(Text)
    dom_comissao_regiao = Column(Text)
    data_assinatura_conselho = Column(Date)
    assinatura_conselho = Column(String(150))

    # ── RELACIONAMENTOS ──────────────────────────────────────
    experiencias_graca = relationship(
        "ExperienciaGraca", back_populates="ficha",
        cascade="all, delete-orphan"
    )
    experiencias_obreiro = relationship(
        "ExperienciaObreiro", back_populates="ficha",
        cascade="all, delete-orphan"
    )
    mensagens_reveladas = relationship(
        "MensagemRevelada", back_populates="ficha",
        cascade="all, delete-orphan"
    )
    questionario = relationship(
        "QuestionarioTeologico", uselist=False,
        back_populates="ficha", cascade="all, delete-orphan"
    )
    questionario_esposa = relationship(
        "QuestionarioEsposa", uselist=False,
        back_populates="ficha", cascade="all, delete-orphan"
    )


# ─────────────────────────────────────────────────────────────
# EXPERIÊNCIAS COM RECURSOS DA GRAÇA (5 tipos)
# ─────────────────────────────────────────────────────────────
class ExperienciaGraca(Base):
    __tablename__ = "experiencias_graca"
    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_obreiro.id"))
    tipo = Column(Enum(TipoExperienciaGraca), nullable=False)
    descricao = Column(Text)
    ficha = relationship("FichaObreiro", back_populates="experiencias_graca")


# ─────────────────────────────────────────────────────────────
# EXPERIÊNCIAS DO OBREIRO (3 tipos)
# ─────────────────────────────────────────────────────────────
class ExperienciaObreiro(Base):
    __tablename__ = "experiencias_obreiro"
    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_obreiro.id"))
    tipo = Column(Enum(TipoExperienciaObreiro), nullable=False)
    descricao = Column(Text)
    ficha = relationship("FichaObreiro", back_populates="experiencias_obreiro")


# ─────────────────────────────────────────────────────────────
# MENSAGENS REVELADAS (até 2)
# ─────────────────────────────────────────────────────────────
class MensagemRevelada(Base):
    __tablename__ = "mensagens_reveladas"
    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_obreiro.id"))
    numero = Column(Integer, nullable=False)     # 1 ou 2
    texto = Column(Text)
    tema = Column(String(200))
    resumo = Column(Text)
    ficha = relationship("FichaObreiro", back_populates="mensagens_reveladas")


# ─────────────────────────────────────────────────────────────
# QUESTIONÁRIO TEOLÓGICO (7 temas)
# ─────────────────────────────────────────────────────────────
class QuestionarioTeologico(Base):
    __tablename__ = "questionario_teorologico"
    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_obreiro.id"), unique=True)

    palavra_revelada = Column(Text)
    clamor_sangue_jesus = Column(Text)
    igreja_corpo_cristo = Column(Text)
    salvacao = Column(Text)
    origens_fe = Column(Text)
    sacerdocio_universal = Column(Text)
    objetivo_satelite = Column(Text)

    ficha = relationship("FichaObreiro", back_populates="questionario")


# ─────────────────────────────────────────────────────────────
# QUESTIONÁRIO DA ESPOSA (5 perguntas + assinatura)
# ─────────────────────────────────────────────────────────────
class QuestionarioEsposa(Base):
    __tablename__ = "questionario_esposa"
    id = Column(Integer, primary_key=True)
    ficha_id = Column(Integer, ForeignKey("fichas_obreiro.id"), unique=True)

    nome_ungido = Column(String(150))
    nome_esposa = Column(String(150))

    q1_acordo_ordenacao = Column(Text)
    q2_concorda_doutinas = Column(Text)
    q3_ministerio_voluntario = Column(Text)
    q4_nao_interferir = Column(Text)
    q5_outros = Column(Text)

    assinatura_esposa = Column(String(150))

    ficha = relationship("FichaObreiro", back_populates="questionario_esposa")

# ─────────────────────────────────────────────────────────────
# RASCUNHO (Para salvar e carregar o formulário em andamento)
# ─────────────────────────────────────────────────────────────
class Rascunho(Base):
    __tablename__ = "rascunhos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_json = Column(Text, nullable=False)
    updated_at = Column(Date, default=date.today, onupdate=date.today)