# AFSIM 脚本智能体框架

基于文档要求搭建的首版工程骨架，包含：

- LangGraph 状态机：`Generator -> Validator -> Debugger` 闭环
- Validator 微服务（FastAPI）：执行 `afsim_cli --check` 并结构化错误
- RAG 知识库接口：本地 JSON 检索占位实现，可替换向量数据库
- 统一配置与启动入口

## 目录结构

`app/`

- `main.py`：应用入口与演示流程
- `config.py`：配置项
- `models/state.py`：LangGraph 状态定义
- `graph/nodes.py`：三个核心节点
- `graph/workflow.py`：图编排与路由
- `validator/`：校验执行、错误解析、API 路由
- `rag/store.py`：知识库检索

`docker/validator/Dockerfile`：AFSIM 校验容器示例  
`data/knowledge/afsim_chunks.json`：知识片段样例

## 快速开始

1. 安装依赖（推荐 `uv`）：

```bash
uv sync
```

2. 启动 Validator API：

```bash
uv run uvicorn app.validator.api:app --reload --port 8001
```

3. 运行一次工作流演示：

```bash
uv run python -m app.main
```

## 环境变量

参考 `.env.example`：

- `AFSIM_CLI`：AFSIM 命令行可执行文件名或绝对路径
- `VALIDATOR_TIMEOUT_SECONDS`：校验超时
- `MAX_ITERATIONS`：最大修复迭代次数
- `KNOWLEDGE_FILE`：知识库 JSON 路径

## 下一步建议

- 用真实 LLM 接入 `generator_node` / `debugger_node`
- 将 `LocalKnowledgeStore` 替换为向量数据库检索
- 按 AFSIM 真实报错格式完善 `error_parser.py`
