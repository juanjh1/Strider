from flask import Flask
from datetime import timedelta
from flask_jwt_extended import JWTManager
from config.extensions import db  


def create_app():
    app = Flask(__name__)

    # Configuración
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    # Inicializar extensiones
    db.init_app(app)
    jwt = JWTManager(app)

    # Registrar blueprints
    from Blueprints.api_bp import api_bp
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app