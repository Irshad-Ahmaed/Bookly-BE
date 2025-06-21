from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGO:str
    
    model_config  = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

config = Settings()