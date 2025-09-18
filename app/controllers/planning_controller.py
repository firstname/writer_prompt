from typing import List, Optional, Dict, Any, Union
import json
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
            
            def serialize_value(value: Union[Dict[str, Any], Any]) -> Optional[str]:
                """Helper to serialize values to string format if they're dictionaries"""
                if isinstance(value, dict):
                    return json.dumps(value, ensure_ascii=False)
                return str(value) if value is not None else None

            # 保存基本构思，确保所有字段都被序列化为字符串
            concept = BasicConcept(
                project_id=expansion.project_id,
                creative_expansion_id=expansion.id,
                
                # 世界观设定
                world_setting=serialize_value(concept_dict.get('world_setting')),
                culture_background=serialize_value(concept_dict.get('culture_background')),
                special_elements=serialize_value(concept_dict.get('special_elements')),
                
                # 故事架构
                core_conflict=serialize_value(concept_dict.get('core_conflict')),
                plot_outline=serialize_value(concept_dict.get('plot_outline')),
                subplot_design=serialize_value(concept_dict.get('subplot_design')),
                key_events=serialize_value(concept_dict.get('key_events')),
                plot_progression=serialize_value(concept_dict.get('plot_progression')),
                
                # 人物系统
                main_characters=serialize_value(concept_dict.get('main_characters')),
                supporting_characters=serialize_value(concept_dict.get('supporting_characters')),
                character_relationships=serialize_value(concept_dict.get('character_relationships')),
                character_arcs=serialize_value(concept_dict.get('character_arcs')),
                
                # 主题与深度
                theme_design=serialize_value(concept_dict.get('theme_design')),
                philosophical_elements=serialize_value(concept_dict.get('philosophical_elements')),
                social_commentary=serialize_value(concept_dict.get('social_commentary')),
                symbolic_system=serialize_value(concept_dict.get('symbolic_system')),
                
                # 叙事策略
                narrative_perspective=serialize_value(concept_dict.get('narrative_perspective')),
                timeline_structure=serialize_value(concept_dict.get('timeline_structure')),
                pacing_design=serialize_value(concept_dict.get('pacing_design')),
                foreshadowing=serialize_value(concept_dict.get('foreshadowing')),
                
                # 写作风格
                writing_style=serialize_value(concept_dict.get('writing_style')),
                language_features=serialize_value(concept_dict.get('language_features')),
                atmosphere_building=serialize_value(concept_dict.get('atmosphere_building')),
                literary_devices=serialize_value(concept_dict.get('literary_devices')),
                
                # 规划信息
                chapter_structure=serialize_value(concept_dict.get('chapter_structure')),
                volume_planning=serialize_value(concept_dict.get('volume_planning')),
                word_count_target=int(concept_dict.get('word_count_target', 0)),
                estimated_chapters=int(concept_dict.get('estimated_chapters', 0))
            )
            
            db.session.add(concept)
            db.session.commit()
            return concept
            
        except Exception as e:
            current_app.logger.error(f"生成基本构思失败: {str(e)}")
            db.session.rollback()
            return None