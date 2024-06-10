from api import ma
from ..models import formacao_model
from marshmallow import fields

class FormacaoRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = formacao_model.Formacao
        load_instance = True
        fields = ("id", "nome", "descricao", "cursos", "professores")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    cursos = fields.List(fields.Nested('CursoChema', only=("id", "title")))
