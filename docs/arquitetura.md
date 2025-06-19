# Arquitetura do Projeto de Engenharia de Dados

## Visão Geral

Este projeto adota uma arquitetura moderna baseada em serviços gerenciados da Azure para ingestão, armazenamento, processamento, orquestração e visualização de dados. Ele segue o padrão de **Data Lakehouse**, utilizando camadas de dados (Landing, Bronze, Silver, Gold), garantindo escalabilidade, reprodutibilidade e separação de responsabilidades.

---

## Componentes Principais

### Geração e Ingestão

- **Python com Faker**  
  Responsável por simular dados transacionais e inseri-los diretamente no banco de dados relacional.

- **Azure SQL Database**  
  Serve como fonte de dados estruturados transacionais.

- **Azure Data Factory (ADF)**  
  - Copia os dados do Azure SQL Database para o Data Lake (camada *Landing*).
  - Dispara notebooks do Azure Databricks para transformação.

---

### Armazenamento

- **Azure Data Lake Storage Gen2 (ADLS)**  
  Armazena os dados em camadas distintas:
  - `Landing`: Dados crus recém-ingestados.
  - `Bronze`: Dados brutos organizados.
  - `Silver`: Dados limpos e tratados.
  - `Gold`: Dados agregados e otimizados para relatórios.

---

### Processamento e Transformação

- **Azure Databricks (Notebooks)**  
  Realiza o processamento e transformação dos dados entre as camadas Bronze → Silver → Gold.  
  Aplica regras de negócio, limpeza de dados, junções e agregações.

---

### Orquestração

- **Azure Data Factory (ADF)**  
  Coordena a execução de atividades como:
  - Ingestão dos dados
  - Processamento nos notebooks do Databricks

---

### Visualização

- **Power BI**  
  Conecta-se diretamente à camada Gold do ADLS.  
  Gera dashboards e relatórios com dados prontos para consumo analítico.

---

### Provisionamento

- **Terraform (Infraestrutura como Código)**  
  Automatiza a criação dos serviços Azure envolvidos:
  - Azure SQL Database  
  - Azure Data Factory  
  - Azure Data Lake Storage  
  - Azure Databricks   
  Garante versionamento, reprodutibilidade e padronização da infraestrutura.

---

## Diagrama da Arquitetura

![Diagrama da Arquitetura](/assets/diagrama-arquitetura.png)

---

## Fluxo de Dados

1. **Python + Faker → Azure SQL Database**  
   (Geração e simulação de dados)

2. **Azure SQL → ADF → ADLS (Landing/Bronze)**  
   (Ingestão dos dados brutos)

3. **ADF → Databricks (Bronze → Silver → Gold)**  
   (Transformações com regras de negócio)

4. **Power BI → ADLS (Gold)**  
   (Visualização dos dados processados)

---

## Benefícios da Arquitetura

- Escalável e modular
- Separação clara entre ingestão, processamento e visualização
- Automação completa com Terraform
- Utilização de ferramentas modernas e gerenciadas da Azure
