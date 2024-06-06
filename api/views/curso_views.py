from flask_restful import Resource
from api import api
from ..schemas import curso_schema
from flask import request, make_response, jsonify
from ..entidades import curso
from ..services import curso_service
from datetime import datetime

class CursoList(Resource):
    def get(self):
        return "Estudando API com FLASK"

    def post(self):
        cs = curso_schema.CursoSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]

            # Verificar se 'data_publicacao' está presente, caso contrário, usar a data atual
            if "data_publicacao" in request.json:
               data_publicacao = request.json["data_publicacao"]
            else:
               data_publicacao = datetime.now().date()  # Usar a data atual se não estiver presente

            novo_curso = curso.Curso(nome=nome, descricao=descricao, data_publicacao=data_publicacao)
            resultado = curso_service.cadastrar_curso(novo_curso)
            x = cs.dump(resultado)
            return make_response(jsonify(x), 201)

api.add_resource(CursoList, '/cursos')