from flask_restful import Resource
from api import api
from ..schemas import curso_schema
from flask import request, make_response, jsonify
from ..entidades import curso
from ..services import curso_service, formacao_service
from datetime import datetime
from ..paginate import paginate
from ..models.curso_model import Curso
from flask_jwt_extended import jwt_required, get_jwt

class CursoList(Resource):
    @jwt_required()
    def get(self):
        cs = curso_schema.CursoSchema(many=True)
        return paginate(Curso, cs)

    @jwt_required()
    def post(self):
        claims = get_jwt() # recuperar o claims do login_views
        if claims['roles'] != 'admin':
            return make_response(jsonify(mensagem='Não é permitido esse recurso. Apenas administradores'), 403)
        cs = curso_schema.CursoSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            formacao = request.json["formacao"]
            formacao_curso = formacao_service.listar_formacao_id(formacao)
            if formacao_curso is None:
                return make_response(jsonify(f"Formação com ID: {formacao} não foi encontrada!"), 404)

            # Verificar se 'data_publicacao' está presente, caso contrário, usar a data atual
            if "data_publicacao" in request.json:
               data_publicacao = request.json["data_publicacao"]
            else:
               data_publicacao = datetime.now().date()  # Usar a data atual se não estiver presente

            novo_curso = curso.Curso(
                nome=nome,
                descricao=descricao,
                data_publicacao=data_publicacao,
                formacao=formacao_curso
            )
            resultado = curso_service.cadastrar_curso(novo_curso)
            x = cs.dump(resultado)
            return make_response(jsonify(x), 201)

class CursoDetails(Resource):

    @jwt_required()
    def get(self, id):
        curso = curso_service.listar_curso_id(id)
        if curso is None:
            return make_response(jsonify("Curso não foi encontrado!"), 404)
        cs = curso_schema.CursoSchema()
        return make_response(jsonify(cs.dump(curso)), 200)

    @jwt_required()
    def put(self, id):
        claims = get_jwt()  # recuperar o claims do login_views
        if claims['roles'] != 'admin':
            return make_response(jsonify(mensagem='Não é permitido esse recurso. Apenas administradores'), 403)
        curso_bd = curso_service.listar_curso_id(id)
        if curso_bd is None:
            return make_response(jsonify("Curso não foi encontrado!"), 404)
        cs = curso_schema.CursoSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            data_publicacao =request.json["data_publicacao"]
            formacao = request.json["formacao"]
            formacao_curso = formacao_service.listar_formacao_id(formacao)
            if formacao_curso is None:
                return make_response(jsonify(f"Formação com ID: {formacao} não foi encontrada!"), 404)
            novo_curso = curso.Curso(
                nome=nome,
                descricao=descricao,
                data_publicacao=data_publicacao,
                formacao=formacao_curso
            )
            curso_service.atualiza_curso(curso_bd, novo_curso)
            curso_atualizado = curso_service.listar_curso_id(id)
            return make_response(jsonify(cs.dump(curso_atualizado)), 200)

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()  # recuperar o claims do login_views
        if claims['roles'] != 'admin':
            return make_response(jsonify(mensagem='Não é permitido esse recurso. Apenas administradores'), 403)
        curso_bd = curso_service.listar_curso_id(id)
        if curso_bd is None:
            return make_response(jsonify("Curso não encontrado"), 400)
        curso_service.remove_curso(curso_bd)
        return make_response("Curso excluido com sucesso", 204)


api.add_resource(CursoList, '/cursos')
api.add_resource(CursoDetails, '/cursos/<int:id>')
