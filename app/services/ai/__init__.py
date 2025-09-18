from flask import current_app
from typing import Union

from .base_ai_service import BaseAIService
from .gemini_ai_service import GeminiAIService

def get_ai_service() -> BaseAIService:
    """获取配置的AI服务实例"""
    service_name = current_app.config.get('AI_SERVICE', 'gemini')
    
    if service_name == 'gemini':
        return GeminiAIService()
    else:
        raise ValueError(f'不支持的AI服务: {service_name}')