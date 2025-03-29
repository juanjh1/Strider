from flask import Blueprint,request
from services.auth import register_service
register_bp = Blueprint("register", __name__, url_prefix='/register')

@register_bp.route("/", methods=["POST", "GET"])
def register():
    _request = request
    return register_service(_request)
