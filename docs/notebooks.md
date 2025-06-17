# Documentação dos Notebooks Databricks

Esta documentação apresenta os notebooks que fazem o processo de ingestão e tratamento dos dados em três camadas: **Bronze**, **Silver** e **Gold** .

---

## Notebook Bronze

### Objetivo

Ingerir os arquivos CSV da landing zone no armazenamento Azure Data Lake (ADLS), montar os containers, carregar os dados em DataFrames Spark, aplicar algumas transformações básicas e salvar no formato Delta na camada Bronze.

### Configurações e Montagem

```
storageAccountName = ""
storageAccountAccessKey = ""
sasToken = ""

def mount_adls(blobContainerName):
    try:
        dbutils.fs.mount(
            source = "wasbs://{}@{}.blob.core.windows.net".format(blobContainerName, storageAccountName),
            mount_point = f"/mnt/{storageAccountName}/{blobContainerName}",
            extra_configs = {'fs.azure.sas.' + blobContainerName + '.' + storageAccountName + '.blob.core.windows.net': sasToken}
        )
        print("OK!")
    except Exception as e:
        print("Falha", e)

mount_adls('landing-zone')
mount_adls('bronze')
mount_adls('silver')
mount_adls('gold')
```

### Ingestão dos Dados CSV

Leitura dos arquivos CSV da landing zone para os DataFrames Spark e definição dos nomes das colunas.

Exemplo para o arquivo vendedores:

```
df_vendedores_raw = spark.read.option("header", "false").csv(f"/mnt/{storageAccountName}/landing-zone/ecommerce/vendedores.csv")
colunas_vendedores = ["id", "nome", "email", "telefone", "data_cadastro"]
df_vendedores = df_vendedores_raw.toDF(*colunas_vendedores)
```

Processo similar para os demais arquivos:

- clientes.csv
- categorias.csv
- estoque.csv
- pagamentos.csv
- entregas.csv
- avaliacoes.csv
- pedidos.csv
- enderecos_cliente.csv
- transportadoras.csv
- formas_pagamento.csv
- itens_pedido.csv
- produtos.csv

### Enriquecimento dos DataFrames

Adição das colunas `data_hora_bronze` (timestamp da ingestão) e `nome_arquivo` para rastreamento.

```
from pyspark.sql.functions import current_timestamp, lit

df_vendedores = df_vendedores.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("vendedores.csv"))
# Mesmo para os demais DataFrames...
```

### Sanitização dos nomes das colunas

Função para padronizar os nomes das colunas:

```
def sanitize_columns(df):
    for col_name in df.columns:
        new_name = (
            col_name.strip()
            .lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "_")
            .replace(",", "")
            .replace(";", "")
            .replace("{", "")
            .replace("}", "")
            .replace("=", "")
            .replace("\n", "")
            .replace("\t", "")
        )
        df = df.withColumnRenamed(col_name, new_name)
    return df
```

### Salvamento dos dados na camada Bronze

```
dfs = [
    (df_vendedores, "vendedores"),
    (df_clientes, "clientes"),
    (df_categorias, "categorias"),
    (df_estoque, "estoque"),
    (df_pagamentos, "pagamentos"),
    (df_entregas, "entregas"),
    (df_avaliacoes, "avaliacoes"),
    (df_formas_pagamento, "formas_pagamento"),
    (df_transportadoras, "transportadoras"),
    (df_pedidos, "pedidos"),
    (df_enderecos_cliente, "enderecos_cliente"),
    (df_itens_pedido, "itens_pedido"),
    (df_produtos, "produtos"),
]

for df, name in dfs:
    df_sanitized = sanitize_columns(df)
    path = f"/mnt/{storageAccountName}/bronze/ecommerce/{name}"
    df_sanitized.write.format("delta").save(path)
```

---

## Notebook Silver

### Objetivo

Ler os dados da camada Bronze, aplicar tratamentos e renomeações, adicionar metadados, e salvar os dados processados na camada Silver.

### Montagem dos containers (mesma função do notebook Bronze)

```
storageAccountName = ""
storageAccountAccessKey = ""
sasToken= ""

def mount_adls(blobContainerName):
    try:
        dbutils.fs.mount(
            source = "wasbs://{}@{}.blob.core.windows.net".format(blobContainerName, storageAccountName),
            mount_point = f"/mnt/{storageAccountName}/{blobContainerName}",
            extra_configs = {'fs.azure.sas.' + blobContainerName + '.' + storageAccountName + '.blob.core.windows.net': sasToken}
        )
        print("OK!")
    except Exception as e:
        print("Falha", e)
```

### Leitura dos dados Bronze em formato Delta

```
df_avaliacoes          = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/avaliacoes")
df_categorias          = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/categorias")
df_clientes            = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/clientes")
df_enderecos_cliente   = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/enderecos_cliente")
df_entregas            = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/entregas")
df_estoque             = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/estoque")
df_formas_pagamento    = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/formas_pagamento")
df_itens_pedidos       = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/itens_pedido")
df_pagamentos          = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/pagamentos")
df_pedidos             = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/pedidos")
df_produtos            = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/produtos")
df_transportadoras     = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/transportadoras")
df_vendedores          = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/ecommerce/vendedores")
```

### Adição de colunas de metadados para Silver

```
from pyspark.sql.functions import current_timestamp, lit

df_avaliacoes = df_avaliacoes.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("avaliacoes"))
# Repetir para os demais DataFrames
```

### Renomeação das colunas para padrão maiúsculo e tratamento de sufixos

Função para renomear as colunas:

```
from pyspark.sql.functions import lit, current_timestamp

def renomear_colunas(diretorio):
    df = spark.read.format('delta').load(diretorio)
    tabela = diretorio.split('/')[-2]

    novos_nomes = {}

    for coluna in df.columns:
        novo_nome = coluna.upper()

        if novo_nome.endswith("_ID"):
            prefixo = novo_nome[:-3]
            novo_nome = f"CODIGO_{prefixo}"
        else:
            novo_nome = novo_nome.replace("ID", "CODIGO")

        novos_nomes[coluna] = novo_nome

    for antigo, novo in novos_nomes.items():
        df = df.withColumnRenamed(antigo, novo)

    for col_drop in ["DATA_HORA_BRONZE", "NOME_ARQUIVO"]:
        if col_drop in df.columns:
            df = df.drop(col_drop)

    df = df.withColumn("NOME_ARQUIVO_BRONZE", lit(tabela))
    df = df.withColumn("DATA_ARQUIVO_SILVER", current_timestamp())

    df.write.format('delta').mode("overwrite").save(f"/mnt/{storageAccountName}/silver/ecommerce/{tabela}")

def renomear_arquivos_delta(diretorio):
    arquivos = dbutils.fs.ls(diretorio)
    for arquivo in arquivos:
        renomear_colunas(arquivo.path)

diretorio = f'/mnt/{storageAccountName}/bronze/ecommerce'
renomear_arquivos_delta(diretorio)
```

---


