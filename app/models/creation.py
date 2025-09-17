from app import db

class Inspiration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    content = db.Column(db.Text)
    source_type = db.Column(db.String(50))  # 真实事件/虚构世界/主题表达等
    tags = db.Column(db.String(200))  # 以逗号分隔的标签
    materials = db.relationship('InspirationMaterial', backref='inspiration', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class InspirationMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspiration_id = db.Column(db.Integer, db.ForeignKey('inspiration.id'), nullable=False)
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class CreativeIdea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    inspiration_id = db.Column(db.Integer, db.ForeignKey('inspiration.id'))
    summary = db.Column(db.Text)  # 作品简述
    genre = db.Column(db.String(50))  # 体裁
    theme = db.Column(db.String(200))  # 主题
    innovation_points = db.Column(db.Text)  # 创新点
    score = db.Column(db.Float)  # 评分
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())