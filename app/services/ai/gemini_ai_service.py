from typing import List, Optional, Dict, cast
import google.generativeai as genai
from flask import current_app
import json

from app.services.ai.base_ai_service import BaseAIService

class GeminiAIService(BaseAIService):
    """使用 Google Gemini 的 AI 服务实现"""

    def __init__(self):
        self.api_key: str = cast(str, current_app.config.get('GEMINI_API_KEY'))
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def _generate_content(self, prompt: str) -> Optional[str]:
        """通用的内容生成方法"""
        try:
            response = self.model.generate_content(prompt)
            return response.text if response.text else None
        except Exception as e:
            current_app.logger.error(f"Gemini AI内容生成失败: {str(e)}")
            return None

    async def generate_creative_ideas(self, content: str) -> Optional[List[Dict[str, str]]]:
        """基于灵感生成创意方向"""
        system_prompt = """你是一个专业的创意顾问。你的任务是基于用户提供的灵感，生成10个不同方向的创意构思。
        每个创意都应该包含：
        1. 作品简述（100字以内）
        2. 体裁（如：奇幻小说、科幻小说、现实主义小说等）
        3. 主题（作品想要表达的核心思想）
        4. 创新点（这个创意最与众不同的地方）
        
        要求：
        - 每个创意方向都要具有独特性
        - 创意之间要有足够的差异化
        - 确保主题深度和商业价值的平衡
        - 注意可行性，避免过于天马行空
        - 输出格式为JSON数组，每个创意包含summary, genre, theme, innovation四个字段
        """

        prompt = system_prompt + f"\n\n基于以下灵感，生成10个不同的创意方向：\n{content}"
        try:
            response = await self._generate_content(prompt)
            if not response:
                return None
            return json.loads(response)
        except json.JSONDecodeError as e:
            current_app.logger.error(f"Gemini AI创意生成JSON解析失败: {str(e)}")
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

        prompt = system_prompt + f"\n\n基于以下创意构思，提供完整的基本构思方案：\n{content}"
        return await self._generate_content(prompt)

    async def generate_outline(self, content: str) -> Optional[str]:
        """生成全文大纲"""
        system_prompt = """你是一个专业的小说大纲策划师。你的任务是基于作品的基本构思，生成详细的全文大纲。
        大纲需要包含：
        1. 故事主线概述
        2. 分部规划（建议3-5个部分）
           - 每部分的核心剧情
           - 主要情节线的发展
           - 次要情节线的安排
           - 情感线索的推进
        3. 主要转折点和高潮设置
        4. 伏笔布置计划
        
        要求：
        - 情节发展要符合逻辑
        - 节奏要有张弛变化
        - 各条线索要有机结合
        - 保持悬念和吸引力
        """

        prompt = system_prompt + f"\n\n基于以下基本构思，生成全文大纲：\n{content}"
        return await self._generate_content(prompt)

    async def generate_chapter_outline(self, outline: str, chapter_number: int) -> Optional[List[str]]:
        """生成章节大纲"""
        system_prompt = f"""你是一个专业的小说章节策划师。你的任务是基于全文大纲，详细规划第{chapter_number}章的内容。
        章节大纲需要包含：
        1. 章节目标
           - 推动主线发展的关键点
           - 角色发展的重要节点
           - 信息揭示的关键内容
        2. 场景设计
           - 场景描述
           - 氛围营造
           - 环境细节
        3. 人物互动
           - 关键对话
           - 冲突设置
           - 情感变化
        4. 节奏控制
           - 紧张度变化
           - 叙事节奏
        
        输出要求：
        - 以列表形式输出具体的场景和事件安排
        - 每个场景/事件要有简要说明
        - 确保与整体故事的连贯性
        """

        prompt = system_prompt + f"\n\n基于以下全文大纲，请详细规划第{chapter_number}章：\n{outline}"
        content = await self._generate_content(prompt)
        return content.split('\n') if content else None

    async def generate_section_outline(self, chapter_outline: str, section_number: int) -> Optional[str]:
        """生成段落大纲"""
        system_prompt = f"""你是一个专业的小说细节策划师。你的任务是基于章节大纲，详细规划第{section_number}节的内容。
        段落大纲需要包含：
        1. 段落主旨
           - 核心内容/事件
           - 情感基调
           - 目标效果
        2. 具体场景描写规划
           - 环境描写要点
           - 人物动作细节
           - 心理活动描写
        3. 对话设计
           - 关键对话内容
           - 潜台词安排
           - 言外之意
        4. 文学性设计
           - 修辞手法运用
           - 意象安排
           - 节奏控制
        
        要求：
        - 细节要丰富具体
        - 确保逻辑连贯
        - 注意情感渲染
        - 保持文学性
        """

        prompt = system_prompt + f"\n\n基于以下章节大纲，请详细规划第{section_number}节：\n{chapter_outline}"
        return await self._generate_content(prompt)

    async def generate_section_summary(self, section_outline: str) -> Optional[str]:
        """生成段落概要"""
        system_prompt = """你是一个专业的文学创作助手。你的任务是基于段落大纲，生成一个简洁的段落概要。
        概要需要包含：
        1. 核心事件/内容
        2. 关键场景描写
        3. 主要情感变化
        4. 重要对话要点
        
        要求：
        - 概要应该简明扼要
        - 突出重点内容
        - 保留关键细节
        - 为正文创作提供清晰指导
        """

        prompt = system_prompt + f"\n\n基于以下段落大纲，生成段落概要：\n{section_outline}"
        return await self._generate_content(prompt)

    async def generate_section_content(self, section_summary: str) -> Optional[str]:
        """生成段落正文"""
        system_prompt = """你是一个专业的小说创作者。你的任务是基于段落概要，创作出生动的段落正文。
        正文创作要求：
        1. 文字表现
           - 生动形象的描写
           - 富有感染力的叙述
           - 自然流畅的对话
        2. 细节处理
           - 丰富的环境细节
           - 传神的人物刻画
           - 细腻的心理描写
        3. 艺术性追求
           - 恰当的修辞运用
           - 优美的语言风格
           - 富有韵律感的文字
        
        要求：
        - 符合作品整体风格
        - 感情真挚自然
        - 细节丰富传神
        - 避免说教和刻意
        """

        prompt = system_prompt + f"\n\n基于以下段落概要，创作段落正文：\n{section_summary}"
        return await self._generate_content(prompt)