from flask_restful import Resource
from api import api
from ..schemas import formacao_schema
from flask import request, make_response, jsonify
from ..entidades import formacao
from ..services import formacao_service

class FormacaoList(Resource):
    def get(self):
        formacoes = formacao_service.listar_formacoes()
        fs = formacao_schema.FormacaoSchema(many=True)
        return make_response(jsonify(fs.dump(formacoes)), 200)

    def post(self):
        fs = formacao_schema.FormacaoSchema()
        validate = fs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            professores = request.json["professores"]
            nova_formacao = formacao.Formacao(
                nome=nome,
                descricao=descricao,
                professores=professores
            )
            resultado = formacao_service.cadastrar_formacao(nova_formacao)
            x = fs.dump(resultado)
            return make_response(jsonify(x), 201)

class FormacaoDetails(Resource):
    def get(self, id):
        formacao = formacao_service.listar_formacao_id(id)
        if formacao is None:
            return make_response(jsonify("Formacão não foi encontrada!"), 404)
        fs = formacao_schema.FormacaoSchema()
        return make_response(jsonify(fs.dump(formacao)), 200)

    def put(selfself, id):
        formacao_bd = formacao_service.listar_formacao_id(id)
        if formacao_bd is None:
            return make_response(jsonify("Formacão não foi encontrada!"), 404)
        fs = formacao_schema.FormacaoSchema()
        validate = fs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            professores = request.json["professores"]
            nova_formacao = formacao.Formacao(
                nome=nome,
                descricao=descricao,
                professores=professores
            )
            formacao_service.atualiza_formacao(formacao_bd, nova_formacao)
            formacao_atualizada = formacao_service.listar_formacao_id(id)
            return make_response(jsonify(fs.dump(formacao_atualizada)), 200)

    def delete(self, id):
        formacao_bd = formacao_service.listar_formacao_id(id)
        if formacao_bd is None:
            return make_response(jsonify("Formacão não encontrada"), 400)
        formacao_service.remove_formacao(formacao_bd)
        return make_response("Formacão excluida com sucesso", 204)

api.add_resource(FormacaoList, '/formacoes')
api.add_resource(FormacaoDetails, '/formacoes/<int:id>')
