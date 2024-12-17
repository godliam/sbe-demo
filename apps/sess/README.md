 # 会话服务 (Session Service)

## 服务概述
该服务提供会话管理功能，包括会话创建、查看和聊天消息管理。服务采用 REST API 设计，使用 JWT (JSON Web Token) 实现用户认证。

## 数据流程

### 1. 创建会话流程
1. 客户端发送创建请求，包含会话名称和 token
2. 服务器验证 token，确保用户已登录
3. 服务器创建新会话，记录为当前用户所有
4. 返回会话 ID 给客户端

### 2. 查看会话列表流程
1. 客户端发送请求，包含 token
2. 服务器验证 token，确保用户已登录
3. 服务器查找并返回当前用户的所有会话

### 3. 发送聊天消息流程
1. 客户端发送消息请求，包含会话 ID、消息内容和 token
2. 服务器验证 token 和会话所有权
3. 服务器保存用户消息
4. 服务器生成自动回复
5. 返回成功响应

### 4. 获取聊天记录流程
1. 客户端发送请求，包含会话 ID 和 token
2. 服务器验证 token 和会话所有权
3. 服务器返回该会话的所有聊天记录

## API 接口说明

### 1. 创建会话
- 端点：`POST /sess`
- 请求头：
  ```
  Authorization: Bearer <token>
  ```
- 请求体：
  ```json
  {
    "sess_name": "string"
  }
  ```
- 响应：
  ```json
  {
    "status": "success",
    "message": "创建会话成功",
    "data": {
      "sess_id": "string"
    }
  }
  ```

### 2. 获取会话列表
- 端点：`GET /sessions`
- 请求头：
  ```
  Authorization: Bearer <token>
  ```
- 响应：
  ```json
  {
    "status": "success",
    "message": "获取会话列表成功",
    "data": [
      {
        "id": "string",
        "sess_name": "string",
        "create_at": "datetime"
      }
    ]
  }
  ```

### 3. 发送聊天消息
- 端点：`POST /sess/<sess_id>/chat`
- 请求头：
  ```
  Authorization: Bearer <token>
  ```
- 请求体：
  ```json
  {
    "chat_content": "string"
  }
  ```
- 响应：
  ```json
  {
    "status": "success",
    "message": "发送消息成功"
  }
  ```

### 4. 获取聊天记录
- 端点：`GET /sess/<sess_id>/chats`
- 请求头：
  ```
  Authorization: Bearer <token>
  ```
- 响应：
  ```json
  {
    "status": "success",
    "message": "获取聊天记录成功",
    "data": [
      {
        "chat_id": "string",
        "chat_content": "string",
        "create_at": "datetime",
        "from": "string"
      }
    ]
  }
  ```

## 数据库设计

### Sessions 集合
```json
{
  "_id": "ObjectId",
  "user_id": "string",  // 用户ID
  "sess_name": {
    "type": "string",
    "required": true,
    "description": "会话名称"
  },
  "create_at": {
    "type": "datetime",
    "required": true,
    "description": "创建时间"
  },
  "update_at": {
    "type": "datetime",
    "required": true,
    "description": "更新时间"
  }
}
```

### Chats 集合
```json
{
  "_id": "ObjectId",
  "sess_id": "ObjectId",  // 会话ID
  "user_id": "string",    // 用户ID
  "chat_content": {
    "type": "string",
    "required": true,
    "description": "聊天内容"
  },
  "from": {
    "type": "string",
    "required": true,
    "description": "消息来源（user/server）"
  },
  "create_at": {
    "type": "datetime",
    "required": true,
    "description": "创建时间"
  }
}
```

## 运行服务
```bash
python app.py
```
服务将在配置的端口（默认 5003）上启动，并自动注册到 mDNS。

## 注意事项
1. 确保 MongoDB 服务已启动且配置正确
2. 生产环境部署时请修改 JWT_SECRET_KEY
3. 建议在生产环境中使用 HTTPS