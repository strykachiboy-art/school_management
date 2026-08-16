"""School management application package."""
from typing import Optional
from flask import Flask, g, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from App.models.user import User
from App.errors import register_error_handlers

from .config import get_config_class
from .extensions import cors, db, jwt, limiter, migrate


def create_app(config: Optional[dict] = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(get_config_class())

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    
    from App.routes.admin.subject_route import subject_bp
    from App.routes.admin.classroom_route import classroom_bp
    from App.routes.admin.assignment_route import ass_bp
    from App.routes.admin.teacher_route import teacher_bp
    from App.routes.admin.student_route import student_bp
    from App.routes.admin.exam_route import exam_bp
    from App.routes.admin.result_route import result_bp
    from App.routes.admin.admin import admin_bp
    from App.routes.teacher.teacher_grade_route import teacher_grade_bp
    from App.routes.admin import admin_reports_route
    from App.auth.auth import auth_bp
    from App.auth.routes.change_password import change_password_route
    import App.auth.routes.forgot_password
    import App.routes.admin.admin_grade_route
    import App.auth.routes.log_out
    import App.auth.routes.register
    import App.auth.routes.login
    import App.auth.routes.refresh_access_token
    from App.routes.student.student_grade_route import student_grade_bp
    from App.routes.admin.academic_session import academic_session_bp
    from App.routes.admin.term import term_bp
    from App.routes.admin.attendance import attendance_bp
    
    

    app.register_blueprint(subject_bp, url_prefix="/subjects")
    app.register_blueprint(classroom_bp, url_prefix="/classrooms")
    app.register_blueprint(ass_bp, url_prefix="/assignments")
    app.register_blueprint(teacher_bp, url_prefix="/teachers")
    app.register_blueprint(student_bp, url_prefix="/students")
    app.register_blueprint(exam_bp, url_prefix="/exams")
    app.register_blueprint(result_bp, url_prefix = "/results")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(teacher_grade_bp, url_prefix="/teacher")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(student_grade_bp, url_prefix="/student")
    app.register_blueprint(academic_session_bp, url_prefix="/academic-sessions")
    app.register_blueprint(term_bp, url_prefix = "/terms")
    app.register_blueprint(attendance_bp, url_prefix = "/attendances")
    
    
    register_error_handlers(app)
    

    @app.before_request
    def load_current_user():
    # 1. Bypass JWT check on the refresh route (let @jwt_required(refresh=True) handle it)
       if request.endpoint == "auth.refresh":
        g.user = None
        return

    # 2. Safely verify standard Access Tokens for all other endpoints
       try:
         verify_jwt_in_request(optional=True)
         user_id = get_jwt_identity()
         if user_id:
            g.user = db.session.get(User, user_id)
         else:
            g.user = None
       except Exception:
        g.user = None

    @app.after_request
    def after(response):
        return response

    return app


__all__ = ["create_app", "db"]