# Utilizando o Azure Databricks

Este guia descreve os passos necessários para acessar o workspace do Azure Databricks criado via Terraform, importar notebooks, configurar um cluster de computação e gerar um token de acesso.

---

## 1. Acessando o Workspace e Importando Notebooks

Após a execução do Terraform, o recurso **Azure Databricks** estará provisionado. Caso você não tenha feito o provisionamento dos resursos, acesse a [documentação do Terraform do projeto](iac.md). Para acessar o workspace:

1. Acesse o portal do Azure.
2. Pesquise por **"Azure Databricks"** e clique no recurso criado.
3. Clique em **"Launch Workspace"** para abrir a interface do Databricks.
4. No menu lateral esquerdo, vá até a seção **"Workspace"**.
5. Clique com o botão direito em seu usuário ou pasta principal e selecione **"Create > Folder"**.
   - Nomeie a pasta como `notebooks`.

6. Dentro da pasta `notebooks`, clique em **"Import"**.
   - Selecione os arquivos localizados na pasta do projeto:  
     `src/notebooks/`
   - Importe todos os arquivos `.ipynb` necessários para o seu trabalho.

---

## 2. Criando um Cluster de Computação

Para executar os notebooks, será necessário configurar um cluster Databricks.

1. No menu esquerdo, clique em **"Compute"**.
2. Clique no botão **"Create Cluster"**.
3. Preencha as informações conforme abaixo:

   - **Cluster name**: Nome de sua escolha (ex: `cluster-projeto`)
   - **Databricks Runtime Version**: `10.4 LTS (Scala 2.12, Spark 3.2.1)`
   - **Node type**: `Standard_D4s_v3`
   - **Autopilot Options**: Pode deixar as opções padrão ou configurar conforme necessidade.

4. Clique em **"Create Cluster"**.

![Exemplo de criação de cluster no Databricks](/assets/foto-compute.png)


---

## 3. Gerando um Token de Acesso (para o Azure Data Factory)

Para integração com outros serviços, como o Azure Data Factory, é necessário um token de acesso do Databricks.

1. No canto superior direito da interface do Databricks, clique no ícone de **usuário** e depois em **"User Settings"**.
2. Vá até a aba **"Developer"** ou **"Access Tokens"**.
3. Clique em **"Generate New Token"**.
4. Defina o tempo de expiração desejado.
5. Clique em **"Generate"** e **copie o token gerado**.

> ⚠️ **Atenção**: o token **não poderá ser recuperado novamente**, portanto salve-o com segurança.
> Você irá utilizá-lo posteriormente na configuração do Azure Data Factory.

---

## Recursos Relacionados

- Pasta com notebooks: `src/notebooks/`
- Imagem de referência do cluster: `assets/foto-compute.png`

---

## Requisitos

- O Azure Databricks deve estar provisionado via Terraform.
- Você precisa de permissões para acessar o recurso e criar notebooks/cluster.
