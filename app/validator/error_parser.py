from __future__ import annotations

import re

ERROR_PATTERNS = [
    re.compile(r"line (\d+): (.*)", re.IGNORECASE),
    re.compile(r"Error at line (\d+): (.*)", re.IGNORECASE),
]


def parse_errors(stderr: str) -> list[dict]:
    errors: list[dict] = []
    for row in stderr.splitlines():
        for pattern in ERROR_PATTERNS:
            matched = pattern.search(row)
            if matched:
                errors.append(
                    {
                        "line": int(matched.group(1)),
                        "message": matched.group(2).strip(),
                        "raw": row.strip(),
                    }
                )
                break
    return errors
