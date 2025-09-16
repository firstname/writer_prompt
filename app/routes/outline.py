from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models import db, Project, Outline

bp = Blueprint('outline', __name__, url_prefix='/outline')

@bp.route('/<int:project_id>/new', methods=['GET', 'POST'])
def new_outline(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        outline = Outline(
            project_id=project_id,
            title=request.form['title'],
            content=request.form.get('content', ''),
            order=request.form.get('order', 0)
        )
        db.session.add(outline)
        db.session.commit()
        return jsonify({'status': 'success', 'id': outline.id})
    return render_template('outline/new.html', project=project)

@bp.route('/<int:outline_id>/edit', methods=['GET', 'POST'])
def edit_outline(outline_id):
    outline = Outline.query.get_or_404(outline_id)
    if request.method == 'POST':
        outline.title = request.form['title']
        outline.content = request.form.get('content', '')
        outline.order = request.form.get('order', outline.order)
        db.session.commit()
        return jsonify({'status': 'success'})
    return render_template('outline/edit.html', outline=outline)

@bp.route('/<int:outline_id>/delete', methods=['POST'])
def delete_outline(outline_id):
    outline = Outline.query.get_or_404(outline_id)
    db.session.delete(outline)
    db.session.commit()
    return jsonify({'status': 'success'})