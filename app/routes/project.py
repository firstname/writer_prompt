from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models import db, Project, Setting

bp = Blueprint('project', __name__, url_prefix='/project')

@bp.route('/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        project = Project(
            name=request.form['name'],
            description=request.form.get('description', ''),
            genre=request.form.get('genre', 'novel')
        )
        db.session.add(project)
        db.session.commit()

        # 根据项目类型创建默认设定模板
        default_settings = {
            'novel': [
                ('world', '世界观设定'),
                ('character', '人物设定'),
                ('plot', '故事背景')
            ],
            'script': [
                ('scene', '场景设定'),
                ('character', '角色设定'),
                ('timeline', '时间线')
            ],
            'article': [
                ('topic', '主题设定'),
                ('outline', '大纲设定'),
                ('reference', '参考资料')
            ]
        }
        
        # 获取当前项目类型的默认设定
        settings = default_settings.get(project.genre, default_settings['novel'])
        
        # 创建默认设定
        for setting_type, content in settings:
            setting = Setting(
                project_id=project.id,
                setting_type=setting_type,
                content='请在此填写' + content
            )
            db.session.add(setting)
        
        db.session.commit()
        return redirect(url_for('project.view', project_id=project.id))
    # 获取所有项目用于侧边栏显示
    projects = Project.query.all()
    return render_template('project/new.html', projects=projects)

@bp.route('/<int:project_id>')
def view(project_id):
    project = Project.query.get_or_404(project_id)
    projects = Project.query.all()  # 获取所有项目用于侧边栏显示
    return render_template('project/view.html', project=project, projects=projects)

@bp.route('/<int:project_id>/settings', methods=['GET', 'POST'])
def settings(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        data = request.get_json()
        setting = Setting.query.filter_by(
            project_id=project_id,
            setting_type=data['type']
        ).first()
        
        if not setting:
            setting = Setting(
                project_id=project_id,
                setting_type=data['type']
            )
            
        setting.content = data['content']
        db.session.add(setting)
        db.session.commit()
        return jsonify({'status': 'success'})
    
    projects = Project.query.all()  # 获取所有项目用于侧边栏显示
    return render_template('project/settings.html', project=project, projects=projects)