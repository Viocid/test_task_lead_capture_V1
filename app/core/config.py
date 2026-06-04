from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Alakris Lead Capture"
    app_description: str = (
        "Мини-прототип backend-first API для создания и просмотра заявок."
    )
    database_url: str = "sqlite+aiosqlite:///./data/leads.db"
    logging_format: str = "%(asctime)s - %(levelname)s - %(message)s"
    logging_dt_format: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        env_file = ".env"


settings = Settings()
