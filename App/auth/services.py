from flask import g, session
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from App.models.user import User
from App.extensions import db


