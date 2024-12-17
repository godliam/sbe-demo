我需要你使用 python 3.12 帮我编写一个会话功能的后端服务，类似chatGPT聊天窗口功能，名为：sess。提供如下restult API接口：

1. 新建会话
  - 描述：创建一个会话，以供用户与服务器聊天
  - 地址：POST /api/sess
  - 入参：sess_name, token(request header)
  - 返回：成功或失败
  - 处理逻辑：会话可以理解为一个对话框，它包含了无数条聊天信息。
2. 查询会话
  - 描述：列出当前登录用户下所有的会话。
  - 地址：GET /api/sess
  - 入参：token(request header)
  - 返回：sess。至少包含：id, sess_name字段
  - 处理逻辑：根据token中的用户信息，查找并列出对应用户下的会话。不可列出其他用户的会话。
3. 发送聊天信息
  - 描述：登录用户在指定的sess内发送聊天内容
  - 地址：POST /api/sess/:sess_id/chat
  - 入参：sess_id, chat_content, token(request header)
  - 返回：成功或失败
  - 处理逻辑：在对应的sess内创建聊天记录，需要记录聊天的内容、发送的时间，以及是由谁发送的。由用户发送的聊天记录其 from 属性标记为 user ，由服务自动回复的 from 属性标记为 server 。在服务器接收完用的消息后，自动回复一条“好的，我收到了。”以模拟chatGPT的回复。另外，用户的聊天内容可以选择文档服务中用户自己的文档，这个文档以链接形式在聊天内容中呈现。格式类似markdown中的链接：[doc_nam](doc_link)。
4. 查询会话下所有聊天记录
  - 描述：列出当前登录用户下所有的会话。
  - 地址：GET /api/sess/:sess_id/chat
  - 入参：sess_id, token(request header)
  - 返回：依据时间正向排序，返回sess_id下对应所有聊天记录。至少包含：chat_id, chat_content, create_at, from字段
  - 处理逻辑：根据token中的用户信息，查找并列出对应用户所指定会话下的所有聊天记录。不可列出其他用户的会话中的聊天记录。

技术要求：
1. 以微服务形式，使用python 3.12、flask开发
2. 使用mongodb 8.0.3作为数据库
3. 代码生成在./apps/sess目录内
4. 服务启动后们需要注册到mDNS内，以便后续的其他服务能够找到它，并可通过restful调用它。
5. 书写详细的设计文档，包括数据流程，到./apps/sess/readme.md内
6. requirements请更新在 ./requirements.txt中
