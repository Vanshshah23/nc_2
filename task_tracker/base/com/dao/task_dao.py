from base import db
from base.com.vo.task_vo import TaskVO
from sqlalchemy import asc


class TaskDAO:
    def insert_task(self, task_vo):
        db.session.add(task_vo)
        db.session.commit()

    def view_task(self,task_vo1):
        task_vo = TaskVO.query.filter_by(task_user_id=task_vo1.task_user_id).order_by(asc(TaskVO.task_due_date))
        return task_vo

    def search_task(self,task_vo):
        task_edit = TaskVO.query.filter_by(task_id=task_vo.task_id).all()
        return task_edit

    def update_task(self, task_vo):
        db.session.merge(task_vo)
        db.session.commit()

    def delete_task(self, task_vo):
        task_vo_delete = TaskVO.query.get(task_vo.task_id)
        db.session.delete(task_vo_delete)
        db.session.commit()
