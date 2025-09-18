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
            # 将CreativeExpansion对象转换为字典
            expansion_dict = {
                'summary': expansion.summary or '',
                'genre': expansion.genre or '',
                'theme': expansion.theme or '',
                'innovation_points': expansion.innovation_points or ''
            }
            
            # 调用AI服务生成基本构思
            concept_dict = await self.ai_service.enhance_basic_concept(expansion_dict)
            if not concept_dict:
                return None
                
            return concept_dict

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