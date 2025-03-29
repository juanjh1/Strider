from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix="/api")

from Blueprints.auth.auth import auth_bp
api_bp.register_blueprint(auth_bp)
