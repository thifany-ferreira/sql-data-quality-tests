# Testes de qualidade de dados em SQL

[![Qualidade de dados](https://github.com/thifany-ferreira/sql-data-quality-tests/actions/workflows/ci.yml/badge.svg)](https://github.com/thifany-ferreira/sql-data-quality-tests/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?logo=sqlite&logoColor=white)
![pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC?logo=pytest&logoColor=white)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)](LICENSE)

> 🇺🇸 *Data quality test suite in SQL + pytest: 10 business rules written as SQL queries (including JOINs and GROUP BY) that catch negative prices, missing or duplicated e-mails, orphan orders and invalid statuses. A planted-defects dataset proves every check actually catches its bug, and the CI publishes a quality report.*

Uma tela pode estar perfeita e o banco por trás dela, cheio de problemas: pedido de cliente que não existe, preço negativo, dois clientes com o mesmo e-mail. Esta suíte **testa os dados**, não a tela.

Cada regra de negócio vira uma **consulta SQL que procura as linhas com defeito**. Banco saudável = nenhuma linha encontrada. O banco é o da **Loja Aurora**, uma loja **fictícia**.

**Autora:** Thifany Ferreira · [LinkedIn](https://www.linkedin.com/in/thifanyferreira) · [Portfólio interativo](https://thifany-ferreira.github.io/apresentacao)

## As 10 regras

| Verificação | Regra | Severidade | SQL usado |
|---|---|---|---|
| `preco_negativo` | Todo produto tem preço maior que zero | alta | `WHERE` |
| `estoque_negativo` | Estoque nunca fica abaixo de zero | alta | `WHERE` |
| `email_vazio` | Todo cliente tem e-mail | média | `IS NULL`, `TRIM` |
| `email_invalido` | E-mail preenchido tem formato válido | média | `LIKE` |
| `email_duplicado` | Cada e-mail pertence a um só cliente | alta | `GROUP BY` + `HAVING` |
| `pedido_sem_cliente` | Todo pedido pertence a um cliente que existe | alta | `LEFT JOIN` |
| `pedido_sem_produto` | Todo pedido aponta para um produto que existe | alta | `LEFT JOIN` |
| `quantidade_invalida` | Todo pedido tem pelo menos 1 item | alta | `WHERE` |
| `status_invalido` | Status é pendente, entregue ou cancelado | média | `NOT IN` |
| `pedido_de_cliente_inativo` | Cliente inativo não tem pedido pendente | média | `JOIN` |

As consultas estão em [`dq/checks.py`](dq/checks.py). Exemplo, pedido de um cliente que não existe:

```sql
SELECT p.id AS pedido, p.cliente_id
FROM pedidos p LEFT JOIN clientes c ON c.id = p.cliente_id
WHERE c.id IS NULL;
```

## Prova de eficácia

Uma verificação que nunca falha não protege nada. Por isso existem dois conjuntos de dados:

- [`sql/dados_limpos.sql`](sql/dados_limpos.sql): dados saudáveis, **todas as regras precisam passar**.
- [`sql/dados_com_defeitos.sql`](sql/dados_com_defeitos.sql): os mesmos dados com **um defeito plantado para cada regra**, marcado no comentário.

O teste [`tests/test_eficacia.py`](tests/test_eficacia.py) confere que cada verificação encontra **exatamente** o defeito plantado: nem menos (deixaria o bug passar), nem mais (alarme falso).

## Relatório

```bash
python -m dq.report --dados defeitos
```

```
**0 de 10 verificações passaram.**

| Resultado | Verificação          | Regra                                 | Severidade | Linhas com defeito |
| ❌ falhou | `preco_negativo`     | Todo produto tem preço maior que zero | alta       | 1                  |
| ❌ falhou | `pedido_sem_cliente` | Todo pedido pertence a um cliente ... | alta       | 1                  |
...
```

No CI, o relatório aparece no **resumo da execução** do GitHub Actions e fica salvo como artefato.

## Como rodar

```bash
pip install -r requirements.txt
pytest                                        # 26 testes
python -m dq.report                           # relatório dos dados limpos
python -m dq.report --dados defeitos          # relatório com os defeitos encontrados
```

Usa SQLite, que já vem com o Python: nada de servidor de banco para instalar.

## Estrutura

```
sql/
  schema.sql               estrutura das tabelas clientes, produtos e pedidos
  dados_limpos.sql         dados saudáveis
  dados_com_defeitos.sql   um defeito plantado por regra
dq/
  db.py                    monta o banco em memória
  checks.py                as 10 regras em SQL
  report.py                relatório em Markdown
tests/
  test_qualidade_dados.py  as regras no banco saudável
  test_eficacia.py         cada regra pega o seu defeito
  test_relatorio.py        o relatório e os códigos de saída
```

## Outros projetos

- [llm-chatbot-security-tests](https://github.com/thifany-ferreira/llm-chatbot-security-tests): segurança de chatbot com IA
- [llm-answer-quality-evals](https://github.com/thifany-ferreira/llm-answer-quality-evals): qualidade de respostas de IA
- [serverest-api-tests](https://github.com/thifany-ferreira/serverest-api-tests): testes de API REST em Java
