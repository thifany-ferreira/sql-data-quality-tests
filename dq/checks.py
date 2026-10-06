"""As verificações de qualidade de dados.

Cada verificação é uma consulta SQL que devolve as linhas COM DEFEITO.
Banco saudável = nenhuma linha devolvida.
"""

import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class Check:
    name: str
    regra: str
    severidade: str  # "alta" ou "média"
    sql: str


CHECKS: list[Check] = [
    Check(
        "preco_negativo",
        "Todo produto tem preço maior que zero",
        "alta",
        "SELECT id, nome, preco FROM produtos WHERE preco <= 0",
    ),
    Check(
        "estoque_negativo",
        "Estoque nunca fica abaixo de zero",
        "alta",
        "SELECT id, nome, estoque FROM produtos WHERE estoque < 0",
    ),
    Check(
        "email_vazio",
        "Todo cliente tem e-mail",
        "média",
        "SELECT id, nome FROM clientes WHERE email IS NULL OR TRIM(email) = ''",
    ),
    Check(
        "email_invalido",
        "E-mail preenchido tem formato válido",
        "média",
        """SELECT id, nome, email FROM clientes
           WHERE email IS NOT NULL AND TRIM(email) <> '' AND email NOT LIKE '%_@_%._%'""",
    ),
    Check(
        "email_duplicado",
        "Cada e-mail pertence a um só cliente",
        "alta",
        "SELECT email, COUNT(*) AS clientes FROM clientes WHERE email IS NOT NULL GROUP BY email HAVING COUNT(*) > 1",
    ),
    Check(
        "pedido_sem_cliente",
        "Todo pedido pertence a um cliente que existe",
        "alta",
        """SELECT p.id AS pedido, p.cliente_id
           FROM pedidos p LEFT JOIN clientes c ON c.id = p.cliente_id
           WHERE c.id IS NULL""",
    ),
    Check(
        "pedido_sem_produto",
        "Todo pedido aponta para um produto que existe",
        "alta",
        """SELECT p.id AS pedido, p.produto_id
           FROM pedidos p LEFT JOIN produtos pr ON pr.id = p.produto_id
           WHERE pr.id IS NULL""",
    ),
    Check(
        "quantidade_invalida",
        "Todo pedido tem pelo menos 1 item",
        "alta",
        "SELECT id AS pedido, quantidade FROM pedidos WHERE quantidade <= 0",
    ),
    Check(
        "status_invalido",
        "Status do pedido é pendente, entregue ou cancelado",
        "média",
        "SELECT id AS pedido, status FROM pedidos WHERE status NOT IN ('pendente', 'entregue', 'cancelado')",
    ),
    Check(
        "pedido_de_cliente_inativo",
        "Cliente inativo não tem pedido pendente",
        "média",
        """SELECT p.id AS pedido, c.nome AS cliente
           FROM pedidos p JOIN clientes c ON c.id = p.cliente_id
           WHERE c.ativo = 0 AND p.status = 'pendente'""",
    ),
]


def run(conn: sqlite3.Connection, check: Check) -> list[dict]:
    """Executa uma verificação e devolve as linhas com defeito."""
    return [dict(row) for row in conn.execute(check.sql).fetchall()]


def run_all(conn: sqlite3.Connection) -> dict[str, list[dict]]:
    return {check.name: run(conn, check) for check in CHECKS}
