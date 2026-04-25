# AFSIM 脚本智能体设计方案 (专业版 - 最终修正)

## 1. 引言

本方案旨在为 AFSIM 仿真系统构建一个高度智能化的 AI 代理，其核心任务是将用户提供的结构化文本（如仿真场景描述、实体行为设定）自动转换为可执行的 AFSIM 领域特定语言（DSL）脚本。基于您提供的 `acoustic_demo.txt`，本方案已针对 AFSIM 的 **关键字定义、嵌套结构、单位系统及黑盒校验反馈** 进行了深度优化。

## 2. 系统架构设计

### 2.1 总体架构

系统采用基于 **LangGraph** 的多代理协作流。AI 不直接与底层 C++ 交互，而是作为“DSL 专家”，通过 AFSIM 命令行工具的反馈来迭代优化脚本。

![AFSIM 脚本智能体总体架构图](https://private-us-east-1.manuscdn.com/sessionFile/iE7SdQXBpuMOTJTXMjekYj/sandbox/i4W17RwPXE9dU4xSZ5e3yj-images_1777085404233_na1fn_L2hvbWUvdWJ1bnR1L2RldGFpbGVkX2FyY2hpdGVjdHVyZV9kaWFncmFt.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvaUU3U2RRWEJwdU1PVEpUWE1qZWtZai9zYW5kYm94L2k0VzE3UndQWEU5ZFU0eFNaNWUzeWotaW1hZ2VzXzE3NzcwODU0MDQyMzNfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyUmxkR0ZwYkdWa1gyRnlZMmhwZEdWamRIVnlaVjlrYVdGbmNtRnQucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=t5v8YueD9JzgZLWLVySMxL2AZOH8-yHxdh86snou~wuDFL9Jnc~GH~1HTPTHXUmXr402MFGqL32EbSydmdNpEZmBb1mtDESeOlRSrDVYRXatS5VdbhceAkM6VKQEMow4-egQ-LHq~cX-EhSTgoBo8ptlvUGUtijQiOTWDI5AzdgZPgFja-QEkATC9a4aLxTSDnQd4uvlC-BpkvDtDZVKlqjzmWsn44mp1CiPBrjZ7i8iJYyeSa2tB44XH-I~gxiIV7rmp5TnAdBdJ2jx~uxmtQjcCtOitsK4t798AEFB3wa7Sl2475L2cX9AYCwBIvHfvyYphemRrRLMMdPdJXq8Pg__)

### 2.2 针对 AFSIM DSL 的核心设计

基于 Demo 的语法特征，系统在以下三个维度进行了专项设计：

#### 2.2.1 结构化语法建模 (DSL Modeling)
AI 需要识别并生成以下典型的 AFSIM 结构：
*   **资源定义层**：如 `acoustic_signature` 及其嵌套的 `spectrum_data` 块。
*   **类型定义层**：如 `platform_type` 与 `sensor` 的组合，支持基于父类（如 `WSF_PLATFORM`, `WSF_ACOUSTIC_SENSOR`）的扩展。
*   **实例部署层**：如 `platform` 实例，包含 `position`, `side`, `route` 等属性。
*   **环境与输出控制**：如 `event_pipe`, `event_output`, `end_time`。

#### 2.2.2 黑盒校验反馈循环 (Black-box Feedback)
当 AFSIM 命令行工具返回错误时，系统将错误分为两类处理：
*   **语法错误 (Parser Errors)**：如 `end_spectrum_data` 缺失。AI 直接定位行号并根据 DSL 规范修复。
*   **运行时逻辑错误 (Runtime Clues)**：如 `position` 坐标格式不合法或 `side` 未定义。即使报错信息包含 C++ 堆栈，AI 也会通过“错误模式库”将其映射回 DSL 脚本中的具体参数。

#### 2.2.3 知识库与 Few-shot 策略
*   **Demo 驱动**：将 `acoustic_demo.txt` 作为核心示例（Few-shot），引导 AI 学习 `freq`, `noise_pressure`, `dB_20uPa` 等单位和关键字的用法。
*   **模式匹配**：建立“结构化文本 -> DSL 片段”的映射库，例如：将“红方部署在 30.1n”映射为 `platform ... side red position 30.1n ... end_platform`。

## 3. 任务开发文档 (Implementation Guide)

本节面向开发人员，详细描述如何实现该智能体系统。

### 3.1 核心组件实现

#### A. DSL 知识库构建 (Vector DB)
*   **存储内容**：将 AFSIM 用户手册、DSL 关键字说明、以及 `acoustic_demo.txt` 进行分块存储。
*   **检索逻辑**：当用户提到“声纳”或“轨迹”时，优先检索 `sensor`, `acoustic_signature` 和 `route` 相关的 DSL 片段。

#### B. LangGraph 节点逻辑
1.  **`Generator` 节点**：
    *   **Prompt 策略**：使用系统级指令定义 AI 为“AFSIM 资深仿真工程师”。
    *   **上下文注入**：注入检索到的 DSL 示例。
2.  **`Validator` 节点**：
    *   **环境**：Docker 容器，安装 AFSIM 环境。
    *   **执行**：`afsim_cli --check scenario.txt`。
    *   **输出标准化**：将 `stderr` 解析为 JSON 格式：`{"line": 76, "error": "Unexpected end of file", "context": "end_spectrum_data"}`。
3.  **`Refiner` 节点**：
    *   **分析逻辑**：根据 `Validator` 的 JSON 输出，结合 `Generator` 的历史记录，生成修复指令。

### 3.2 任务清单 (Roadmap)

| 阶段 | 任务描述 | 关键产出 |
| :--- | :--- | :--- |
| **S1: 基础环境** | 搭建 AFSIM Docker 镜像，实现 Python 调用 CLI 接口。 | `Validator` 微服务 |
| **S2: 知识工程** | 对 `acoustic_demo.txt` 进行标注，构建初版向量知识库。 | DSL 知识库 |
| **S3: 代理开发** | 编写 LangGraph 状态机，实现“生成-校验-修复”闭环。 | AI 代理核心代码 |
| **S4: 调优测试** | 针对 demo 语法进行 50+ 组压力测试，优化修复准确率。 | 评估报告 |

### 3.3 示例 Prompt 结构 (针对 Demo)

```markdown
### 角色：AFSIM DSL 专家
### 任务：将以下描述转换为 AFSIM 脚本
### 描述：创建一个名为 "blue_sub" 的平台，使用 ACOUSTIC_TARGET 类型，部署在 30n 30e，向北以 10 节速度行驶。
### 参考示例：
(此处插入 acoustic_demo.txt 中的相关片段)
### 要求：
1. 必须包含 end_platform 闭合标签。
2. 坐标格式必须符合 30n 30e 规范。
3. 必须定义 side 属性。
```

## 4. 总结

本方案通过将 AFSIM 视为“黑盒环境”，利用 AI 的强语言理解能力来适配其自定义 DSL。提供的 `acoustic_demo.txt` 已经为 AI 学习复杂的嵌套结构（如 `spectrum_data`）提供了完美的蓝图。后续开发应重点关注**错误信息的结构化解析**，这是提升系统自动修复率的关键。
