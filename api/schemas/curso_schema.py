from api import ma
from ..models import curso_model
from marshmallow import fields

class CursoSchema(ma.SQLAlchemyAutoSchema):
    model = curso_model.Curso
    load_instance = True
    fields = ("id", "nome", "descricao", "data_puclicacao")

    name = fields.String(require=True)
    descricao = fields.String(required=True)
    data_publicacao = fields.Date(required=True)