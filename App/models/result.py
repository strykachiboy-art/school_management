from App.extensions import db

class Result(db.Model):
    __tablename__ = 'results'

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "exam_id",
            name="uq_student_exam_result"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    student = db.relationship('Student', back_populates="results")
    exam = db.relationship('Exam', back_populates="results")