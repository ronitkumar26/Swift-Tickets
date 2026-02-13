from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    SECRET_KEY: str = Field(..., env="SECRET_KEY")  # required
    ALGORITHM: str = Field("HS256", env="ALGORITHM")  # default is HS256
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")  # default 30
    DATABASE_URL: str = Field(..., env="DATABASE_URL")  # required

    class Config:
        env_file = ".env"

settings = Settings()
