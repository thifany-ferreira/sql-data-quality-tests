from dq.report import main


def test_dados_limpos_passam(capsys):
    assert main(["--dados", "limpos"]) == 0
    assert "10 de 10 verificações passaram" in capsys.readouterr().out


def test_dados_com_defeitos_reprovam(capsys):
    assert main(["--dados", "defeitos"]) == 1
    saida = capsys.readouterr().out
    assert "0 de 10 verificações passaram" in saida
    assert "❌ falhou | `preco_negativo`" in saida


def test_expect_fail_inverte_o_resultado():
    assert main(["--dados", "defeitos", "--expect-fail"]) == 0
    assert main(["--dados", "limpos", "--expect-fail"]) == 1


def test_relatorio_salvo_em_arquivo(tmp_path, capsys):
    destino = tmp_path / "reports" / "relatorio.md"
    main(["--dados", "defeitos", "--saida", str(destino)])
    assert destino.read_text(encoding="utf-8").startswith("# Relatório de qualidade de dados")
