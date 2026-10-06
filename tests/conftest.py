import pytest

from dq.db import connect


@pytest.fixture
def banco_limpo():
    conn = connect("limpos")
    yield conn
    conn.close()


@pytest.fixture
def banco_com_defeitos():
    conn = connect("defeitos")
    yield conn
    conn.close()
