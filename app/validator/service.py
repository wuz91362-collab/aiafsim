from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from app.config import settings
from app.validator.error_parser import parse_errors


def validate_script(script_content: str) -> dict:
    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = Path(temp_dir) / "scenario.txt"
        script_path.write_text(script_content, encoding="utf-8")

        command = [settings.afsim_cli, "--check", str(script_path)]
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
