import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 建立 SQLAlchemy 實例
db = SQLAlchemy()

def create_app():
    """
    建立與配置 Flask 應用程式 (Application Factory Pattern)
    """
    app = Flask(__name__)
    
    # 基本設定
    app.config['SECRET_KEY'] = 'task-manager-secret-key-12345'
    
    # 設定 SQLite 資料庫，資料庫檔案將存在 instance/database.db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化資料庫
    db.init_app(app)
    
    # 註冊 Blueprints 与建立資料庫表格
    with app.app_context():
        # 匯入 Model 以確保 SQLAlchemy 能識別並建表
        from app.models.task import Task
        
        # 匯入並註冊路由藍圖
        from app.routes.task_routes import task_bp
        app.register_blueprint(task_bp)
        
        # 自動建立資料表 (如果不存在)
        db.create_all()
        
    return app
