# AFSIM 脚本智能体任务开发文档 (Implementation Guide)

## 1. 任务目标
开发一个基于 LangGraph 的 AI 智能体系统，实现从结构化文本（需求）到 AFSIM DSL 脚本的自动生成与闭环校验修复。

## 2. 核心模块开发指南

### 2.1 校验器模块 (Validator Service)
**目标**：在隔离环境中运行 AFSIM 命令行工具并返回结构化错误。

*   **技术栈**：Docker, Python `subprocess`, FastAPI
*   **关键代码逻辑**：
    ```python
    def check_script(script_content: str):
        with open("temp.txt", "w") as f:
            f.write(script_content)
        # 调用 AFSIM 校验命令 (示例命令)
        result = subprocess.run(
            ["afsim_cli", "--validate", "temp.txt"],
            capture_output=True, text=True
        )
        return parse_errors(result.stderr)
    ```
*   **错误解析规则**：
    *   匹配模式：`Error at line (\d+): (.*)`
    *   映射逻辑：提取行号和错误描述，供 AI 节点使用。

### 2.2 知识库构建 (RAG & Few-shot)
**目标**：为 AI 提供 AFSIM DSL 的“标准答案”。

*   **数据处理**：
    *   将 `acoustic_demo.txt` 拆分为：`acoustic_signature` 模板、`platform_type` 模板、`platform` 部署模板。
*   **向量化策略**：使用 OpenAI `text-embedding-3-small` 或类似模型。
*   **检索逻辑**：
    ```python
    # 当输入包含 "acoustic" 时，检索 demo 中的：
    # acoustic_signature, spectrum_data, noise_pressure
    ```

### 2.3 AI 代理工作流 (LangGraph)
**目标**：实现状态机逻辑。

*   **状态定义 (State)**：
    ```python
    class AgentState(TypedDict):
        requirement: str      # 用户原始需求
        current_script: str   # 当前生成的脚本
        errors: List[Dict]    # 校验器返回的错误列表
        iteration: int        # 当前重试次数
    ```
*   **节点设计**：
    1.  **`designer`**：负责根据 `requirement` 和检索到的知识生成初稿。
    2.  **`executor`**：调用校验器模块。
    3.  **`debugger`**：如果 `errors` 不为空，分析错误并给出修改建议。

## 3. 针对 Demo 语法的专项开发建议

### 3.1 嵌套结构处理
AFSIM 脚本中存在大量 `... end_...` 的嵌套（如 `spectrum_data ... end_spectrum_data`）。
*   **开发建议**：在 Prompt 中强制要求 AI 进行“闭合标签自检”。
*   **示例指令**：`"Ensure every block starting with 'sensor' ends with 'end_sensor'."`

### 3.2 单位系统映射
Demo 中使用了 `feet`, `hz`, `dB_20uPa`, `kts`, `deg` 等单位。
*   **开发建议**：建立单位白名单。如果校验器报错“Invalid unit”，引导 AI 检索单位规范库。

### 3.3 坐标系统转换
Demo 坐标支持 `30.1n 30e` 和 `29:30:57.34n 30e`。
*   **开发建议**：提供坐标转换工具函数作为 LLM 的 Tool 调用，确保生成的坐标格式始终合法。

## 4. 测试与评估 (QA)

### 4.1 测试用例集
1.  **基础部署测试**：仅包含一个平台和基本属性。
2.  **声纳配置测试**：包含 `acoustic_signature` 和 `sensor` 关联。
3.  **复杂航线测试**：包含多点 `route` 和变速率设定。

### 4.2 评估指标
*   **一次通过率 (Pass@1)**：AI 首次生成即通过校验的比例。
*   **修复成功率**：在 3 次迭代内通过校验的比例。

## 5. 开发者 Checklist
- [ ] AFSIM 命令行工具是否能在 Linux 环境稳定运行？
- [ ] 向量数据库是否已包含所有 Demo 中的关键字？
- [ ] LangGraph 是否设置了最大循环次数（防止无限重试）？
- [ ] 错误解析器是否能处理包含 C++ 堆栈信息的复杂报错？
