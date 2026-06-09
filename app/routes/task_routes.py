from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models import Task

# 建立任務路由藍圖
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/')
def index():
    """
    GET /
    首頁：顯示所有或依完成狀態篩選後的任務清單。
    
    Query String:
        status (str): 篩選條件，可為 'all'、'pending' 或 'completed'
        
    重導向/渲染：
        渲染 app/templates/index.html 並傳入任務列表與篩選條件
    """
    status = request.args.get('status', 'all')
    if status not in ['all', 'pending', 'completed']:
        status = 'all'
        
    tasks = Task.get_all(status)
    return render_template('index.html', tasks=tasks, current_status=status)

@task_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """
    POST /tasks/add
    新增任務：接收表單資料，驗證通過後寫入資料庫。
    
    Form Data:
        title (str): 任務名稱（必填，最多 100 字）
        
    重導向/渲染：
        成功或失敗皆重導向至 url_for('tasks.index')
    """
    title = request.form.get('title', '').strip()
    
    if not title:
        flash('任務名稱不可為空！', 'danger')
        return redirect(url_for('tasks.index'))
        
    if len(title) > 100:
        flash('任務名稱長度不可超過 100 字！', 'danger')
        return redirect(url_for('tasks.index'))
        
    try:
        Task.create(title=title)
        flash('成功新增一筆待辦任務！', 'success')
    except Exception as e:
        flash(f'新增任務時發生錯誤：{str(e)}', 'danger')
        
    return redirect(url_for('tasks.index'))

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """
    POST /tasks/<int:id>/toggle
    切換完成狀態：將指定 ID 任務之 is_completed 屬性取反。
    
    Path Parameter:
        id (int): 任務 ID
        
    重導向/渲染：
        完成後重導向至 url_for('tasks.index')
    """
    task = Task.get_by_id(id)
    if task is None:
        abort(404)
        
    try:
        task.update(is_completed=not task.is_completed)
        status_text = '已標記為完成！' if task.is_completed else '已重設為未完成！'
        flash(f'任務「{task.title}」{status_text}', 'success')
    except Exception as e:
        flash(f'更新任務狀態時發生錯誤：{str(e)}', 'danger')
        
    # 重導時，保留當前的篩選狀態（從 Referer URL 獲取 status 參數，或者維持原狀）
    referer = request.referrer
    if referer and 'status=' in referer:
        status_val = referer.split('status=')[-1].split('&')[0]
        return redirect(url_for('tasks.index', status=status_val))
        
    return redirect(url_for('tasks.index'))

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    POST /tasks/<int:id>/delete
    刪除任務：自資料庫永久刪除指定 ID 之任務。
    
    Path Parameter:
        id (int): 任務 ID
        
    重導向/渲染：
        完成後重導向至 url_for('tasks.index')
    """
    task = Task.get_by_id(id)
    if task is None:
        abort(404)
        
    try:
        task.delete()
        flash(f'任務「{task.title}」已成功刪除！', 'success')
    except Exception as e:
        flash(f'刪除任務時發生錯誤：{str(e)}', 'danger')
        
    referer = request.referrer
    if referer and 'status=' in referer:
        status_val = referer.split('status=')[-1].split('&')[0]
        return redirect(url_for('tasks.index', status=status_val))
        
    return redirect(url_for('tasks.index'))
