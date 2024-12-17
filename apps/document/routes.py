import threading
import time
from datetime import datetime

import jwt
from bson import ObjectId
from flask import Blueprint, request, jsonify, current_app

document_bp = Blueprint('document', __name__)


def extract_user_id_from_token(token):
    """从 token 中提取用户 ID"""
    try:
        # 使用 JWT 解码 token，使用固定的 SECRET_KEY
        SECRET_KEY = "your-secret-key"  # 这里应该从配置中获取，暂时使用固定值
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        print(f"Decoded user_id: {user_id}")  # 调试信息
        return user_id
    except jwt.ExpiredSignatureError:
        raise Exception('Token已过期')
    except jwt.InvalidTokenError as e:
        print(f"Token验证错误: {str(e)}")  # 调试信息
        raise Exception('无效的Token')
    except Exception as e:
        print(f"解析Token时发生错误: {str(e)}")  # 调试信息
        raise Exception(f'Token处理错误: {str(e)}')


def create_index_async(app, document):
    """异步创建索引的函数"""
    try:
        print(f"开始为文档 {document['doc_name']} 生成索引...")
        time.sleep(3)  # 模拟索引生成过程

        # 更新文档状态为可用
        with app.app_context():
            app.mongodb.documents.update_one(
                {'_id': document['_id']},
                {'$set': {'status': '可用'}}
            )
            print(f"文档 {document['doc_name']} 索引生成完成")
    except Exception as e:
        print(f"生成索引时发生错误: {str(e)}")
        # 更新文档状态为错误
        with app.app_context():
            app.mongodb.documents.update_one(
                {'_id': document['_id']},
                {'$set': {'status': '索引生成失败'}}
            )


def run_async_task(app, document):
    """在新线程中运行异步任务"""
    create_index_async(app, document)


@document_bp.route('/document', methods=['POST'])
def upload_document():
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
        doc_name = data.get('doc_name')
        content = data.get('content')

        if not doc_name or not content:
            return jsonify({'status': 'error', 'message': '文档名称和内容不能为空'}), 400

        # 记录文档信息
        document = {
            'user_id': user_id,
            'doc_name': doc_name,
            'content': content,
            'status': '生成索引中',
            'upload_at': datetime.utcnow()
        }

        result = current_app.mongodb.documents.insert_one(document)
        document['_id'] = result.inserted_id

        # 在新线程中启动异步任务
        app = current_app._get_current_object()  # 获取真实的应用对象
        threading.Thread(target=run_async_task, args=(app, document)).start()

        return jsonify({
            'status': 'success',
            'message': '文档上传成功，正在异步生成索引',
            'doc_id': str(document['_id'])
        }), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@document_bp.route('/documents', methods=['GET'])
def get_documents():
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

        documents = current_app.mongodb.documents.find({'user_id': user_id})
        result = []
        for doc in documents:
            result.append({
                'id': str(doc['_id']),
                'doc_name': doc['doc_name'],
                'status': doc['status'],
                'upload_at': doc['upload_at']
            })

        return jsonify({'documents': result}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@document_bp.route('/document/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
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

        # 删除文档
        result = current_app.mongodb.documents.delete_one({
            '_id': ObjectId(doc_id),
            'user_id': user_id
        })

        if result.deleted_count == 0:
            return jsonify({'status': 'error', 'message': '文档不存在或无权限删除'}), 404

        return jsonify({'status': 'success', 'message': '文档删除成功'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
