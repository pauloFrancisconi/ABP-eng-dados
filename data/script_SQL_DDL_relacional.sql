CREATE DATABASE ecommerce;

USE ecommerce;

CREATE SCHEMA relacional;


CREATE TABLE relacional.clientes (
  id int PRIMARY KEY IDENTITY(1,1),
  nome varchar(100),
  email varchar(150) UNIQUE,
  telefone varchar(20),
  data_cadastro datetime
);
GO

CREATE TABLE relacional.vendedores (
  id int PRIMARY KEY IDENTITY(1,1),
  nome varchar(100),
  email varchar(150) UNIQUE,
  telefone varchar(20),
  data_cadastro datetime
);
GO

CREATE TABLE relacional.enderecos_cliente (
  id int PRIMARY KEY IDENTITY(1,1),
  cliente_id int,
  logradouro varchar(150),
  numero varchar(10),
  complemento varchar(50),
  bairro varchar(50),
  cidade varchar(50),
  estado varchar(2),
  cep varchar(10)
);
GO

CREATE TABLE relacional.categorias (
  id int PRIMARY KEY IDENTITY(1,1),
  nome varchar(50),
  descricao varchar(150)
);
GO

CREATE TABLE relacional.produtos (
  id int PRIMARY KEY IDENTITY(1,1),
  vendedor_id int,
  categoria_id int,
  nome varchar(100),
  descricao varchar(max),
  preco decimal(10,2),
  data_cadastro datetime
);
GO

CREATE TABLE relacional.estoque (
  id int PRIMARY KEY IDENTITY(1,1),
  produto_id int,
  quantidade int
);
GO

CREATE TABLE relacional.pedidos (
  id int PRIMARY KEY IDENTITY(1,1),
  cliente_id int,
  endereco_entrega_id int,
  data_pedido datetime,
  status varchar(50),
  total decimal(10,2)
);
GO

CREATE TABLE relacional.itens_pedido (
  id int PRIMARY KEY IDENTITY(1,1),
  pedido_id int,
  produto_id int,
  quantidade int,
  preco_unitario decimal(10,2)
);
GO

CREATE TABLE relacional.formas_pagamento (
  id int PRIMARY KEY IDENTITY(1,1),
  descricao varchar(50)
);
GO

CREATE TABLE relacional.pagamentos (
  id int PRIMARY KEY IDENTITY(1,1),
  pedido_id int,
  forma_pagamento_id int,
  valor_pago decimal(10,2),
  data_pagamento datetime,
  status varchar(50)
);
GO

CREATE TABLE relacional.transportadoras (
  id int PRIMARY KEY IDENTITY(1,1),
  nome varchar(100),
  telefone varchar(20),
  email varchar(150)
);
GO

CREATE TABLE relacional.entregas (
  id int PRIMARY KEY IDENTITY(1,1),
  pedido_id int,
  transportadora_id int,
  data_envio datetime,
  data_entrega datetime,
  status varchar(50)
);
GO

CREATE TABLE relacional.avaliacoes (
  id int PRIMARY KEY IDENTITY(1,1),
  cliente_id int,
  produto_id int,
  nota int,
  comentario varchar(max),
  data_avaliacao datetime
);
GO

-- Foreign Keys

ALTER TABLE relacional.enderecos_cliente 
ADD CONSTRAINT FK_EnderecosCliente_Cliente FOREIGN KEY (cliente_id) REFERENCES relacional.clientes (id);
GO

ALTER TABLE relacional.produtos 
ADD CONSTRAINT FK_Produtos_Vendedor FOREIGN KEY (vendedor_id) REFERENCES relacional.vendedores (id);
GO

ALTER TABLE relacional.produtos 
ADD CONSTRAINT FK_Produtos_Categoria FOREIGN KEY (categoria_id) REFERENCES relacional.categorias (id);
GO

ALTER TABLE relacional.estoque 
ADD CONSTRAINT FK_Estoque_Produto FOREIGN KEY (produto_id) REFERENCES relacional.produtos (id);
GO

ALTER TABLE relacional.pedidos 
ADD CONSTRAINT FK_Pedidos_Cliente FOREIGN KEY (cliente_id) REFERENCES relacional.clientes (id);
GO

ALTER TABLE relacional.pedidos 
ADD CONSTRAINT FK_Pedidos_EnderecoEntrega FOREIGN KEY (endereco_entrega_id) REFERENCES relacional.enderecos_cliente (id);
GO

ALTER TABLE relacional.itens_pedido 
ADD CONSTRAINT FK_ItensPedido_Pedido FOREIGN KEY (pedido_id) REFERENCES relacional.pedidos (id);
GO

ALTER TABLE relacional.itens_pedido 
ADD CONSTRAINT FK_ItensPedido_Produto FOREIGN KEY (produto_id) REFERENCES relacional.produtos (id);
GO

ALTER TABLE relacional.pagamentos 
ADD CONSTRAINT FK_Pagamentos_Pedido FOREIGN KEY (pedido_id) REFERENCES relacional.pedidos (id);
GO

ALTER TABLE relacional.pagamentos 
ADD CONSTRAINT FK_Pagamentos_FormaPagamento FOREIGN KEY (forma_pagamento_id) REFERENCES relacional.formas_pagamento (id);
GO

ALTER TABLE relacional.entregas 
ADD CONSTRAINT FK_Entregas_Pedido FOREIGN KEY (pedido_id) REFERENCES relacional.pedidos (id);
GO

ALTER TABLE relacional.entregas 
ADD CONSTRAINT FK_Entregas_Transportadora FOREIGN KEY (transportadora_id) REFERENCES relacional.transportadoras (id);
GO

ALTER TABLE relacional.avaliacoes 
ADD CONSTRAINT FK_Avaliacoes_Cliente FOREIGN KEY (cliente_id) REFERENCES relacional.clientes (id);
GO

ALTER TABLE relacional.avaliacoes 
ADD CONSTRAINT FK_Avaliacoes_Produto FOREIGN KEY (produto_id) REFERENCES relacional.produtos (id);
GO