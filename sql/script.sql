SET NAMES utf8mb4 COLLATE utf8mb4_0900_ai_ci;
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_results = utf8mb4;

CREATE DATABASE IF NOT EXISTS db
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

USE db;

CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pf TINYINT NOT NULL,
    documento VARCHAR(14) UNIQUE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(45) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE canal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(45) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE movimentacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fk_canal INT,
    valor DOUBLE NOT NULL,
    dt_hora DATETIME NOT NULL,
    CONSTRAINT fk_movimentacao_canal
        FOREIGN KEY (fk_canal)
        REFERENCES canal(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE compra (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fk_cliente INT,
    fk_produto INT,
    fk_movimentacao INT NOT NULL,
    qtd INT NOT NULL,
    CONSTRAINT fk_compra_cliente
        FOREIGN KEY (fk_cliente)
        REFERENCES cliente(id),
    CONSTRAINT fk_compra_produto
        FOREIGN KEY (fk_produto)
        REFERENCES produto(id),
    CONSTRAINT fk_compra_movimentacao
        FOREIGN KEY (fk_movimentacao)
        REFERENCES movimentacao(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

ALTER TABLE compra MODIFY fk_produto INT NULL;
ALTER TABLE compra DROP FOREIGN KEY fk_compra_produto;
ALTER TABLE compra ADD CONSTRAINT fk_compra_produto 
FOREIGN KEY (fk_produto) REFERENCES produto(id) ON DELETE SET NULL;

INSERT INTO cliente (pf, documento) VALUES
(0, '22415775000160'),
(0, '08462561000114'),
(0, '26308517000136');

INSERT INTO produto (nome) VALUES
('Bolo de Chocolate'),
('Bolo de Morango'),
('Torta de Limão'),
('Torta de Maracujá');

INSERT INTO canal (categoria) VALUES
('Loja Física');

INSERT INTO movimentacao (fk_canal, valor, dt_hora) VALUES
(1, 20.0, '2025-12-01 09:00:00'),
(1, 40.0, '2025-12-04 09:00:00'),
(1, 35.0, '2025-12-12 09:00:00'),
(1, 30.0, '2025-12-13 09:00:00'),
(1, 30.0, '2026-01-04 09:00:00'),
(1, 45.0, '2026-01-11 09:00:00'),
(1, 45.0, '2026-01-11 09:00:00'),
(1, 45.0, '2026-02-22 09:00:00'),
(1, 45.0, '2026-02-23 09:00:00'),
(1, 20.0, '2026-02-28 09:00:00'),
(1, 35.0, '2026-03-10 09:00:00'),
(1, 40.0, '2026-03-20 09:00:00'),
(1, 45.0, '2026-03-30 09:00:00'),
(1, 35.0, '2026-04-02 09:00:00'),
(1, 45.0, '2026-04-07 09:00:00'),
(1, 40.0, '2026-04-16 09:00:00'),
(1, 40.0, '2026-04-21 09:00:00'),
(1, 30.0, '2026-04-30 09:00:00'),
(1, 30.0, '2026-05-01 09:00:00'),
(1, 35.0, '2026-05-09 09:00:00'),
(1, 30.0, '2026-05-10 09:00:00'),
(1, 40.0, '2026-05-17 09:00:00'),
(1, 40.0, '2026-05-20 09:00:00'),
(1, 60.0, '2026-05-21 09:00:00'),
(1, 60.0, '2026-06-01 09:00:00'),
(1, 60.0, '2026-06-10 09:00:00'),
(1, 20.0, '2026-06-17 09:00:00'),
(1, 80.0, '2026-06-19 09:00:00'),
(1, 20.0, '2026-07-16 09:00:00'),
(1, 80.0, '2026-07-20 09:00:00');


INSERT INTO compra (fk_cliente, fk_produto, fk_movimentacao, qtd) VALUES
(1, 1, 1, 1),
(1, 2, 1, 2),
(1, 3, 1, 1),
(2, 2, 2, 3),
(2, 4, 2, 1),
(3, 1, 3, 1),
(3, 3, 3, 2),
(1, 2, 4, 1),
(1, 4, 4, 1),
(2, 1, 5, 2),
(3, 4, 6, 1),
(3, 2, 6, 1),
(1, 3, 7, 2),
(2, 2, 8, 1),
(2, 1, 8, 1),
(3, 3, 9, 1),
(3, 4, 9, 2),
(1, 1, 10, 1),
(2, 3, 11, 2),
(3, 2, 12, 1),
(3, 1, 12, 1),
(1, 4, 13, 2),
(2, 1, 14, 1),
(2, 2, 14, 1),
(3, 3, 15, 1),
(3, 4, 15, 1),
(1, 2, 16, 2),
(2, 4, 17, 1),
(2, 3, 17, 2),
(3, 1, 18, 1),
(1, 4, 19, 1),
(1, 2, 19, 2),
(2, 3, 20, 1),
(3, 1, 21, 2),
(3, 2, 21, 1),
(1, 4, 22, 1),
(1, 3, 22, 1),
(2, 2, 23, 2),
(3, 1, 24, 2),
(3, 4, 24, 2),
(1, 3, 25, 2),
(1, 2, 25, 1),
(2, 4, 26, 2),
(2, 1, 26, 1),
(3, 2, 27, 1),
(1, 1, 28, 2),
(1, 2, 28, 2),
(1, 3, 28, 1),
(1, 4, 28, 1);

# DDL analítico

CREATE TABLE raw_cnpjs (
    id BIGINT NOT NULL AUTO_INCREMENT,
    cnpj_raiz CHAR(14) NOT NULL,
    simples JSON,
    estabelecimento JSON,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    razao_social VARCHAR(255),
    capital_social DECIMAL(18,2),
    responsavel_federativo VARCHAR(255),
    atualizado_em DATETIME,
    porte JSON,
    natureza_juridica JSON,
    qualificacao_do_responsavel VARCHAR(255),
    socios JSON,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    anomes INT,
    PRIMARY KEY (id),
    UNIQUE KEY uk_raw_cnpjs_cnpj (cnpj_raiz)
);

CREATE TABLE raw_movimentacoes (
    id BIGINT NOT NULL AUTO_INCREMENT,
    nome_produto VARCHAR(255),
    dtHora DATETIME,
    qtd INT,
    id_canal INT,
    categoria_canal VARCHAR(100),
    id_movimentacao INT,
    valor_movimentacao DECIMAL(15,2),
    id_cliente INT,
    documento_cliente VARCHAR(20),
    id_produto INT,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    anomes INT,
    KEY idx_movimentacao (id_movimentacao),
    KEY idx_cliente (id_cliente),
    KEY idx_documento (documento_cliente),
    KEY idx_produto (id_produto),
    KEY idx_data (dtHora)
);

CREATE TABLE IF NOT EXISTS trusted_cnpjs (
    id BIGINT NOT NULL AUTO_INCREMENT,
    cnpj_raiz CHAR(14) NOT NULL,
    id_aplicacao BIGINT,
    mei_simples TINYINT,
    atividade_principal JSON,
    atividade_secundarias JSON,
    tipo VARCHAR(50),
    nome_fantasia VARCHAR(255),
    situacao VARCHAR(100),
    tipo_logradouro VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(50),
    razao_social VARCHAR(255),
    bairro VARCHAR(255),
    cep VARCHAR(20),
    cidade_nome VARCHAR(255),
    cidade_ibge_id INT,
    cidade_siafi_id INT,
    estado_nome VARCHAR(100),
    estado_sigla CHAR(2),
    pais_nome VARCHAR(100),
    telefone1 VARCHAR(50),
    telefone2 VARCHAR(50),
    capital_social DECIMAL(18,2),
    fax VARCHAR(50),
    email VARCHAR(255),
    situacao_especial VARCHAR(255),
    data_situacao_especial DATE,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    responsavel_federativo TINYINT,
    atualizado_em DATE,
    porte VARCHAR(255),
    natureza_juridica VARCHAR(255),
    qualificacao_do_responsavel VARCHAR(255),
    socios JSON,
    anomes INT NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_trusted_cnpjs_cnpj_anomes (
        cnpj_raiz,
        anomes
    ),
    KEY idx_trusted_cnpjs_cnpj (
        cnpj_raiz
    ),
    KEY idx_trusted_cnpjs_razao_social (
        razao_social
    ),
    KEY idx_trusted_cnpjs_cidade (
        cidade_ibge_id
    ),
    KEY idx_trusted_cnpjs_estado (
        estado_sigla
    ),
    KEY idx_trusted_cnpjs_anomes (
        anomes
    )
) CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS trusted_movimentacoes (
    id BIGINT NOT NULL AUTO_INCREMENT,
    id_aplicacao BIGINT,
    id_canal INT,
    categoria_canal VARCHAR(100),
    valor_movimentacao DECIMAL(15,2),
    id_cliente INT,
    documento_cliente VARCHAR(20),
    id_produto INT,
    nome_produto VARCHAR(255),
    dthora DATETIME,
    anomes INT NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_trusted_movimentacao (
        id_aplicacao
    ),
    KEY idx_trusted_cliente (
        id_cliente
    ),
    KEY idx_trusted_documento (
        documento_cliente
    ),
    KEY idx_trusted_produto (
        id_produto
    ),
    KEY idx_trusted_data (
        dthora
    ),
    KEY idx_trusted_anomes (
        anomes
    )
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;