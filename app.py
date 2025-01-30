from flask import Flask
from datetime import timedelta
import os
from extensions import db, jwt, cors
from flask_migrate import Migrate
from routes import auth_routes, landlord_routes, tenant_routes

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boarding_spot.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, 
        origins=[f"http://{os.environ.get('CURRENT_IP')}:5173", f"http://{os.environ.get('CURRENT_IP')}:5174", "http://localhost:5173", "http://localhost:5174"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Content-Type", "Authorization"]
    )
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(landlord_routes.bp)
    app.register_blueprint(tenant_routes.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0') 