# Documentação do Banco de Dados - Projeto E-commerce

## Visão Geral

Este projeto utiliza o **Azure SQL Server** para gerenciar os dados de um sistema de e-commerce. O banco de dados foi estruturado com base em um **modelo relacional**, contendo entidades que representam clientes, pedidos, produtos, pagamentos, entregas, entre outros.

> O passo a passo completo para criação da instância no Azure está descrito [aqui](iac.md).

---

## Modelo Físico

O diagrama abaixo representa o modelo relacional físico utilizado no banco de dados, com as tabelas, colunas e relacionamentos:

![Modelo Físico](/assets/Diagrama-Modelo-Relacional-Varejo-ENG-DADOS.png)

---

## Modelo Dimensional

O modelo dimensional é utilizado para fins analíticos e geração de relatórios, organizando os dados em fatos e dimensões.

![Modelo Dimensional](/assets/Diagrama-modelo-dimensional.png)

---

## Descrição das Tabelas

### `clientes`
Armazena os dados dos clientes cadastrados.

| Coluna         | Tipo         | Descrição                            |
|----------------|--------------|----------------------------------------|
| `id`           | int (PK)     | Identificador único                   |
| `nome`         | varchar(100) | Nome completo                         |
| `email`        | varchar(150) | E-mail único                          |
| `telefone`     | varchar(20)  | Telefone de contato                   |
| `data_cadastro`| datetime     | Data de cadastro                      |

---

### `vendedores`
Informações dos vendedores da plataforma.

| Coluna         | Tipo         | Descrição                            |
|----------------|--------------|----------------------------------------|
| `id`           | int (PK)     | Identificador único                   |
| `nome`         | varchar(100) | Nome do vendedor                      |
| `email`        | varchar(150) | E-mail único                          |
| `telefone`     | varchar(20)  | Telefone de contato                   |
| `data_cadastro`| datetime     | Data de cadastro                      |

---

### `enderecos_cliente`
Lista de endereços vinculados a clientes.

| Coluna         | Tipo         | Descrição                            |
|----------------|--------------|----------------------------------------|
| `id`           | int (PK)     | Identificador do endereço             |
| `cliente_id`   | int (FK)     | Cliente associado                     |
| `logradouro`   | varchar(150) | Nome da rua                           |
| `numero`       | varchar(10)  | Número da residência                  |
| `complemento`  | varchar(50)  | Complemento do endereço               |
| `bairro`       | varchar(50)  | Bairro                                |
| `cidade`       | varchar(50)  | Cidade                                |
| `estado`       | varchar(2)   | UF                                    |
| `cep`          | varchar(10)  | CEP                                   |

---

### `categorias`
Categorias de produtos.

| Coluna       | Tipo         | Descrição                      |
|--------------|--------------|----------------------------------|
| `id`         | int (PK)     | Identificador                   |
| `nome`       | varchar(50)  | Nome da categoria               |
| `descricao`  | varchar(150) | Descrição                       |

---

### `produtos`
Produtos cadastrados no sistema.

| Coluna         | Tipo           | Descrição                            |
|----------------|----------------|----------------------------------------|
| `id`           | int (PK)       | Identificador                         |
| `vendedor_id`  | int (FK)       | Vendedor responsável                  |
| `categoria_id` | int (FK)       | Categoria do produto                  |
| `nome`         | varchar(100)   | Nome                                  |
| `descricao`    | varchar(MAX)   | Descrição detalhada                   |
| `preco`        | decimal(10,2)  | Preço                                 |
| `data_cadastro`| datetime       | Data de cadastro                      |

---

### `estoque`
Controle de quantidade em estoque.

| Coluna      | Tipo         | Descrição                            |
|-------------|--------------|----------------------------------------|
| `id`        | int (PK)     | Identificador                         |
| `produto_id`| int (FK)     | Produto relacionado                   |
| `quantidade`| int          | Quantidade disponível                 |

---

### `pedidos`
Pedidos realizados pelos clientes.

| Coluna               | Tipo           | Descrição                        |
|----------------------|----------------|------------------------------------|
| `id`                 | int (PK)       | Identificador do pedido           |
| `cliente_id`         | int (FK)       | Cliente que realizou o pedido     |
| `endereco_entrega_id`| int (FK)       | Endereço de entrega               |
| `data_pedido`        | datetime       | Data do pedido                    |
| `status`             | varchar(50)    | Status do pedido                  |
| `total`              | decimal(10,2)  | Valor total do pedido             |

---

### `itens_pedido`
Itens que compõem um pedido.

| Coluna         | Tipo           | Descrição                        |
|----------------|----------------|------------------------------------|
| `id`           | int (PK)       | Identificador                     |
| `pedido_id`    | int (FK)       | Pedido associado                  |
| `produto_id`   | int (FK)       | Produto adquirido                 |
| `quantidade`   | int            | Quantidade comprada               |
| `preco_unitario`| decimal(10,2) | Valor unitário na compra          |

---

### `formas_pagamento`
Formas aceitas para pagamento.

| Coluna     | Tipo         | Descrição                          |
|------------|--------------|--------------------------------------|
| `id`       | int (PK)     | Identificador                       |
| `descricao`| varchar(50)  | Descrição (Cartão, PIX, Boleto etc.)|

---

### `pagamentos`
Pagamentos efetuados nos pedidos.

| Coluna              | Tipo           | Descrição                        |
|---------------------|----------------|------------------------------------|
| `id`                | int (PK)       | Identificador do pagamento        |
| `pedido_id`         | int (FK)       | Pedido pago                       |
| `forma_pagamento_id`| int (FK)       | Forma de pagamento utilizada      |
| `valor_pago`        | decimal(10,2)  | Valor efetivamente pago           |
| `data_pagamento`    | datetime       | Data do pagamento                 |
| `status`            | varchar(50)    | Status (Aprovado, Recusado, etc.)|

---

### `transportadoras`
Empresas responsáveis pelas entregas.

| Coluna     | Tipo         | Descrição                  |
|------------|--------------|------------------------------|
| `id`       | int (PK)     | Identificador               |
| `nome`     | varchar(100) | Nome da transportadora      |
| `telefone` | varchar(20)  | Contato                     |
| `email`    | varchar(150) | E-mail                      |

---

### `entregas`
Informações sobre o envio dos pedidos.

| Coluna           | Tipo         | Descrição                        |
|------------------|--------------|------------------------------------|
| `id`             | int (PK)     | Identificador                     |
| `pedido_id`      | int (FK)     | Pedido entregue                   |
| `transportadora_id`| int (FK)   | Transportadora responsável        |
| `data_envio`     | datetime     | Data de envio                     |
| `data_entrega`   | datetime     | Data de entrega                   |
| `status`         | varchar(50)  | Status da entrega                 |

---

### `avaliacoes`
Avaliações feitas por clientes nos produtos.

| Coluna          | Tipo         | Descrição                        |
|-----------------|--------------|------------------------------------|
| `id`            | int (PK)     | Identificador                     |
| `cliente_id`    | int (FK)     | Cliente que avaliou               |
| `produto_id`    | int (FK)     | Produto avaliado                  |
| `nota`          | int          | Nota de avaliação (1 a 5, por ex.)|
| `comentario`    | varchar(MAX) | Comentário textual                |
| `data_avaliacao`| datetime     | Data da avaliação                 |

---



