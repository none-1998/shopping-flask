from flask import Flask
from config import Config
from app.extensions import db, csrf  # ایمپورت db از extensions نه از app
from app.routes.products import products_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    app.register_blueprint(products_bp)

    return app

