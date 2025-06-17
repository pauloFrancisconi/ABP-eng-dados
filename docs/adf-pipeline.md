# Azure Data Factory - Pipeline de Integração

Este documento descreve como criar e configurar uma **pipeline no Azure Data Factory** para orquestrar a movimentação e transformação de dados entre o Azure SQL Database, Azure Data Lake Storage Gen2 e notebooks do Azure Databricks.

---

## 1. Set Variable - Definindo as Tabelas

A primeira atividade da pipeline é definir uma **variável do tipo array** com os nomes das tabelas que serão copiadas do banco de dados.

1. Na aba de atividades, arraste a atividade **Set Variable** para a pipeline.
2. Crie uma nova variável do tipo **Array**, por exemplo: `tabelas`.
3. Configure o valor com os nomes das tabelas, por exemplo:

📷 Exemplo de configuração:

![Set Variable com array de tabelas](/assets/set-variable-pipeline.png)

📄 **Configuração do array:**

@{
  "tabelas": [
    "clientes",
    "vendedores",
    "produtos",
    "pedidos",
    "pagamentos"
  ]
}

---

## 2. Foreach - Loop nas Tabelas

1. Adicione a atividade **Foreach** após o `Set Variable`.
2. Na aba "Configurações" do Foreach, defina como **item sequencial** e adicione a seguinte expressão no campo de itens:

@`@variables('tabelas')`

3. Dentro do Foreach, adicione uma atividade **Copy Data**.

### Configurações da Atividade Copy Data:

- **Origem:** Dataset do Azure SQL Database com suporte a parâmetro de nome de tabela.
- **Destino:** Dataset de arquivo delimitado no ADLS (também parametrizado).

📷 Exemplo de configuração:

![Copy Data na pipeline](/assets/foreach-copy.png)

📄 **Exemplo de mapeamento dinâmico:**

@{
  "source": {
    "type": "AzureSqlSource",
    "sqlReaderQuery": "SELECT * FROM @{item()}"
  },
  "sink": {
    "type": "DelimitedTextSink"
  },
  "translator": {
    "type": "TabularTranslator",
    "typeConversion": true,
    "typeConversionMode": "AllowCompatible"
  }
}

---

## 3. Executando Notebook Bronze no Databricks

1. Após o loop, adicione uma nova atividade: **Databricks Notebook**.
2. Configure com o serviço vinculado (Linked Service) do Databricks criado anteriormente.
3. Preencha o campo **Path** com o caminho do notebook **bronze**, que deve estar no workspace.

> ℹ️ O caminho do notebook pode ser encontrado conforme instruído na [documentação do Azure Databricks](azdabri.md).

---

## 4. Executando Notebook Silver no Databricks

1. Adicione outra atividade **Databricks Notebook**.
2. Use o mesmo Linked Service.
3. Preencha com o caminho do notebook **silver**.

---

## 5. Executando Notebook Gold no Databricks

1. Adicione mais uma atividade **Databricks Notebook**.
2. Configure novamente com o Linked Service e o caminho do notebook **gold**.

---

## 6. Considerações Finais

- Certifique-se de que o cluster do Databricks está ativo antes da execução dos notebooks.
- O nome das tabelas no array do `Set Variable` deve existir no banco SQL.
- Os datasets devem estar parametrizados para receber dinamicamente o nome da tabela e do arquivo.
- O pipeline pode ser agendado ou executado manualmente.
- Todas as dependências (Linked Services, Datasets, e Notebooks) devem estar previamente criadas.

---
