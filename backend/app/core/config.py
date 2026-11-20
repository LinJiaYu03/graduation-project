from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置，可通过环境变量或 backend/.env 覆盖"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_env: str = "development"
    debug: bool = True
    project_name: str = "Campus Activity System"
    logs_root: str = str(Path(__file__).resolve().parents[2] / "logs")

    jwt_secret_key: str = "campus-activity-system-dev-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    # 本地默认数据库，线上通过 backend/.env 的 DATABASE_URL 覆盖
    database_url: str = (
        "mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4"
    )
    redis_url: str = "redis://localhost:6379/0"


settings = Settings()
