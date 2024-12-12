from datetime import timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Gestão de Resgates")

# Rota de autenticação
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Rotas de Usuário
@app.post("/usuarios/", response_model=schemas.Usuario)
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    hashed_password = auth.get_password_hash(user.senha)
    db_user = models.Usuario(
        nome=user.nome,
        email=user.email,
        telefone=user.telefone,
        senha=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Rotas de Equipe
@app.post("/equipes/", response_model=schemas.Equipe)
def create_team(
    equipe: schemas.EquipeCreate,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(auth.get_current_active_user)
):
    if current_user.role != "coordenador":
        raise HTTPException(status_code=403, detail="Apenas coordenadores podem criar equipes")
    
    db_equipe = models.Equipe(**equipe.dict())
    db.add(db_equipe)
    db.commit()
    db.refresh(db_equipe)
    return db_equipe

@app.get("/equipes/", response_model=List[schemas.Equipe])
def get_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(auth.get_current_active_user)
):
    equipes = db.query(models.Equipe).offset(skip).limit(limit).all()
    return equipes

# Rotas de Resgate
@app.post("/resgates/", response_model=schemas.Resgate)
def create_rescue(
    resgate: schemas.ResgateCreate,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(auth.get_current_active_user)
):
    if current_user.role != "coordenador":
        raise HTTPException(status_code=403, detail="Apenas coordenadores podem criar missões de resgate")
    
    db_resgate = models.Resgate(**resgate.dict())
    db.add(db_resgate)
    db.commit()
    db.refresh(db_resgate)
    return db_resgate

@app.get("/resgates/", response_model=List[schemas.Resgate])
def get_rescues(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(auth.get_current_active_user)
):
    query = db.query(models.Resgate)
    if status:
        query = query.filter(models.Resgate.status == status)
    resgates = query.offset(skip).limit(limit).all()
    return resgates

@app.put("/resgates/{resgate_id}", response_model=schemas.Resgate)
def update_rescue_status(
    resgate_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(auth.get_current_active_user)
):
    if current_user.role != "coordenador":
        raise HTTPException(status_code=403, detail="Apenas coordenadores podem atualizar o status de resgates")
    
    db_resgate = db.query(models.Resgate).filter(models.Resgate.id == resgate_id).first()
    if not db_resgate:
        raise HTTPException(status_code=404, detail="Resgate não encontrado")
    
    if status not in ["planejado", "em_andamento", "concluido"]:
        raise HTTPException(status_code=400, detail="Status inválido")
    
    db_resgate.status = status
    db.commit()
    db.refresh(db_resgate)
    return db_resgate

@app.delete("/resgates/{resgate_id}")
def delete_rescue(
    resgate_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(auth.get_current_active_user)
):
    if current_user.role != "coordenador":
        raise HTTPException(status_code=403, detail="Apenas coordenadores podem excluir resgates")
    
    db_resgate = db.query(models.Resgate).filter(models.Resgate.id == resgate_id).first()
    if not db_resgate:
        raise HTTPException(status_code=404, detail="Resgate não encontrado")
    
    db.delete(db_resgate)
    db.commit()
    return {"message": "Resgate excluído com sucesso"} 