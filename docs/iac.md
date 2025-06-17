# Infraestrutura como Código (IaC) com Terraform

Este projeto utiliza Terraform para provisionar a infraestrutura na Azure, adotando uma abordagem modular. Cada módulo está isolado em sua própria pasta e deve ser aplicado separadamente.

---

## Estrutura dos Módulos

Cada pasta representa um módulo de infraestrutura:

- `resource_group/` — Grupo de recursos no Azure  
- `sql_server/` — Azure SQL Database
- `adls/` — Azure Data Lake Storage  
- `az_databricks/` — Azure Databricks  
- `adf/` — Azure Data Factory  

---

## Como executar

### Pré-requisitos

- Azure CLI  
- Terraform  
- Conta Azure com permissões adequadas  

---

### Passos para provisionar cada módulo

Para provisionar os recursos, você deve entrar em cada pasta de módulo e executar os comandos do Terraform individualmente. Por exemplo, para o módulo `resource_group`:

```
cd resource_group  
terraform init  
terraform plan -var-file="../terraform.tfvars"  
terraform apply -var-file="../terraform.tfvars"  
```

Repita esses passos para cada módulo (`sql_server`, `adls`, `az_databricks`, `adf`), sempre navegando para a respectiva pasta antes de executar os comandos.

---

### Comandos gerais para cada módulo

```
terraform init  
terraform plan -var-file="../terraform.tfvars"  
terraform apply -var-file="../terraform.tfvars"  
```

---

## Exemplos do arquivo terraform.tfvars

Aqui estão exemplos fictícios de valores para cada módulo no arquivo `terraform.tfvars`:

### resource_group

```
resource_group_name = "rg-exemplo-projeto"  
location            = "eastus"  
```

---

### sql_server

```
subscription_id     = "12345678-1234-1234-1234-123456789abc"  
resource_group_name = "rg-exemplo-projeto"  
usuario_admin       = "admin_exemplo"  
password            = "SenhaForte!2025"  
```

---

### az_databricks

```
azure_client_id     = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"  
azure_client_secret = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVv"  
azure_tenant_id     = "ffffffff-1111-2222-3333-444444444444"  
workspace_name      = "ws-exemplo-databricks"  
subscription_id     = "12345678-1234-1234-1234-123456789abc"  
resource_group_name = "rg-exemplo-projeto"  
```

---

### adls

```
subscription_id     = "12345678-1234-1234-1234-123456789abc"  
resource_group_name = "rg-exemplo-projeto"  
```

---

### adf

```
resource_group_name = "rg-exemplo-projeto"  
data_factory_name   = "adf-exemplo-projeto"  
```

---

## Autenticação no Azure

Antes de iniciar o provisionamento, é necessário autenticar na sua conta Azure usando o Azure CLI:

```
az login  
```

Esse comando abrirá uma janela no navegador para login. Após logado, você poderá executar comandos `az` para consultar os recursos e configurar variáveis no `terraform.tfvars`.

---

## Como obter os valores para o terraform.tfvars

Use os comandos abaixo para descobrir os valores usados nas variáveis dos módulos:

### subscription_id

```
az account show --query id -o tsv  
```

### resource_group_name

```
az group list --query "[].name" -o tsv  
```
recomendado utilizar o mesmo grupo de recursos para todos os serviços provisionados.

### location

```
az account list-locations --query "[].{Region:name}" -o table  
```

### azure_client_id, azure_client_secret e azure_tenant_id

Para criar um novo Service Principal:

```
az ad sp create-for-rbac --name "sp-nome-exemplo" --role Contributor --scopes /subscriptions/<subscription_id>  
```

O retorno incluirá:

- `appId` → `azure_client_id`  
- `password` → `azure_client_secret`  
- `tenant` → `azure_tenant_id`  

⚠️ **Importante**: guarde esses dados com segurança e **nunca versiona** esse arquivo no Git (o projeto ja possui um .gitigore com esse arquivo em cada pasta).


---

## Considerações finais

- O arquivo `terraform.tfvars` na raiz deve conter as variáveis de configuração utilizadas por todos os módulos.  
- Para destruir recursos, entre em cada módulo e rode:

```
terraform destroy -var-file="../terraform.tfvars"  
```


