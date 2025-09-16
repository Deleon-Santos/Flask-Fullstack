"""
Esta é uma API construída para gerenciar (CRUD) com Flask e PostgreSQL.
A aplicação conta com funcionalidades para adicionar, atualizar, deletar e listar livros 
através de uma interface gráfica gerada com HTML, CSS e JavaScript.
"""

import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "http://127.0.0.1:5500",     
    "http://localhost:3000",     
    "https://deleon-santos.github.io"  
]}})

# Configuração do banco de dados PostgreSQL via variável de ambiente
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco com SQLAlchemy
db = SQLAlchemy(app)

# Modelo do banco
class Livro(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200), nullable=False)

# Cria as tabelas no banco (executa uma vez ao iniciar)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify({"message": "API Flask rodando com sucesso!"})

# Retorna todos os livros
@app.route('/bibliotecas', methods=['GET'])
def get_livros():
    livros = Livro.query.all()
    return jsonify([{'id': l.id, 'titulo': l.titulo, 'autor': l.autor} for l in livros]), 200

# Retorna livro por ID
@app.route('/bibliotecas/<int:id>', methods=['GET'])
def get_livro_por_id(id):
    livro = Livro.query.get(id)
    if livro:
        return jsonify({'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor}), 200
    return jsonify({'message': 'Livro não encontrado!'}), 404

# Adiciona um novo livro
@app.route('/bibliotecas', methods=['POST'])
def adicionar_livro():
    dados = request.get_json()
    titulo = dados.get('titulo')
    autor = dados.get('autor')

    if not titulo or not autor:
        return jsonify({'message': 'Campos obrigatórios: titulo e autor'}), 400

    novo_livro = Livro(titulo=titulo, autor=autor)
    db.session.add(novo_livro)
    db.session.commit()

    return jsonify({'id': novo_livro.id, 'titulo': novo_livro.titulo, 'autor': novo_livro.autor}), 201

# Atualiza um livro
@app.route('/bibliotecas/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    dados = request.get_json()
    titulo = dados.get('titulo')
    autor = dados.get('autor')

    if not titulo or not autor:
        return jsonify({'message': 'Campos obrigatórios: titulo e autor'}), 400

    livro = Livro.query.get(id)
    if livro:
        livro.titulo = titulo
        livro.autor = autor
        db.session.commit()
        return jsonify({'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor}), 200
    return jsonify({'message': 'Livro não encontrado!'}), 404

# Deleta um livro
@app.route('/bibliotecas/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    livro = Livro.query.get(id)
    if livro:
        db.session.delete(livro)
        db.session.commit()
        return jsonify({'message': f'Livro ID: {id} excluído com sucesso!'}), 200
    return jsonify({'message': 'Livro não encontrado!'}), 404

if __name__ == '__main__':
    app.run(debug=True)
