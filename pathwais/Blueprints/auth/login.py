from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from config.extensions import db
from models.auth import User
from utils.reguex_engeen import ReguexPatter
login_bp = Blueprint("login", __name__, url_prefix='/login')

@login_bp.route("/", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none() 
    if(not ReguexPatter.PASSWORD.validate(password) or not ReguexPatter.EMAIL.validate(email)):
         return jsonify({"error":["Password or email don't has a correct format"]})
    if(user == None):
          return jsonify({"error":["User not found"]})

    if(not user.check_password(password)):
         return jsonify({"error":["Incorrect password"]})
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)