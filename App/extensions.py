"""Application-wide Flask extensions."""

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv


load_dotenv()

ma = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# PS C:\Users\HP\Downloads\indie-game-studio-website\studio_site> .venv\Scripts\Activate.ps1
# (.venv) PS C:\Users\HP\Downloads\indie-game-studio-website\studio_site> flask --app run.py shell
# Ctrl click to launch VS Code Native REPL
# Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] on win32
# App: app
# Instance: C:\Users\HP\Downloads\indie-game-studio-website\studio_site\instance
# >>> from app.extensions import db
# >>> from app.models import User
# >>> u = User.query.filter_by(username="StrykaMax").first()
# >>> print(u)
# <User StrykaMax>
# >>> u.set_password("StrykaMaximum63")
# >>> db.session.commit()
# >>> exit()
# (.venv) PS C:\Users\HP\Downloads\indie-game-studio-website\studio_site>


# cd "c:\Users\HP\Documents\Flask\My_project"
# python run.py

# cd "c:\Users\HP\Documents\Flask\My_project"
# pytest -q

# Generate secret key:
#     python -c "import secrets; print(secrets.token_hex(32))"

# cd "c:\Users\HP\Documents\Flask\My_project"
# C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe run.py

# cd "c:\Users\HP\Documents\Flask\My_project"
# C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe -m pytest -q


# Microsoft Windows [Version 10.0.19045.6466]
# (c) Microsoft Corporation. All rights reserved.

# C:\Users\HP>psql -U postgres
# 'psql' is not recognized as an internal or external command,
# operable program or batch file.

# C:\Users\HP>cd C:\Program Files\PostgreSQL\18\bin

# C:\Program Files\PostgreSQL\18\bin>psql -U postgres
# psql (18.3)
# WARNING: Console code page (437) differs from Windows code page (1252)
#          8-bit characters might not work correctly. See psql reference
#          page "Notes for Windows users" for details.
# Type "help" for help.

# postgres=# 

# npx @tailwindcss/cli -i ./src/input.css -o ./static/css/output.css --minify

# & "C:\msys64\mingw64\bin\git.exe" add .
# & "C:\msys64\mingw64\bin\git.exe" commit -m "update tailwind styles"
# & "C:\msys64\mingw64\bin\git.exe" push








# ```python
# """Application configuration for development, testing, and production."""

# import os
# from datetime import timedelta
# from typing import Any


# class Config:
#     """Base configuration shared by all environments."""

#     SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///site.db")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
#     JWT_TOKEN_LOCATION = ["cookies"]
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
#     JWT_COOKIE_SECURE = False
#     JWT_COOKIE_CSRF_PROTECT = True
#     JWT_COOKIE_SAMESITE = "Lax"

#     ADMIN_ACCESS_ENABLED = os.getenv("ADMIN_ACCESS_ENABLED", "true").lower() in {
#         "1",
#         "true",
#         "yes",
#         "on",
#     }

#     TESTING = False
#     DEBUG = False


# class DevelopmentConfig(Config):
#     """Local development settings."""

#     DEBUG = True
#     JWT_COOKIE_SECURE = False


# class TestingConfig(Config):
#     """Settings for automated tests."""

#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
#     ADMIN_ACCESS_ENABLED = True


# class ProductionConfig(Config):
#     """Production settings."""

#     DEBUG = False
#     JWT_COOKIE_SECURE = True


# config_by_name: dict[str, type[Config]] = {
#     "development": DevelopmentConfig,
#     "testing": TestingConfig,
#     "production": ProductionConfig,
# }


# def get_config_class(config_name: str | None = None) -> type[Config]:
#     """Return a configuration class based on the current environment."""

#     name = (config_name or os.getenv("FLASK_ENV", "development")).strip().lower()
#     return config_by_name.get(name, DevelopmentConfig)


# __all__ = [
#     "Config",
#     "DevelopmentConfig",
#     "TestingConfig",
#     "ProductionConfig",
#     "get_config_class",
# ]

# ```