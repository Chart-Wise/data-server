from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 기본값 설정 및 환경변수(.env) 연동
    KAFKA_BOOTSTRAP_SERVERS: str = Field(default=...)
    UPBIT_WS_URL: str = Field(default=...)
    TOPIC_NAME: str = Field(default=...)
    KAFKA_CLUSTER_ID: str = Field(default=...)

    # Pydantic v2 스타일 설정
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()