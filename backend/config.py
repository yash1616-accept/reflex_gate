from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TYPESAFE_API_KEY: str = ""
    DEFAULT_RLCD_THRESHOLD: float = 0.75

    class Config:
        env_file = ".env"

settings = Settings()
