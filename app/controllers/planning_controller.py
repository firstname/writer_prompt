from typing import List, Optional, Dict
from flask import current_app
from app.models import db
from app.models.planning import InitialIdea, CreativeExpansion, BasicConcept
from app.services.ai_assistant import AIAssistant

class PlanningController:
    """作品规划控制器"""
    
    def __init__(self):
        self.ai_assistant = AIAssistant()
    
    async def save_initial_idea(self, project_id: int, content: str, source_type: str) -> Optional[InitialIdea]:
        """保存初始灵感"""
        try:
            idea = InitialIdea(
                project_id=project_id,
                content=content,
                source_type=source_type
            )
            db.session.add(idea)
            db.session.commit()
            return idea
        except Exception as e:
            current_app.logger.error(f"保存初始灵感失败: {str(e)}")
            db.session.rollback()
            return None
            
    async def generate_creative_expansions(self, idea_id: int) -> Optional[List[CreativeExpansion]]:
        """基于初始灵感生成创意发散"""
        try:
            current_app.logger.info(f'Generating creative expansions for idea {idea_id}')
            initial_idea = InitialIdea.query.get(idea_id)
            if not initial_idea:
                current_app.logger.error(f'Initial idea {idea_id} not found')
                return None
                
            # 调用AI生成创意发散
            creative_ideas = await self.ai_assistant.generate_creative_ideas(initial_idea.content)
            if not creative_ideas:
                return None
            
            # 保存创意发散结果
            expansions = []
            for idea in creative_ideas:
                expansion = CreativeExpansion(
                    project_id=initial_idea.project_id,
                    initial_idea_id=initial_idea.id,
                    summary=idea.get('summary'),
                    genre=idea.get('genre'),
                    theme=idea.get('theme'),
                    innovation_points=idea.get('innovation')  # 修复字段名称匹配
                )
                db.session.add(expansion)
                expansions.append(expansion)
            
            db.session.commit()
            return expansions
            
        except Exception as e:
            current_app.logger.error(f"生成创意发散失败: {str(e)}")
            db.session.rollback()
            return None
            
    async def select_creative_expansion(self, expansion_id: int) -> Optional[CreativeExpansion]:
        """选择一个创意方向作为最终创意"""
        try:
            expansion = CreativeExpansion.query.get(expansion_id)
            if not expansion:
                return None
                
            # 将同一项目下的其他创意都设为未选中
            CreativeExpansion.query.filter_by(
                project_id=expansion.project_id
            ).update({'is_selected': False})
            
            # 将当前创意设为选中
            expansion.is_selected = True
            db.session.commit()
            return expansion
            
        except Exception as e:
            current_app.logger.error(f"选择创意失败: {str(e)}")
            db.session.rollback()
            return None
            
    async def generate_basic_concept(self, expansion_id: int) -> Optional[BasicConcept]:
        """基于选中的创意生成作品基本构思"""
        try:
            expansion = CreativeExpansion.query.get(expansion_id)
            if not expansion or not expansion.is_selected:
                return None
                
            # 调用AI生成基本构思
            concept_dict = await self.ai_assistant.generate_basic_concept(expansion)
            if not concept_dict:
                return None
            
            # 保存基本构思
            concept = BasicConcept(
                project_id=expansion.project_id,
                creative_expansion_id=expansion.id,
                world_setting=concept_dict.get('world_setting'),
                plot_development=concept_dict.get('plot_development'),
                character_design=concept_dict.get('character_design'),
                structure_design=concept_dict.get('structure_design'),
                style_design=concept_dict.get('style_design'),
                theme_expression=concept_dict.get('theme_expression')
            )
            
            db.session.add(concept)
            db.session.commit()
            return concept
            
        except Exception as e:
            current_app.logger.error(f"生成基本构思失败: {str(e)}")
            db.session.rollback()
            return None