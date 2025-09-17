from app import db
from datetime import datetime

class InitialIdea(db.Model):
    """初始灵感模型"""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)  # 灵感内容
    source_type = db.Column(db.String(50))  # 真实事件/虚构世界/主题表达等
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BasicConcept(db.Model):
    """作品全文基本构思模型"""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    creative_expansion_id = db.Column(db.Integer, db.ForeignKey('creative_expansion.id'), nullable=False)
    world_setting = db.Column(db.Text)  # 世界设定
    plot_development = db.Column(db.Text)  # 故事情节发展
    character_design = db.Column(db.Text)  # 人物特点
    structure_design = db.Column(db.Text)  # 全文结构
    style_design = db.Column(db.Text)  # 风格、文笔特点
    theme_expression = db.Column(db.Text)  # 主题表达方式
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)