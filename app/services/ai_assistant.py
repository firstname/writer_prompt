from typing import List, Optional, Dict
from flask import current_app
import json
from datetime import datetime
from app.models.creation import Inspiration, CreativeIdea
from app.services.ai.gemini_ai_service import GeminiAIService

class AIAssistant:
    def __init__(self):
        self.ai_service = GeminiAIService()

    async def generate_creative_ideas(self, inspiration: Inspiration) -> Optional[List[Dict[str, str]]]:
        """基于灵感生成创意方向"""
        try:
            content = f"""灵感内容：{inspiration.content}
            灵感来源：{inspiration.source_type or '未指定'}
            灵感标签：{inspiration.tags or '无标签'}"""
            
            return await self.ai_service.generate_creative_ideas(content)

        except Exception as e:
            current_app.logger.error(f"AI创意生成失败: {str(e)}")
            return None

    async def enhance_basic_concept(self, idea: CreativeIdea) -> Optional[str]:
        """完善基本构思"""
        try:
            content = f"""作品简述：{idea.summary or ''}
            体裁：{idea.genre or ''}
            主题：{idea.theme or ''}
            创新点：{idea.innovation_points or ''}"""
            
            return await self.ai_service.enhance_basic_concept(content)

        except Exception as e:
            current_app.logger.error(f"AI构思完善失败: {str(e)}")
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