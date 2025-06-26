# Eng Dados ecommerce
 
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)]()  


Repositorio do projeto final da disciplina de Engenharia de Dados do curso de Engenharia de Software da UNISATC.

## Desenho de Arquitetura


![image](/docs/assets/diagrama-arquitetura.png)

## Ferramentas utilizadas

## Stack Tecnológica

| Categoria        | Ferramenta               |
|------------------|--------------------------|
| Banco de Dados   | **Azure SQL Database**           |
| Orquestração     | **Azure Data Factory**   |
| Processamento    | **Azure Databricks**     |
| Armazenamento    | **Azure Data Lake Storage Gen2** |
| Visualização     | **Power BI**             |


# Pré-requisitos

Antes de iniciar o projeto, certifique-se de que você possui os seguintes itens instalados e configurados em seu ambiente:

## Ambiente Local

| Requisito                        | Versão recomendada       | Descrição                                                                 |
|----------------------------------|---------------------------|---------------------------------------------------------------------------|
| [Python](https://www.python.org) | 3.10+                     | Linguagem usada para scripts e geração de dados fake                      |
| [Poetry](https://python-poetry.org/) | 1.5+                   | Gerenciador de dependências do Python                                     |
| [Git](https://git-scm.com/)      | Qualquer versão estável   | Para clonar o repositório                                                 |
| [Terraform](https://www.terraform.io/) | 1.4+                 | Provisionamento da infraestrutura na Azure                                |

## Conta em Nuvem

| Requisito                | Observação                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Conta na [Microsoft Azure](https://azure.microsoft.com/pt-br/free/) | É possível criar uma conta gratuita com 200 USD de crédito inicial       |
| Acesso ao portal Azure Portal ([portal.azure.com](https://portal.azure.com/)) | Para criar e gerenciar recursos como Data Factory, Databricks, etc. |

## Outras Ferramentas Recomendadas

| Ferramenta                           | Uso                                                               |
|-------------------------------------|-------------------------------------------------------------------|
| [SSMS](https://aka.ms/ssmsfullsetup) ou [DBeaver](https://dbeaver.io/) | Gerenciar o banco de dados relacional na Azure SQL                |
| [Power BI Desktop](https://powerbi.microsoft.com/pt-br/downloads/) | Conectar-se ao Azure SQL e criar dashboards de visualização      |
| Editor de texto ou IDE (VS Code, PyCharm etc.) | Para editar scripts e notebooks                                   |


# Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/pauloFrancisconi/ABP-eng-dados
cd ABP-eng-dados
```

## 2. Instalar dependências 
 Instalação das dependências poetry do projeto
```bash
poetry add
```
## Documentação (MkDocs)

Toda a documentação está em `docs/`: [(link docks)](https://paulofrancisconi.github.io/ABP-eng-dados)
Você tambem pode executar o comando mkdocs serve para acessar localmente a documetação.
```bash
mkdocs serve
```
# Execução do projeto


## Conta na azure
Antes de conseguir provisionar os ambientes utilizados na azure, você precisa criar uma conta gratuita de 200$ ou uma conta pay as you go. Você poderá criar sua conta [clicando aqui](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account)

## Provisionamento Terraform
Na pasta `/Iac` você encontrará outras 5 pastas, navegue em cada uma utilizando:
```bash
cd Iac/pasta_desejada
```
Crie um arquivo tfvars.terraform com as variáveis necessárias.
utilize os comandos Terraform em cada uma das pastas.
```bash
terraform init  
terraform plan -var-file="../terraform.tfvars"  
terraform apply -var-file="../terraform.tfvars" 
```

Os exemplos de criação dos arquivos tfvars e listagem de variáveis podem ser encontrados na nossa documentação oficial na parte de [Iac](https://paulofrancisconi.github.io/ABP-eng-dados/iac)

## Dados do projeto

### Criação banco de dados
Utilizando um SSMS ou então outro gerenciador de banco de dados, conecte-se ao seu banco utilizando as credenciais passadas no terraform e execute o comando sql listado em `/data/script_SQL_DDL_relacional.sql`.

### Faker dos dados
Após a instalação das dependências do projeto, crie um arquivo .env na raiz do projeto seguindo o exemplo do arquivo .env.example, colque os dados corretos do banco de dados criado com o terraform execute o script de criação de dados faker. Navegue até a pasta do faker:
```bash
cd src/faker
```
e execute o comando
```bash
python faker_data.py
```
Após a execução do script, aguarde até que todos os dados sejam inseridos no banco de dados.

## Ambiente Data Factory
Com a conta gratuita feita, acesse o [Portal da azure](https://portal.azure.com/).
Você poderá encontrar o seu grupo de recursos criado na etapa de provisionamento de recursos com Azure, acesse o Data Factory e entre no ambiente de desenvolvimento, ali você poderá criar os links de serviços relacionando os recursos criados e construir e orquestrar a sua pipeline de dados. Você pode conferir todas as configurações necessárias de linked services, pipelines e orquestrações na documentação oficial do projeto, na aba de [Configuração de pipeline](https://paulofrancisconi.github.io/ABP-eng-dados/adf-config/) e [Criação de pipeline](https://paulofrancisconi.github.io/ABP-eng-dados/adf-pipeline/).

## Ambiente databricks
Com a conta gratuita feita, acesse o [Portal da azure](https://portal.azure.com/).
Você poderá encontrar o seu grupo de recursos criado na etapa de provisionamento de recursos com Azure, acesse o Azure Databricks e entre no ambiente de desenvolvimento, ali você importará os notebooks localizados em `/src/notebooks` para dentro do seu workspace. Você pode conferir toda a documentação e configuração de cluster na documentação oficial do projeto, na aba de [Azure Databricks](https://paulofrancisconi.github.io/ABP-eng-dados/azdabri/).

## Power BI
Com a sua conta da microsoft você poderá entrar em uma conta de PowerBi e realizar os passos de criação na documentação oficial do projeto, em [Power BI](https://paulofrancisconi.github.io/ABP-eng-dados/powerbi/) para realizar a visualização final dos dados.


## Versão

Versão do projeto: 1.0

## Autores

- [**Alexandre Destro Zanoni**](https://github.com/AlexandreDestro) — Documentação MkDocs e README  
- [**Gabriel Milano Alves**](https://github.com/gabrielmilano) — Transformações no Databricks  
- [**Gabriel Rona Guzzatti**](https://github.com/Guzzatti) — Scripts IaC, Faker e documentação  
- [**Gustavo Neskovek Goulart**](https://github.com/gosttavo) — Transformações no Databricks e Power BI  
- [**João Daniel de Liz**](https://github.com/f5joaodanieldeliz) — Documentação MkDocs e README  
- [**Paulo Ronchi Francisconi**](https://github.com/pauloFrancisconi) — Azure Data Factory, Banco de Dados, Faker e documentação



## Licença

Este projeto está sob a licença (MIT license) - veja o arquivo LICENSE para detalhes.

## Referências

### Documentação

- [Azure SQL Database](https://learn.microsoft.com/pt-br/azure/azure-sql/?view=azuresql)
- [Azure Data Factory](https://learn.microsoft.com/pt-br/azure/data-factory/)
- [Azure Databricks](https://learn.microsoft.com/pt-br/azure/databricks/)
- [Azure Data Lake Storage Gen2](https://learn.microsoft.com/pt-br/azure/storage/blobs/data-lake-storage-introduction)

### Canais e Vídeos

- [Engenharia de Dados (YouTube)](https://www.youtube.com/@EngenhariadeDados) – Canal com vídeos e séries sobre a área de dados.
- [DataWayBR (YouTube)](https://www.youtube.com/@datawaybr) – Conteúdo educativo sobre engenharia de dados na prática.
- [Tutorial Terraform + Azure](https://www.youtube.com/watch?v=uk1wvsBvF34&t=1s) – Tutorial passo a passo de provisionamento na Azure com Terraform.
- [Tutorial Azure Databricks + Data Factory](https://www.youtube.com/watch?v=w_neG_E_mzI) – Exemplo prático de integração entre ferramentas.

### Projetos de Referência

- [Projeto Engenharia de Dados SATC](https://github.com/jlsilva01/projeto-ed-satc.git) – Exemplo prático de projeto semelhante utilizado como inspiração.
- [Projeto Databricks na Azure](https://github.com/jlsilva01/engenharia-dados-azure-databricks) - Utilizado alguns scripts de provisionamento do terraform de exemplo.

