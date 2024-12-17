import logging
import socket
import sys

from flask import Flask
from pymongo import MongoClient
from zeroconf import ServiceInfo, Zeroconf

from config import (
    SERVICE_NAME,
    SERVICE_HOST,
    SERVICE_PORT,
    MONGODB_CONFIG
)
from routes import auth_bp


def configure_logging():
    """配置日志处理"""
    # 创建处理器
    handler = logging.StreamHandler(sys.stdout)

    # 设置格式化器
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)

    # 配置 Werkzeug 日志
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.handlers = []
    werkzeug_logger.addHandler(handler)
    werkzeug_logger.setLevel(logging.INFO)

    # 配置应用日志
    app_logger = logging.getLogger('auth_service')
    app_logger.handlers = []
    app_logger.addHandler(handler)
    app_logger.setLevel(logging.INFO)

    return app_logger


def create_app():
    app = Flask(__name__)

    # 配置日志
    app.logger = configure_logging()

    # 配置 MongoDB 连接
    client = MongoClient(
        host=MONGODB_CONFIG['host'],
        port=MONGODB_CONFIG['port'],
        username=MONGODB_CONFIG['username'],
        password=MONGODB_CONFIG['password'],
        authSource=MONGODB_CONFIG['authentication_source'],
        authMechanism=MONGODB_CONFIG['authentication_mechanism']
    )

    # 获取数据库实例
    app.mongodb = client[MONGODB_CONFIG['database']]

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app


def register_service():
    # 获取本机IP
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # 创建 mDNS 服务信息
    info = ServiceInfo(
        SERVICE_NAME,
        f"auth-service.{SERVICE_NAME}",
        addresses=[socket.inet_aton(local_ip)],
        port=SERVICE_PORT,
        properties={},
        server=f"auth-service.local."
    )

    # 注册服务
    zeroconf = Zeroconf()
    zeroconf.register_service(info)
    return zeroconf


if __name__ == '__main__':
    # 设置默认编码为 UTF-8
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    app = create_app()
    zeroconf = register_service()
    try:
        app.run(
            host=SERVICE_HOST,
            port=SERVICE_PORT,
            use_reloader=True,
            use_debugger=True
        )
    finally:
        zeroconf.unregister_all_services()
        zeroconf.close()
