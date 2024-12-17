import jwt
from functools import wraps
from flask import request, jsonify
from config import JWT_SECRET_KEY


def extract_user_id_from_token(token):
    """从 token 中提取用户 ID"""
    try:
        # 使用 JWT 解码 token，使用固定的 SECRET_KEY
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
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


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 获取并验证 token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "message": "未授权访问",
                "status": "error"
            }), 401

        token = auth_header.split(" ")[1]

        try:
            # 从 token 中提取用户 ID
            user_id = extract_user_id_from_token(token)
            if not user_id:
                return jsonify({
                    "message": "无效的用户信息",
                    "status": "error"
                }), 401
                
            request.user_id = user_id
        except Exception as e:
            return jsonify({
                "message": str(e),
                "status": "error"
            }), 401
            
        return f(*args, **kwargs)
    return decorated