"""Esta é uma API contruida para gerenciar (CRUD) com Flask e SQLite.
A aplicação conta com funcionalidades para adicionar, atualizar, deletar e listar livros 
atravez de uma interface gafica gerada com HTML, CSS e JavaScript.
 
"""
import sqlite3
from bd_livros import conectar_bd, criar_tabela
from flask import Flask, request, jsonify, render_template



app = Flask(__name__)

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

criar_tabela()

@app.route('/')# retorna a pagina html
def index():
    return render_template('index.html')

# Retorna todos os livros
@app.route('/bibliotecas', methods=['GET'])
def get_livros():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros')
    livros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(livros), 200

# Retorna livro por ID
@app.route('/bibliotecas/<int:id>', methods=['GET'])
def get_livro_por_id(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row)), 200
    return jsonify({'message': 'Livro não encontrado!'}), 404

# Adiciona um novo livro
@app.route('/bibliotecas', methods=['POST'])
def adicionar_livro():
    dados = request.get_json()
    titulo = dados.get('titulo')
    autor = dados.get('autor')
    print(dados, titulo, autor)
    if not titulo or not autor:
        return jsonify({'message': 'Campos obrigatórios: titulo e autor'}), 400

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livros (titulo, autor) VALUES (?, ?)', (titulo, autor))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': novo_id, 'titulo': titulo, 'autor': autor}), 201

# Atualiza um livro
@app.route('/bibliotecas/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    dados = request.get_json()
    titulo = dados.get('titulo')
    autor = dados.get('autor')

    if not titulo or not autor:
        return jsonify({'message': 'Campos obrigatórios: titulo e autor'}), 400

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('UPDATE livros SET titulo = ?, autor = ? WHERE id = ?', (titulo, autor, id))
    conn.commit()
    atualizado = cursor.rowcount
    conn.close()

    if atualizado:
        return jsonify({'id': id, 'titulo': titulo, 'autor': autor}), 200
    return jsonify({'message': 'Livro não encontrado!'}), 404

# Deleta um livro
@app.route('/bibliotecas/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livros WHERE id = ?', (id,))
    conn.commit()
    deletado = cursor.rowcount
    conn.close()

    if deletado:
        return jsonify({'message': f'Livro ID: {id} excluído com sucesso!'}), 200
    return jsonify({'message': 'Livro não encontrado!'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
