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


#configurações padão do postgres
db_url = os.environ.get('DATABASE_URL') #aqui carregamos a variável de ambiente DATABASE_URL com a URL e senha do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Livro(db.Model): #modelo do banco de dados
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()

#rota para carregar a pagina inicial
@app.route('/')
def index():
    return('API de Biblioteca com Flask e PostgreSQL. Acesse /bibliotecas para ver os livros.')

#rotas para operações no banco
@app.route('/bibliotecas', methods=['GET'])
def get_livros():
    livros = Livro.query.all()
    return jsonify([{'id': l.id, 'titulo': l.titulo, 'autor': l.autor} for l in livros]), 200

@app.route('/bibliotecas/<int:id>', methods=['GET'])
def get_livro_por_id(id):
    livro = Livro.query.get(id)
    if livro:
        return jsonify({'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor}), 200
    return jsonify({'message': 'Livro não encontrado!'}), 404

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

@app.route('/bibliotecas/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    livro = Livro.query.get(id)
    if livro:
        db.session.delete(livro)
        db.session.commit()
        return jsonify({'message': f'Livro ID: {id} excluído com sucesso!'}), 200
    return jsonify({'message': 'Livro não encontrado!'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))#porta padrão para o app
    app.run(host='0.0.0.0', port=port)
    
