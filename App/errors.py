import logging
from flask import jsonify, render_template, request
from pydantic import ValidationError
from App.utils.helpers import wants_json

logger = logging.getLogger(__name__)


def register_error_handlers(app):

    @app.errorhandler(400)
    def handle_400(e):
        message = getattr(e, "description", None) or "Bad request"
        if wants_json():
            return jsonify({"error": message}), 400
        return render_template("errors/400.html", message=message), 400

    @app.errorhandler(403)
    def handle_403(e):
        message = getattr(e, "description", None) or "Forbidden"
        if wants_json():
            return jsonify({"error": message}), 403
        return render_template("errors/403.html", message=message), 403

    @app.errorhandler(404)
    def handle_404(e):
        message = getattr(e, "description", None) or "Not found"
        if wants_json():
            return jsonify({"error": message}), 404
        return render_template("errors/404.html", message=message), 404

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        details = [
            {"field": str(err["loc"][-1]) if err["loc"] else "unknown", "message": err["msg"]}
            for err in e.errors()
        ]
        message = "Validation failed: " + ", ".join(f'{d["field"]} - {d["message"]}' for d in details)
        if wants_json():
            return jsonify({"error": message, "details": details}), 400
        return render_template("errors/400.html", message=message), 400

    @app.errorhandler(500)
    def handle_500(e):
        logger.exception("Unhandled exception: %s", e)
        if wants_json():
            return jsonify({"error": "An unexpected error occurred."}), 500
        return render_template("errors/500.html"), 500