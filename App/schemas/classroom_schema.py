from marshmallow import Schema, fields
from App.models.classroom import Classroom
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from App.extensions import ma

class ClassroomSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing classroom data in API responses."""

    class Meta:
        model = Classroom
        ordered = True
        load_instance = True

    id = fields.Int(dump_only=True)
    name = fields.String(required=True, allow_none=False)
    capacity = fields.Int(required=True, allow_none=False)
    location = fields.String(allow_none=True)
    teacher_id = fields.Int(allow_none=True)
    created_at = fields.DateTime(dump_only=True, allow_none=True)
    updated_at = fields.DateTime(dump_only=True, allow_none=True)