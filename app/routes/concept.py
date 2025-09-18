from flask import (
    Blueprint, jsonify, request, current_app,
    render_template
)
from app.models.planning import BasicConcept, CreativeExpansion
from app.services.ai import get_ai_service
from app import db
from datetime import datetime, timezone

bp = Blueprint('concept', __name__, url_prefix='/concept')

@bp.route('/generate/<int:expansion_id>', methods=['POST'])
async def generate_concept(expansion_id):
    """生成全文构思"""
    try:
        # 获取创意发散
        expansion = CreativeExpansion.query.get_or_404(expansion_id)
        
        # 调用AI服务生成全文构思
        ai_service = get_ai_service()
        concept_data = await ai_service.enhance_basic_concept(expansion.to_dict())
        
        if not concept_data:
            return jsonify({
                'success': False,
                'message': '构思生成失败'
            }), 500
            
        # 创建新的全文构思
        concept = BasicConcept(
            project_id=expansion.project_id,
            creative_expansion_id=expansion_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            **concept_data
        )
        
        # 保存到数据库
        db.session.add(concept)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': concept.to_dict()
        })
        
    except Exception as e:
        current_app.logger.error(f'生成全文构思失败: {str(e)}')
        return jsonify({
            'success': False,
            'message': f'生成全文构思失败: {str(e)}'
        }), 500
        
@bp.route('/<int:concept_id>')
def show_concept(concept_id):
    """显示全文构思"""
    concept = BasicConcept.query.get_or_404(concept_id)
    from app.models import Project
    projects = Project.query.all()
    return render_template('planning/concept.html', concept=concept, projects=projects)