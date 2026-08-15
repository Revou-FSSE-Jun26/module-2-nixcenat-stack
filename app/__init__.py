from flask import Flask
from app.config import Config
from app.database import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Impor Blueprint produk dan user
    from app.routes.products import products_bp
    from app.routes.users import users_bp

    # Register Blueprint ke aplikasi
    app.register_blueprint(products_bp)
    app.register_blueprint(users_bp)

    return app
    
