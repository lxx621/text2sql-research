"""
Vanna 2.0 快速入门示例 - 使用 Ollama LLM
本示例演示如何使用本地 Ollama 模型（gemma4:e4b）创建 Text-to-SQL Agent
"""

import httpx
from vanna import Agent, AgentConfig
from vanna.core.user import UserResolver, User, RequestContext
from vanna.core.registry import ToolRegistry
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.ollama import OllamaLlmService
from vanna.servers.fastapi import VannaFastAPIServer


def download_database():
    """
    下载 Chinook SQLite 示例数据库
    Chinook 是一个包含艺术家、专辑、曲目和客户信息的示例数据库
    如果本地文件已存在，则跳过下载
    """
    import os
    
    database_path = "Chinook.sqlite"
    
    # 检查本地文件是否已存在
    if os.path.exists(database_path):
        print(f"数据库文件 {database_path} 已存在，跳过下载")
        return
    
    print("正在下载 Chinook SQLite 示例数据库...")
    with open(database_path, "wb") as f:
        with httpx.stream("GET", "https://vanna.ai/Chinook.sqlite") as response:
            for chunk in response.iter_bytes():
                f.write(chunk)
    print("数据库下载完成！")


class SimpleUserResolver(UserResolver):
    """
    简单的用户认证解析器
    从 Cookie 中提取用户邮箱并分配用户组权限
    """

    async def resolve_user(self, request_context: RequestContext) -> User:
        """
        解析用户身份
        支持从 Cookie、URL 参数或请求头中提取用户标识
        :param request_context: 请求上下文
        :return: 用户对象
        :raises ValueError: 如果缺少用户标识
        """
        # 优先从 Cookie 中提取用户标识
        user_email = request_context.get_cookie('vanna_email')
        
        # 如果 Cookie 中没有，尝试从 URL 参数获取
        if not user_email:
            # query_params 是一个字典，直接访问
            if request_context.query_params and 'email' in request_context.query_params:
                user_email = request_context.query_params['email']
        
        # 如果 URL 参数也没有，尝试从请求头获取
        if not user_email:
            user_email = request_context.get_header('X-Vanna-Email')
        
        if not user_email:
            raise ValueError("缺少用户标识，请通过 Cookie、URL 参数 (?email=xxx) 或请求头 (X-Vanna-Email) 提供")

        # 为权限检查分配用户组成员资格
        if user_email == "admin@example.com":
            return User(
                id="admin1",
                email=user_email,
                group_memberships=['admin']
            )
        return User(
            id="user1",
            email=user_email,
            group_memberships=['user']
        )


def setup_tools():
    """
    配置工具注册表和访问控制
    :return: 工具注册表和代理记忆
    """
    # 创建工具注册表
    tools = ToolRegistry()

    # 使用基于组的访问控制注册工具
    # RunSqlTool - 执行 SQL 查询（admin 和 user 都可访问）
    tools.register_local_tool(
        RunSqlTool(sql_runner=SqliteRunner(database_path="./Chinook.sqlite")),
        access_groups=['admin', 'user']
    )

    # VisualizeDataTool - 数据可视化（admin 和 user 都可访问）
    tools.register_local_tool(
        VisualizeDataTool(),
        access_groups=['admin', 'user']
    )

    # 代理记忆工具
    agent_memory = DemoAgentMemory(max_items=1000)

    # SaveQuestionToolArgsTool - 保存正确的工具使用（仅 admin 可访问）
    tools.register_local_tool(
        SaveQuestionToolArgsTool(),
        access_groups=['admin']
    )

    # SearchSavedCorrectToolUsesTool - 搜索保存的正确工具使用（admin 和 user 都可访问）
    tools.register_local_tool(
        SearchSavedCorrectToolUsesTool(),
        access_groups=['admin', 'user']
    )

    return tools, agent_memory


def main():
    """
    主函数：配置并启动 Vanna Agent 服务器
    """
    # 步骤 1：下载示例数据库
    try:
        download_database()
    except Exception as e:
        print(f"数据库下载失败: {e}")
        return

    # 步骤 2：配置 Ollama LLM 服务
    # 使用本地 Ollama 模型 gemma4:e4b
    print("正在配置 Ollama LLM 服务...")
    llm = OllamaLlmService(
        model="gemma4:e4b",
        base_url="http://localhost:11434"
    )
    print("Ollama LLM 服务配置完成！")

    # 步骤 3：配置工具和访问控制
    print("正在配置工具...")
    tools, agent_memory = setup_tools()
    print("工具配置完成！")

    # 步骤 4：创建 Agent
    print("正在创建 Agent...")
    agent = Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=SimpleUserResolver(),
        config=AgentConfig(),
        agent_memory=agent_memory
    )
    print("Agent 创建完成！")

    # 步骤 5：创建并运行 FastAPI 服务器
    print("正在启动 FastAPI 服务器...")
    server = VannaFastAPIServer(agent)
    print("\n" + "="*60)
    print("Vanna Agent 服务器已启动！")
    print("="*60)
    print("Web UI 访问地址: http://localhost:8000")
    print("API 端点: POST http://localhost:8000/api/vanna/v2/chat_sse")
    print("\n使用提示:")
    print("1. 在浏览器中打开 http://localhost:8000")
    print("2. 设置 Cookie: vanna_email=admin@example.com (或 user@example.com)")
    print("3. 开始用自然语言提问，例如：'列出所有艺术家'")
    print("="*60 + "\n")

    server.run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    main()
