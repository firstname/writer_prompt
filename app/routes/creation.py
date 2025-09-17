from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory
from typing import List, Optional
from app.models import db, Project
from app.models.creation import Inspiration, InspirationMaterial, CreativeIdea
from app.controllers.creation_controller import CreationController
import os

bp = Blueprint('creation', __name__, url_prefix='/project/<int:project_id>/creation')

@bp.route('/inspiration', methods=['GET', 'POST'])
def inspiration(project_id: int):
    project: Project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        inspiration: Inspiration = Inspiration(
            project_id=project_id,
            content=request.form['content'],
            source_type=request.form['source_type'],
            tags=request.form['tags']
        )
        db.session.add(inspiration)
        db.session.commit()
        
        # 处理上传的材料
        if 'materials' in request.files:
            files = request.files.getlist('materials')
            for file in files:
                if file.filename:
                    filename: str = f"{inspiration.id}_{file.filename}"
                    file_path: str = os.path.join(str(current_app.config['UPLOAD_FOLDER']), filename)
                    file.save(file_path)
                    
                    material: InspirationMaterial = InspirationMaterial(
                        inspiration_id=inspiration.id,
                        file_path=filename,
                        file_type=file.content_type,
                        description=request.form.get('material_description', '')
                    )
                    db.session.add(material)
            db.session.commit()
            
        return jsonify({'status': 'success', 'id': inspiration.id})
    
    projects: List[Project] = Project.query.all()  # 为侧边栏准备数据
    inspirations: List[Inspiration] = Inspiration.query.filter_by(project_id=project_id).all()
    return render_template('project/creation/inspiration.html', 
                         project=project, 
                         projects=projects,
                         inspirations=inspirations)

@bp.route('/inspiration/<int:inspiration_id>/material/<filename>')
def get_inspiration_material(project_id: int, inspiration_id: int, filename: str):
    material: InspirationMaterial = InspirationMaterial.query.filter_by(inspiration_id=inspiration_id, file_path=filename).first_or_404()
    return send_from_directory(str(current_app.config['UPLOAD_FOLDER']), filename)

@bp.route('/generate_ideas', methods=['POST'])
async def generate_ideas(project_id: int):
    inspiration_id: Optional[str] = request.form.get('inspiration_id')
    if not inspiration_id:
        return jsonify({'error': 'Missing inspiration_id'}), 400
        
    inspiration: Optional[Inspiration] = Inspiration.query.get(int(inspiration_id))
    if not inspiration:
        return jsonify({'error': 'Inspiration not found'}), 404
        
    controller: CreationController = CreationController()
    ideas: List[str] = await controller.generate_ideas_from_inspiration(inspiration.id)
    
    return jsonify({'ideas': ideas if ideas else []})

@bp.route('/creative', methods=['GET', 'POST'])
def creative(project_id: int):
    project: Project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        # 手动创建创意
        inspiration_id: Optional[str] = request.form.get('inspiration_id')
        idea: CreativeIdea = CreativeIdea(
            project_id=project_id,
            inspiration_id=int(inspiration_id) if inspiration_id else None,
            summary=request.form['summary'],
            genre=request.form.get('genre', ''),
            theme=request.form.get('theme', ''),
            innovation_points=request.form.get('innovation_points', ''),
            score=float(request.form.get('score', 0))
        )
        db.session.add(idea)
        db.session.commit()
        return jsonify({'status': 'success', 'id': idea.id})
    
    projects: List[Project] = Project.query.all()  # 为侧边栏准备数据
    inspirations: List[Inspiration] = Inspiration.query.filter_by(project_id=project_id).all()
    ideas: List[CreativeIdea] = CreativeIdea.query.filter_by(project_id=project_id).all()
    return render_template('project/creation/creative.html', 
                         project=project,
                         projects=projects,
                         inspirations=inspirations,
                         ideas=ideas)