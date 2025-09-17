from app import create_app, db
from flask_migrate import init, migrate, upgrade

app = create_app()
with app.app_context():
    # 初始化迁移
    try:
        init()
    except:
        pass  # 如果已经初始化则跳过
    
    # 创建迁移
    migrate()
    
    # 应用迁移
    upgrade()