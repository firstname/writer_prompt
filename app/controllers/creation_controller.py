from app.services.ai_assistant import AIAssistant
from app.models.creation import Inspiration, CreativeIdea
from typing import List, Optional
from typing_extensions import TypedDict

class IdeaData(TypedDict, total=False):
    summary: str
    genre: str
    theme: str
    innovation_points: str

class CreationController:
    def __init__(self):
        self.ai_assistant = AIAssistant()

    async def generate_ideas_from_inspiration(self, inspiration_id: int) -> List[str]:
        """根据灵感生成创意方向"""
        inspiration: Optional[Inspiration] = Inspiration.query.get(inspiration_id)
        if not inspiration:
            return []

        # 调用AI助手生成创意
        result: Optional[List[IdeaData]] = await self.ai_assistant.generate_creative_ideas(inspiration)
        if not result:
            return []

        # 将每个创意格式化为文本
        ideas_list: List[str] = []
        for idea_data in result:
            summary = (
                f"{idea_data.get('summary', '')}\n\n"
                f"体裁：{idea_data.get('genre', '')}\n"
                f"主题：{idea_data.get('theme', '')}\n"
                f"创新点：{idea_data.get('innovation_points', '')}"
            )
            ideas_list.append(summary)

        return ideas_list

    async def enhance_creative_idea(self, idea_id: int) -> Optional[str]:
        """完善创意构思"""
        idea = CreativeIdea.query.get(idea_id)
        if not idea:
            return None
        
        # 调用AI助手完善构思
        enhanced_concept = await self.ai_assistant.enhance_basic_concept(idea)
        if isinstance(enhanced_concept, str):
            return enhanced_concept
        return None

    async def generate_full_outline(self, concept_id: int) -> Optional[str]:
        """生成全文大纲"""
        # TODO: 实现全文大纲生成逻辑
        pass

    async def generate_chapter_outlines(self, outline_id: int) -> Optional[List[str]]:
        """生成章节大纲"""
        # TODO: 实现章节大纲生成逻辑
        pass

    async def generate_section_outlines(self, chapter_id: int) -> Optional[List[str]]:
        """生成分节大纲"""
        # TODO: 实现分节大纲生成逻辑
        pass

    async def generate_content_summary(self, section_id: int) -> Optional[str]:
        """生成内容概要"""
        # TODO: 实现内容概要生成逻辑
        pass

    async def generate_final_content(self, summary_id: int) -> Optional[str]:
        """生成最终内容"""
        # TODO: 实现最终内容生成逻辑
        pass