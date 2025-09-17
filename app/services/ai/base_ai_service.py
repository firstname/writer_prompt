from abc import ABC, abstractmethod
from typing import List, Optional, Dict

class BaseAIService(ABC):
    """AI服务的基类，定义了所有AI服务需要实现的接口"""

    @abstractmethod
    async def generate_creative_ideas(self, content: str) -> Optional[List[Dict[str, str]]]:
        """基于灵感生成创意方向"""
        pass

    @abstractmethod
    async def enhance_basic_concept(self, content: str) -> Optional[str]:
        """完善基本构思"""
        pass

    @abstractmethod
    async def generate_outline(self, content: str) -> Optional[str]:
        """生成全文大纲"""
        pass

    @abstractmethod
    async def generate_chapter_outline(self, outline: str, chapter_number: int) -> Optional[List[str]]:
        """生成章节大纲"""
        pass

    @abstractmethod
    async def generate_section_outline(self, chapter_outline: str, section_number: int) -> Optional[str]:
        """生成段落大纲"""
        pass

    @abstractmethod
    async def generate_section_summary(self, section_outline: str) -> Optional[str]:
        """生成段落概要"""
        pass

    @abstractmethod
    async def generate_section_content(self, section_summary: str) -> Optional[str]:
        """生成段落正文"""
        pass