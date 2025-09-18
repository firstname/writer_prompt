from app import db
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Mapped

class InitialIdea(db.Model):
    """初始灵感模型"""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)  # 灵感内容
    source_type = db.Column(db.String(50))  # 真实事件/虚构世界/主题表达等
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class CreativeExpansion(db.Model):
    """创意发散模型"""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    initial_idea_id = db.Column(db.Integer, db.ForeignKey('initial_idea.id'), nullable=False)
    summary = db.Column(db.Text)  # 作品简述
    genre = db.Column(db.String(50))  # 体裁
    theme = db.Column(db.String(200))  # 主题
    innovation_points = db.Column(db.Text)  # 创新点
    is_selected = db.Column(db.Boolean, default=False)  # 是否被选中作为最终创意
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # 关联全文构思
    concepts = db.relationship('BasicConcept', backref='creative_expansion', lazy=True)

    @property
    def has_concept(self) -> bool:
        """是否已经生成了全文构思"""
        return bool(self.concepts.first())
        
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'initial_idea_id': self.initial_idea_id,
            'summary': self.summary,
            'genre': self.genre,
            'theme': self.theme,
            'innovation_points': self.innovation_points,
            'is_selected': self.is_selected,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class BasicConcept(db.Model):
    """作品全文基本构思模型"""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    creative_expansion_id = db.Column(db.Integer, db.ForeignKey('creative_expansion.id'), nullable=False)
    
    # 世界观设定
    world_setting = db.Column(db.Text)  # 时代背景、社会环境、特殊规则等
    culture_background = db.Column(db.Text)  # 文化背景、风俗习惯、社会制度等
    special_elements = db.Column(db.Text)  # 特殊元素（如魔法系统、科技水平等）
    
    # 故事架构
    core_conflict = db.Column(db.Text)  # 核心冲突
    plot_outline = db.Column(db.Text)  # 故事大纲（三幕结构或其他）
    subplot_design = db.Column(db.Text)  # 子情节设计
    key_events = db.Column(db.Text)  # 关键事件
    plot_progression = db.Column(db.Text)  # 情节推进方式
    
    # 人物系统
    main_characters = db.Column(db.Text)  # 主要人物（性格、背景、动机等）
    supporting_characters = db.Column(db.Text)  # 重要配角
    character_relationships = db.Column(db.Text)  # 人物关系网
    character_arcs = db.Column(db.Text)  # 人物成长线
    
    # 主题与深度
    theme_design = db.Column(db.Text)  # 主题设计（核心思想、寓意等）
    philosophical_elements = db.Column(db.Text)  # 哲学元素
    social_commentary = db.Column(db.Text)  # 社会评论
    symbolic_system = db.Column(db.Text)  # 象征系统
    
    # 叙事策略
    narrative_perspective = db.Column(db.Text)  # 叙事视角
    timeline_structure = db.Column(db.Text)  # 时间线结构
    pacing_design = db.Column(db.Text)  # 节奏设计
    foreshadowing = db.Column(db.Text)  # 伏笔设置
    
    # 写作风格
    writing_style = db.Column(db.Text)  # 写作风格
    language_features = db.Column(db.Text)  # 语言特色
    atmosphere_building = db.Column(db.Text)  # 氛围营造
    literary_devices = db.Column(db.Text)  # 文学手法
    
    # 规划信息
    chapter_structure = db.Column(db.Text)  # 章节结构
    volume_planning = db.Column(db.Text)  # 分卷规划
    word_count_target = db.Column(db.Integer)  # 预计字数
    estimated_chapters = db.Column(db.Integer)  # 预计章节数

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BasicConcept {self.id}>'
        
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'creative_expansion_id': self.creative_expansion_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            
            'world_setting': self.world_setting,
            'culture_background': self.culture_background,
            'special_elements': self.special_elements,
            
            'core_conflict': self.core_conflict,
            'plot_outline': self.plot_outline,
            'subplot_design': self.subplot_design,
            'key_events': self.key_events,
            'plot_progression': self.plot_progression,
            
            'main_characters': self.main_characters,
            'supporting_characters': self.supporting_characters,
            'character_relationships': self.character_relationships,
            'character_arcs': self.character_arcs,
            
            'theme_design': self.theme_design,
            'philosophical_elements': self.philosophical_elements,
            'social_commentary': self.social_commentary,
            'symbolic_system': self.symbolic_system,
            
            'narrative_perspective': self.narrative_perspective,
            'timeline_structure': self.timeline_structure,
            'pacing_design': self.pacing_design,
            'foreshadowing': self.foreshadowing,
            
            'writing_style': self.writing_style,
            'language_features': self.language_features,
            'atmosphere_building': self.atmosphere_building,
            'literary_devices': self.literary_devices,
            
            'chapter_structure': self.chapter_structure,
            'volume_planning': self.volume_planning,
            'word_count_target': self.word_count_target,
            'estimated_chapters': self.estimated_chapters
        }
    social_commentary = db.Column(db.Text)  # 社会评论
    symbolic_system = db.Column(db.Text)  # 象征系统
    
    # 叙事策略
    narrative_perspective = db.Column(db.Text)  # 叙事视角
    timeline_structure = db.Column(db.Text)  # 时间线结构
    pacing_design = db.Column(db.Text)  # 节奏设计
    foreshadowing = db.Column(db.Text)  # 伏笔设置
    
    # 风格与技巧
    writing_style = db.Column(db.Text)  # 写作风格
    language_features = db.Column(db.Text)  # 语言特色
    atmosphere_building = db.Column(db.Text)  # 氛围营造
    literary_devices = db.Column(db.Text)  # 文学手法
    
    # 结构规划
    chapter_structure = db.Column(db.Text)  # 章节结构
    volume_planning = db.Column(db.Text)  # 分卷规划
    word_count_target = db.Column(db.Integer)  # 目标字数
    estimated_chapters = db.Column(db.Integer)  # 预计章节数
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)