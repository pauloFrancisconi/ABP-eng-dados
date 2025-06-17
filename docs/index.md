# Documentação do Projeto de Engenharia de Dados

Este projeto consiste em uma arquitetura de engenharia de dados na nuvem utilizando os principais serviços da Azure. O fluxo contempla ingestão, armazenamento, transformação e visualização de dados.

## Ferramentas utilizadas

- **Banco de dados:** Azure SQL Database
- **Orquestração:** Azure Data Factory
- **Processamento:** Azure Databricks
- **Armazenamento:** Azure Data Lake Storage Gen2
- **Visualização:** Power BI

## Estrutura do Repositório

- `data/`: Scripts SQL para criação do banco de dados relacional, schema e tabelas. Diagramas ER também podem ser adicionados a partir de `/assets`.
- `Iac/`: Infraestrutura como Código (IaC) com Terraform para provisionamento dos recursos na Azure.
  - Subpastas para cada serviço: `adls/`, `sql_server/`, `az_databricks/`, `adf/`, `resource_group/`.
- `assets/`: Imagens, diagramas ER e arquivos auxiliares.
- `docs/`: Documentação completa da aplicação (este diretório).
- `src/`: Pasta com subpastas `faker/`: Script Python que gera dados fictícios e insere no banco SQL e `notebooks/`: Notebooks Python com os scripts de transformação de arquivos no ADLS Gen2 utilizando Azure Databricks.

## Conteúdo da Documentação

- [Visão Geral da Arquitetura](arquitetura.md)
- [Provisionamento com Terraform (IaC)](iac.md)
- [Banco de Dados e Diagramas ER](database.md)
- [Criação de Dados com Faker](faker.md)
- [Notebooks do Databricks (ETL)](notebooks.md)
- [Pipelines no Azure Data Factory - Configuração](adf-config.md)
- [Pipelines no Azure Data Factory - Pipeline](adf-pipeline.md)
- [Dashboard no Power BI](powerbi.md)
