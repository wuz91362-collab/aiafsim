from __future__ import annotations

import json
from urllib import error, request

from app.config import settings


class BaseLLMClient:
    """定义脚本生成与修复能力的统一接口。"""

    def generate_script(self, requirement: str, references: str) -> str:
        """根据需求和参考片段生成 AFSIM 脚本。"""
        raise NotImplementedError

    def refine_script(self, script: str, errors: list[dict], references: str) -> str:
        """根据校验错误对脚本进行修复。"""
        raise NotImplementedError


class MockLLMClient(BaseLLMClient):
    """本地占位模型，保证无大模型环境也可运行流程。"""

    def generate_script(self, requirement: str, references: str) -> str:
        """返回可用于联调的固定模板脚本。"""
        return (
            f"# requirement\n{requirement}\n\n"
            f"# references\n{references}\n\n"
            "platform blue_sub WSF_PLATFORM\n"
            "  side blue\n"
            "  position 30n 30e\n"
            "end_platform\n"
        )

    def refine_script(self, script: str, errors: list[dict], references: str) -> str:
        """将错误摘要追加到脚本末尾，作为占位修复策略。"""
        error_hint = "\n".join(
            [f"- line {e.get('line', '?')}: {e.get('message', '')}" for e in errors]
        )
        return (
            f"{script}\n"
            f"# debug_references\n{references}\n"
            f"# auto_fix_hints\n{error_hint}\n"
        )


class OllamaLLMClient(BaseLLMClient):
    """通过 Ollama HTTP API 调用本地模型。"""

    def __init__(self, base_url: str, model: str, timeout_seconds: int) -> None:
        """初始化 Ollama 连接配置。"""
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def _generate(self, prompt: str) -> str:
        """调用 /api/generate 获取非流式文本结果。"""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1},
        }
        req = request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return body.get("response", "").strip()
        except (error.URLError, TimeoutError, json.JSONDecodeError):
            # 大模型不可达时回退空字符串，由上层触发降级策略。
            return ""

    def generate_script(self, requirement: str, references: str) -> str:
        """使用 AFSIM 专家提示词生成脚本。"""
        prompt = f"""
你是一位 AFSIM DSL 专家。请根据需求输出可校验通过的脚本。
约束：
1) 所有块必须正确闭合（如 end_platform / end_sensor）。
2) 坐标、单位合法（hz, dB_20uPa, kts, deg）。
3) 仅输出脚本正文，不要解释。

需求：
{requirement}

参考片段：
{references}
""".strip()
        generated = self._generate(prompt)
        if generated:
            return generated
        return MockLLMClient().generate_script(requirement, references)

    def refine_script(self, script: str, errors: list[dict], references: str) -> str:
        """根据错误信息请求模型返回修复后的完整脚本。"""
        error_text = "\n".join(
            [f"- line {item.get('line', '?')}: {item.get('message', '')}" for item in errors]
        )
        prompt = f"""
你是一位 AFSIM DSL 修复专家。请根据错误修复脚本并返回完整脚本。
仅输出修复后的脚本正文，不要解释。

当前脚本：
{script}

错误信息：
{error_text}

参考片段：
{references}
""".strip()
        refined = self._generate(prompt)
        if refined:
            return refined
        return MockLLMClient().refine_script(script, errors, references)


def build_llm_client() -> BaseLLMClient:
    """按配置构建 LLM 客户端，默认使用本地占位实现。"""
    if settings.llm_backend.lower() == "ollama":
        return OllamaLLMClient(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            timeout_seconds=settings.ollama_timeout_seconds,
        )
    return MockLLMClient()
