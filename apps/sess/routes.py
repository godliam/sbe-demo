from datetime import datetime

from bson import ObjectId
from flask import Blueprint, request, jsonify, current_app

from utils import extract_user_id_from_token
from models import Session, Chat

sess_bp = Blueprint('sess', __name__)


@sess_bp.route('/sess', methods=['POST'])
def create_session():
    try:
        # 获取并验证 token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'status': 'error', 'message': '未授权访问'}), 401

        token = auth_header.split(" ")[1]

        # 从 token 中提取用户 ID
        user_id = extract_user_id_from_token(token)
        if not user_id:
            return jsonify({'status': 'error', 'message': '无效的用户信息'}), 401

        data = request.get_json()
        sess_name = data.get('sess_name')
        if not sess_name:
            return jsonify({'status': 'error', 'message': '会话名称不能为空'}), 400

        session = Session(current_app.mongodb)
        sess_id = session.create(user_id, sess_name)

        return jsonify({
            'status': 'success',
            'message': '创建会话成功',
            'data': {'sess_id': sess_id}
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@sess_bp.route('/sessions', methods=['GET'])
def get_sessions():
    try:
        # 获取并验证 token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'status': 'error', 'message': '未授权访问'}), 401

        token = auth_header.split(" ")[1]

        # 从 token 中提取用户 ID
        user_id = extract_user_id_from_token(token)
        if not user_id:
            return jsonify({'status': 'error', 'message': '无效的用户信息'}), 401

        session = Session(current_app.mongodb)
        sessions = session.get_user_sessions(user_id)

        return jsonify({
            'status': 'success',
            'message': '获取会话列表成功',
            'data': [{
                'id': str(s['_id']),
                'sess_name': s['sess_name'],
                'create_at': s['create_at'].isoformat()
            } for s in sessions]
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@sess_bp.route('/sess/<sess_id>/chat', methods=['POST'])
def create_chat(sess_id):
    try:
        # 获取并验证 token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'status': 'error', 'message': '未授权访问'}), 401

        token = auth_header.split(" ")[1]

        # 从 token 中提取用户 ID
        user_id = extract_user_id_from_token(token)
        if not user_id:
            return jsonify({'status': 'error', 'message': '无效的用户信息'}), 401

        session = Session(current_app.mongodb)
        if not session.verify_ownership(sess_id, user_id):
            return jsonify({'status': 'error', 'message': '无权访问该会话'}), 403

        data = request.get_json()
        chat_content = data.get('chat_content')
        if not chat_content:
            return jsonify({'status': 'error', 'message': '聊天内容不能为空'}), 400

        chat = Chat(current_app.mongodb)
        # 保存用户消息
        chat.create_message(sess_id, user_id, chat_content, "user")
        # 自动回复
        chat.create_message(sess_id, user_id, "好的，我收到了。", "server")

        return jsonify({
            'status': 'success',
            'message': '发送消息成功'
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@sess_bp.route('/sess/<sess_id>/chats', methods=['GET'])
def get_chats(sess_id):
    try:
        # 获取并验证 token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'status': 'error', 'message': '未授权访问'}), 401

        token = auth_header.split(" ")[1]

        # 从 token 中提取用户 ID
        user_id = extract_user_id_from_token(token)
        if not user_id:
            return jsonify({'status': 'error', 'message': '无效的用户信息'}), 401

        session = Session(current_app.mongodb)
        if not session.verify_ownership(sess_id, user_id):
            return jsonify({'status': 'error', 'message': '无权访问该会话'}), 403

        chat = Chat(current_app.mongodb)
        chats = chat.get_session_chats(sess_id)

        return jsonify({
            'status': 'success',
            'message': '获取聊天记录成功',
            'data': [{
                'chat_id': str(c['_id']),
                'chat_content': c['chat_content'],
                'create_at': c['create_at'].isoformat(),
                'from': c['from']
            } for c in chats]
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
