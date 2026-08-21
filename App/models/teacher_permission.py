from App.extensions import db
from App.enums.permission import Permission

class TeacherPermission(db.Model):
    __tablename__ = "teacher_permissions"
    
    __table_args__ = (db.UniqueConstraint("teacher_id", "permission"),)
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    permission = db.Column(db.Enum(Permission), nullable=False)
    
    teacher = db.relationship("Teacher", back_populates = "permission")