# Azure Data Factory - Integração de Dados

Este documento explica como acessar o Azure Data Factory criado via Terraform, configurar os serviços vinculados (Linked Services) e criar os conjuntos de dados (Datasets) necessários para a movimentação de dados entre o Azure SQL Database, Azure Data Lake Storage Gen2 e o Azure Databricks.

---

## 1. Acessando o Azure Data Factory

Acesse o recurso Azure Data Factory criado por Terraform em seu ambiente Azure:

1. Vá para o [Portal Azure](https://portal.azure.com)
2. Na barra de pesquisa, digite **"Data Factory"**
3. Selecione o recurso com o nome provisionado no Terraform.
4. Clique em **"Iniciar o Studio"** (Open Azure Data Factory Studio) para acessar o ambiente de integração visual.

---

## 2. Configurando os Linked Services

Com o Azure Data Factory aberto:

1. No menu à esquerda, clique em **"Gerenciar" (Manage)**.
2. Selecione **"Serviços vinculados" (Linked Services)**.
3. Clique em **"Novo"** para adicionar os serviços abaixo:

###  a) Azure SQL Database

- Tipo: **Azure SQL Database**
- Inscrição: Selecione sua subscrição Azure
- Banco de dados: Selecione o provisionado via Terraform
- Autenticação: Nome de usuário e senha (Admin do SQL Server)

###  b) Azure Data Lake Storage Gen2

- Tipo: **Azure Data Lake Storage Gen2**
- Inscrição: Selecione sua subscrição Azure
- Conta de Armazenamento: Selecione a provisionada no Terraform
- Autenticação: Conta de Serviço (Managed Identity ou Chave de Conta)

###  c) Azure Databricks

- Tipo: **Azure Databricks**
- Inscrição: Selecione sua subscrição Azure
- Workspace: Selecione o workspace Databricks criado via Terraform
- Autenticação: Token pessoal do Databricks  
  - Caso não tenha um token, consulte a [Documentação do Azure Databricks](azdabri.md)
- Cluster: Selecione o cluster interativo existente (criado anteriormente)

---

## 3. Criando os Conjuntos de Dados (Datasets)

###  a) Dataset de Origem: Azure SQL Database

Crie um novo dataset para conectar-se às tabelas do banco de dados SQL hospedado no Azure:

- Tipo: **Azure SQL Database**
- Linked Service: Selecione o serviço criado acima
- Query/Table: Selecione a tabela desejada ou use parâmetros

 Exemplo de parâmetro configurado:

![Exemplo de Dataset SQL com Parâmetro](/assets/ds-sql-parametro.png)

**JSON do Dataset:**

JSON

```
{
    "name": "DS_SQL_Parametro",
    "properties": {
        "linkedServiceName": {
            "referenceName": "AzureSqlDatabase",
            "type": "LinkedServiceReference"
        },
        "parameters": {
            "tabela_nome": {
                "type": "string"
            }
        },
        "annotations": [],
        "type": "AzureSqlTable",
        "schema": [],
        "typeProperties": {
            "schema": "relacional",
            "table": "avaliacoes"
        }
    }
}
```

---

### b) Dataset de Destino: Azure Data Lake Storage Gen2 (Delimited Text)

Configure um dataset para exportar os dados em formato `.csv` para a landing zone no Data Lake:

- Tipo: **Delimited Text**
- Linked Service: Azure Data Lake Storage Gen2
- Pasta de destino: landing-zone/
- Nome do arquivo: pode ser parametrizado (ex: `@dataset().nome_arquivo`)
- Delimitador: `,`
- First Row as Header: true

 Exemplo de configuração:

![Exemplo de Dataset destino para CSV](/assets/ds-dest-csv.png)

**JSON do Dataset:**

JSON

```
{
    "name": "DS_DEST_CSV",
    "properties": {
        "linkedServiceName": {
            "referenceName": "AzureDataLakeStorage",
            "type": "LinkedServiceReference"
        },
        "parameters": {
            "nome_arquivo": {
                "type": "string"
            }
        },
        "annotations": [],
        "type": "DelimitedText",
        "typeProperties": {
            "location": {
                "type": "AzureBlobFSLocation",
                "fileSystem": {
                    "value": "@concat(\n  'landing-zone/ecommerce/',\n  trim(\n    uriComponent(\n      trim(\n        split(trim(dataset().nome_arquivo), '.')[1]\n      )\n    )\n  ),\n  '.csv'\n)",
                    "type": "Expression"
                }
            },
            "columnDelimiter": ",",
            "escapeChar": "\\",
            "firstRowAsHeader": true,
            "quoteChar": "\""
        },
        "schema": []
    }
}
```

---


> ⚠️ **Importante:** Certifique-se de testar a conexão de cada Linked Service e Dataset após a criação.

---

[Ir para ciração da pipeline no Azure Data Factory](adf-pipeline.md)