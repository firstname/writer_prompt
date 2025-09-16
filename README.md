# Writer Prompt

一个基于 Flask 的写作辅助工具，帮助作者管理写作项目、创作内容和组织思路。

## 功能特点

- 项目管理：创建和管理多个写作项目
- 全文设定：管理项目的世界观、人物和背景设定
- 纲要生成：规划和组织故事结构
- 正文生成：基于设定和纲要进行创作
- 数据互通：各个模块之间的数据关联和共享

## 技术栈

- Backend: Flask + SQLAlchemy
- Frontend: HTML + CSS + JavaScript
- Database: SQLite

## 开始使用

1. 克隆项目
```bash
git clone https://github.com/firstname/writer_prompt.git
cd writer_prompt
```

2. 创建虚拟环境
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用
```bash
python run.py
```

访问 http://127.0.0.1:5000 开始使用。

## 项目结构

```
writer_prompt/
├── app/
│   ├── models/        # 数据模型
│   ├── routes/        # 路由处理
│   ├── static/        # 静态文件
│   └── templates/     # 页面模板
├── config.py          # 配置文件
├── requirements.txt   # 依赖列表
└── run.py            # 启动脚本
```

## License

MIT License