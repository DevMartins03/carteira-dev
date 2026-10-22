import os
import psycopg2
from dotenv import load_dotenv

# Carrega a senha guardada no arquivo secreto .env
load_dotenv()

# ==========================================================
# 1. CONEXÃO SEGURA COM O POSTGRESQL
# ==========================================================
def conectar():
    return psycopg2.connect(
        host="localhost",
        database="carteira_db",
        user="postgres",
        password=os.getenv("SENHA_BANCO"),  # Busca a senha do arquivo .env!
        port="5432"
    )

# ==========================================================
# 2. GARANTIR QUE A TABELA EXISTE
# ==========================================================
def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id SERIAL PRIMARY KEY,
            descricao VARCHAR(100) NOT NULL,
            valor NUMERIC(10, 2) NOT NULL,
            data_registro DATE DEFAULT CURRENT_DATE
        );
    """)
    conexao.commit()
    cursor.close()
    conexao.close()

# ==========================================================
# 3. OPERAÇÕES DO BANCO (CRUD)
# ==========================================================

# [1] ADICIONAR (INSERT)
def adicionar():
    descricao = input("\nDigite a descrição (ex: Corrida, Almoço, Combustível): ")
    valor_texto = input("Digite o valor (use - para gastos, ex: -40.00 ou 150.00): ").replace(",", ".")
    valor = float(valor_texto)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO movimentacoes (descricao, valor) VALUES (%s, %s);",
        (descricao, valor)
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    print("✅ Registro salvo com sucesso no PostgreSQL!")

# [2] LISTAR E CALCULAR SALDO (SELECT)
def listar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, descricao, valor, data_registro FROM movimentacoes ORDER BY id ASC;")
    registros = cursor.fetchall()

    print("\n================ EXTRATO DA CARTEIRA ================")
    saldo = 0
    for linha in registros:
        id_item, descricao, valor, data = linha[0], linha[1], float(linha[2]), linha[3]
        saldo += valor
        print(f"ID [{id_item}] | {data} | {descricao} | R$ {valor:.2f}")
    print("-----------------------------------------------------")
    print(f"💰 SALDO TOTAL: R$ {saldo:.2f}")
    print("=====================================================")

    cursor.close()
    conexao.close()

# [3] ATUALIZAR UM REGISTRO (UPDATE)
def atualizar():
    listar()
    id_item = input("\nDigite o número do ID que você quer corrigir: ")
    nova_descricao = input("Digite a nova descrição: ")
    novo_valor = float(input("Digite o novo valor: ").replace(",", "."))

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE movimentacoes SET descricao = %s, valor = %s WHERE id = %s;",
        (nova_descricao, novo_valor, id_item)
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    print("✏️ Registro atualizado com sucesso!")

# [4] APAGAR UM REGISTRO (DELETE)
def apagar():
    listar()
    id_item = input("\nDigite o número do ID que você quer APAGAR: ")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM movimentacoes WHERE id = %s;", (id_item,))
    conexao.commit()
    cursor.close()
    conexao.close()
    print("🗑️ Registro apagado do banco de dados!")

# ==========================================================
# 4. MENU INTERATIVO NO TERMINAL
# ==========================================================
def menu():
    criar_tabela()
    while True:
        print("\n=== SISTEMA CARTEIRA-DEV (NÍVEL 2) ===")
        print("1 - Adicionar ganho ou gasto")
        print("2 - Ver extrato e saldo")
        print("3 - Corrigir um registro")
        print("4 - Apagar um registro")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            atualizar()
        elif opcao == "4":
            apagar()
        elif opcao == "0":
            print("Encerrando o sistema. Até mais, DevMartins!")
            break
        else:
            print("⚠️ Opção inválida! Digite de 0 a 4.")

if __name__ == "__main__":
    menu()