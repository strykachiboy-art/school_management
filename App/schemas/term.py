from App.extensions import ma
from App.models import Term
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class TermSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Term
        load_instance = True
        include_fk = True