from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import time

document_bp = Blueprint('document', __name__)

@document_bp.route('/document', methods=['POST'])
def upload_document():
    data = request.get_json()
    doc_name = data.get('doc_name')
    content = data.get('content')
    token = request.headers.get('Authorization').split(" ")[1]

    if not doc_name or not content:
        return jsonify({'status': 'error', 'message': '文档名称和内容不能为空'}), 400

    # 验证 token（这里省略具体实现）
    user_id = "extracted_user_id_from_token"  # 从 token 中提取用户 ID

    # 记录文档信息
    document = {
        'user_id': user_id,
        'doc_name': doc_name,
        'content': content,
        'status': '生成索引中',
        'upload_at': datetime.utcnow()
    }

    current_app.mongodb.documents.insert_one(document)

    # 模拟索引生成
    time.sleep(10)

    # 更新文档状态
    current_app.mongodb.documents.update_one(
        {'_id': document['_id']},
        {'$set': {'status': '可用'}}
    )

    return jsonify({'status': 'success', 'message': '文档上传成功'}), 201


@document_bp.route('/documents', methods=['GET'])
def get_documents():
    token = request.headers.get('Authorization').split(" ")[1]
    user_id = "extracted_user_id_from_token"  # 从 token 中提取用户 ID

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


@document_bp.route('/document/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    print(doc_id)

    token = request.headers.get('Authorization').split(" ")[1]
    user_id = "extracted_user_id_from_token"  # 从 token 中提取用户 ID
    # 删除文档
    result = current_app.mongodb.documents.delete_one({
        '_id': doc_id,
        # 'user_id': user_id
    })

    if result.deleted_count == 0:
        return jsonify({'status': 'error', 'message': '文档不存在或无权限删除'}), 404

    return jsonify({'status': 'success', 'message': '文档删除成功'}), 200 