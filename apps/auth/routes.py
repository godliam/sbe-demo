from datetime import datetime

from flask import Blueprint, request, jsonify, current_app

from utils import hash_password, verify_password, generate_token, verify_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': '用户名和密码不能为空'}), 400

    # 检查用户是否已存在
    if current_app.mongodb.users.find_one({'username': username}):
        return jsonify({'status': 'error', 'message': '用户名已存在'}), 400

    # 创建新用户
    user = {
        'username': username,
        'password': hash_password(password),
        'created_at': datetime.utcnow(),
        'last_login': None
    }

    current_app.mongodb.users.insert_one(user)
    return jsonify({'status': 'success', 'message': '注册成功'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    current_app.logger.info('收到登录请求')
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': '用户名和密码不能为空'}), 400

    user = current_app.mongodb.users.find_one({'username': username})
    if not user or not verify_password(user['password'], password):
        return jsonify({'status': 'error', 'message': '用户名或密码错误'}), 401

    # 更新最后登录时间
    current_app.mongodb.users.update_one(
        {'_id': user['_id']},
        {'$set': {'last_login': datetime.utcnow()}}
    )

    token = generate_token(str(user['username']), str(user['_id']))
    return jsonify({
        'status': 'success',
        'token': token,
        'message': '登录成功'
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'status': 'error', 'message': '无效的认证头'}), 401

    token = auth_header.split(' ')[1]
    payload = verify_token(token)
    if not payload:
        return jsonify({'status': 'error', 'message': '无效的token'}), 401

    # 将token加入黑名单
    current_app.mongodb.blacklisted_tokens.insert_one({
        'token': token,
        'blacklisted_at': datetime.utcnow()
    })

    return jsonify({'status': 'success', 'message': '登出成功'}), 200
