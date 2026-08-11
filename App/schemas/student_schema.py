from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from App.extensions import ma
from App.models import Student 

class StudentSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing student data in API responses."""

    class Meta:
        model = Student
        ordered = True
        load_instance = True

    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    full_name = fields.String(required=True, allow_none=False)
    email = fields.Email(allow_none=True)
    phone = fields.String(allow_none=True)
    admission_number = fields.String(allow_none=True)
    classroom_id = fields.Int(allow_none=True)
    gender = fields.String(allow_none=True)
    date_of_birth = fields.Date(allow_none=True)
    address = fields.String(allow_none=True)
    password = fields.String(load_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True, allow_none=True)
    updated_at = fields.DateTime(dump_only=True, allow_none=True)