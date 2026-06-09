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
    pass

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
    pass

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
    pass

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
    pass
