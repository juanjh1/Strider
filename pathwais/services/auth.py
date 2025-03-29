from models.auth import User
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies
from flask import  jsonify, make_response
from config.extensions import db  
from sqlalchemy.exc import IntegrityError
from utils.reguex_engeen import RegexPattern
from models.auth import Gender, User, StatusUser

def login_service(request):

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none() 
    if(not RegexPattern.PASSWORD.validate(password) or not RegexPattern.EMAIL.validate(email)):
         return jsonify({"error":["Password or email don't has a correct format"]})
    if(user == None):
          return jsonify({"error":["User not found"]})

    if(not user.check_password(password)):
         return jsonify({"error":["Incorrect password"]})
    access_token = create_access_token(identity=email)
    response = make_response(jsonify(message="Login exitoso"))
    response.set_cookie("access_token_cookie", access_token, httponly=True, secure=True, samesite="Strict")
    return response
    

def register_service(request):
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

        for value, pattern in [
        (email, RegexPattern.EMAIL),
        (password, RegexPattern.PASSWORD),
        (username, RegexPattern.USERNAME),
        (name, RegexPattern.NAME),
        (last_name, RegexPattern.LASTNAME)
        ]:
            if pattern.validate(value) is None:
                return jsonify({"error": "invalid " + pattern.get_field_name()}), 400

        if gender not in [gender.value for gender in Gender]:
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
   

@jwt_required()
def logout_service():
    response = make_response(jsonify(message="Logout successful"))
    unset_jwt_cookies(response)  
    return response