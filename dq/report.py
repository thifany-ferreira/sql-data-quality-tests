"""Gera o relatório de qualidade de dados.

Uso:
    python -m dq.report                          # dados limpos
    python -m dq.report --dados defeitos --expect-fail
"""

import argparse
import sys
from pathlib import Path

from dq.checks import CHECKS, run_all
from dq.db import DATASETS, connect


def build_markdown(dataset: str, results: dict[str, list[dict]]) -> str:
    failed = [c for c in CHECKS if results[c.name]]
    lines = [
        f"# Relatório de qualidade de dados · `{dataset}`",
        "",
        f"**{len(CHECKS) - len(failed)} de {len(CHECKS)} verificações passaram.**",
        "",
        "| Resultado | Verificação | Regra | Severidade | Linhas com defeito |",
        "|---|---|---|---|---|",
    ]
    for check in CHECKS:
        rows = results[check.name]
        mark = "❌ falhou" if rows else "✅ passou"
        lines.append(f"| {mark} | `{check.name}` | {check.regra} | {check.severidade} | {len(rows)} |")
    for check in failed:
        lines += ["", f"## `{check.name}`", "", f"Regra: {check.regra}.", "", "```"]
        lines += [str(row) for row in results[check.name]]
        lines.append("```")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Relatório de qualidade de dados")
    parser.add_argument("--dados", choices=list(DATASETS), default="limpos")
    parser.add_argument("--saida", type=Path, default=None, help="arquivo .md para salvar o relatório")
    parser.add_argument(
        "--expect-fail", action="store_true", help="sucesso apenas se a suíte encontrar defeitos (prova de eficácia)"
    )
    args = parser.parse_args(argv)

    results = run_all(connect(args.dados))
    report = build_markdown(args.dados, results)
    print(report)
    if args.saida:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(report, encoding="utf-8")

    found_defects = any(results.values())
    if args.expect_fail:
        return 0 if found_defects else 1
    return 1 if found_defects else 0


if __name__ == "__main__":
    sys.exit(main())
