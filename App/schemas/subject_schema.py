from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from App.models.subject import Subject

from App.extensions import ma


class SubjectSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing subject data in API responses."""

    class Meta:
        model = Subject
        load_instance = True

    id = fields.Int(dump_only=True)
    name = fields.String(required=True, allow_none=False)
    code = fields.String(required=True, allow_none=False)
    description = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True, allow_none=True)
    updated_at = fields.DateTime(dump_only=True, allow_none=True)