from typing import Any, Dict, List, Optional, Literal, cast
from anthropic import Anthropic, APIConnectionError, APIStatusError
from anthropic.types import MessageParam, TextBlock
from flask import current_app
import json



from app.services.ai.base_ai_service import BaseAIService

Role = Literal['user', 'assistant']

class UserMessage:
    def __init__(self, content: str):
        self.role: Role = 'user'
        self.content = content
        
    def to_dict(self) -> MessageParam:
        return {'role': self.role, 'content': self.content}

class ClaudeAIService(BaseAIService):
    """使用 Anthropic Claude 的 AI 服务实现"""

    def __init__(self):
        self.api_key: str = cast(str, current_app.config.get('CLAUDE_API_KEY', ''))
        self.client: Anthropic = Anthropic(api_key=self.api_key)

    async def generate_creative_ideas(self, content: str) -> Optional[List[Dict[str, str]]]:
        """基于灵感生成创意方向"""
        system_prompt = """你是一个专业的创意顾问。你的任务是基于用户提供的灵感，生成10个不同方向的创意构思。
        每个创意都应该包含：
        1. 作品简述（100字以内）
        2. 体裁（如：奇幻小说、科幻小说、现实主义小说等）
        3. 主题（作品想要表达的核心思想）
        4. 创新点（这个创意最与众不同的地方）
        
        要求：
        - 保持对原始灵感的忠实，但要有创新性的延伸
        - 每个创意方向都要足够独特
        - 注重可行性和吸引力的平衡
        - 用简洁明了的语言表达
        
        请用JSON格式返回结果，每个创意包含：summary（简述）, genre（体裁）, theme（主题）, innovation_points（创新点）
        """

        try:
            message = UserMessage(
                system_prompt + f"\n\n基于以下灵感，生成10个不同的创意方向：\n{content}"
            )

            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[message.to_dict()]
            )
            
            content_block = response.content[0]
            if isinstance(content_block, TextBlock):
                ideas: List[Dict[str, str]] = json.loads(content_block.text)
                return ideas
            return None

        except (APIConnectionError, APIStatusError, json.JSONDecodeError) as e:
            current_app.logger.error(f"Claude AI创意生成失败: {str(e)}")
            return None

    async def enhance_basic_concept(self, content: str) -> Optional[str]:
        """完善基本构思"""
        system_prompt = """你是一个专业的小说创作顾问。你的任务是帮助作者完善作品的基本构思。
        你需要基于作者的创意构思，提供以下方面的具体建议和构思：
        1. 世界观设定：构建完整的故事背景
        2. 故事框架：确定核心冲突、主要情节发展、转折点
        3. 人物系统：设计主要人物性格、关系网络、成长轨迹
        4. 叙事策略：确定叙事视角、时间线处理、节奏控制
        5. 主题表达：设计主题的呈现方式和层次
        
        注意平衡以下要素：
        - 创新性与可行性
        - 深度与可读性
        - 艺术性与商业性
        """

        try:
            message = UserMessage(
                system_prompt + f"\n\n基于以下创意构思，提供完整的基本构思方案：\n{content}"
            )

            message = UserMessage(
                system_prompt + f"\n\n基于以下创意构思，提供完整的基本构思方案：\n{content}"
            )

            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[message.to_dict()]
            )
            
            content_block = response.content[0]
            if isinstance(content_block, TextBlock):
                return content_block.text
            return None

        except (APIConnectionError, APIStatusError) as e:
            current_app.logger.error(f"Claude AI构思完善失败: {str(e)}")
            return None

    async def generate_outline(self, content: str) -> Optional[str]:
        """生成全文大纲"""
        # TODO: 实现全文大纲生成
        pass

    async def generate_chapter_outline(self, outline: str, chapter_number: int) -> Optional[List[str]]:
        """生成章节大纲"""
        # TODO: 实现章节大纲生成
        pass

    async def generate_section_outline(self, chapter_outline: str, section_number: int) -> Optional[str]:
        """生成段落大纲"""
        # TODO: 实现段落大纲生成
        pass

    async def generate_section_summary(self, section_outline: str) -> Optional[str]:
        """生成段落概要"""
        # TODO: 实现段落概要生成
        pass

    async def generate_section_content(self, section_summary: str) -> Optional[str]:
        """生成段落正文"""
        # TODO: 实现段落正文生成
        pass