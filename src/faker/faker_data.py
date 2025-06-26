from faker import Faker
from datetime import datetime, timedelta
import random
import pyodbc
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

fake = Faker('pt_BR')
Faker.seed(42)
random.seed(42)

server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
driver = os.getenv('DB_DRIVER')

print("Driver:", driver)

# Conexão ao Azure SQL
conn = pyodbc.connect(
    f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"
)
cursor = conn.cursor()
cursor.fast_executemany = True  # 🚀 Ativa envio rápido

conn.autocommit = False  # Controla commits manualmente

def tabela_existe(schema, tabela):
    cursor.execute("""
        SELECT 1 FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
    """, (schema, tabela))
    return cursor.fetchone() is not None

def checar_tabelas_obrigatorias(lista):
    faltando = []
    for schema, tabela in lista:
        if not tabela_existe(schema, tabela):
            faltando.append(f"{schema}.{tabela}")
    if faltando:
        print("❌ Faltando tabelas:", ", ".join(faltando))
        exit(1)
    print("✅ Todas tabelas existem.\n")

def insert_many(query, values, batch_size=5000):
    try:
        for i in range(0, len(values), batch_size):
            batch = values[i:i+batch_size]
            cursor.executemany(query, batch)
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        exit(1)

# Verifica dependências
checar_tabelas_obrigatorias([
    ('relacional', 'clientes'), ('relacional', 'vendedores'),
    ('relacional', 'categorias'), ('relacional', 'formas_pagamento'),
    ('relacional', 'produtos'), ('relacional', 'estoque'),
    ('relacional', 'enderecos_cliente'), ('relacional', 'pedidos'),
    ('relacional', 'itens_pedido'), ('relacional', 'pagamentos'),
    ('relacional', 'transportadoras'), ('relacional', 'entregas'),
    ('relacional', 'avaliacoes'),
])

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
    ('Cartão de Crédito',), ('Boleto Bancário',),
    ('Pix',), ('Transferência Bancária',),
    ('PayPal',), ('Débito',), ('Vale Presente',),
    ('Cheque',), ('Dinheiro',), ('Cartão de Débito',)
]

# Quantidades
n_clientes = 20000
n_vendedores = 1000
n_produtos = 30000
n_enderecos = 20000
n_pedidos = 25000
n_itens_pedido = 40000
n_pagamentos = 25000
n_transportadoras = 100
n_entregas = 25000
n_avaliacoes = 20000

print("Gerando clientes")
def gen_email(name):
    return name.lower().replace(" ", ".") + str(random.randint(1, 9999)) + "@example.com"
def generate_clientes(n):
    clientes = []
    for _ in range(n):
        nome = fake.name()
        clientes.append((nome, gen_email(nome), fake.phone_number(), fake.date_time_between(start_date='-3y', end_date='now')))
    return clientes

clientes = generate_clientes(n_clientes)
insert_many(
    "INSERT INTO relacional.clientes (nome, email, telefone, data_cadastro) VALUES (?, ?, ?, ?)",
    clientes
)
cliente_ids = list(range(1, n_clientes + 1))

print("Gerando vendedores")
def generate_vendedores(n):
    vendedores = []
    for _ in range(n):
        nome = fake.name()
        vendedores.append((nome, gen_email(nome), fake.phone_number(), fake.date_time_between(start_date='-3y', end_date='now')))
    return vendedores

vendedores = generate_vendedores(n_vendedores)
insert_many(
    "INSERT INTO relacional.vendedores (nome, email, telefone, data_cadastro) VALUES (?, ?, ?, ?)",
    vendedores
)
vendedor_ids = list(range(1, n_vendedores + 1))

print("Inserindo categorias e formas de pagamento")
insert_many("INSERT INTO relacional.categorias (nome, descricao) VALUES (?, ?)", categorias_reais)
insert_many("INSERT INTO relacional.formas_pagamento (descricao) VALUES (?)", formas_pagamento_reais)
categoria_ids = list(range(1, len(categorias_reais) + 1))
forma_pagamento_ids = list(range(1, len(formas_pagamento_reais) + 1))

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
insert_many(
    "INSERT INTO relacional.produtos (vendedor_id, categoria_id, nome, descricao, preco, data_cadastro) VALUES (?, ?, ?, ?, ?, ?)",
    produtos
)
produto_ids = list(range(1, n_produtos + 1))

print("Gerando estoque")
estoque = [(pid, random.randint(0, 1000)) for pid in produto_ids]
insert_many("INSERT INTO relacional.estoque (produto_id, quantidade) VALUES (?, ?)", estoque)

print("Gerando endereços")
enderecos = []
for _ in range(n_enderecos):
    cid = random.choice(cliente_ids)
    enderecos.append((
        cid, fake.street_name(), str(fake.building_number()), "", fake.city_suffix(),
        fake.city(), fake.state_abbr(), fake.postcode()
    ))
insert_many(
    "INSERT INTO relacional.enderecos_cliente (cliente_id, logradouro, numero, complemento, bairro, cidade, estado, cep) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    enderecos
)
endereco_ids = list(range(1, n_enderecos + 1))
end_por_cliente = {}
for idx, e in enumerate(enderecos, start=1):
    end_por_cliente.setdefault(e[0], []).append(idx)

print("Gerando pedidos")
pedidos = []
for _ in range(n_pedidos):
    cid = random.choice(cliente_ids)
    ends = end_por_cliente.get(cid)
    if not ends: continue
    pedidos.append((cid, random.choice(ends), fake.date_time_between(start_date='-3y', end_date='now'),
                    random.choice(['pendente','enviado','entregue','cancelado']),
                    round(random.uniform(100,5000),2)))
insert_many(
    "INSERT INTO relacional.pedidos (cliente_id, endereco_entrega_id, data_pedido, status, total) VALUES (?, ?, ?, ?, ?)",
    pedidos
)
pedido_ids = list(range(1, len(pedidos) + 1))

print("Gerando itens de pedido")
itens = [(random.choice(pedido_ids), random.choice(produto_ids), random.randint(1,5),
          round(random.uniform(10,1000),2)) for _ in range(n_itens_pedido)]
insert_many("INSERT INTO relacional.itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)", itens)

print("Gerando pagamentos")
pagamentos = [(random.choice(pedido_ids), random.choice(forma_pagamento_ids),
               round(random.uniform(100,5000),2),
               fake.date_time_between(start_date='-3y', end_date='now'),
               random.choice(['pago','pendente','falha']))
              for _ in range(n_pagamentos)]
insert_many("INSERT INTO relacional.pagamentos (pedido_id, forma_pagamento_id, valor_pago, data_pagamento, status) VALUES (?, ?, ?, ?, ?)", pagamentos)

print("Gerando transportadoras")
transportadoras = [(fake.company(), fake.phone_number(), fake.email()) for _ in range(n_transportadoras)]
insert_many("INSERT INTO relacional.transportadoras (nome, telefone, email) VALUES (?, ?, ?)", transportadoras)
transportadora_ids = list(range(1, n_transportadoras + 1))

print("Gerando entregas")
entregas = []
for _ in range(n_entregas):
    pid = random.choice(pedido_ids)
    data_envio = fake.date_between(start_date='-30d', end_date='today')
    entregas.append((
        pid, random.choice(transportadora_ids),
        data_envio,
        fake.date_between(start_date=data_envio, end_date='+10d'),
        random.choice(['Pendente','Enviado','Entregue'])
    ))
insert_many("INSERT INTO relacional.entregas (pedido_id, transportadora_id, data_envio, data_entrega, status) VALUES (?, ?, ?, ?, ?)", entregas)

print("Gerando avaliações")
avaliacoes = [(random.choice(cliente_ids), random.choice(produto_ids),
               random.randint(1,5), fake.sentence(nb_words=10),
               fake.date_time_between(start_date='-3y', end_date='now'))
              for _ in range(n_avaliacoes)]
insert_many("INSERT INTO relacional.avaliacoes (cliente_id, produto_id, nota, comentario, data_avaliacao) VALUES (?, ?, ?, ?, ?)", avaliacoes)

print("✅ Inserção concluída com sucesso!")

cursor.close()
conn.close()
