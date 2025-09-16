from flask import Blueprint, render_template, jsonify, request
from app.models import Project

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)