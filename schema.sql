-- Criação do banco de dados
CREATE DATABASE resgate_db;

-- Conectar ao banco de dados
\c resgate_db;

-- Criação da tabela de usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('voluntario', 'coordenador')) NOT NULL
);

-- Criação da tabela de equipes
CREATE TABLE equipes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    contato_coordenador VARCHAR(100) NOT NULL,
    membros TEXT[] -- Array de IDs de usuários
);

-- Criação da tabela de resgates
CREATE TABLE resgates (
    id SERIAL PRIMARY KEY,
    localizacao_lat DECIMAL(10, 8) NOT NULL,
    localizacao_long DECIMAL(11, 8) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('planejado', 'em_andamento', 'concluido')) NOT NULL,
    equipes_ids INTEGER[], -- Array de IDs de equipes
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserção de dados de exemplo
INSERT INTO usuarios (nome, email, telefone, senha, role) VALUES
('João Coordenador', 'joao@exemplo.com', '11999999999', '$2b$10$exemplo_hash', 'coordenador'),
('Maria Voluntária', 'maria@exemplo.com', '11988888888', '$2b$10$exemplo_hash', 'voluntario');

INSERT INTO equipes (nome, contato_coordenador, membros) VALUES
('Equipe Alpha', 'joao@exemplo.com', ARRAY[1]),
('Equipe Beta', 'maria@exemplo.com', ARRAY[2]);

INSERT INTO resgates (localizacao_lat, localizacao_long, status, equipes_ids, notas) VALUES
(-23.550520, -46.633308, 'planejado', ARRAY[1], 'Resgate na região central'),
(-23.550520, -46.633308, 'em_andamento', ARRAY[1,2], 'Resgate urgente em andamento');

-- Índices para melhor performance
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_resgates_status ON resgates(status); 