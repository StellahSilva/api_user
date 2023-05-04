-- Criar  Banco Usuário
CREATE DATABASE api_stella
default character set utf8mb4
default collate utf8mb4_general_ci;

USE api_stella;


CREATE TABLE usuarios (
    id integer not null auto_increment,
    nome VARCHAR(50),
    login VARCHAR(30),
    senha VARCHAR(30),
    PRIMARY KEY (id)
);

SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8;

INSERT INTO usuarios (nome, login, senha) VALUES ('Stella Henrique', 'user 1', '05111999');
INSERT INTO usuarios (nome, login, senha) VALUES ('Ana Carolina', 'user2', '120504');
INSERT INTO usuarios (nome, login, senha) VALUES ('Pedro Henrique', 'user_3', '130902');

USE api_stella VIEW TABLES;
