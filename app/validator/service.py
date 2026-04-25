from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from app.config import settings
from app.validator.error_parser import parse_errors


def validate_script(script_content: str) -> dict:
    """执行 AFSIM CLI 校验并统一返回结构化结果。"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # 使用临时文件隔离每次校验，避免并发时互相覆盖。
        script_path = Path(temp_dir) / "scenario.txt"
        script_path.write_text(script_content, encoding="utf-8")

        command = [settings.afsim_cli, "--check", str(script_path)]
        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=settings.validator_timeout_seconds,
                check=False,
            )
            errors = parse_errors(process.stderr)
            return {
                "is_valid": process.returncode == 0 and not errors,
                "errors": errors,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "return_code": process.returncode,
            }
        except FileNotFoundError:
            # 离线部署中常见：AFSIM 可执行文件尚未挂载或路径配置错误。
            return {
                "is_valid": False,
                "errors": [
                    {
                        "line": 0,
                        "message": f"AFSIM CLI not found: {settings.afsim_cli}",
                        "raw": "FileNotFoundError",
                    }
                ],
                "stdout": "",
                "stderr": "",
                "return_code": 127,
            }
        except subprocess.TimeoutExpired:
            return {
                "is_valid": False,
                "errors": [
                    {
                        "line": 0,
                        "message": f"Validation timeout after {settings.validator_timeout_seconds}s",
                        "raw": "TimeoutExpired",
                    }
                ],
                "stdout": "",
                "stderr": "",
                "return_code": 124,
            }
