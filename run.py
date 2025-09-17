from dotenv import load_dotenv
from app import create_app, db
import os

# 加载环境变量
load_dotenv()

app = create_app()

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()

if __name__ == '__main__':
    # 检查必要的环境变量
    if not os.environ.get('GEMINI_API_KEY'):
        print("错误：未设置 GEMINI_API_KEY 环境变量")
        print("请在 .env 文件中添加你的 Gemini API 密钥")
        exit(1)
        
    init_db()  # Initialize database
    app.run(debug=True)