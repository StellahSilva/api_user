#1. Objetivo - Api para consulta, criação, edição, exclusão de usuários

#2. URL base - localhost

#3. Endpoints -

#Todos usuários - localhost/usuarios (GET)
#Usuários específico - localhost/usuarios/id (GET)
#Modificar um usuário específico - localhost/usuarios/id (PUT)
#Criar novos usuários - localhost/usuarios (POST)
#Deletar usuário - localhost/usuarios/ (DELETE)

#4. Quais recursos - USUÁRIOS
import mysql.connector
from flask import Flask, jsonify, request, make_response
from bd import usuarios

banco = mysql.connector.connect(
    user="root",
    password="stellahenrique",
    host="localhost",
    database="api_stella"
)

api = Flask(__name__)
api.config['JSON_SORT_KEYS'] = False


#Consultar(todos)
@api.route('/usuarios',methods=['GET'])
def obter_usuarios():
    meu_cursor = banco.cursor()
    meu_cursor.execute('SELECT * FROM usuarios')
    meus_usuarios = meu_cursor.fetchall()

    usuarios = list()
    for usuario in meus_usuarios:
        usuarios.append(
            {
                'id': usuario[0],
                'nome': usuario[1],
                'login': usuario[2],
                'senha': usuario[3]
            }
        )

    return make_response(
        jsonify(
        mensagem='Lista de usuários.',
        usuarios=usuarios
        )
    )

#Consultar(id)
@api.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuarios_id(id):
    # Execute a instrução SELECT para buscar o usuário no banco de dados
    meu_cursor = banco.cursor()
    sql = "SELECT * FROM usuarios WHERE id = %s"
    meu_cursor.execute(sql, (id,))
    usuario = meu_cursor.fetchone()

    # Se encontrar o usuário, retorna seus dados
    if usuario:
        return jsonify({'id': usuario[0], 'nome': usuario[1], 'login': usuario[2], 'senha': usuario[3]})
    # Se não encontrar, retorna uma mensagem de erro
    else:
        return make_response(jsonify(mensagem='Usuário não encontrado.'))



#Editar
@api.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuarios_id(id):
    # Recebe os dados do usuário a ser editado
    usuario_editado = request.get_json()
    novo_nome = usuario_editado['nome']
    novo_login = usuario_editado['login']
    nova_senha = usuario_editado['senha']

    # Executa a instrução UPDATE no banco de dados
    meu_cursor = banco.cursor()
    sql = "UPDATE usuarios SET nome = %s, login = %s, senha = %s WHERE id = %s"
    meu_cursor.execute(sql, (novo_nome, novo_login, nova_senha, id))
    banco.commit()

    # Retorna a resposta da edição do usuário
    return make_response(
        jsonify(
            mensagem='Usuário atualizado com sucesso.',
            usuario=usuario_editado
        )
    )
        
#Criar
@api.route('/usuarios', methods=['POST'])
def incluir_novo_usuario():
    novo_usuario = request.get_json()

    meu_cursor = banco.cursor()
    sql = f"INSERT INTO usuarios (nome, login, senha) VALUES ('{novo_usuario['nome']}', '{novo_usuario['login']}', '{novo_usuario['senha']}')"
    meu_cursor.execute(sql)
    banco.commit()

    return make_response(
        jsonify(
        mensagem='Usuário cadastrado com sucesso.',
        novo_usuario=novo_usuario
        )
    )

#Excluir
@api.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuarios(id):
    for indice, usuario in enumerate(usuarios):
        if usuario.get('id') == id:
            # Execute a instrução DELETE
            meu_cursor = banco.cursor()
            sql = f"DELETE FROM usuarios WHERE id = {id}"
            meu_cursor.execute(sql)
            banco.commit()

            # Recupera os usuários do banco de dados atualizados
            meu_cursor.execute("SELECT * FROM usuarios")
            usuarios = meu_cursor.fetchall()

            # Remove o usuário da lista
            del usuarios[indice]
            
            return make_response(jsonify(mensagem='Usuário deletado com sucesso.', usuarios=usuarios))
    
    # Se não encontrar o usuário na lista, retorna uma mensagem de erro
    return make_response(jsonify(mensagem='Usuário não encontrado.', usuarios=usuarios))


api.run(port=5000,host='localhost',debug=True)
