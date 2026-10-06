-- Estrutura da Loja Aurora (loja fictícia).
-- Sem chaves estrangeiras de propósito: assim os defeitos conseguem entrar no banco,
-- como acontece em sistemas reais com importações, migrações e integrações antigas.

CREATE TABLE clientes (
  id      INTEGER PRIMARY KEY,
  nome    TEXT NOT NULL,
  email   TEXT,
  cidade  TEXT,
  ativo   INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE produtos (
  id       INTEGER PRIMARY KEY,
  nome     TEXT NOT NULL,
  preco    NUMERIC NOT NULL,
  estoque  INTEGER NOT NULL
);

CREATE TABLE pedidos (
  id           INTEGER PRIMARY KEY,
  cliente_id   INTEGER NOT NULL,
  produto_id   INTEGER NOT NULL,
  quantidade   INTEGER NOT NULL,
  data_pedido  TEXT NOT NULL,
  status       TEXT NOT NULL
);
