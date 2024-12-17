# 文档服务 (Document Service)

## 服务概述
该服务提供文档管理功能，包括文档上传、查看和删除操作。服务采用 REST API 设计，使用 JWT (JSON Web Token) 实现用户认证。

## 数据流程

### 1. 上传文档流程
1. 客户端发送上传请求，包含文档名称、token 和文档内容
2. 服务器验证 token，确保用户已登录
3. 服务器接收文档内容和名称，记录文档为当前用户所有
4. 服务器异步生成文档索引（使用 sleep(10) 模拟）
5. 文档状态更新为“生成索引中”
6. 索引生成完毕后，文档状态更新为“可用”

### 2. 查看文档状态流程
1. 客户端发送请求，包含 token
2. 服务器验证 token，确保用户已登录
3. 服务器查找并列出当前用户的所有文档及其状态

### 3. 删除文档流程
1. 客户端发送删除请求，包含 doc_id 和 token
2. 服务器验证 token，确保用户已登录
3. 服务器根据 doc_id 删除对应文档，不允许删除其他用户的文档

## API 接口说明

### 1. 上传文档
- 端点：`POST /api/document`
- 请求头：
  ```
  Authorization: Bearer <token>
  ```
- 请求体：
  ```json
  {
    "doc_name": "string",
    "content": "string"  // 文档内容
  }
  ```
- 响应：
  ```json
  {
    "status": "success/error",
    "message": "string"
  }
  ```

### 2. 查看文档状态
- 端点：`GET /api/documents`
- 请求头：
  ```
  Authorization: Bearer <token>
  ```
- 响应：
  ```json
  {
    "documents": [
      {
        "id": "string",
        "doc_name": "string",
        "status": "string",
        "upload_at": "datetime"
      }
    ]
  }
  ```

### 3. 删除文档
- 端点：`DELETE /api/document/:doc_id`
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

### Documents 集合
```json
{
  "_id": "ObjectId",
  "user_id": "string",  // 用户ID
  "doc_name": {
    "type": "string",
    "required": true,
    "description": "文档名称"
  },
  "content": {
    "type": "string",
    "required": true,
    "description": "文档内容"
  },
  "status": {
    "type": "string",
    "required": true,
    "description": "文档状态（生成索引中、可用）"
  },
  "upload_at": {
    "type": "datetime",
    "required": true,
    "description": "上传时间"
  }
}
```

## 运行服务
```bash
python app.py
```
服务将在配置的端口（默认 5002）上启动，并自动注册到 mDNS。

## 注意事项
1. 确保 MongoDB 服务已启动且配置正确
2. 生产环境部署时请修改 JWT_SECRET_KEY
3. 建议在生产环境中使用 HTTPS 