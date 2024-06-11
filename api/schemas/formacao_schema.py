from api import ma
from ..models import formacao_model
from marshmallow import fields
from ..schemas import curso_schema, professor_schema
from .professor_schema import ProfessorSchema

class FormacaoSchema(ma.SQLAlchemyAutoSchema):
    #erro nessa linha quando fazer POST ou PUT
    professores = ma.Nested(professor_schema.ProfessorSchema, many=True, only=('id', 'nome'))
    class Meta:
        model = formacao_model.Formacao
        load_instance = True
        fields = ("id", "nome", "descricao", "cursos", "professores", "_links")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    cursos = fields.List(fields.Nested(curso_schema.CursoSchema, only=('id', 'nome')))
    #professores = fields.List(fields.Nested(ProfessorSchema, only=("id", "nome")))

    _links = ma.Hyperlinks(
        {
            "get": ma.URLFor('formacaodetails', values=dict(id="<id>")),
            "put": ma.URLFor('formacaodetails', values=dict(id="<id>")),
            "delete": ma.URLFor('formacaodetails', values=dict(id="<id>"))
        }
    )