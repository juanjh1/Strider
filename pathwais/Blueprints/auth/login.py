from flask import Blueprint, jsonify, request

from services.auth import login_service
login_bp = Blueprint("login", __name__, url_prefix='/login')

@login_bp.route("/", methods=["POST"])
def login():
     _request= request
     return login_service(_request )