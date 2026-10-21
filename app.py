import psycopg2

# 1. ABRINDO A CONEXÃO (A ligação telefônica com o banco)
conexao = psycopg2.connect(
    host="localhost",          # O banco está no seu próprio computador
    database="carteira_db",    # Nome do banco que criamos
    user="postgres",           # Usuário padrão do PostgreSQL
    password="SUA_SENHA_AQUI", # <-- Coloque a sua senha aqui na linha 8!
    port="5432"                # Porta padrão do PostgreSQL
)

print("Conexão com o PostgreSQL realizada com sucesso!")

# 2. CRIANDO O CURSOR (O mensageiro que leva os comandos SQL)
cursor = conexao.cursor()

# 2.5 CRIANDO A TABELA AUTOMATICAMENTE PELO PYTHON (A peça que faltava!)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id SERIAL PRIMARY KEY,
        descricao VARCHAR(100) NOT NULL,
        valor NUMERIC(10, 2) NOT NULL,
        data_registro DATE DEFAULT CURRENT_DATE
    );
""")

# 3. PREPARANDO O COMANDO SQL PARA INSERIR DADOS
comando_sql = """
    INSERT INTO movimentacoes (descricao, valor)
    VALUES (%s, %s);
"""
dados = ("Primeiro ganho registrado via Python", 120.50)

# 4. EXECUTANDO E SALVANDO DE VERDADE
cursor.execute(comando_sql, dados)
conexao.commit()  # O commit salva a criação da tabela e o registro!

print("Registro salvo no banco de dados com sucesso!")

# 5. LENDO OS DADOS DO BANCO PARA CONFIRMAR
cursor.execute("SELECT id, descricao, valor, data_registro FROM movimentacoes;")
registros = cursor.fetchall()

print("\n--- ITENS SALVOS NO POSTGRESQL ---")
for linha in registros:
    print(f"ID: {linha[0]} | Descrição: {linha[1]} | Valor: R$ {linha[2]} | Data: {linha[3]}")

# 6. FECHANDO A PORTA
cursor.close()
conexao.close()