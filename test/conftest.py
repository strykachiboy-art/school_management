from datetime import date, time
import pytest

from App import create_app
from App.extensions import db, limiter, redis_client
from App.models.academic_session import AcademicSession
from App.models.classroom import Classroom
from App.models.exam import Exam
from App.models.result import Result
from App.models.student import Student
from App.models.subject import Subject
from App.models.teacher import Teacher
from App.models.user import User


# ----------------------------------------------------------------------
# 1. Global Setup & Teardown Fixtures
# ----------------------------------------------------------------------

@pytest.fixture(scope="function")
def app():
    """Create a fresh Flask app with an in-memory SQLite DB for each test."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key-that-is-at-least-32-bytes-long",
        "RATELIMIT_ENABLED": True,
        "RATELIMIT_STORAGE_URI": "memory://",
        "WTF_CSRF_ENABLED": False,
        "ADMIN_ACCESS_ENABLED": True,
    }
    app = create_app(config=test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(autouse=True)
def auto_clear_limiter(app):
    """Automatically resets Flask-Limiter state between every single test."""
    yield
    with app.app_context():
        if getattr(limiter, "_storage", None) is not None:
            try:
                limiter.reset()
            except Exception:
                pass


@pytest.fixture(autouse=True)
def auto_clear_redis():
    """Cleans up Redis whitelist keys after each test safely."""
    yield
    try:
        keys = redis_client.keys("refresh_whitelist:*")
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass


# ----------------------------------------------------------------------
# 2. HTTP Client Helpers
# ----------------------------------------------------------------------

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture
def json_client(client):
    """A test client wrapper that attaches 'Accept: application/json'."""
    class JSONClient:
        def __init__(self, c):
            self.c = c
            self.headers = {"Accept": "application/json"}

        def _kwargs(self, kwargs):
            kwargs["headers"] = {**self.headers, **kwargs.get("headers", {})}
            return kwargs

        def post(self, url, **kwargs):
            return self.c.post(url, **self._kwargs(kwargs))

        def patch(self, url, **kwargs):
            return self.c.patch(url, **self._kwargs(kwargs))

        def get(self, url, **kwargs):
            return self.c.get(url, **self._kwargs(kwargs))

        def delete(self, url, **kwargs):
            return self.c.delete(url, **self._kwargs(kwargs))

    return JSONClient(client)


# ----------------------------------------------------------------------
# 3. Model Factories
# ----------------------------------------------------------------------

@pytest.fixture
def make_user(app):
    def _make(suffix="1", role="student"):
        with app.app_context():
            user = User(
                username=f"user_{suffix}",
                email=f"user_{suffix}@example.com",
                password="hashed-placeholder",
                role=role,
            )
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            db.session.expunge(user)
            return user
    return _make


@pytest.fixture
def make_teacher(app):
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

            teacher = Teacher(user_id=user.id, full_name=f"Teacher {suffix}")
            db.session.add(teacher)
            db.session.commit()
            db.session.refresh(teacher)
            db.session.expunge(teacher)
            return teacher
    return _make


@pytest.fixture
def make_student(app):
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

            student = Student(user_id=user.id, full_name=f"Student {suffix}")
            db.session.add(student)
            db.session.commit()
            db.session.refresh(student)
            db.session.expunge(student)
            return student
    return _make


@pytest.fixture
def make_classroom(app):
    def _make(suffix="1"):
        with app.app_context():
            classroom = Classroom(name=f"Room {suffix}", capacity=30)
            db.session.add(classroom)
            db.session.commit()
            db.session.refresh(classroom)
            db.session.expunge(classroom)
            return classroom
    return _make


@pytest.fixture
def make_exam(app, subject, classroom, academic_session):
    def _make(suffix="1"):
        with app.app_context():
            exam = Exam(
                title=f"Exam {suffix}",
                description="Test description",
                subject_id=subject.id,
                classroom_id=classroom.id,
                session_id=academic_session.id,
                exam_date=date(2026, 12, 1),
                start_time=time(9, 0),
                duration_minutes=90,
                total_marks=100,
            )
            db.session.add(exam)
            db.session.commit()
            db.session.refresh(exam)
            db.session.expunge(exam)
            return exam
    return _make


@pytest.fixture
def make_result(app, student, exam):
    def _make(student_obj=student, exam_obj=exam, marks=85.5):
        with app.app_context():
            result = Result(
                student_id=student_obj.id,
                exam_id=exam_obj.id,
                marks_obtained=marks,
            )
            db.session.add(result)
            db.session.commit()
            db.session.refresh(result)
            db.session.expunge(result)
            return result
    return _make


# ----------------------------------------------------------------------
# 4. Standard Model Fixtures
# ----------------------------------------------------------------------

@pytest.fixture
def base_user(make_user):
    return make_user("base")


@pytest.fixture
def teacher(make_teacher):
    return make_teacher("1")


@pytest.fixture
def teacher2(make_teacher):
    return make_teacher("2")


@pytest.fixture
def student(make_student):
    return make_student("1")


@pytest.fixture
def student2(make_student):
    return make_student("2")


@pytest.fixture
def subject(app):
    with app.app_context():
        subj = Subject(name="Mathematics", code="MATH101")
        db.session.add(subj)
        db.session.commit()
        db.session.refresh(subj)
        db.session.expunge(subj)
        return subj


@pytest.fixture
def classroom(app):
    with app.app_context():
        cls = Classroom(name="Room A", capacity=30)
        db.session.add(cls)
        db.session.commit()
        db.session.refresh(cls)
        db.session.expunge(cls)
        return cls


@pytest.fixture
def academic_session(app):
    with app.app_context():
        sess = AcademicSession(name="2026/2027", end_date=date(2027, 6, 1))
        db.session.add(sess)
        db.session.commit()
        db.session.refresh(sess)
        db.session.expunge(sess)
        return sess


@pytest.fixture
def exam(make_exam):
    return make_exam("1")


@pytest.fixture
def result(make_result):
    return make_result()


@pytest.fixture
def student_in_teacher_classroom(app, teacher, classroom, student):
    with app.app_context():
        c = db.session.merge(classroom)
        s = db.session.merge(student)
        c.teacher_id = teacher.id
        s.classroom_id = c.id
        db.session.commit()
        db.session.refresh(s)
        db.session.expunge(s)
        return s


# ----------------------------------------------------------------------
# 5. Auth / Header Fixtures
# ----------------------------------------------------------------------

@pytest.fixture(scope="function")
def admin_headers(app):
    from flask_jwt_extended import create_access_token

    with app.app_context():
        admin = User(
            username="admin_test",
            email="admin_test@example.com",
            password="hashed-placeholder",
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()

        token = create_access_token(
            identity=str(admin.id),
            additional_claims={"role": "admin"},
        )

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


@pytest.fixture(scope="function")
def teacher_headers(app, teacher):
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(
            identity=str(teacher.user_id),
            additional_claims={"role": "teacher"},
        )

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


@pytest.fixture(scope="function")
def student_headers(app, student):
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(
            identity=str(student.user_id),
            additional_claims={"role": "student"},
        )

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


@pytest.fixture(scope="function")
def user_with_password(app):
    from flask_jwt_extended import create_access_token
    from App.utils.password import hash_password

    plain_password = "OriginalPass123"

    with app.app_context():
        user = User(
            username="pwtest_user",
            email="pwtest_user@example.com",
            password=hash_password(plain_password),
            role="student",
        )
        db.session.add(user)
        db.session.commit()

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": "student"},
        )

        user_id = user.id

    return {
        "user_id": user_id,
        "plain_password": plain_password,
        "headers": {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    }