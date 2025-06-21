import sqlite3
# Função para conectar ao banco de dados

def conectar_bd():
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

# Criação da tabela (executa apenas 1 vez)
def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()