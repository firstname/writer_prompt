from flask import Blueprint, render_template, request, jsonify
from app.models import db, Project, Content, Outline

bp = Blueprint('content', __name__, url_prefix='/content')

@bp.route('/<int:project_id>/new', methods=['GET', 'POST'])
def new_content(project_id):
    project = Project.query.get_or_404(project_id)
    outlines = Outline.query.filter_by(project_id=project_id).all()
    
    if request.method == 'POST':
        content = Content(
            project_id=project_id,
            outline_id=request.form.get('outline_id'),
            title=request.form['title'],
            content=request.form.get('content', '')
        )
        db.session.add(content)
        db.session.commit()
        return jsonify({'status': 'success', 'id': content.id})
    return render_template('content/new.html', project=project, outlines=outlines)

@bp.route('/<int:content_id>/edit', methods=['GET', 'POST'])
def edit_content(content_id):
    content = Content.query.get_or_404(content_id)
    outlines = Outline.query.filter_by(project_id=content.project_id).all()
    
    if request.method == 'POST':
        content.outline_id = request.form.get('outline_id')
        content.title = request.form['title']
        content.content = request.form.get('content', '')
        db.session.commit()
        return jsonify({'status': 'success'})
    return render_template('content/edit.html', content=content, outlines=outlines)

@bp.route('/<int:content_id>/delete', methods=['POST'])
def delete_content(content_id):
    content = Content.query.get_or_404(content_id)
    db.session.delete(content)
    db.session.commit()
    return jsonify({'status': 'success'})