from flask import Flask
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from typing import Optional

db = SQLAlchemy()
migrate = Migrate()

def nl2br(value: Optional[str]) -> str:
    """Convert newlines to <br> tags."""
    if not value:
        return ""
    return value.replace('\n', Markup('<br>\n'))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # 注册自定义过滤器
    app.jinja_env.filters['nl2br'] = nl2br

    from app.routes import main, project, outline, content, planning, concept
    app.register_blueprint(main.bp)
    app.register_blueprint(project.bp)
    app.register_blueprint(outline.bp)
    app.register_blueprint(content.bp)
    app.register_blueprint(planning.bp)
    app.register_blueprint(concept.bp)

    return app