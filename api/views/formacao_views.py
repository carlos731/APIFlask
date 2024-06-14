from flask_restful import Resource
from api import api
from ..schemas import formacao_schema, formacao_request_schema
from flask import request, make_response, jsonify
from ..entidades import formacao
from ..services import formacao_service, professor_service
from ..paginate import paginate
from ..models.formacao_model import Formacao
from flask_jwt_extended import jwt_required, get_jwt

class FormacaoList(Resource):

    @jwt_required()
    def get(self):
        fs = formacao_schema.FormacaoSchema(many=True)
        return paginate(Formacao, fs)

    @jwt_required()
    def post(self):
        # verificar se usuário é admin ou não para fazer essa operação.
        claims = get_jwt()  # recuperar o claims do login_views
        if claims['roles'] != 'admin':
            return make_response(jsonify(mensagem='Não é permitido esse recurso. Apenas administradores'), 403)

        fs = formacao_request_schema.FormacaoRequestSchema()
        validate = fs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            professores = request.json["professores"]

            # Verificar se todos os IDs de professores existem
            professores_existentes = professor_service.listar_professores()
            professores_existentes_ids = [prof.id for prof in professores_existentes]

            ids_invalidos = [prof_id for prof_id in professores if prof_id not in professores_existentes_ids]

            if ids_invalidos:
                return make_response(jsonify({"error": f"Professor com ID {ids_invalidos} não existe!"}), 400)

            nova_formacao = formacao.Formacao(
                nome=nome,
                descricao=descricao,
                professores=professores
            )
            resultado = formacao_service.cadastrar_formacao(nova_formacao)

            # para mudar a response para formacao_schema e não ficar com formação_request_schema
            fs = formacao_schema.FormacaoSchema()

            x = fs.dump(resultado)
            return make_response(jsonify(x), 201)

class FormacaoDetails(Resource):
    @jwt_required()
    def get(self, id):
        formacao = formacao_service.listar_formacao_id(id)
        if formacao is None:
            return make_response(jsonify("Formacão não foi encontrada!"), 404)
        fs = formacao_schema.FormacaoSchema()
        return make_response(jsonify(fs.dump(formacao)), 200)

    @jwt_required()
    def put(self, id):
        # verificar se usuário é admin ou não para fazer essa operação.
        claims = get_jwt()  # recuperar o claims do login_views
        if claims['roles'] != 'admin':
            return make_response(jsonify(mensagem='Não é permitido esse recurso. Apenas administradores'), 403)

        formacao_bd = formacao_service.listar_formacao_id(id)
        if formacao_bd is None:
            return make_response(jsonify("Formacão não foi encontrada!"), 404)

        fs = formacao_request_schema.FormacaoRequestSchema()
        validate = fs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            professores = request.json["professores"]

            # verificar se todos os IDs de professores existem
            professores_existentes = professor_service.listar_professores()
            professores_existentes_ids = [prof.id for prof in professores_existentes]

            ids_invalidos = [prof_id for prof_id in professores if prof_id not in professores_existentes_ids]

            if ids_invalidos:
                return make_response(jsonify({"error": f"Professor com ID {ids_invalidos} não existe!"}), 400)

            nova_formacao = formacao.Formacao(
                nome=nome,
                descricao=descricao,
                professores=professores
            )
            formacao_service.atualiza_formacao(formacao_bd, nova_formacao)
            formacao_atualizada = formacao_service.listar_formacao_id(id)

            # para mudar a response para formacao_schema e não ficar com formação_request_schema
            fs = formacao_schema.FormacaoSchema()

            return make_response(jsonify(fs.dump(formacao_atualizada)), 200)

    @jwt_required()
    def delete(self, id):
        # verificar se usuário é admin ou não para fazer essa operação.
        claims = get_jwt()  # recuperar o claims do login_views
        if claims['roles'] != 'admin':
            return make_response(jsonify(mensagem='Não é permitido esse recurso. Apenas administradores'), 403)

        formacao_bd = formacao_service.listar_formacao_id(id)
        if formacao_bd is None:
            return make_response(jsonify("Formacão não encontrada"), 400)
        formacao_service.remove_formacao(formacao_bd)
        return make_response("Formacão excluida com sucesso", 204)


api.add_resource(FormacaoList, '/formacoes')
api.add_resource(FormacaoDetails, '/formacoes/<int:id>')
