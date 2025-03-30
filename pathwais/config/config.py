from flask import Flask
from datetime import timedelta
from flask_jwt_extended import JWTManager
from config.extensions import db  
import os
from dotenv import load_dotenv


#-----------------#
#   Constants
#-----------------#

R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_TOKEN_VALUE = os.getenv("R2_TOKEN_VALUE ")

load_dotenv()


def create_app():
    app = Flask(__name__)


    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False  
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  


    db.init_app(app)
    jwt = JWTManager(app)


    from Blueprints.api_bp import api_bp
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app