from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main, project, outline, content, creation
    app.register_blueprint(main.bp)
    app.register_blueprint(project.bp)
    app.register_blueprint(outline.bp)
    app.register_blueprint(content.bp)
    app.register_blueprint(creation.bp)

    return app