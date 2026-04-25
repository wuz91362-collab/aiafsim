from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """集中管理应用运行参数，支持从环境变量覆盖默认值。"""

    afsim_cli: str = "afsim_cli"
    validator_timeout_seconds: int = 15
    max_iterations: int = 3
    knowledge_file: str = "data/knowledge/afsim_chunks.json"
    rag_backend: str = "json"
    chroma_persist_directory: str = "data/chroma"
    chroma_collection_name: str = "afsim_dsl"
    chroma_enable_bootstrap: bool = True
    llm_backend: str = "mock"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b-instruct-2507"
    ollama_timeout_seconds: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
