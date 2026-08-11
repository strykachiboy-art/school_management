import pytest
from datetime import date, time

from App import create_app
from App.extensions import db
from App.models.exam import Exam
from App.models.subject import Subject
from App.models.classroom import Classroom


from App.models.user import User
from App.models.teacher import Teacher
from App.models.student import Student

@pytest.fixture
def teacher2(make_teacher):
    return make_teacher("2")

@pytest.fixture
def student2(make_student):
    return make_student("2")

@pytest.fixture
def make_teacher(app):
    """Factory: creates a User + Teacher pair. Call with a unique suffix."""
    def _make(suffix="1"):
        with app.app_context():
            user = User(
                username=f"teacher_{suffix}",
                email=f"teacher_{suffix}@example.com",
                password="hashed-placeholder",
                role="teacher",
            )
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

            teacher = Teacher(user_id=user.id, full_name=f"Teacher {suffix}")
            db.session.add(teacher)
            db.session.commit()
            db.session.refresh(teacher)
            return teacher
    return _make


@pytest.fixture
def make_student(app):
    """Factory: creates a User + Student pair. Call with a unique suffix."""
    def _make(suffix="1"):
        with app.app_context():
            user = User(
                username=f"student_{suffix}",
                email=f"student_{suffix}@example.com",
                password="hashed-placeholder",
                role="student",
            )
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

            student = Student(user_id=user.id, full_name=f"Student {suffix}")
            db.session.add(student)
            db.session.commit()
            db.session.refresh(student)
            return student
    return _make


@pytest.fixture
def make_classroom(app):
    """Factory: creates a Classroom. Call with a unique suffix (name is unique)."""
    def _make(suffix="1"):
        with app.app_context():
            classroom = Classroom(name=f"Room {suffix}", capacity=30)
            db.session.add(classroom)
            db.session.commit()
            db.session.refresh(classroom)
            return classroom
    return _make


@pytest.fixture
def teacher(make_teacher):
    return make_teacher("1")


@pytest.fixture
def student(make_student):
    return make_student("1")

@pytest.fixture(scope="function")
def app():
    """Create a fresh Flask app with an in-memory SQLite DB for each test."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key",
        "RATELIMIT_ENABLED": False,
        "WTF_CSRF_ENABLED": False,
        "ADMIN_ACCESS_ENABLED": True,   # <-- required or role_required() always 403s
    }
    app = create_app(config=test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def admin_headers(app):
    """Create a real admin User row and mint a token against its id."""
    from flask_jwt_extended import create_access_token
    from App.models.user import User

    with app.app_context():
        admin = User(
            username="admin_test",
            email="admin_test@example.com",
            password="hashed-placeholder",  # not used for login here, just satisfies nullable=False
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        db.session.refresh(admin)

        token = create_access_token(
            identity=str(admin.id),
            additional_claims={"role": "admin"},
        )

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


@pytest.fixture
def subject(app):
    """A valid Subject row, since Exam.subject_id is a required FK."""
    with app.app_context():
        subj = Subject(name="Mathematics", code="MATH101")
        db.session.add(subj)
        db.session.commit()
        db.session.refresh(subj)
        yield subj


@pytest.fixture
def classroom(app):
    """A valid Classroom row, since Exam.classroom_id is a required FK."""
    with app.app_context():
        cls = Classroom(name="Room A", capacity=30)
        db.session.add(cls)
        db.session.commit()
        db.session.refresh(cls)
        yield cls


@pytest.fixture
def exam(app, subject, classroom):
    """A persisted Exam row for get/delete tests."""
    with app.app_context():
        exam = Exam(
            title="Midterm Exam",
            description="Covers chapters 1-5",
            subject_id=subject.id,
            classroom_id=classroom.id,
            exam_date=date(2026, 12, 1),
            start_time=time(9, 0),
            duration_minutes=90,
            total_marks=100,
        )
        db.session.add(exam)
        db.session.commit()
        db.session.refresh(exam)
        yield exam