from flask import jsonify, render_template
from pydantic import ValidationError
from App.utils.helpers import wants_json


def register_error_handlers(app):

    @app.errorhandler(400)
    def handle_400(e):
        message = e.description if hasattr(e, "description") else "Bad request"
        if wants_json():
            return jsonify({"error": message}), 400
        return render_template("errors/400.html", message=message), 400

    @app.errorhandler(404)
    def handle_404(e):
        message = e.description if getattr(e, "description", None) else "Not found"
        if wants_json():
            return jsonify({"error": message}), 404
        return render_template("errors/404.html", message=message), 404

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
         field_names = [str(err["loc"][-1]) if err["loc"] else err["msg"] for err in e.errors()]
         message = "Validation failed: " + ", ".join(field_names)
         if wants_json():
             return jsonify({"error": message}), 400
         return render_template("errors/400.html", message=message), 400

    @app.errorhandler(500)
    def handle_500(e):
        if wants_json():
            return jsonify({"error": "An unexpected error occurred."}), 500
        return render_template("errors/500.html"), 500