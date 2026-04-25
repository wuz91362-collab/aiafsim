from __future__ import annotations

import json
from urllib import error, request

from app.config import settings


class OllamaLLMClient:
    """通过 Ollama HTTP API 调用本地模型。"""

    def __init__(self, ollama_url: str, model: str, timeout_seconds: int) -> None:
        """初始化 Ollama 连接配置。"""
        self.ollama_url = ollama_url
        self.model = model
        self.timeout_seconds = timeout_seconds

    def _generate(self, prompt: str) -> str:
        """调用 Ollama generate 接口获取非流式文本结果。"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7},
        }
        req = request.Request(
            url=self.ollama_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                response = body.get("response", "").strip()
                if not response:
                    raise RuntimeError("Ollama 返回空响应，无法生成脚本。")
                return response
        except error.URLError as exc:
            raise RuntimeError(f"Ollama 请求失败: {exc}") from exc
        except TimeoutError as exc:
            raise RuntimeError("Ollama 请求超时。") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError("Ollama 响应 JSON 解析失败。") from exc

    def generate_script(self, requirement: str, references: str) -> str:
        """使用 AFSIM 专家提示词生成脚本。"""
        prompt = f"""
你是一位 AFSIM DSL 专家。请根据需求输出可校验通过的脚本。

平台语法规则：
1) 平台定义格式：platform <platform_name> <platform_type>
2) 平台名称是自定义的，不可重复
3) 平台类型必须是已定义的类型，如 SUB_TYPE, ACOUSTIC_TARGET 等
4) 阵营定义：side <side_name>，如 blue 或 red
5) 位置定义：position <latitude> <longitude> altitude <altitude_value> <altitude_unit>
   - 纬度格式如 30n 或 30:10:00.00n
   - 经度格式如 30e 或 30:10:00.00e
   - 高度单位如 m, ft, agl
6) 路线定义：route ... end_route
   - 路线包含多个位置点和速度
   - 速度定义：speed <speed_value> <speed_unit>，如 speed 10 kts
7) 朝向定义：heading <heading_value> deg
8) 所有块必须正确闭合，如 end_platform

约束：
1) 所有块必须正确闭合（如 end_platform / end_sensor）。
2) 坐标、单位合法（hz, dB_20uPa, kts, deg, m, ft, agl）。
3) 仅输出脚本正文，不要解释。

需求：
{requirement}

参考片段：
{references}
""".strip()
        return self._generate(prompt)

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
        return self._generate(prompt)


def build_llm_client() -> OllamaLLMClient:
    """按配置构建 Ollama LLM 客户端。"""
    return OllamaLLMClient(
        ollama_url=settings.ollama_url,
        model=settings.ollama_model,
        timeout_seconds=settings.ollama_timeout_seconds,
    )
