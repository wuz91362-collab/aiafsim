from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.validator.service import validate_script

app = FastAPI(title="AFSIM Validator Service", version="0.1.0")


class ValidateRequest(BaseModel):
    script_content: str = Field(..., min_length=1)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/validate")
def validate(request: ValidateRequest) -> dict:
    return validate_script(request.script_content)
