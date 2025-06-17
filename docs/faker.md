# Gerando Dados Falsos com Faker

Nesta etapa, utilizamos a biblioteca **Faker** para popular automaticamente o banco de dados com dados sintéticos realistas. Isso facilita o teste do sistema com um volume significativo de dados.

---

## Arquivos Relacionados

- `faker_data.py` — Script principal de geração e inserção de dados.
- `.env.example` — Modelo de variáveis de ambiente necessárias.
- `teste_conexao.py` — Script para testar a conexão com o banco.

---

## Como Funciona

O script `faker_data.py` utiliza:

- **Faker** para gerar dados como nomes, emails, endereços, datas etc.
- **pyodbc** para conectar-se ao SQL Server hospedado na Azure.
- **dotenv** para carregar variáveis de ambiente de um arquivo `.env`.

Ele gera dados para diversas tabelas do schema `relacional`, como:

- `clientes`, `vendedores`, `produtos`, `pedidos`, `pagamentos`, `entregas` e mais.
- Categorias e formas de pagamento são fixas.
- A inserção é feita em lote, e a execução só começa se todas as tabelas existirem.

---

## Antes de Executar

### 1. Criar o Banco de Dados (se necessário)

Se ainda não houver um Azure SQL Database criado, consulte a documentação de provisionamento com Terraform:

[Provisionamento com Terraform](iac.md)

---

### 2. Instalar o Driver ODBC para SQL Server

> É necessário ter o driver ODBC instalado no sistema.

- **Windows:**  
  [Download do ODBC Driver](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

- **Linux/Mac:**  
  Consulte o [guia oficial](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server) para instruções específicas.

---

### 3. Configurar as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

``` 
DB_SERVER=seu_servidor.database.windows.net  
DB_DATABASE=nome_do_banco  
DB_USERNAME=seu_usuario  
DB_PASSWORD=sua_senha  
DB_DRIVER=ODBC Driver 18 for SQL Server  
```

---

### 4. Garantir que as Tabelas Estão Criadas

Antes de rodar o script, **certifique-se de que todas as tabelas do banco já foram criadas**.

Consulte:

- Scripts SQL fornecidos pelo projeto, ou  
- A documentação de banco de dados:  
  [Documentação do Banco](database.md)

---

### 5. Testar a Conexão com o Banco

Execute o script de teste:

``` 
python teste_conexao.py  
```

---

### 6. Executar o Script Faker

Se a conexão estiver correta, execute:

``` 
python faker_data.py  
```

---

## ⚠️ Observações Importantes

- O script **valida a existência das tabelas** antes de iniciar.
- Dados são sempre os mesmos, pois o script usa **seeds fixas** (`Faker.seed(42)`, `random.seed(42)`).
- **Não há limpeza de dados anterior** — evite rodar múltiplas vezes se o banco já contiver registros.
- Se alguma tabela estiver faltando, a execução será interrompida com mensagem de erro.
- Para garantir que tudo está em ordem, **verifique a estrutura do banco de dados** antes de usar o Faker.

---


