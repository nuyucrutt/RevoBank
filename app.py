from flask import Flask
from flask_migrate import Migrate
from src.models import db
import os
from dotenv import load_dotenv
import pymysql

pymysql.install_as_MySQLdb()

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # Configure database
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3307')
    db_user = os.getenv('DB_USER', 'revolut_user')
    db_pass = os.getenv('DB_PASS', 'revolut_pass')
    db_name = os.getenv('DB_NAME', 'revolut')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset=utf8mb4'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 3600
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints/routes
    from src.routes import user_bp, account_bp, transaction_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transaction_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
