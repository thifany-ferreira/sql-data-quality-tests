"""A suíte de verdade: o banco precisa respeitar todas as regras de negócio."""

import pytest

from dq.checks import CHECKS, run


@pytest.mark.parametrize("check", CHECKS, ids=lambda c: c.name)
def test_regra_respeitada(banco_limpo, check):
    defeitos = run(banco_limpo, check)
    assert not defeitos, f"{check.regra}: {len(defeitos)} linha(s) com defeito -> {defeitos}"
