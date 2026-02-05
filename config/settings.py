from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment / .env file."""

    groq_api_key: str
    gemini_api_key: str = ""
    embedding_model: str = "all-MiniLM-L6-v2"
    max_sub_tasks: int = 5
    arxiv_max_results: int = 5
    web_max_results: int = 5

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
