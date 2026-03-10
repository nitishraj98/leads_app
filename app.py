from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config.settings import SECRET_KEY, DEFAULT_RATE_LIMIT, SUBMIT_RATE_LIMIT
from db.database import init_db
from routes.index import index_bp
from routes.submit import submit_bp
from routes.leads import leads_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    # Extensions
    CORS(app)
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[DEFAULT_RATE_LIMIT],
        storage_uri="memory://"
    )
    # Apply the stricter limit to the submit endpoint
    limiter.limit(SUBMIT_RATE_LIMIT)(submit_bp)

    # Blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(submit_bp)
    app.register_blueprint(leads_bp)
    
    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return jsonify({
            "success": False,
            "message": f"Rate limit exceeded. Try again later.",
            "retry_after": e.description,
        }), 429

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Endpoint not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"success": False, "message": "Method not allowed."}), 405

    return app


if __name__ == "__main__":
    init_db()
    app = create_app()
    app.run(debug=True, port=5000)
