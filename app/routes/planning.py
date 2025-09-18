from flask import Blueprint, render_template, request, jsonify, current_app
from typing import List, Optional
from app.models import Project
from app.models.planning import InitialIdea, CreativeExpansion, BasicConcept
from app.controllers.planning_controller import PlanningController
from sqlalchemy import desc

bp = Blueprint('project_planning', __name__, url_prefix='/project/<int:project_id>/planning')

@bp.route('/concepts')
def view_concepts(project_id: int):
    """查看项目的所有全文构思"""
    # 获取项目信息
    project = Project.query.get_or_404(project_id)
    
    # 获取所有构思，按创建时间倒序排列
    concepts = BasicConcept.query.filter_by(project_id=project_id).order_by(desc(BasicConcept.created_at)).all()
    
    # 获取每个构思对应的创意发散信息
    for concept in concepts:
        concept.expansion = CreativeExpansion.query.get(concept.creative_expansion_id)
    
    # 获取所有项目用于侧边栏
    projects = Project.query.all()
    
    return render_template(
        'planning/concepts.html',
        project=project,
        concepts=concepts,
        projects=projects
    )

@bp.route('/initial-idea', methods=['GET', 'POST'])
async def initial_idea(project_id: int):
    """初始灵感管理"""
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        current_app.logger.info('Received POST request for initial idea')
        content = request.form.get('content')
        source_type = request.form.get('source_type')
        current_app.logger.info(f'Content: {content}, Source Type: {source_type}')
        
        if not content:
            current_app.logger.warning('No content provided')
            return jsonify({'error': '请输入灵感内容'}), 400
            
        controller = PlanningController()
        idea = await controller.save_initial_idea(project_id, content, source_type)
        if not idea:
            return jsonify({'error': '保存灵感失败'}), 500
            
        return jsonify({
            'status': 'success',
            'id': idea.id
        })
    
    # GET 请求展示表单和列表
    # 获取所有灵感并检查是否有创意发散
    initial_ideas = InitialIdea.query.filter_by(project_id=project_id).order_by(InitialIdea.created_at.desc()).all()
    for idea in initial_ideas:
        # 检查是否有对应的创意发散
        idea.has_expansions = CreativeExpansion.query.filter_by(initial_idea_id=idea.id).first() is not None
    
    # 获取所有项目列表用于侧边栏
    projects = Project.query.all()
    return render_template('project/planning/initial_idea.html',
                         project=project,
                         projects=projects,
                         initial_ideas=initial_ideas)

@bp.route('/initial-idea/<int:idea_id>/creative-expansions', methods=['GET', 'POST'])
async def creative_expansions(project_id: int, idea_id: int):
    """创意发散管理"""
    project = Project.query.get_or_404(project_id)
    initial_idea = InitialIdea.query.get_or_404(idea_id)
    
    if request.method == 'POST':
        current_app.logger.info(f'Received POST request for creative expansions. Idea ID: {idea_id}')
        try:
            controller = PlanningController()
            # 获取已存在的创意
            existing_expansions = CreativeExpansion.query.filter_by(
                initial_idea_id=idea_id
            ).order_by(desc(CreativeExpansion.created_at)).all()
            
            # 生成新的创意
            new_expansions = await controller.generate_creative_expansions(idea_id)
            if not new_expansions:
                return jsonify({'error': '生成创意发散失败，请重试'}), 500
                
            # 返回成功响应
            return jsonify({
                'status': 'success',
                'count': len(new_expansions),
                'new_expansions': [expansion.to_dict() for expansion in new_expansions]
            })
            
            # 生成新的创意
            expansions = await controller.generate_creative_expansions(idea_id)
            if not expansions:
                return jsonify({'error': '生成创意发散失败，请重试'}), 500
                
            return jsonify({
                'status': 'success',
                'count': len(expansions)
            })
        except Exception as e:
            current_app.logger.error(f"创意生成失败: {str(e)}")
            return jsonify({'error': '生成过程发生错误，请重试'}), 500
    
    # GET 请求展示创意列表
    expansions = CreativeExpansion.query.filter_by(
        project_id=project_id,
        initial_idea_id=idea_id
    ).order_by(CreativeExpansion.created_at.desc()).all()
    
    # 获取所有项目列表用于侧边栏
    projects = Project.query.all()
    
    return render_template('project/planning/creative_expansions.html',
                         project=project,
                         projects=projects,
                         initial_idea=initial_idea,
                         expansions=expansions)

@bp.route('/creative-expansion/<int:expansion_id>/select', methods=['POST'])
async def select_expansion(project_id: int, expansion_id: int):
    """选择创意方向"""
    controller = PlanningController()
    expansion = await controller.select_creative_expansion(expansion_id)
    if not expansion:
        return jsonify({'error': '选择创意失败'}), 500
        
    return jsonify({
        'status': 'success',
        'id': expansion.id
    })

@bp.route('/creative-expansion/<int:expansion_id>/basic-concept', methods=['GET', 'POST'])
async def basic_concept(project_id: int, expansion_id: int):
    """作品基本构思"""
    project = Project.query.get_or_404(project_id)
    expansion = CreativeExpansion.query.get_or_404(expansion_id)
    
    if request.method == 'POST':
        if not expansion.is_selected:
            return jsonify({'error': '请先选择该创意方向'}), 400
            
        controller = PlanningController()
        concept = await controller.generate_basic_concept(expansion_id)
        if not concept:
            return jsonify({'error': '生成基本构思失败'}), 500
            
        return jsonify({
            'status': 'success',
            'id': concept.id
        })
    
    # GET 请求展示基本构思
    concept = BasicConcept.query.filter_by(
        project_id=project_id,
        creative_expansion_id=expansion_id
    ).first()
    
    # 获取所有项目列表用于侧边栏
    projects = Project.query.all()
    
    return render_template('project/planning/basic_concept.html',
                         project=project,
                         projects=projects,
                         expansion=expansion,
                         concept=concept)