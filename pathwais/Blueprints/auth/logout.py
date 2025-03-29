from flask import Blueprint, request
from services.auth import logout_service
from flask_jwt_extended import jwt_required
logout_bp = Blueprint("logout", __name__, url_prefix='/logout')


@logout_bp.route("/", methods=["GET"])
@jwt_required()
def logout():
     return logout_service( )