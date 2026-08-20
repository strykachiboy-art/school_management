from App.extensions import db
from App.enums.role import Role

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default=Role.STUDENT)
    
    password_reset_token = db.relationship("PasswordResetToken", 
                                           back_populates = "user", 
                                           cascade = "all, delete-orphan")
    
    student_profile = db.relationship("Student", back_populates="user", uselist=False)
    teacher_profile = db.relationship("Teacher", back_populates="user", uselist=False)