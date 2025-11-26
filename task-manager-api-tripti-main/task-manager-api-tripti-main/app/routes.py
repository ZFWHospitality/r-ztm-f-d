from flask import Blueprint, request, jsonify, current_app, url_for
from . import db
from .models import Task, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from .schemas import TaskSchema
from flasgger import swag_from

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@tasks_bp.route('', methods=['GET'])
@swag_from({'tags':['tasks'], 'parameters':[{'name':'page','in':'query','type':'integer'},{'name':'per_page','in':'query','type':'integer'},{'name':'completed','in':'query','type':'string'}], 'responses':{200:{'description':'A list of tasks'}}})
def list_tasks():
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 10)), 100)
    completed = request.args.get('completed')

    q = Task.query
    if completed is not None:
        if completed.lower() in ('1','true','yes'):
            q = q.filter_by(completed=True)
        elif completed.lower() in ('0','false','no'):
            q = q.filter_by(completed=False)

    pag = q.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    tasks = pag.items
    return jsonify({
        'tasks': tasks_schema.dump(tasks),
        'page': page,
        'per_page': per_page,
        'total': pag.total,
        'pages': pag.pages
    }), 200

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@swag_from({'tags':['tasks'], 'responses':{200:{'description':'Task detail'},404:{'description':'Not found'}}})
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return task_schema.dump(task), 200

@tasks_bp.route('', methods=['POST'])
@jwt_required()
@swag_from({'tags':['tasks'], 'parameters':[{'name':'body','in':'body','schema':{'type':'object','properties':{'title':{'type':'string'},'description':{'type':'string'}}}}], 'responses':{201:{'description':'Created'}}})
def create_task():
    data = request.get_json() or {}
    errors = task_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    identity = get_jwt_identity()
    user_id = identity['id']
    task = Task(title=data['title'], description=data.get('description'), user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return task_schema.dump(task), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
@swag_from({'tags':['tasks'], 'parameters':[{'name':'body','in':'body','schema':{'type':'object','properties':{'title':{'type':'string'},'description':{'type':'string'},'completed':{'type':'boolean'}}}}], 'responses':{200:{'description':'Updated'},403:{'description':'Forbidden'}}})
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    identity = get_jwt_identity()
    user_id = identity['id']
    role = identity.get('role','user')

    if task.user_id != user_id and role != 'admin':
        return jsonify({'msg':'forbidden'}), 403

    data = request.get_json() or {}
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = bool(data['completed'])

    db.session.commit()
    return task_schema.dump(task), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
@swag_from({'tags':['tasks'], 'responses':{200:{'description':'Deleted'},403:{'description':'Forbidden'}}})
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    identity = get_jwt_identity()
    user_id = identity['id']
    role = identity.get('role','user')

    if task.user_id != user_id and role != 'admin':
        return jsonify({'msg':'forbidden'}), 403

    db.session.delete(task)
    db.session.commit()
    return jsonify({'msg':'deleted'}), 200
