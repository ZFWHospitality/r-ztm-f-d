from models import Task
from db_config import db
from datetime import datetime 

def get_all_task(user_id, page=1, per_page=5):
    query = Task.query.filter_by(user_id=user_id, deleted_at=None).order_by(Task.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = [task.to_dict() for task in pagination.items]
    return {
        "tasks": tasks,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "total_tasks": pagination.total,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
    }

def get_task_by_id(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id, deleted_at=None).first()
    return task


def create_new_task(title, description, user_id):
    new_task = Task(title=title, description=description, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return new_task


def update_task(task_id, title, description, completed, user_id):
    task = get_task_by_id(task_id, user_id)
    if not task:
        return None

    # Only update fields that are not None
    if title is not None:
        task.title = title.strip()

    if description is not None:
        task.description = description.strip()

    if completed is not None:
        task.completed = bool(completed)
    db.session.commit()
    return task


def delete_task(task_id, user_id):
    task = get_task_by_id(task_id, user_id)
    if not task:
        return False

    # Mark as deleted instead of removing
    task.deleted_at = datetime.utcnow()
    db.session.commit()
    return True


def filter_tasks(user_id, completed=None, created_before=None, created_after=None):
    query = Task.query.filter_by(user_id=user_id)

    if completed is not None:
        query = query.filter(Task.completed==bool(completed))

    if created_before is not None:
        try:
            date_obj = datetime.strptime(created_before, "%Y-%m-%d")
            query = query.filter(Task.created_at < date_obj)
        except ValueError:
            return {"error": "Invalid date format for created_before. Use YYYY-MM-DD."}

    if created_after is not None:
        try:
            date_obj = datetime.strptime(created_after, "%Y-%m-%d")
            query = query.filter(Task.created_at > date_obj)
        except ValueError:
            return {"error": "Invalid date format for created_after. Use YYYY-MM-DD."}

    tasks = query.order_by(Task.created_at.desc()).all()
    return [task.to_dict() for task in tasks]


