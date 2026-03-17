from flask import Flask
from flask_cors import CORS
from app.routes.health import health_bp
from app.routes.transcriptions import transcriptions_bp
from app.routes.search import search_bp
from app.database.schema import init_db


def create_app():
    app = Flask(__name__)

    CORS(app)

    init_db()

    app.register_blueprint(health_bp)
    app.register_blueprint(transcriptions_bp)
    app.register_blueprint(search_bp)

    return app
