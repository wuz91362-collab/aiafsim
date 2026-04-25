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

## Docker 与离线部署

项目已支持“离线优先”镜像构建策略：

- 如果 `wheelhouse/` 里有依赖包，Docker 构建时使用离线安装（`--no-index`）
- 如果 `wheelhouse/` 为空，构建时回退在线安装（方便开发环境）

### 1) 在联网机器准备离线依赖包

```powershell
./scripts/prepare_offline_bundle.ps1
```

执行后会把 `requirements.txt` 对应依赖下载到 `wheelhouse/`。

### 2) 构建并启动容器（目标离线环境）

请先将 AFSIM 运行时文件放到项目根目录 `afsim_bin/`（容器内挂载到 `/opt/afsim`）。

```bash
docker compose up -d --build
```

### 3) 健康检查

```bash
curl http://localhost:8001/health
```

返回 `{"status":"ok"}` 即启动成功。

## 环境变量

参考 `.env.example`：

- `AFSIM_CLI`：AFSIM 命令行可执行文件名或绝对路径
- `VALIDATOR_TIMEOUT_SECONDS`：校验超时
- `MAX_ITERATIONS`：最大修复迭代次数
- `KNOWLEDGE_FILE`：知识库 JSON 路径
- `AFSIM_CLI`：容器中建议设为 `/opt/afsim/afsim_cli`

## 下一步建议

- 用真实 LLM 接入 `generator_node` / `debugger_node`
- 将 `LocalKnowledgeStore` 替换为向量数据库检索
- 按 AFSIM 真实报错格式完善 `error_parser.py`
