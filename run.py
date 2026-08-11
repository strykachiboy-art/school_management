from dotenv import load_dotenv
load_dotenv()

from App.config import get_config_class
from flask import Flask
from flask_migrate import Migrate
from App.extensions import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config_class())
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from App import models
    return app



# $env:FLASK_APP = "run.py"
# flask shell
# git commit -am "Your descriptive message here" 