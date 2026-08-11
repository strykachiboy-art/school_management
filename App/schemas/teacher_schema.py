from marshmallow import Schema, fields
from App.extensions import ma 
from App.models.teacher import Teacher
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class TeacherSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing teacher data in API responses."""

    class Meta:
        model = Teacher
        ordered = True
        load_instance = True

    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    full_name = fields.String(required=True, allow_none=False)
    email = fields.Email(allow_none=True)
    phone = fields.String(allow_none=True)
    subject = fields.String(allow_none=True)
    gender = fields.String(allow_none=True)
    date_of_birth = fields.Date(allow_none=True)
    password = fields.String(load_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True, allow_none=True)
    updated_at = fields.DateTime(dump_only=True, allow_none=True)