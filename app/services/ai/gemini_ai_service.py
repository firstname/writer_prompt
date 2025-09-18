from typing import Any, Dict, List, Optional, TypeVar, Union, cast
import google.generativeai as genai  # type: ignore
from flask import current_app
import json
from typing_extensions import TypeAlias

from app.services.ai.base_ai_service import BaseAIService

T = TypeVar('T')
JSONValue: TypeAlias = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JSONObject: TypeAlias = Dict[str, JSONValue]
JSONList: TypeAlias = List[JSONObject]

class GeminiAIService(BaseAIService):
    api_key: Optional[str]
    model: Any  # Using Any since we can't properly type hint the GenerativeModel
    
    def __init__(self) -> None:
        """初始化 Gemini AI 服务"""
        # 从配置中获取API密钥
        api_key = current_app.config.get('GEMINI_API_KEY', '')  # type: ignore
        if not api_key:
            raise ValueError("Gemini API key not found in configuration")
        
        try:
            # 初始化Google AI配置和模型
            genai.configure(api_key=api_key)  # type: ignore
            self.model = genai.GenerativeModel('gemini-2.5-pro')  # type: ignore
            self.api_key = api_key
            current_app.logger.info("Initialized Gemini AI service with model: gemini-2.5-pro")
        except Exception as e:
            current_app.logger.error(f"Failed to initialize Gemini AI service: {str(e)}")
            raise

    def _validate_concept_data(self, concept_data: Dict[str, Any]) -> None:
        """验证生成的概念数据的有效性"""
        required_fields = [
            "world_setting", "culture_background", "special_elements",
            "core_conflict", "plot_outline", "subplot_design",
            "key_events", "plot_progression", "main_characters",
            "supporting_characters", "character_relationships",
            "character_arcs", "theme_design", "philosophical_elements",
            "social_commentary", "symbolic_system", "narrative_perspective",
            "timeline_structure", "pacing_design", "foreshadowing",
            "writing_style", "language_features", "atmosphere_building",
            "literary_devices", "chapter_structure", "volume_planning",
            "word_count_target", "estimated_chapters"
        ]
        
        for field in required_fields:
            if field not in concept_data:
                raise ValueError(f"缺少必要字段: {field}")

    def _process_concept_data(self, concept_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理生成的概念数据"""
        # 确保所有字段都被转换为字符串（除了整数字段）
        str_fields = [
            "world_setting", "culture_background", "special_elements",
            "core_conflict", "plot_outline", "subplot_design",
            "key_events", "plot_progression", "main_characters",
            "supporting_characters", "character_relationships",
            "character_arcs", "theme_design", "philosophical_elements",
            "social_commentary", "symbolic_system", "narrative_perspective",
            "timeline_structure", "pacing_design", "foreshadowing",
            "writing_style", "language_features", "atmosphere_building",
            "literary_devices", "chapter_structure", "volume_planning"
        ]
        
        for field in str_fields:
            if isinstance(concept_data.get(field), (dict, list)):
                concept_data[field] = json.dumps(concept_data[field], ensure_ascii=False)
            elif not isinstance(concept_data.get(field), str):
                concept_data[field] = str(concept_data.get(field, ''))
                
        # 确保整数字段是整数
        int_fields = ["word_count_target", "estimated_chapters"]
        for field in int_fields:
            try:
                concept_data[field] = int(concept_data.get(field, 0))
            except (TypeError, ValueError):
                concept_data[field] = 0
                
        return concept_data

    async def generate_concept(self, prompt: str) -> Optional[Dict[str, Any]]:
        """生成全文构思"""
        response = await self._generate_content(prompt, "全文构思生成")
        if not response:
            return None
            
        try:
            # 尝试清理响应文本，移除可能的前后缀
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # 将所有行尾的换行符移除，确保JSON格式正确
            cleaned_response = cleaned_response.replace('\n', ' ').replace('\r', '')
            # 去除多余的空格
            cleaned_response = ' '.join(cleaned_response.split())
            
            # 尝试预验证JSON格式
            try:
                # 先尝试解析一次，如果失败就记录错误的具体位置
                json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                current_app.logger.error(f"JSON预验证失败: {str(e)}")
                current_app.logger.error(f"错误位置附近的内容: {cleaned_response[max(0, e.pos-50):min(len(cleaned_response), e.pos+50)]}")
                raise

            current_app.logger.info(f"清理后的JSON响应: {cleaned_response[:200]}...")
            
            # 解析JSON
            concept_data = json.loads(cleaned_response)
            # 验证必要字段
            self._validate_concept_data(concept_data)
            # 处理字段数据类型
            processed_data = self._process_concept_data(concept_data)
            return processed_data
            
        except json.JSONDecodeError as e:
            current_app.logger.error(f"解析JSON失败: {str(e)}")
            return None
        except ValueError as e:
            current_app.logger.error(f"概念数据验证失败: {str(e)}")
            return None
        except Exception as e:
            current_app.logger.error(f"处理概念数据时发生未知错误: {str(e)}")
            return None
            # 尝试解析一次，如果失败就记录错误的具体位置
            json.loads(cleaned_response)

            current_app.logger.info(f"清理后的JSON响应: {cleaned_response[:200]}...")

            # 解析JSON
            concept_data = json.loads(cleaned_response)

    async def _generate_content(self, prompt: str, feature_name: str = "未指定功能") -> Optional[str]:
        """生成内容的通用方法"""
        import time
        from datetime import datetime

        start_time = time.time()
        try:
            # 记录请求开始
            request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            current_app.logger.info(
                f"\n{'='*80}\n"
                f"AI请求开始 - {feature_name}\n"
                f"时间: {request_time}\n"
                f"模型: gemini-2.5-pro\n"
                f"提示词长度: {len(prompt)} 字符\n"
                f"提示词前200字符: {prompt[:200]}...\n"
                f"{'='*80}"
            )

            # 生成内容
            response = self.model.generate_content(prompt)
            
            # 计算用时
            end_time = time.time()
            duration = end_time - start_time
            
            # 获取响应文本
            response_text = response.text if response and hasattr(response, 'text') else None
            
            # 记录响应结果
            current_app.logger.info(
                f"\n{'='*80}\n"
                f"AI响应完成 - {feature_name}\n"
                f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"用时: {duration:.2f} 秒\n"
                f"响应长度: {len(response_text) if response_text else 0} 字符\n"
                f"响应内容前200字符: {response_text[:200] if response_text else 'None'}...\n"
                f"{'='*80}"
            )
            
            return response_text
            
        except Exception as e:
            # 记录错误信息
            current_app.logger.error(
                f"\n{'='*80}\n"
                f"AI请求失败 - {feature_name}\n"
                f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"错误类型: {type(e).__name__}\n"
                f"错误信息: {str(e)}\n"
                f"提示词: {prompt}\n"
                f"{'='*80}"
            )
            return None

    async def generate_creative_ideas(self, content: str) -> Optional[List[Dict[str, str]]]:
        """基于灵感生成创意方向"""
        system_prompt = """你是一个专业的创意顾问。你的任务是基于用户提供的灵感，生成5个不同方向的创意构思。
        请以下面的JSON格式返回结果（注意：必须是可解析的JSON格式，不要添加额外的解释文字）：

        [
            {
                "summary": "作品简述（100字以内）",
                "genre": "体裁（如：奇幻小说、科幻小说等）",
                "theme": "主题（作品想要表达的核心思想）",
                "innovation": "创新点（这个创意最与众不同的地方）"
            },
            ...（重复5次）
        ]

        要求：
        1. 每个创意方向必须独特，彼此有显著差异
        2. 确保主题深度和商业价值的平衡
        3. 保持可行性，避免过于天马行空
        4. 严格按照示例的JSON格式输出
        5. 不要在JSON前后添加任何额外的文字说明
        """

        prompt = system_prompt + f"\n\n基于以下灵感，生成5个不同的创意方向：\n{content}"
        response = None  # 初始化response变量
        try:
            response = await self._generate_content(prompt, "创意发散生成")
            if not response:
                current_app.logger.error("Gemini AI返回空响应")
                return None

            # 尝试清理响应文本，移除可能的前后缀
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()

            current_app.logger.info(f"清理后的JSON响应: {cleaned_response[:200]}...")
            
            result = json.loads(cleaned_response)
            if not isinstance(result, list):
                raise ValueError("响应不是JSON数组格式")
            
            # 验证和转换结果格式
            validated_result: List[Dict[str, str]] = []
            json_result = cast(JSONList, result)
            
            for item_dict in json_result:
                # 创建新的字典，确保所有值都是字符串
                idea_item = {
                    'summary': str(item_dict.get('summary', '')),
                    'genre': str(item_dict.get('genre', '')),
                    'theme': str(item_dict.get('theme', '')),
                    'innovation': str(item_dict.get('innovation', ''))
                }
                validated_result.append(idea_item)
            
            return validated_result
            
        except json.JSONDecodeError as e:
            current_app.logger.error(f"Gemini AI创意生成JSON解析失败: {str(e)}")
            current_app.logger.error(f"原始响应: {response[:200] if response else 'None'}")
            return None
        except Exception as e:
            current_app.logger.error(f"Gemini AI创意生成过程出错: {str(e)}")
            return None

    async def enhance_basic_concept(self, expansion: Dict[str, str]) -> Optional[Dict[str, str]]:
        """生成全文构思"""
        system_prompt = """你是一个专业的小说策划顾问。你的任务是基于提供的创意构思，生成一个详尽的长篇小说构思方案。
        请以JSON格式返回，必须包含以下所有字段（注意：必须返回可解析的JSON，不要添加额外说明）：

        {
            "world_setting": "详细的时代背景、社会环境介绍",
            "culture_background": "具体的文化背景、风俗习惯、社会制度描述",
            "special_elements": "特殊元素（如魔法系统、科技水平等）的具体设定",
            
            "core_conflict": "核心矛盾和冲突的本质及其社会/个人意义",
            "plot_outline": "完整的故事大纲，包括开端、发展、高潮、结局",
            "subplot_design": "2-3条重要子情节的设计及其与主线的关系",
            "key_events": "5-8个关键事件的具体设计",
            "plot_progression": "情节推进的方式和节奏控制的具体规划",
            
            "main_characters": "3-5个主要人物的详细设定（性格、背景、动机等）",
            "supporting_characters": "5-8个重要配角的简要设定",
            "character_relationships": "主要人物之间的关系网络及其演变",
            "character_arcs": "主要人物的成长轨迹和改变历程",
            
            "theme_design": "核心主题的具体阐释和表达方式",
            "philosophical_elements": "作品中的哲学思考和意义探讨",
            "social_commentary": "对现实社会问题的隐喻和思考",
            "symbolic_system": "重要象征元素的系统设计",
            
            "narrative_perspective": "叙事视角的选择及其效果分析",
            "timeline_structure": "时间线的具体安排和特殊处理",
            "pacing_design": "故事节奏的具体规划和情感曲线",
            "foreshadowing": "主要伏笔的设置和呼应设计",
            
            "writing_style": "整体写作风格的定位和特点",
            "language_features": "语言特色的具体规划",
            "atmosphere_building": "不同场景的氛围营造方式",
            "literary_devices": "计划使用的主要文学手法",
            
            "chapter_structure": "章节的组织结构和划分原则",
            "volume_planning": "分卷的规划（如果需要）",
            "word_count_target": 预计字数（整数）,
            "estimated_chapters": 预计章节数（整数）
        }

        要求：
        1. 所有设计必须统一、和谐，相互支持
        2. 确保所有元素都围绕核心主题展开
        3. 充分考虑商业价值和艺术价值的平衡
        4. 特别注意人物和情节的可信度
        5. 为创作团队提供清晰的创作指导
        """

        # 构建创意信息
        concept_info = f"""创意概述：{expansion.get('summary', '')}
体裁：{expansion.get('genre', '')}
主题：{expansion.get('theme', '')}
创新点：{expansion.get('innovation_points', '')}"""

        prompt = system_prompt + f"\n\n基于以下创意信息，生成完整的长篇小说构思方案：\n{concept_info}"
        response = await self._generate_content(prompt, "全文构思生成")
        if not response:
            return None
            
        try:
            # 尝试清理响应文本，移除可能的前后缀
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()

            current_app.logger.info(f"清理后的JSON响应: {cleaned_response[:200]}...")

            # 尝试解析JSON响应
            concept_data = json.loads(cleaned_response)
            # 验证必要字段
            self._validate_concept_data(concept_data)
            # 处理字段数据类型
            processed_data = self._process_concept_data(concept_data)
            return processed_data
            
        except json.JSONDecodeError as e:
            current_app.logger.error(f"解析全文构思JSON失败: {str(e)}")
            current_app.logger.error(f"原始响应: {response[:200]}")
            return None
        except Exception as e:
            current_app.logger.error(f"处理全文构思失败: {str(e)}")
            return None


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
        return await self._generate_content(prompt, "全文大纲生成")

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
        content = await self._generate_content(prompt, f"第{chapter_number}章大纲生成")
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
        return await self._generate_content(prompt, f"第{section_number}节大纲生成")

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
        return await self._generate_content(prompt, "段落概要生成")

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
   - 合理的修辞手法
   - 恰当的意象运用
   - 优美的语言风格
4. 结构安排
   - 段落层次分明
   - 过渡自然流畅
   - 重点突出明确

输出要求：
- 直接输出正文内容，不需要任何额外说明或标注
- 保持内容的连贯性和完整性
- 确保文字优美且富有感染力
- 严格遵循中文创作规范"""

        prompt = system_prompt + f"\n\n基于以下段落概要，创作段落正文：\n{section_summary}"
        return await self._generate_content(prompt, "段落正文创作")
