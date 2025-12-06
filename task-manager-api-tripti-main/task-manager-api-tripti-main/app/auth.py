from flask import Blueprint, request, jsonify
from . import db
from .models import User
from flask_jwt_extended import create_access_token
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
@swag_from({'tags':['auth'], 'parameters':[{'name':'body','in':'body','schema':{'type':'object','properties':{'username':{'type':'string'},'password':{'type':'string'}}}}], 'responses':{201:{'description':'Created'}}})
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'username already exists'}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'user created', 'user': {'id': user.id, 'username': user.username}}), 201

@auth_bp.route('/login', methods=['POST'])
@swag_from({'tags':['auth'], 'parameters':[{'name':'body','in':'body','schema':{'type':'object','properties':{'username':{'type':'string'},'password':{'type':'string'}}}}], 'responses':{200:{'description':'OK'}}})
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'invalid credentials'}), 401

    token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
    return jsonify({'access_token': token}), 200
