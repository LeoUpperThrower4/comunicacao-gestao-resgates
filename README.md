# API de Gestão de Resgates

Esta é uma API RESTful para gestão de resgates, desenvolvida com FastAPI e PostgreSQL.

## Requisitos

- Python 3.8+
- PostgreSQL
- Docker (opcional)

## Instalação

1. Clone o repositório:

```bash
git clone <seu-repositorio>
cd <seu-repositorio>
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Inicie o banco de dados PostgreSQL (usando Docker):

```bash
docker run -d --name resgate_postgres \
  -e POSTGRES_DB=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres123 \
  -p 5444:5432 \
  -v "$(pwd)/schema.sql:/docker-entrypoint-initdb.d/schema.sql" \
  postgres:latest
```

4. Inicie a aplicação:

```bash
python run.py
```

A API estará disponível em `http://localhost:8000`

## Documentação da API

Acesse a documentação interativa da API em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints Principais

### Autenticação

- POST `/token` - Login (obter token de acesso)

### Usuários

- POST `/usuarios/` - Criar novo usuário

### Equipes

- POST `/equipes/` - Criar nova equipe
- GET `/equipes/` - Listar equipes

### Resgates

- POST `/resgates/` - Criar nova missão de resgate
- GET `/resgates/` - Listar missões de resgate
- PUT `/resgates/{resgate_id}` - Atualizar status de resgate
- DELETE `/resgates/{resgate_id}` - Excluir missão de resgate

## Roles e Permissões

- **Coordenador**: Acesso total ao sistema
- **Voluntário**: Acesso limitado a visualização de dados

## Segurança

- Autenticação via JWT (JSON Web Tokens)
- Senhas criptografadas com bcrypt
- Controle de acesso baseado em roles
