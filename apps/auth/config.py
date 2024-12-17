import os

# 服务配置
SERVICE_NAME = 'auth._http._tcp.local.'
SERVICE_HOST = '0.0.0.0'
SERVICE_PORT = 5001

# MongoDB 配置
MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'port': 27017,
    'username': 'mongo',
    'password': 'mongo',
    'database': 'sbe-demo',
    'authentication_source': 'admin',
    'authentication_mechanism': 'SCRAM-SHA-1'
}

# JWT 配置
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时
