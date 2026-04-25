from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.validator.service import validate_script

app = FastAPI(title="AFSIM Validator Service", version="0.1.0")


class ValidateRequest(BaseModel):
    """校验接口请求体，承载待检查的脚本文本。"""

    script_content: str = Field(..., min_length=1)


@app.get("/health")
def health() -> dict:
    """健康检查接口，用于容器与服务存活探针。"""
    return {"status": "ok"}


@app.post("/validate")
def validate(request: ValidateRequest) -> dict:
    """调用校验服务并返回结构化结果。"""
    return validate_script(request.script_content)
