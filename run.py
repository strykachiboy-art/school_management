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
# git commit -m "Your descriptive message here" 
# flask db migrate -m "drop unused teacher.subject column"
# flask db upgrade



# // Frontend JavaScript
# async function updateProfile(data) {
#     const token = localStorage.getItem('jwt_token'); // Or wherever you store it

#     try {
#         const response = await fetch('/api/profile', {
#             method: 'PUT',
#             headers: {
#                 'Content-Type': 'application/json',
#                 'Authorization': `Bearer ${token}` // Passing the JWT
#             },
#             body: JSON.stringify(data)
#         });

#         // 1. Handle Authentication Failures (Redirect to Login)
#         if (response.status === 401) {
#             console.warn("Session expired. Booting to login...");
#             localStorage.removeItem('jwt_token'); // Clean up
#             window.location.href = '/login';      // JS handles the redirect!
#             return;
#         }

#         // 2. Handle Business Logic Errors (Show messages, stay on page)
#         if (response.status === 400) {
#             const errorData = await response.json();
#             alert(`Oops: ${errorData.message}`);
#             return;
#         }

#         // 3. Handle Success (Update UI or redirect to a dashboard)
#         if (response.ok) {
#             const responseData = await response.json();
#             console.log("Success!", responseData);
#             // JS can redirect the user after success:
#             window.location.href = '/dashboard'; 
#         }

#     } catch (error) {
#         console.error("Network error:", error);
#     }
# }