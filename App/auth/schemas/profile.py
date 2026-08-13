from App.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from App.models.user import User

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password", )

