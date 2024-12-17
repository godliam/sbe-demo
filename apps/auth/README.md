# 认证服务 (Auth Service)

## 服务概述
该服务提供用户认证相关的基础功能，包括用户注册、登录和登出操作。服务采用 REST API 设计，使用 JWT (JSON Web Token) 实现用户认证。

## 数据流程

### 1. 用户注册流程
1. 客户端发送注册请求，包含用户名和密码
2. 服务器检查用户名是否已存在
3. 如果用户名已存在，返回错误信息
4. 如果用户名不存在，将用户信息存入数据库
5. 返回注册成功信息

### 2. 用户登录流程
1. 客户端发送登录请求，包含用户名和密码
2. 服务器验证用户名和密码
3. 如果验证失败，返回错误信息
4. 如果验证成功，生成 JWT Token
5. 返回 Token 给客户端

### 3. 用户登出流程
1. 客户端发送登出请求，请求头包含 Token
2. 服务器验证 Token 的有效性
3. 如果 Token 无效，返回错误信息
4. 如果 Token 有效，将其加入黑名单
5. 返回登出成功信息

## API 接口说明

### 1. 用户注册
- 端点：`POST /auth/register`
- 请求体：
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- 响应：
  ```json
  {
    "status": "success/error",
    "message": "string"
  }
  ```

### 2. 用户登录
- 端点：`POST /auth/login`
- 请求体：
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- 响应：
  ```json
  {
    "status": "success/error",
    "token": "string",
    "message": "string"
  }
  ```

### 3. 用户登出
- 端点：`POST /auth/logout`
- 请求头：
  ```
  Authorization: Bearer <token>
  ```
- 响应：
  ```json
  {
    "status": "success/error",
    "message": "string"
  }
  ```

## 数据库设计

### Users 集合
```json
{
  "_id": "ObjectId",
  "username": {
    "type": "string",
    "unique": true,
    "required": true,
    "description": "用户名"
  },
  "password": {
    "type": "string",
    "required": true,
    "description": "密码哈希值（使用 Werkzeug 的 generate_password_hash 生成）"
  },
  "created_at": {
    "type": "datetime",
    "required": true,
    "description": "用户创建时间"
  },
  "last_login": {
    "type": "datetime",
    "required": false,
    "description": "最后登录时间"
  }
}
```

### BlacklistedTokens 集合
```json
{
  "_id": "ObjectId",
  "token": {
    "type": "string",
    "required": true,
    "description": "已失效的 JWT token"
  },
  "blacklisted_at": {
    "type": "datetime",
    "required": true,
    "description": "token 加入黑名单的时间"
  }
}
```

### 索引设计
1. Users 集合索引：
   ```javascript
   db.users.createIndex({ "username": 1 }, { unique: true })
   ```

2. BlacklistedTokens 集合索引：
   ```javascript
   db.blacklisted_tokens.createIndex({ "token": 1 }, { unique: true })
   db.blacklisted_tokens.createIndex({ "blacklisted_at": 1 }, { expireAfterSeconds: 86400 })  // 24小时后自动删除
   ```

## 运行服务
```bash
python app.py
```
服务将在配置的端口（默认 5001）上启动，并自动注册到 mDNS。

## 测试 API

使用 curl 测试服务：

```bash
# 注册新用户
curl -X POST http://localhost:5001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# 用户登录
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# 用户登出
curl -X POST http://localhost:5001/auth/logout \
  -H "Authorization: Bearer <your-token>"
```

## 注意事项
1. 确保 MongoDB 服务已启动且配置正确
2. 生产环境部署时请修改 JWT_SECRET_KEY
3. 建议在生产环境中使用 HTTPS
4. 定期清理过期的黑名单 token