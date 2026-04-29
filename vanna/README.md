# Vanna 2.0.2源码结构

**结构如以下描述但不限于，具体以实际目录结构为准**

- 代码库的组织清晰地分离了关注点，使代码库对新手易于理解，同时为高级用户保持模块化。
- vanna-2.0.2/src/vanna 目录包含按逻辑域组织的主要框架代码：
    - core 用于基础抽象，
    - agents 用于编排逻辑，
    - tools 用于内置功能，
    - capabilities 用于可扩展接口，
    - integrations 用于第三方适配器，
    - servers 用于 Web 服务器实现，
    - web_components 用于前端资源。
    - examples 目录包含全面的、可运行的示例，展示了不同的用例和集成模式。
    - notebooks 目录包括像 quickstart.ipynb 这样的交互式教程，用于动手学习。
    - tests 目录提供广泛的测试覆盖，包括健全性检查、集成测试和工作流测试。
    - papers 目录记录了研究发现和架构决策，包括准确性基准和框架比较。


## 目录结构
```text
vanna-2.0.2/src/vanna
├── core/                    
│   ├── agent/              # Agent 编排和配置
│   ├── tool/               # 工具基类和模型
│   ├── llm/                # LLM 服务接口
│   ├── storage/            # 对话存储接口
│   ├── system_prompt/      # 系统提示词构建器
│   ├── workflow/           # 工作流处理程序系统
│   ├── registry.py         # 工具注册表
│   ├── user/               # 用户和请求上下文
│   ├── lifecycle/          # 生命周期钩子
│   ├── middleware/         # LLM 中间件
│   ├── enricher/           # 上下文增强
│   ├── enhancer/           # LLM 上下文增强
│   ├── filter/             # 对话过滤
│   ├── observability/      # 遥测和监控
│   ├── audit/              # 审计日志
│   └── recovery/           # 错误恢复策略
├── capabilities/            # 可重用能力
│   ├── agent_memory/       # RAG 内存系统
│   ├── file_system/        # 文件系统抽象
│   └── sql_runner/         # 数据库查询抽象
├── components/             # UI 组件
│   ├── base.py             # 组件基础接口
│   ├── simple/             # 简单组件 (文本, 图像, 链接)
│   └── rich/               # 富组件 (表格, 图表 等)
├── tools/                  # 内置工具
│   ├── run_sql.py          # SQL 执行工具
│   ├── visualize_data.py   # 图表生成工具
│   ├── agent_memory.py     # 内存搜索工具
│   ├── file_system.py      # 文件操作工具
│   └── python.py           # Python 执行工具
├── integrations/           # 提供商实现
│   ├── anthropic/          # Anthropic LLM
│   ├── openai/             # OpenAI LLM
│   ├── ollama/             # Ollama LLM
│   ├── google/             # Google Gemini
│   ├── azureopenai/        # Azure OpenAI
│   ├── postgres/           # PostgreSQL 连接器
│   ├── mysql/              # MySQL 连接器
│   ├── sqlite/             # SQLite 连接器
│   ├── snowflake/          # Snowflake 连接器
│   ├── bigquery/           # BigQuery 连接器
│   ├── chromadb/           # ChromaDB 内存
│   ├── pinecone/           # Pinecone 内存
│   ├── qdrant/             # Qdrant 内存
│   └── local/              # 内存实现
├── servers/                # 服务器实现
│   ├── fastapi/            # FastAPI 服务器
│   ├── flask/              # Flask 服务器
│   ├── base/               # 共享服务器工具
│   └── cli/                # 用于服务器管理的 CLI
├── legacy/                 # Vanna 1.x 兼容层
├── examples/               # 示例实现
└── web_components/         # 前端 Web 组件
```
