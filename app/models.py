from sqlalchemy import Column, Integer, String, JSON, DECIMAL, Text, TIMESTAMP, ForeignKey, func
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(20), nullable=False)
    senha = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)

class Equipe(Base):
    __tablename__ = "equipes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    contato_coordenador = Column(String(100), nullable=False)
    membros = Column(JSON)

class Resgate(Base):
    __tablename__ = "resgates"

    id = Column(Integer, primary_key=True, index=True)
    localizacao_lat = Column(DECIMAL(10, 8), nullable=False)
    localizacao_long = Column(DECIMAL(11, 8), nullable=False)
    status = Column(String(20), nullable=False)
    equipes_ids = Column(JSON)
    notas = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 