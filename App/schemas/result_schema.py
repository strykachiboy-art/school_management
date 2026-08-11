from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from App.models.result import Result

from App.extensions import ma


class ResultSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Result
        load_instance = True

    id = fields.Int(dump_only=True)

    student_id = fields.Int(required=True)
    exam_id = fields.Int(required=True)

    marks_obtained = fields.Float(required=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)