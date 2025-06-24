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


## Notebook Gold

### Objetivo

Ler os dados da camada silver, fazer algumas agregações entre tabelas e disponibilizar um modelo dimensional, com tabelas de dimensão e tabelas fato, ja com todos os dados em formatos delta prontos para serem consumidos por Power BI ou outra ferramenta de visualização de dados.

### Montagem dos containers (mesma função do notebook Silver)

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

### Leitura em dos dados da Silver em formato Delta

```
df_avaliacoes          = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/avaliacoes")
df_categorias          = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/categorias")
df_clientes            = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/clientes")
df_enderecos_cliente  = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/enderecos_cliente")
df_entregas            = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/entregas")
df_estoque             = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/estoque")
df_formas_pagamento    = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/formas_pagamento")
df_itens_pedidos       = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/itens_pedido")
df_pagamentos          = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/pagamentos")
df_pedidos             = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/pedidos")
df_produtos            = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/produtos")
df_transportadoras     = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/transportadoras")
df_vendedores          = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/ecommerce/vendedores")
```

### Adiciona metadados para os dataframes utiizados no notebook

from pyspark.sql.functions import current_timestamp, lit

```
df_avaliacoes          = df_avaliacoes.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("avaliacoes"))
df_categorias          = df_categorias.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("categorias"))
df_clientes            = df_clientes.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("clientes"))
df_entregas            = df_entregas.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("entregas"))
df_estoque             = df_estoque.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("estoque"))
df_formas_pagamento    = df_formas_pagamento.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("formas_pagamento"))
df_itens_pedidos       = df_itens_pedidos.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("itens_pedidos"))
df_pagamentos          = df_pagamentos.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("pagamentos"))
df_pedidos             = df_pedidos.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("pedidos"))
df_produtos            = df_produtos.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("produtos"))
df_transportadoras     = df_transportadoras.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("transportadoras"))
df_vendedores          = df_vendedores.withColumn("data_hora_gold", current_timestamp()).withColumn("nome_arquivo", lit("vendedores"))
```

### Cria as tabelas dimensionais 

#### Tabela Dimensão clientes
```
%sql
CREATE TABLE IF NOT EXISTS dim_clientes (
  ID BIGINT GENERATED ALWAYS AS IDENTITY,
  CODIGO_CLIENTE INT,
  NOME STRING,
  EMAIL STRING,
  TELEFONE STRING,
  CIDADE STRING,
  ESTADO STRING,
  DATA_CADASTRO TIMESTAMP
)
USING delta
LOCATION '/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_clientes';

```
#### Tabela Dimensão produtos
```
%sql
CREATE TABLE IF NOT EXISTS dim_produtos (
  ID BIGINT GENERATED ALWAYS AS IDENTITY,  -- Chave substituta (SK)
  CODIGO_PRODUTO INT,                      -- Chave natural do sistema transacional
  NOME STRING,
  DESCRICAO STRING,
  PRECO DECIMAL(10,2),
  CATEGORIA STRING,
  DATA_CADASTRO TIMESTAMP
)
USING delta
LOCATION '/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_produtos';

```
#### Tabela Dimensão vendedores
```
%sql
CREATE TABLE IF NOT EXISTS dim_vendedores (
  ID BIGINT GENERATED ALWAYS AS IDENTITY,   -- Chave substituta (SK)
  CODIGO_VENDEDOR INT,                      -- Chave natural do sistema de origem
  NOME STRING,
  EMAIL STRING,
  TELEFONE STRING,
  DATA_CADASTRO TIMESTAMP
)
USING delta
LOCATION '/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_vendedores';

```
#### Tabela Dimensão formas de pagamento
```
%sql
CREATE TABLE IF NOT EXISTS dim_formas_pagamento (
  ID BIGINT GENERATED ALWAYS AS IDENTITY,  -- Chave substituta (SK)
  CODIGO_FORMA INT,                        -- Chave natural (caso exista)
  DESCRICAO STRING
)
USING delta
LOCATION '/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_formas_pagamento';

```
#### Tabela Dimensão tempo
```
from pyspark.sql.functions import expr, date_format, year, month, dayofmonth, dayofweek, when, col

data_inicial = "2022-01-01"
data_final = "2025-12-31"

num_dias = spark.sql(f"SELECT datediff('{data_final}', '{data_inicial}')").collect()[0][0]

df_calendario = spark.range(0, num_dias + 1) \
    .selectExpr(f"date_add(to_date('{data_inicial}'), CAST(id AS INT)) AS Data")

# Criar colunas nome mês e dia da semana com when (case when)
df_tempo = df_calendario.select(
    col("Data"),
    year("Data").alias("Ano"),
    month("Data").alias("Mes"),
    when(month("Data") == 1, "JANEIRO")
    .when(month("Data") == 2, "FEVEREIRO")
    .when(month("Data") == 3, "MARCO")
    .when(month("Data") == 4, "ABRIL")
    .when(month("Data") == 5, "MAIO")
    .when(month("Data") == 6, "JUNHO")
    .when(month("Data") == 7, "JULHO")
    .when(month("Data") == 8, "AGOSTO")
    .when(month("Data") == 9, "SETEMBRO")
    .when(month("Data") == 10, "OUTUBRO")
    .when(month("Data") == 11, "NOVEMBRO")
    .when(month("Data") == 12, "DEZEMBRO")
    .alias("NomeMes"),
    dayofmonth("Data").alias("Dia"),
    when(dayofweek("Data") == 1, "DOMINGO")
    .when(dayofweek("Data") == 2, "SEGUNDA-FEIRA")
    .when(dayofweek("Data") == 3, "TERCA-FEIRA")
    .when(dayofweek("Data") == 4, "QUARTA-FEIRA")
    .when(dayofweek("Data") == 5, "QUINTA-FEIRA")
    .when(dayofweek("Data") == 6, "SEXTA-FEIRA")
    .when(dayofweek("Data") == 7, "SABADO")
    .alias("NomeDiaSemana"),
    dayofweek("Data").alias("NumeroDiaSemana"),
    date_format("Data", "yyyyMMdd").cast("int").alias("ID")
)

df_tempo.display()

df_tempo.write.mode("overwrite")\
    .option("path", f"/mnt/{storageAccountName}/gold/ecommerce/dim_tempo")\
    .saveAsTable("dim_tempo")

```
#### Tabela Dimensão entregas
```
%sql
CREATE TABLE IF NOT EXISTS dim_entregas (
  ID BIGINT GENERATED ALWAYS AS IDENTITY,  -- Chave substituta (SK)
  CODIGO_ENTREGA INT,                       -- Chave natural (caso exista)
  TRANSPORTADORA STRING,
  STATUS STRING,
  DATA_ENVIO TIMESTAMP,
  DATA_ENTREGA TIMESTAMP
)
USING delta
LOCATION '/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_entregas';

```

### Cria os merges e faz os inserts nas tabelas a partir de tabelas temporárias criadas com os dataframes

```
df_clientes.createOrReplaceTempView("silver_clientes")
df_enderecos_cliente.createOrReplaceTempView("silver_enderecos_cliente")
df_produtos.createOrReplaceTempView("silver_produtos")
df_categorias.createOrReplaceTempView("silver_categorias")
df_vendedores.createOrReplaceTempView("silver_vendedores")
df_formas_pagamento.createOrReplaceTempView("silver_formas_pagamento")
df_entregas.createOrReplaceTempView("silver_entregas")
df_transportadoras.createOrReplaceTempView("silver_transportadoras")
df_pedidos.createOrReplaceTempView("pedidos")
df_itens_pedidos.createOrReplaceTempView("itens_pedidos")
df_pagamentos.createOrReplaceTempView("pagamentos")
df_avaliacoes.createOrReplaceTempView("avaliacoes")
df_produtos.createOrReplaceTempView("produtos")

```

#### Tabela Dimensão clientes
```
%sql
-- Criar TEMP VIEW com os dados de origem
CREATE OR REPLACE TEMP VIEW dim_clientes_temp AS
SELECT
    c.CODIGO AS CODIGO_CLIENTE,
    c.NOME,
    c.EMAIL,
    c.TELEFONE,
    ec.CIDADE,
    ec.ESTADO,
    c.DATA_CADASTRO
FROM silver_clientes c
LEFT JOIN silver_enderecos_cliente ec ON c.CODIGO = ec.CODIGO_CLIENTE;

-- MERGE na tabela de dimensão usando a chave natural
MERGE INTO dim_clientes AS target
USING dim_clientes_temp AS source
ON target.CODIGO_CLIENTE = source.CODIGO_CLIENTE
WHEN MATCHED THEN
  UPDATE SET
    target.NOME = source.NOME,
    target.EMAIL = source.EMAIL,
    target.TELEFONE = source.TELEFONE,
    target.CIDADE = source.CIDADE,
    target.ESTADO = source.ESTADO,
    target.DATA_CADASTRO = source.DATA_CADASTRO
WHEN NOT MATCHED THEN
  INSERT (CODIGO_CLIENTE, NOME, EMAIL, TELEFONE, CIDADE, ESTADO, DATA_CADASTRO)
  VALUES (source.CODIGO_CLIENTE, source.NOME, source.EMAIL, source.TELEFONE, source.CIDADE, source.ESTADO, source.DATA_CADASTRO);

```

#### Tabela Dimensão produtos
```
%sql
-- Criar ou substituir a TEMP VIEW com os dados transformados
CREATE OR REPLACE TEMP VIEW dim_produtos_temp AS
SELECT
    p.CODIGO AS CODIGO_PRODUTO,
    p.NOME,
    p.DESCRICAO,
    p.PRECO,
    c.NOME AS CATEGORIA,
    p.DATA_CADASTRO
FROM silver_produtos p
LEFT JOIN silver_categorias c ON p.CODIGO_CATEGORIA = c.CODIGO;

-- Realizar o MERGE na tabela de dimensão
MERGE INTO dim_produtos AS target
USING dim_produtos_temp AS source
ON target.CODIGO_PRODUTO = source.CODIGO_PRODUTO
WHEN MATCHED THEN
  UPDATE SET
    target.NOME = source.NOME,
    target.DESCRICAO = source.DESCRICAO,
    target.PRECO = source.PRECO,
    target.CATEGORIA = source.CATEGORIA,
    target.DATA_CADASTRO = source.DATA_CADASTRO
WHEN NOT MATCHED THEN
  INSERT (CODIGO_PRODUTO, NOME, DESCRICAO, PRECO, CATEGORIA, DATA_CADASTRO)
  VALUES (source.CODIGO_PRODUTO, source.NOME, source.DESCRICAO, source.PRECO, source.CATEGORIA, source.DATA_CADASTRO);
```
#### Tabela Dimensão vendedores
```
%sql
-- Criar ou substituir a TEMP VIEW com os dados transformados
CREATE OR REPLACE TEMP VIEW dim_vendedores_temp AS
SELECT
    CODIGO AS CODIGO_VENDEDOR,
    NOME,
    EMAIL,
    TELEFONE,
    DATA_CADASTRO
FROM silver_vendedores;

-- Realizar o MERGE na tabela de dimensão
MERGE INTO dim_vendedores AS target
USING dim_vendedores_temp AS source
ON target.CODIGO_VENDEDOR = source.CODIGO_VENDEDOR
WHEN MATCHED THEN
  UPDATE SET
    target.NOME = source.NOME,
    target.EMAIL = source.EMAIL,
    target.TELEFONE = source.TELEFONE,
    target.DATA_CADASTRO = source.DATA_CADASTRO
WHEN NOT MATCHED THEN
  INSERT (CODIGO_VENDEDOR, NOME, EMAIL, TELEFONE, DATA_CADASTRO)
  VALUES (source.CODIGO_VENDEDOR, source.NOME, source.EMAIL, source.TELEFONE, source.DATA_CADASTRO);

```

#### Tabela Dimensão formas de pagamento
```
%sql
-- Criar ou substituir a TEMP VIEW com dados da origem
CREATE OR REPLACE TEMP VIEW dim_formas_pagamento_temp AS
SELECT
    CODIGO AS CODIGO_FORMA,
    DESCRICAO
FROM silver_formas_pagamento;

-- MERGE na dimensão dim_formas_pagamento
MERGE INTO dim_formas_pagamento AS target
USING dim_formas_pagamento_temp AS source
ON target.CODIGO_FORMA = source.CODIGO_FORMA
WHEN MATCHED THEN
  UPDATE SET
    target.DESCRICAO = source.DESCRICAO
WHEN NOT MATCHED THEN
  INSERT (CODIGO_FORMA, DESCRICAO)
  VALUES (source.CODIGO_FORMA, source.DESCRICAO);

```

#### Tabela Dimensão entregas
```
%sql
-- Criar ou substituir a TEMP VIEW com os dados de origem
CREATE OR REPLACE TEMP VIEW dim_entregas_temp AS
SELECT
    e.CODIGO AS CODIGO_ENTREGA,
    t.NOME AS TRANSPORTADORA,
    e.STATUS,
    e.DATA_ENVIO,
    e.DATA_ENTREGA
FROM silver_entregas e
LEFT JOIN silver_transportadoras t ON e.CODIGO_TRANSPORTADORA = t.CODIGO;

-- Executar o MERGE na tabela de dimensão
MERGE INTO dim_entregas AS target
USING dim_entregas_temp AS source
ON target.CODIGO_ENTREGA = source.CODIGO_ENTREGA
WHEN MATCHED THEN
  UPDATE SET
    target.TRANSPORTADORA = source.TRANSPORTADORA,
    target.STATUS = source.STATUS,
    target.DATA_ENVIO = source.DATA_ENVIO,
    target.DATA_ENTREGA = source.DATA_ENTREGA
WHEN NOT MATCHED THEN
  INSERT (CODIGO_ENTREGA, TRANSPORTADORA, STATUS, DATA_ENVIO, DATA_ENTREGA)
  VALUES (source.CODIGO_ENTREGA, source.TRANSPORTADORA, source.STATUS, source.DATA_ENVIO, source.DATA_ENTREGA);

```

### Criação da tabela Fato vendas 

```
%sql
CREATE TABLE IF NOT EXISTS fato_vendas (
  ID BIGINT GENERATED ALWAYS AS IDENTITY,  -- SK automática
  CLIENTE_SK INT,
  PRODUTO_SK INT,
  VENDEDOR_SK INT,
  TEMPO_SK INT,
  FORMA_PAGAMENTO_SK INT,
  ENTREGA_SK INT,
  QUANTIDADE INT,
  PRECO_UNITARIO DECIMAL(10,2),
  VALOR_TOTAL DECIMAL(12,2),
  TEMPO_ENTREGA_DIAS INT,
  NOTA_AVALIACAO INT
)
USING delta
LOCATION '/mnt/datalake922b9abd80170b5b/gold/ecommerce/fato_vendas';

```

Depois criação de views temporária

```
spark.read.format("delta").load("/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_clientes").createOrReplaceTempView("dim_clientes")
spark.read.format("delta").load("/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_produtos").createOrReplaceTempView("dim_produtos")
spark.read.format("delta").load("/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_vendedores").createOrReplaceTempView("dim_vendedores")
spark.read.format("delta").load("/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_tempo").createOrReplaceTempView("dim_tempo")
spark.read.format("delta").load("/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_formas_pagamento").createOrReplaceTempView("dim_formas_pagamento")
spark.read.format("delta").load("/mnt/datalake922b9abd80170b5b/gold/ecommerce/dim_entregas").createOrReplaceTempView("dim_entregas")

```

e por fim adiciona os dados na tabela fato

```
%sql
MERGE INTO fato_vendas AS target
USING (
  SELECT
    dc.ID AS CLIENTE_SK,
    dp.ID AS PRODUTO_SK,
    dv.ID AS VENDEDOR_SK,
    dt.ID AS TEMPO_SK,
    dfp.ID AS FORMA_PAGAMENTO_SK,
    de.ID AS ENTREGA_SK,
    ip.QUANTIDADE,
    ip.PRECO_UNITARIO,
    ip.QUANTIDADE * ip.PRECO_UNITARIO AS VALOR_TOTAL,
    DATEDIFF(de.DATA_ENTREGA, de.DATA_ENVIO) AS TEMPO_ENTREGA_DIAS,
    av.NOTA AS NOTA_AVALIACAO
  FROM pedidos p
  INNER JOIN itens_pedidos ip ON ip.CODIGO_PEDIDO = p.CODIGO
  INNER JOIN dim_clientes dc ON dc.CODIGO_CLIENTE = p.CODIGO_CLIENTE
  INNER JOIN dim_produtos dp ON dp.CODIGO_PRODUTO = ip.CODIGO_PRODUTO
  INNER JOIN produtos pr ON pr.CODIGO = ip.CODIGO_PRODUTO
  INNER JOIN dim_vendedores dv ON dv.CODIGO_VENDEDOR = pr.CODIGO_VENDEDOR
  INNER JOIN dim_tempo dt ON dt.Data = CAST(p.DATA_PEDCODIGOO AS DATE)
  LEFT JOIN pagamentos pg ON pg.CODIGO_PEDIDO = p.CODIGO
  LEFT JOIN dim_formas_pagamento dfp ON dfp.CODIGO_FORMA = pg.CODIGO
  LEFT JOIN dim_entregas de ON de.CODIGO_ENTREGA = p.CODIGO_ENDERECO_ENTREGA
  LEFT JOIN (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY CODIGO_PRODUTO, CODIGO_CLIENTE ORDER BY DATA_AVALIACAO DESC) AS rn
    FROM avaliacoes
  ) av ON av.CODIGO_PRODUTO = ip.CODIGO_PRODUTO
       AND av.CODIGO_CLIENTE = p.CODIGO_CLIENTE
       AND av.rn = 1
) AS source
ON 
  target.CLIENTE_SK = source.CLIENTE_SK
  AND target.PRODUTO_SK = source.PRODUTO_SK
  AND target.VENDEDOR_SK = source.VENDEDOR_SK
  AND target.TEMPO_SK = source.TEMPO_SK
  AND target.FORMA_PAGAMENTO_SK = source.FORMA_PAGAMENTO_SK
  AND target.ENTREGA_SK = source.ENTREGA_SK
  AND target.QUANTIDADE = source.QUANTIDADE
  AND target.PRECO_UNITARIO = source.PRECO_UNITARIO
WHEN NOT MATCHED THEN
INSERT (
  CLIENTE_SK,
  PRODUTO_SK,
  VENDEDOR_SK,
  TEMPO_SK,
  FORMA_PAGAMENTO_SK,
  ENTREGA_SK,
  QUANTIDADE,
  PRECO_UNITARIO,
  VALOR_TOTAL,
  TEMPO_ENTREGA_DIAS,
  NOTA_AVALIACAO
)
VALUES (
  source.CLIENTE_SK,
  source.PRODUTO_SK,
  source.VENDEDOR_SK,
  source.TEMPO_SK,
  source.FORMA_PAGAMENTO_SK,
  source.ENTREGA_SK,
  source.QUANTIDADE,
  source.PRECO_UNITARIO,
  source.VALOR_TOTAL,
  source.TEMPO_ENTREGA_DIAS,
  source.NOTA_AVALIACAO
);
```




