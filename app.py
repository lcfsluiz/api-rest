#!/usr/bin/python3
import json
import requests
from pymongo import MongoClient
from flask import (Flask, jsonify, make_response,
                    redirect, Response, request)

try:
    con = MongoClient()
    db = con['projeto']
except Exception as e:
    print('Erro:{}'.format(e))
    exit()


app = Flask(__name__)


@app.route('/')
def index():
    mensagem = {'mensagem': 'minha api'}
    return jsonify(mensagem)


@app.route('/usuarios', methods=['GET'])
def usuarios():
    return jsonify([x for x in db.usuarios.find()])


@app.route('/usuario/<int:id>', methods=['GET'])
def usuario(id):
    busca = db.usuarios.find_one({"_id": id})
    if busca:
        return jsonify(busca)
    else:
        busca = {"mensagem": "Usuario não encontrado"}
        return Response(json.dumps(busca), 404, content_type="application/json")

    # return jsonify(busca) if busca else Response(json.dumps({"mensagem":"Usuario não encontrado"}), 404, content_type="application/json")

@app.route('/usuario', methods=['POST'])
def registrar_usuario():
    try:
        data = request.get_json()
        if data["_id"] and isinstance(data["_id"], int):
            db.usuarios.insert(request.get_json())
            return jsonify({"mensagem":"cadastrado com sucesso!"})  
        else:
            return jsonify({"mensagem":"id invalido"})
    except Exception:
        return jsonify({"mensagem": "usuario ja cadastrado"})


    # print(data["_id"])


@app.route('/cep/<busca>')
def buscar_cep(busca):
    requisicao = requests.get("https://viacep.com.br/ws/{}/json/".format(busca))
    return jsonify(requisicao.json())


if __name__ == "__main__":
    app.run(host='0.0.0.0',  port=5000,  debug=True)


# import requests
# requisicao = requests.get("https://viacep.com.br/ws/08270630/json/")
# print(requisicao.json()
