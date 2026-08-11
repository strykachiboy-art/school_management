from App.extensions import db
from App.models.user import User
from App.models.student import Student
from App.models.teacher import Teacher
from App.models.subject import Subject

def get_admin_dashboard_stats():
    """Queries the database to gather summary statistics for the admin dashboard."""
    stats = {
        "total_users": db.session.query(User).count(),
        "total_students": db.session.query(Student).count(),
        "total_teachers": db.session.query(Teacher).count(),
        "total_subjects": db.session.query(Subject).count(),
        "total_classrooms": db.session.query(Subject).count()
    }
    return stats