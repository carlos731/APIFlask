from api import ma
from ..models import formacao_model, professor_model
from marshmallow import fields, post_load
from ..schemas import curso_schema, professor_schema
from .professor_schema import ProfessorSchema

class FormacaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = formacao_model.Formacao
        load_instance = True
        fields = ("id", "nome", "descricao", "cursos", "professores", "_links")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    cursos = fields.List(fields.Nested(curso_schema.CursoSchema, only=('id', 'nome')))
    professores = ma.Nested(professor_schema.ProfessorSchema, many=True, only=('id', 'nome'))
    #professores_ids = fields.List(fields.Integer(), load_only=True)

    _links = ma.Hyperlinks(
        {
            "get": ma.URLFor('formacaodetails', values=dict(id="<id>")),
            "put": ma.URLFor('formacaodetails', values=dict(id="<id>")),
            "delete": ma.URLFor('formacaodetails', values=dict(id="<id>"))
        }
    )

    # @post_load
    # def make_formacao(self, data, **kwargs):
    #     if 'professores_ids' in data:
    #         data['professores'] = [professor_model.Professor.query.get(id) for id in data['professores_ids']]
    #     return data