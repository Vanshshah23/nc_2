from base import db
from base.com.vo.login_vo import LoginVO


class TaskVO(db.Model):
    __tablename__ = 'task_table'
    task_id = db.Column('login_id', db.Integer, primary_key=True, autoincrement=True)
    task_title = db.Column('task_title', db.String(100), nullable=False)
    task_description = db.Column('task_description', db.String(100), nullable=False)
    task_user_id = db.Column("user_id", db.Integer, db.ForeignKey(LoginVO.login_id))
    task_due_date = db.Column("task_due_date", db.Date, nullable=False)

    def as_dict(self):
        return {
            'task_id': self.task_id,
            'task_title': self.task_title,
            'task_description': self.task_description,
        }
db.create_all()
