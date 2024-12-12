from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    role: str

class UsuarioCreate(UsuarioBase):
    senha: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class LoginData(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class EquipeBase(BaseModel):
    nome: str
    contato_coordenador: str
    membros: List[str]

class EquipeCreate(EquipeBase):
    pass

class Equipe(EquipeBase):
    id: int

    class Config:
        from_attributes = True

class ResgateBase(BaseModel):
    localizacao_lat: float
    localizacao_long: float
    status: str
    equipes_ids: List[int]
    notas: Optional[str] = None

class ResgateCreate(ResgateBase):
    pass

class Resgate(ResgateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 