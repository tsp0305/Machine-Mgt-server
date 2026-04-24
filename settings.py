from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = ConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8"
    )

    DATABASE_URL: str
    PORT: Optional[int] = 8000
    JWT_PRIVATE_KEY_PATH: str = "private.pem"
    JWT_PUBLIC_KEY_PATH: str = "public.pem"
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def private_key(self) -> str:
        with open(self.JWT_PRIVATE_KEY_PATH, "r") as f:
            return f.read()

    @property
    def public_key(self) -> str:
        with open(self.JWT_PUBLIC_KEY_PATH, "r") as f:
            return f.read()


settings = Settings()