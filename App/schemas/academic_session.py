from marshmallow import fields
from App.models.academic_session import AcademicSession
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from App.extensions import ma


class AcademicSessionSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing academic session data in API responses."""

    class Meta:
        model = AcademicSession
        ordered = True
        load_instance = True

    id = fields.Int(dump_only=True)
    name = fields.String(required=True, allow_none=False)
    start_date = fields.DateTime(required=True, allow_none=False)
    end_date = fields.DateTime(required=True, allow_none=False)
    created_at = fields.DateTime(dump_only=True, allow_none=True)
    updated_at = fields.DateTime(dump_only=True, allow_none=True)