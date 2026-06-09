from datetime import datetime
from app import db

class Task(db.Model):
    """
    任務資料模型 (Task Model)
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}: {self.title} (Completed: {self.is_completed})>"

    @classmethod
    def create(cls, title):
        """
        新增一筆任務
        """
        task = cls(title=title)
        db.session.add(task)
        db.session.commit()
        return task

    @classmethod
    def get_all(cls, status=None):
        """
        取得所有任務，並依建立時間降序排序（最新任務在最前）
        支援篩選狀態: 'completed', 'pending', 或 'all' (預設)
        """
        query = cls.query
        if status == 'completed':
            query = query.filter_by(is_completed=True)
        elif status == 'pending':
            query = query.filter_by(is_completed=False)
        return query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, task_id):
        """
        依 ID 尋找單一任務
        """
        return cls.query.get(task_id)

    def update(self, title=None, is_completed=None):
        """
        更新任務欄位值
        """
        if title is not None:
            self.title = title
        if is_completed is not None:
            self.is_completed = is_completed
        db.session.commit()
        return self

    def delete(self):
        """
        刪除此任務
        """
        db.session.delete(self)
        db.session.commit()
