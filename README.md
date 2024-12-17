# SBE-Demo

## 技术栈
- Python 3.12
- Flask
- MongoDB 8.0.3
- zeroconf (用于 mDNS 服务发现)
- PyJWT (用于 token 生成和验证)

## 演示
### 1. [认证服务演示]()
### 2. [文档服务演示]()
### 3. [会话服务演示]()


## 设计文档
### 1. [认证服务设计文档](./apps/auth/README.md)
### 2. [文档服务设计文档](./apps/document/README.md)
### 2. [会话服务设计文档]()

## 部署说明

### 环境要求
- Python 3.12 或更高版本
- MongoDB 8.0.3
- 所有依赖包（见 requirements.txt）

### 安装步骤
1. 克隆代码库
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 配置环境变量（可选）：
   ```bash
   export JWT_SECRET_KEY=your-secret-key
   ```

### 运行服务
```bash
python ./apps/<service_name>/app.py
```
服务将在配置的端口（auth==`5001`, document==`5002`, sess==`5003`）上启动，并自动注册到 mDNS。

## 注意事项
1. 确保 MongoDB 服务已启动且配置正确
2. 生产环境部署时请修改 JWT_SECRET_KEY
3. 建议在生产环境中使用 HTTPS
4. 定期清理过期的黑名单 token