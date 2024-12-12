import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.auth import get_password_hash

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user(test_db):
    response = client.post(
        "/usuarios/",
        json={
            "nome": "Teste Coordenador",
            "email": "teste@exemplo.com",
            "telefone": "11999999999",
            "senha": "senha123",
            "role": "coordenador"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "teste@exemplo.com"
    assert data["role"] == "coordenador"

def test_create_duplicate_user(test_db):
    # Criar primeiro usuário
    client.post(
        "/usuarios/",
        json={
            "nome": "Teste Coordenador",
            "email": "teste@exemplo.com",
            "telefone": "11999999999",
            "senha": "senha123",
            "role": "coordenador"
        }
    )
    
    # Tentar criar usuário com mesmo email
    response = client.post(
        "/usuarios/",
        json={
            "nome": "Teste Coordenador 2",
            "email": "teste@exemplo.com",
            "telefone": "11999999999",
            "senha": "senha123",
            "role": "coordenador"
        }
    )
    assert response.status_code == 400

def test_login(test_db):
    # Criar usuário
    client.post(
        "/usuarios/",
        json={
            "nome": "Teste Coordenador",
            "email": "teste@exemplo.com",
            "telefone": "11999999999",
            "senha": "senha123",
            "role": "coordenador"
        }
    )
    
    # Tentar login
    response = client.post(
        "/token",
        data={
            "username": "teste@exemplo.com",
            "password": "senha123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_rescue_without_auth(test_db):
    response = client.post(
        "/resgates/",
        json={
            "localizacao_lat": -23.550520,
            "localizacao_long": -46.633308,
            "status": "planejado",
            "equipes_ids": [1],
            "notas": "Teste de resgate"
        }
    )
    assert response.status_code == 401

def test_create_rescue_with_auth(test_db):
    # Criar usuário coordenador
    client.post(
        "/usuarios/",
        json={
            "nome": "Teste Coordenador",
            "email": "teste@exemplo.com",
            "telefone": "11999999999",
            "senha": "senha123",
            "role": "coordenador"
        }
    )
    
    # Login
    response = client.post(
        "/token",
        data={
            "username": "teste@exemplo.com",
            "password": "senha123"
        }
    )
    token = response.json()["access_token"]
    
    # Criar resgate
    response = client.post(
        "/resgates/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "localizacao_lat": -23.550520,
            "localizacao_long": -46.633308,
            "status": "planejado",
            "equipes_ids": [1],
            "notas": "Teste de resgate"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "planejado"
    assert data["notas"] == "Teste de resgate"

def test_get_rescues(test_db):
    # Criar usuário coordenador
    client.post(
        "/usuarios/",
        json={
            "nome": "Teste Coordenador",
            "email": "teste@exemplo.com",
            "telefone": "11999999999",
            "senha": "senha123",
            "role": "coordenador"
        }
    )
    
    # Login
    response = client.post(
        "/token",
        data={
            "username": "teste@exemplo.com",
            "password": "senha123"
        }
    )
    token = response.json()["access_token"]
    
    # Listar resgates
    response = client.get(
        "/resgates/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list) 