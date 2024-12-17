from datetime import datetime, timedelta

import jwt
from werkzeug.security import generate_password_hash, check_password_hash

from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES


def hash_password(password):
    """对密码进行哈希处理"""
    return generate_password_hash(password)


def verify_password(hashed_password, password):
    """验证密码"""
    return check_password_hash(hashed_password, password)


def generate_token(username, user_id):
    """生成 JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')


def verify_token(token):
    """验证 JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        # 检查token是否在黑名单中
        from flask import current_app
        if current_app.mongodb.blacklisted_tokens.find_one({'token': token}):
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
