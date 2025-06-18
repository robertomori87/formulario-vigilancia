# database.py (Atualizado)

from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Boolean, Text, DateTime, func # Adicionado DateTime e func
from sqlalchemy.orm import declarative_base, sessionmaker
from src.common.config import DATABASE_URL
from sqlalchemy.dialects.postgresql import ENUM

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Definir os valores permitidos para o status da SolicitacaoReceituario
STATUS_OPTIONS = (
    "AGUARDANDO DOCUMENTO ASSINADO",
    "AGUARDANDO ANÁLISE",
    "DEFERIDO",
    "INDEFERIDO"
)

# Modelo existente para o Receituário
class SolicitacaoReceituario(Base):
    __tablename__ = "solicitacoes_receituario"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(ENUM(*STATUS_OPTIONS, name="solicitacao_status_enum", create_type=True), nullable=False, default="AGUARDANDO ANÁLISE")
    nome = Column(String, nullable=False)
    cpf_cnpj = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    responsavel = Column(String, nullable=False)
    conselho = Column(String, nullable=False)
    numero_conselho = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    nome_terceiro = Column(String, nullable=False)
    cpf_terceiro = Column(String, nullable=False)
    receita_a = Column(String)
    receita_b = Column(String)
    receita_b2 = Column(String)
    retinoides = Column(String)
    talidomida = Column(String)
    protocolo = Column(String, nullable=False)
    data_protocolo = Column(Date, nullable=False)
    hora_protocolo = Column(Time, nullable=False)


# NOVO MODELO para o Checklist de Projeto
class Checklist(Base):
    __tablename__ = "checklist"
    __table_args__ = {'schema': 'aprovacao_projeto'} # DESCOMENTADO (se você for usar o schema)

    id = Column(Integer, primary_key=True, index=True)
    numero_item = Column(Integer, nullable=False, unique=True)
    pergunta = Column(Text, nullable=False)
    texto_legal = Column(Text)
    interpretacao_legal = Column(Text)
    orientacao_documentacao = Column(Text)
    base_legal = Column(Text)
    observacao_fluxo = Column(Text)

    # Campos de resposta do formulário (apenas SIM/NÃO como opção de resposta do usuário)
    resposta = Column(String(20)) # Agora aceitará apenas 'SIM' ou 'NÃO' devido ao CHECK no SQL
    atende = Column(Boolean)
    nao_atende = Column(Boolean)
    medida_mitigatoria = Column(Text)


    comentario_requerente = Column(Text)
    comentario_avaliador = Column(Text)
    criado_em = Column(DateTime, default=func.now())

    # SE A PERGUNTA TIVER UM STATUS "NÃO SE APLICA" PRÉ-DEFINIDO, ADICIONE UMA COLUNA AQUI
    # Exemplo:
    # tipo_de_projeto_aplicavel = Column(String(50)) # 'RESIDENCIAL', 'COMERCIAL', 'TODOS', etc.
    # ou
    # nao_se_aplica_status = Column(Boolean, default=False) # True se a pergunta é "não aplicável" por padrão



