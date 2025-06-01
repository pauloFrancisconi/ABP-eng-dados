
ALTER TABLE relacional.avaliacoes NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.entregas NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.pagamentos NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.itens_pedido NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.pedidos NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.enderecos_cliente NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.estoque NOCHECK CONSTRAINT ALL;

ALTER TABLE relacional.transportadoras NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.produtos NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.formas_pagamento NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.categorias NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.vendedores NOCHECK CONSTRAINT ALL;
ALTER TABLE relacional.clientes NOCHECK CONSTRAINT ALL;


DELETE FROM relacional.avaliacoes;
DBCC CHECKIDENT ('relacional.avaliacoes', RESEED, 0);

DELETE FROM relacional.entregas;
DBCC CHECKIDENT ('relacional.entregas', RESEED, 0);

DELETE FROM relacional.pagamentos;
DBCC CHECKIDENT ('relacional.pagamentos', RESEED, 0);

DELETE FROM relacional.itens_pedido;
DBCC CHECKIDENT ('relacional.itens_pedido', RESEED, 0);

DELETE FROM relacional.pedidos;
DBCC CHECKIDENT ('relacional.pedidos', RESEED, 0);

DELETE FROM relacional.enderecos_cliente;
DBCC CHECKIDENT ('relacional.enderecos_cliente', RESEED, 0);

DELETE FROM relacional.estoque;
DBCC CHECKIDENT ('relacional.estoque', RESEED, 0);


DELETE FROM relacional.transportadoras;
DBCC CHECKIDENT ('relacional.transportadoras', RESEED, 0);

DELETE FROM relacional.produtos;
DBCC CHECKIDENT ('relacional.produtos', RESEED, 0);

DELETE FROM relacional.formas_pagamento;
DBCC CHECKIDENT ('relacional.formas_pagamento', RESEED, 0);

DELETE FROM relacional.categorias;
DBCC CHECKIDENT ('relacional.categorias', RESEED, 0);

DELETE FROM relacional.vendedores;
DBCC CHECKIDENT ('relacional.vendedores', RESEED, 0);

DELETE FROM relacional.clientes;
DBCC CHECKIDENT ('relacional.clientes', RESEED, 0);


ALTER TABLE relacional.avaliacoes WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.entregas WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.pagamentos WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.itens_pedido WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.pedidos WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.enderecos_cliente WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.estoque WITH CHECK CHECK CONSTRAINT ALL;

ALTER TABLE relacional.transportadoras WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.produtos WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.formas_pagamento WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.categorias WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.vendedores WITH CHECK CHECK CONSTRAINT ALL;
ALTER TABLE relacional.clientes WITH CHECK CHECK CONSTRAINT ALL;
