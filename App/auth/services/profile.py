from sqlalchemy.exc import SQLAlchemyError
from App.models.user import User
from App.extensions import db
from App.auth.request.profile import ProfileUpdateRequest

def update_profile(user: User, data: ProfileUpdateRequest) -> User:
    try:
        # Check username uniqueness
        if data.username is not None and data.username != user.username:
            existing_user = User.query.filter(
                User.username == data.username,
                User.id != user.id
            ).first()
            if existing_user:
                raise ValueError("Username already exists")
            user.username = data.username

        # Check email uniqueness
        if data.email is not None and data.email != user.email:
            existing_user = User.query.filter(
                User.email == data.email,
                User.id != user.id
            ).first()
            if existing_user:
                raise ValueError("Email already exists")
            user.email = data.email

        db.session.commit()
        return user
    except SQLAlchemyError as e:
        db.session.rollback()
        # You can log the error here: logger.error(f"DB Error: {e}")
        raise RuntimeError("A database error occurred while updating the profile.") from e