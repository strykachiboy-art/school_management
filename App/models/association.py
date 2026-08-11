from App.extensions import db

student_subjects = db.Table(
    "student_subject",
    db.Column(
        "student_id",
        db.Integer,
        db.ForeignKey("students.id"),
        primary_key=True,
    ),
    db.Column(
        "subject_id",
        db.Integer,
        db.ForeignKey("subjects.id"),
        primary_key=True,
    ),
)

teacher_subjects = db.Table(
    "teacher_subject",
    db.Column(
        "teacher_id",
        db.Integer,
        db.ForeignKey("teachers.id"),
        primary_key=True,
    ),
    db.Column(
        "subject_id",
        db.Integer,
        db.ForeignKey("subjects.id"),
        primary_key=True,
    ),
)

classroom_subjects = db.Table(
    "classroom_subject",
    db.Column(
        "classroom_id",
        db.Integer,
        db.ForeignKey("classrooms.id"),
        primary_key=True,
    ),
    db.Column(
        "subject_id",
        db.Integer,
        db.ForeignKey("subjects.id"),
        primary_key=True,
    ),
)