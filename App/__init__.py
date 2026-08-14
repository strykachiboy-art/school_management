"""School management application package."""
from typing import Optional
from flask import Flask, g
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
    from App.routes.teacher.grade_route import teacher_grade_bp
    from App.routes.admin import admin_reports_route
    from App.auth.auth import auth_bp
    from App.auth.routes.change_password import change_password_route
    import App.auth.routes.forgot_password
    import App.routes.admin.grade_route
    import App.auth.routes.log_out
    import App.auth.routes.register
    

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
    
    
    register_error_handlers(app)
    

    @app.before_request
    def load_current_user():
        
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()

        if user_id:
            g.user = db.session.get(User, user_id)
        else:
            g.user = None

    @app.after_request
    def after(response):
        return response

    return app


__all__ = ["create_app", "db"]