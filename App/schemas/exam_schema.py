from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from App.models.exam import Exam

from App.extensions import ma


class ExamSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Exam
        load_instance = True
        
    id = fields.Int(dump_only=True)
    
    title = fields.String(required = True)
    description = fields.String(allow_none=True)
    
    subject_id = fields.Int(required = True)
    classroom_id = fields.Int(required = True)
    
    exam_date = fields.Date(required = True)
    start_time = fields.Time(required = True)
    duration_minutes = fields.Int(allow_none=True)
    
    total_marks = fields.Int(required = True)
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)