from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from config.extensions import db  
from utils.reguex_engeen import ReguexPatter
from models.auth import Gender, User, StatusUser

register_bp = Blueprint("register", __name__, url_prefix='/register')

@register_bp.route("/", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return jsonify({"status_user": [gender.value for gender in Gender]}), 200

    if request.method == "POST":
        username = request.json.get("username")
        name = request.json.get("name")
        last_name = request.json.get("last_name")
        password = request.json.get("password")
        email = request.json.get("email")
        gender = request.json.get("gender")
        status_user = db.session.execute(db.select(StatusUser).filter_by(name="active")).scalar_one()

        if(not ReguexPatter.EMAIL.validate(email) ):
                  return jsonify({"error": "Invalid email"}), 400
        if(not ReguexPatter.PASSWORD.validate(password)):
                 return jsonify({"error": "Invalid password"}), 400
        if(not ReguexPatter.USERNAME.validate(password)):
                 return jsonify({"error": "Invalid password"}), 400
        if( gender not in  [gender.value  for gender in Gender]):
                return jsonify({"error": "Invalid gender"}), 400


        
        try:
            user = User(
                username=username,
                name=name,
                last_name=last_name,
                email=email,
                gender=Gender[gender],
                status_id = status_user.id
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        except  IntegrityError as e :
            db.session.rollback() 
            return jsonify({"error": e._message() }), 400


        return jsonify({"message": "User registered successfully"}), 201
