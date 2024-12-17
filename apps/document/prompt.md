我需要你使用 python 3.12 帮我编写一个文档功能的后端服务，名为：document。提供如下restult API接口：

1. 上传文档
  - 描述：提供已登录用户上传文档的接口，可以上传 PDF、DOC、TXT格式
  - 地址：POST /api/document
  - 入参：doc_name, token(request header)，以及文档内容
  - 返回：成功或失败
  - 处理逻辑：用户提交文档通过前端页面上传给后端，后端通过该请求接收文档内容以及文档名称信息，并且记录该文档为当前用户所有。然后异步生成文档索引（生成过程使用sleep(10)方法暂时替代）并且记录文档的状态为生成索引中。索引生成完毕后，修改文档状态为可用。
2. 查看文档状态
  - 描述：列出当前登录用户下所有的文档以及状态。
  - 地址：GET /api/documents
  - 入参：token(request header)
  - 返回：documents。至少包含：id, doc_name, status, upload_at等字段
  - 处理逻辑：根据token中的用户信息，查找并列出对应用户下的文档。不可列出其他用户的文档。
3. 删除文档
  - 描述：删除当前用户的指定文档。
  - 地址：DELETE /api/document/:doc_id
  - 入参：doc_id, token(request header)
  - 返回：成功或失败
  - 处理逻辑：根据输入内容，删除对应文档。不允许删除其他用户的文档。

技术要求：
1. 以微服务形式，使用python 3.12、flask开发
2. 使用mongodb 8.0.3作为数据库
3. 代码生成在./apps/document目录内
4. 服务启动后们需要注册到mDNS内，以便后续的其他服务能够找到它，并可通过restful调用它。
5. 书写详细的设计文档，包括数据流程，到./apps/document/readme.md内
6. requirements请更新在 ./requirements.txt中
