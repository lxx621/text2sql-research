# Vanna 2.0 快速入门示例

基于 Vanna 2.0 的 Text-to-SQL Agent 示例项目，使用本地 Ollama 模型（gemma4:e4b）实现自然语言到 SQL 的转换。

## 项目说明

本项目演示了如何使用 Vanna 2.0 框架创建一个 AI Agent，能够：
- 理解自然语言问题
- 自动生成 SQL 查询
- 执行查询并返回结果
- 提供数据可视化
- 支持用户权限管理

## 技术栈

- **框架**: Vanna 2.0.2
- **LLM**: Ollama (gemma4:e4b)
- **数据库**: SQLite (Chinook 示例数据库)
- **Web 服务**: FastAPI
- **Python 版本**: 3.9+

## 前置要求

### 1. 安装 Ollama

下载并安装 [Ollama](https://ollama.com/)

### 2. 拉取 gemma4:e4b 模型

```bash
ollama pull gemma4:e4b
```

### 3. 启动 Ollama 服务

```bash
ollama serve
```

默认运行在 `http://localhost:11434`

## 安装步骤

### 1. 创建虚拟环境

```bash
python -m venv venv
```

### 2. 激活虚拟环境

**Windows:**
```bash
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python app.py
```

启动后，服务器将运行在 `http://localhost:8000`

## 使用说明

### Web UI 访问

1. 在浏览器中打开: http://localhost:8000
2. 设置 Cookie: `vanna_email=admin@example.com` (管理员权限)
   - 或设置 `vanna_email=user@example.com` (普通用户权限)
3. 开始用自然语言提问

### 示例问题

- "列出所有艺术家"
- "查询销量最高的专辑"
- "显示客户数量"
- "查找某个艺术家的所有专辑"

### API 端点

- **流式聊天**: `POST http://localhost:8000/api/vanna/v2/chat_sse`

## 项目结构

```
src/1-quickstart/
├── app.py              # 主程序文件
├── requirements.txt    # 项目依赖
├── README.md          # 说明文档
└── Chinook.sqlite     # 示例数据库（首次运行时自动下载）
```

## 核心功能

### 1. 用户认证

使用基于 Cookie 的简单认证系统：
- `admin@example.com`: 管理员权限（可保存正确的工具使用）
- 其他用户: 普通用户权限（仅可查询和搜索）

### 2. 工具权限控制

- **RunSqlTool**: 执行 SQL 查询（admin, user）
- **VisualizeDataTool**: 数据可视化（admin, user）
- **SaveQuestionToolArgsTool**: 保存正确工具使用（admin only）
- **SearchSavedCorrectToolUsesTool**: 搜索历史记录（admin, user）

### 3. Agent 记忆

使用 `DemoAgentMemory` 存储最多 1000 条历史记录，支持学习和改进。

## 配置说明

### Ollama 配置

在 `app.py` 中修改以下配置：

```python
llm = OllamaLlmService(
    model="gemma4:e4b",        # 模型名称
    base_url="http://localhost:11434"  # Ollama 服务地址
)
```

### 服务器配置

```python
server.run(host='0.0.0.0', port=8000)  # 修改端口和主机
```

## 常见问题

### 1. Ollama 连接失败

确保 Ollama 服务正在运行：
```bash
ollama serve
```

### 2. 模型未找到

确保已拉取 gemma4:e4b 模型：
```bash
ollama pull gemma4:e4b
```

### 3. 数据库下载失败

首次运行需要联网下载 Chinook.sqlite，如果失败可手动下载：
https://vanna.ai/Chinook.sqlite

## 参考文档

- [Vanna 2.0 官方文档](https://zread.ai/vanna-ai/vanna/2-quick-start)
- [Ollama 官方文档](https://ollama.com/)
- [Chinook 数据库文档](https://github.com/lerocha/chinook-database)

## 注意事项

- 所有文件使用 UTF-8 编码（无 BOM）
- 依赖安装在项目虚拟环境中
- 目录 `vanna` 为只读，禁止修改
- 技术决策需参考官方文档
