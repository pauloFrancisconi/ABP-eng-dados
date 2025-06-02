from faker import Faker
from datetime import datetime, timedelta
import random
import pyodbc
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

fake = Faker('pt_BR')
Faker.seed(42)
random.seed(42)

server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
driver = os.getenv('DB_DRIVER')

conn = pyodbc.connect(
    f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"
)
cursor = conn.cursor()

def insert_many(query, values, batch_size=1000):
    for i in range(0, len(values), batch_size):
        batch = values[i:i+batch_size]
        cursor.executemany(query, batch)
        conn.commit()

categorias_reais = [
    ('Eletrônicos', 'Produtos eletrônicos e gadgets'),
    ('Moda', 'Roupas, calçados e acessórios'),
    ('Casa', 'Itens para casa e decoração'),
    ('Beleza', 'Produtos de beleza e cuidados pessoais'),
    ('Esporte', 'Equipamentos e roupas esportivas'),
    ('Brinquedos', 'Brinquedos e jogos infantis'),
    ('Livros', 'Livros e revistas'),
    ('Automotivo', 'Peças e acessórios automotivos'),
    ('Alimentos', 'Comidas e bebidas'),
    ('Saúde', 'Produtos de saúde e farmácia'),
    ('Informática', 'Computadores, periféricos e softwares'),
    ('Telefonia', 'Celulares e acessórios'),
    ('Móveis', 'Móveis para casa e escritório'),
    ('Jardinagem', 'Ferramentas e acessórios para jardim'),
    ('Papelaria', 'Material de escritório e escolar'),
    ('Pets', 'Produtos para animais de estimação'),
    ('Bebês', 'Produtos para bebês e crianças'),
    ('Ferramentas', 'Ferramentas manuais e elétricas'),
    ('Relógios', 'Relógios e acessórios'),
    ('Calçados', 'Sapatos, tênis e sandálias'),
    ('Joias', 'Joias e bijuterias'),
    ('Instrumentos Musicais', 'Instrumentos e acessórios musicais'),
    ('Arte', 'Materiais artísticos e decoração'),
    ('Construção', 'Materiais para construção e reforma'),
    ('Cinema', 'DVDs, Blu-rays e filmes'),
    ('Games', 'Jogos eletrônicos e consoles'),
    ('Viagem', 'Malas e acessórios para viagem'),
    ('Segurança', 'Produtos de segurança e vigilância'),
    ('Telefonia Fixa', 'Aparelhos e serviços de telefonia fixa'),
    ('Sustentabilidade', 'Produtos sustentáveis e ecológicos'),
    ('Fitness', 'Equipamentos para academia e fitness'),
    ('Culinária', 'Utensílios de cozinha e culinária'),
    ('Cama, Mesa e Banho', 'Produtos para cama, mesa e banho'),
    ('Celulares', 'Smartphones e acessórios'),
    ('Áudio', 'Equipamentos de áudio e som'),
    ('Informática Corporativa', 'Equipamentos para empresas'),
    ('Moda Infantil', 'Roupas infantis'),
    ('Moda Feminina', 'Roupas femininas'),
    ('Moda Masculina', 'Roupas masculinas'),
    ('Cosméticos', 'Produtos cosméticos'),
    ('Decoração', 'Itens de decoração'),
    ('Eletrônicos Automotivos', 'Equipamentos eletrônicos para veículos'),
    ('Eletrodomésticos', 'Aparelhos eletrodomésticos'),
    ('Ferramentas Elétricas', 'Ferramentas com motor elétrico'),
    ('Fotografia', 'Câmeras e acessórios fotográficos'),
    ('Iluminação', 'Lâmpadas e luminárias'),
    ('Infantil', 'Brinquedos e produtos infantis'),
    ('Instrumentos de Medição', 'Equipamentos para medição'),
    ('Lazer', 'Produtos para lazer e hobbies'),
    ('Material Escolar', 'Material para estudantes')
]

formas_pagamento_reais = [
    ('Cartão de Crédito',),
    ('Boleto Bancário',),
    ('Pix',),
    ('Transferência Bancária',),
    ('PayPal',),
    ('Débito',),
    ('Vale Presente',),
    ('Cheque',),
    ('Dinheiro',),
    ('Cartão de Débito',)
]

n_clientes = 10000
n_vendedores = 1000
n_categorias = len(categorias_reais)
n_produtos = 30000
n_estoque = 30000
n_enderecos = 10000
n_pedidos = 25000
n_itens_pedido = 40000
n_formas_pagamento = len(formas_pagamento_reais)
n_pagamentos = 25000
n_transportadoras = 100
n_entregas = 25000
n_avaliacoes = 20000

print("Gerando clientes")
def generate_clientes(n):
    return [
        (
            fake.name(),
            fake.unique.email(),
            fake.phone_number(),
            fake.date_time_between(start_date='-3y', end_date='now')
        )
        for _ in range(n)
    ]
clientes = generate_clientes(n_clientes)
insert_many("INSERT INTO relacional.clientes (nome, email, telefone, data_cadastro) VALUES (?, ?, ?, ?)", clientes)
cliente_ids = list(range(1, n_clientes + 1))

print("Gerando vendedores")
def generate_vendedores(n):
    return [
        (
            fake.name(),
            fake.unique.email(),
            fake.phone_number(),
            fake.date_time_between(start_date='-3y', end_date='now')
        )
        for _ in range(n)
    ]
vendedores = generate_vendedores(n_vendedores)
insert_many("INSERT INTO relacional.vendedores (nome, email, telefone, data_cadastro) VALUES (?, ?, ?, ?)", vendedores)
vendedor_ids = list(range(1, n_vendedores + 1))

print("Inserindo categorias fixas")
insert_many("INSERT INTO relacional.categorias (nome, descricao) VALUES (?, ?)", categorias_reais)
categoria_ids = list(range(1, n_categorias + 1))

print("Inserindo formas de pagamento fixas")
insert_many("INSERT INTO relacional.formas_pagamento (descricao) VALUES (?)", formas_pagamento_reais)
forma_pagamento_ids = list(range(1, n_formas_pagamento + 1))

print("Gerando produtos")
def generate_produtos(vendedores, categorias, n):
    return [
        (
            random.choice(vendedores),
            random.choice(categorias),
            fake.word().capitalize(),
            fake.sentence(nb_words=8),
            round(random.uniform(10, 1000), 2),
            fake.date_time_between(start_date='-3y', end_date='now')
        )
        for _ in range(n)
    ]
produtos = generate_produtos(vendedor_ids, categoria_ids, n_produtos)
insert_many("INSERT INTO relacional.produtos (vendedor_id, categoria_id, nome, descricao, preco, data_cadastro) VALUES (?, ?, ?, ?, ?, ?)", produtos)
produto_ids = list(range(1, n_produtos + 1))

print("Gerando estoque")
def generate_estoque(produtos):
    return [
        (pid, random.randint(0, 1000))
        for pid in produtos
    ]
estoque = generate_estoque(produto_ids)
insert_many("INSERT INTO relacional.estoque (produto_id, quantidade) VALUES (?, ?)", estoque)

print("Gerando endereços")
def generate_enderecos(clientes, n):
    enderecos = []
    for _ in range(n):
        cliente_id = random.choice(clientes)
        complemento = "" 
        enderecos.append((
            cliente_id,
            fake.street_name(),
            str(fake.building_number()),
            complemento,
            fake.city_suffix(),
            fake.city(),
            fake.state_abbr(),
            fake.postcode()
        ))
    return enderecos

enderecos = generate_enderecos(cliente_ids, n_enderecos)
insert_many("INSERT INTO relacional.enderecos_cliente (cliente_id, logradouro, numero, complemento, bairro, cidade, estado, cep) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", enderecos)
endereco_ids = list(range(1, n_enderecos + 1))

endereco_por_cliente = {}
for idx, endereco in enumerate(enderecos, start=1):
    cid = endereco[0]
    endereco_por_cliente.setdefault(cid, []).append(idx)

print("Gerando pedidos")
def generate_pedidos(clientes, endereco_por_cliente, n):
    pedidos = []
    for _ in range(n):
        cliente = random.choice(clientes)
        enderecos_cliente = endereco_por_cliente.get(cliente)
        if not enderecos_cliente:
            continue
        endereco_entrega = random.choice(enderecos_cliente)
        pedidos.append((
            cliente,
            endereco_entrega,
            fake.date_time_between(start_date='-3y', end_date='now'),
            random.choice(['pendente', 'enviado', 'entregue', 'cancelado']),
            round(random.uniform(100, 5000), 2)
        ))
    return pedidos
pedidos = generate_pedidos(cliente_ids, endereco_por_cliente, n_pedidos)
insert_many("INSERT INTO relacional.pedidos (cliente_id, endereco_entrega_id, data_pedido, status, total) VALUES (?, ?, ?, ?, ?)", pedidos)
pedido_ids = list(range(1, len(pedidos) + 1))

print("Gerando itens de pedidos")
def generate_itens_pedido(pedidos, produtos, n):
    itens = []
    for _ in range(n):
        pedido_id = random.choice(pedidos)
        produto_id = random.choice(produtos)
        quantidade = random.randint(1, 5)
        preco_unitario = round(random.uniform(10, 1000), 2)
        itens.append((pedido_id, produto_id, quantidade, preco_unitario))
    return itens
itens_pedido = generate_itens_pedido(pedido_ids, produto_ids, n_itens_pedido)
insert_many("INSERT INTO relacional.itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)", itens_pedido)

print("Gerando pagamentos")
def generate_pagamentos(pedidos, formas_pagamento, n):
    pagamentos = []
    for _ in range(n):
        pedido_id = random.choice(pedidos)
        forma_pagamento_id = random.choice(formas_pagamento)
        valor_pago = round(random.uniform(100, 5000), 2)
        data_pagamento = fake.date_time_between(start_date='-3y', end_date='now')
        status = random.choice(['pago', 'pendente', 'falha'])
        pagamentos.append((pedido_id, forma_pagamento_id, valor_pago, data_pagamento, status))
    return pagamentos
pagamentos = generate_pagamentos(pedido_ids, forma_pagamento_ids, n_pagamentos)
insert_many("INSERT INTO relacional.pagamentos (pedido_id, forma_pagamento_id, valor_pago, data_pagamento, status) VALUES (?, ?, ?, ?, ?)", pagamentos)

print("Gerando transportadoras")
def generate_transportadoras(n):
    return [
        (
            fake.company(),
            fake.phone_number(),
            fake.email()
        )
        for _ in range(n)
    ]
transportadoras = generate_transportadoras(n_transportadoras)
insert_many("INSERT INTO relacional.transportadoras (nome, telefone, email) VALUES (?, ?, ?)", transportadoras)
transportadora_ids = list(range(1, n_transportadoras + 1))

print("Gerando entregas")
def generate_entregas(pedido_ids, transportadora_ids, n):
    entregas = []
    for _ in range(n):
        pedido_id = random.choice(pedido_ids)
        transportadora_id = random.choice(transportadora_ids) 
        data_envio = fake.date_between(start_date='-30d', end_date='today')
        data_entrega = fake.date_between(start_date=data_envio, end_date='+10d')
        status = random.choice(['Pendente', 'Enviado', 'Entregue'])
        entregas.append((pedido_id, transportadora_id, data_envio, data_entrega, status))
    return entregas
entregas = generate_entregas(pedido_ids, transportadora_ids, n_entregas)
insert_many("INSERT INTO relacional.entregas (pedido_id, transportadora_id, data_envio, data_entrega, status) VALUES (?, ?, ?, ?, ?)", entregas)

print("Gerando avaliações")
def generate_avaliacoes(clientes, produtos, n):
    return [
        (
            random.choice(clientes),
            random.choice(produtos),
            random.randint(1, 5),
            fake.sentence(nb_words=10),
            fake.date_time_between(start_date='-3y', end_date='now')
        )
        for _ in range(n)
    ]
avaliacoes = generate_avaliacoes(cliente_ids, produto_ids, n_avaliacoes)
insert_many("INSERT INTO relacional.avaliacoes (cliente_id, produto_id, nota, comentario, data_avaliacao) VALUES (?, ?, ?, ?, ?)", avaliacoes)

print("Inserçao concluida")

cursor.close()
conn.close()
