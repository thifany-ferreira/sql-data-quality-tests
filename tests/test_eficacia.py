"""Prova de eficácia: cada verificação pega exatamente o defeito plantado e nada além dele.

Uma verificação que nunca falha não protege nada. Por isso cada regra tem um defeito
conhecido em sql/dados_com_defeitos.sql, e o teste confere que ele é encontrado.
"""

import pytest

from dq.checks import CHECKS, run

# verificação -> (coluna que identifica a linha, valores esperados)
ESPERADO = {
    "preco_negativo": ("id", {4}),
    "estoque_negativo": ("id", {5}),
    "email_vazio": ("id", {3}),
    "email_invalido": ("id", {6}),
    "email_duplicado": ("email", {"ana@email.com"}),
    "pedido_sem_cliente": ("pedido", {5}),
    "pedido_sem_produto": ("pedido", {8}),
    "quantidade_invalida": ("pedido", {7}),
    "status_invalido": ("pedido", {9}),
    "pedido_de_cliente_inativo": ("pedido", {7}),
}


def test_toda_verificacao_tem_defeito_plantado():
    assert set(ESPERADO) == {c.name for c in CHECKS}


@pytest.mark.parametrize("check", CHECKS, ids=lambda c: c.name)
def test_verificacao_encontra_o_defeito(banco_com_defeitos, check):
    coluna, esperados = ESPERADO[check.name]
    encontrados = {linha[coluna] for linha in run(banco_com_defeitos, check)}
    assert encontrados == esperados


def test_email_duplicado_conta_os_clientes(banco_com_defeitos):
    check = next(c for c in CHECKS if c.name == "email_duplicado")
    assert run(banco_com_defeitos, check) == [{"email": "ana@email.com", "clientes": 2}]
