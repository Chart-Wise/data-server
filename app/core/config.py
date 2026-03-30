from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = Field(default=...)
    UPBIT_WS_URL: str = Field(default=...)
    TOPIC_NAME: str = Field(default=...)
    KAFKA_CLUSTER_ID: str = Field(default=...)
    JWT_SECRET: str = Field(default=...)

    # Pydantic v2 스타일 설정 수정
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()