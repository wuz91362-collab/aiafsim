from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    afsim_cli: str = "afsim_cli"
    validator_timeout_seconds: int = 15
    max_iterations: int = 3
    knowledge_file: str = "data/knowledge/afsim_chunks.json"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
