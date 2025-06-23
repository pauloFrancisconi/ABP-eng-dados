# Documentação Power BI - Projeto Ecommerce

Este documento descreve os indicadores, métricas e fontes de dados utilizadas no dashboard Power BI construído sobre a camada **Gold** do Data Lake.

---

## Objetivo

Consumir os dados processados da camada **Gold** no Power BI para análise de vendas, desempenho por produto, comportamento do cliente e eficiência da operação logística e financeira.

---

## Conexão com os Dados

Os dados estão armazenados em formato Delta no Azure Data Lake Storage (ADLS) Gen2, organizados nas seguintes tabelas dimensionais e fato:

| Tabela               | Caminho no Data Lake |
|----------------------|----------------------|
| **Fato Vendas**       | [fato_vendas](https://datalake922b9abd80170b5b.dfs.core.windows.net/gold/ecommerce/fato_vendas) |
| **Clientes**          | [dim_clientes](https://datalake922b9abd80170b5b.dfs.core.windows.net/gold/ecommerce/dim_clientes) |
| **Entregas**          | [dim_entregas](https://datalake922b9abd80170b5b.dfs.core.windows.net/gold/ecommerce/dim_entregas) |
| **Formas de Pagamento** | [dim_formas_pagamento](https://datalake922b9abd80170b5b.dfs.core.windows.net/gold/ecommerce/dim_formas_pagamento) |
| **Produtos**          | [dim_produtos](https://datalake922b9abd80170b5b.dfs.core.windows.net/gold/ecommerce/dim_produtos) |
| **Tempo**             | [dim_tempo](https://datalake922b9abd80170b5b.dfs.core.windows.net/gold/ecommerce/dim_tempo) |
| **Vendedores**        | [dim_vendedores](https://datalake922b9abd80170b5b.dfs.core.windows.net/gold/ecommerce/dim_vendedores) |

---

## KPIs Utilizados

As principais métricas de desempenho utilizadas no relatório incluem:

- **Clientes Únicos**  
  `Clientes Únicos = DISTINCTCOUNT(fato_vendas[cliente_sk])`

- **Quantidade Total de Itens Vendidos**  
  `Quantidade Total = SUM(fato_vendas[quantidade])`

- **Receita Total**  
  `Receita Total = SUM(fato_vendas[valor_total])`

- **Ticket Médio**  
  `Ticket Médio = DIVIDE([Receita Total], COUNT(fato_vendas[id]))`

---

## Métricas por Dimensão

Essas métricas possibilitam cortes estratégicos por diferentes dimensões de negócio:

- **Receita Total por Categoria de Produto**  
  Dimensão: `dim_produtos[categoria]`  
  Medida: `Receita Total`

- **Receita Total por Ano**  
  Dimensão: `dim_tempo[data]`  
  Medida: `Receita Total`

---

## Considerações Finais

A camada Gold fornece dados tratados, limpos e modelados prontos para consumo analítico. A conexão no Power BI foi feita utilizando o conector **Azure Data Lake Gen2** com autenticação baseada em chave ou OAuth, dependendo do ambiente.

Para visualizar o dashboard, clique [aqui.](https://app.powerbi.com/links/5qnd5VzxQn?ctid=5929f706-6711-4044-90b8-b2d847b54d9f&pbi_source=linkShare)

---
