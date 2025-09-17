from app import db
from datetime import datetime

# 导入规划模块的模型
from .planning import InitialIdea, CreativeExpansion, BasicConcept

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(50), default='novel')  # 作品类型：novel=小说, script=剧本, article=文章, other=其他
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # 关联其他模块的数据
    settings = db.relationship('Setting', backref='project', lazy=True)
    outlines = db.relationship('Outline', backref='project', lazy=True)
    contents = db.relationship('Content', backref='project', lazy=True)
    initial_ideas = db.relationship('InitialIdea', backref='project', lazy=True)
    creative_expansions = db.relationship('CreativeExpansion', backref='project', lazy=True)
    basic_concepts = db.relationship('BasicConcept', backref='project', lazy=True)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    setting_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Outline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    outline_id = db.Column(db.Integer, db.ForeignKey('outline.id'))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())