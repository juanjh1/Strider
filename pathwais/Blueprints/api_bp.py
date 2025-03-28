from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix="/api")

# Registrar blueprints secundarios
from Blueprints.auth.auth import auth_bp
api_bp.register_blueprint(auth_bp)
