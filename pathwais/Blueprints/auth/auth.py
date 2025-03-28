from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

# Registrar blueprints secundarios
from .login import login_bp
from .register import register_bp

auth_bp.register_blueprint(login_bp)
auth_bp.register_blueprint(register_bp)