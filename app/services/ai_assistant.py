from typing import List, Optional, Dict
from flask import current_app
import json
from app.services.ai.gemini_ai_service import GeminiAIService
from app.models.planning import CreativeExpansion

class AIAssistant:
    def __init__(self):
        self.ai_service = GeminiAIService()

    async def generate_creative_ideas(self, content: str) -> Optional[List[Dict[str, str]]]:
        """基于初始灵感生成10个创意方向"""
        try:
            return await self.ai_service.generate_creative_ideas(content)
        except Exception as e:
            current_app.logger.error(f"AI创意生成失败: {str(e)}")
            return None

    async def generate_basic_concept(self, expansion: CreativeExpansion) -> Optional[Dict[str, str]]:
        """基于选定的创意方向生成作品基本构思"""
        try:
            content = f"""作品简述：{expansion.summary or ''}
            体裁：{expansion.genre or ''}
            主题：{expansion.theme or ''}
            创新点：{expansion.innovation_points or ''}"""
            
            system_prompt = """你是一个专业的小说创作顾问。你的任务是基于作者的创意，提供完整的基本构思方案。

            请按照以下格式提供 JSON 格式的创作构思方案：
            {
                "world_setting": "详细的世界观设定，包括时代背景、社会环境、特殊规则等",
                "plot_development": "主要情节发展规划，包括核心冲突、重要转折、结局设计等",
                "character_design": "主要人物设定，包括性格特点、成长轨迹、人物关系等",
                "structure_design": "全文结构规划，包括篇幅安排、章节规划等",
                "style_design": "写作风格规划，包括叙事视角、语言特点等",
                "theme_expression": "主题表达方式，包括象征、隐喻等手法运用"
            }

            要求：
            1. 确保每个部分都有具体、可执行的内容
            2. 保持前后统一性和逻辑性
            3. 注重创新性和可读性的平衡
            4. 考虑商业价值和艺术性的结合
            """

            user_prompt = f"基于以下创意构思，给出完整的基本构思方案：\n{content}"
            response = await self.ai_service.enhance_basic_concept(system_prompt + "\n\n" + user_prompt)
            if not response:
                return None
                
            return json.loads(response)

        except Exception as e:
            current_app.logger.error(f"生成基本构思失败: {str(e)}")
            return None

    async def generate_outline(self, basic_concept: str) -> Optional[str]:
        """生成全文大纲"""
        try:
            return await self.ai_service.generate_outline(basic_concept)
        except Exception as e:
            current_app.logger.error(f"生成全文大纲失败: {str(e)}")
            return None

    async def generate_chapter_outline(self, outline: str, chapter_number: int) -> Optional[List[str]]:
        """生成章节大纲"""
        try:
            return await self.ai_service.generate_chapter_outline(outline, chapter_number)
        except Exception as e:
            current_app.logger.error(f"生成章节大纲失败: {str(e)}")
            return None

    async def generate_section_outline(self, chapter_outline: str, section_number: int) -> Optional[str]:
        """生成段落大纲"""
        try:
            return await self.ai_service.generate_section_outline(chapter_outline, section_number)
        except Exception as e:
            current_app.logger.error(f"生成段落大纲失败: {str(e)}")
            return None

    async def generate_section_summary(self, section_outline: str) -> Optional[str]:
        """生成段落概要"""
        try:
            return await self.ai_service.generate_section_summary(section_outline)
        except Exception as e:
            current_app.logger.error(f"生成段落概要失败: {str(e)}")
            return None

    async def generate_section_content(self, section_summary: str) -> Optional[str]:
        """生成段落正文"""
        try:
            return await self.ai_service.generate_section_content(section_summary)
        except Exception as e:
            current_app.logger.error(f"生成段落正文失败: {str(e)}")
            return None